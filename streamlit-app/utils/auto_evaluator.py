"""
Auto-Evaluator Module (LLM-as-Judge)

Uses an LLM to automatically evaluate two AI responses across rubric dimensions,
producing structured scores and justifications compatible with the manual evaluation flow.
"""

import json
import re
from typing import Dict, Any, Optional

from utils.llm_client import LLMClient


class AutoEvaluator:
    """Automated evaluation using LLM-as-Judge approach."""

    def __init__(self, llm_client: LLMClient):
        """
        Initialize the auto-evaluator.

        Args:
            llm_client: LLMClient instance for calling the judge model
        """
        self.llm_client = llm_client

    def auto_evaluate(
        self,
        prompt: str,
        response_a: str,
        response_b: str,
        rubric: Dict[str, Any],
        judge_model: str
    ) -> Dict[str, Any]:
        """
        Run automated evaluation of two responses using an LLM judge.

        Args:
            prompt: The original user prompt
            response_a: First AI response
            response_b: Second AI response
            rubric: Parsed rubric dictionary with dimensions
            judge_model: Model ID for the judge LLM

        Returns:
            Dictionary containing:
                - scores_a: {dim_name: {'score': 1-3, 'comment': str}}
                - scores_b: {dim_name: {'score': 1-3, 'comment': str}}
                - preferred_response: 'A' or 'B'
                - justification: Comparative justification text
        """
        judge_prompt = self._build_judge_prompt(prompt, response_a, response_b, rubric)

        system_prompt = (
            "You are an expert AI response evaluator. You evaluate AI-generated responses "
            "using structured rubrics. You MUST respond ONLY with valid JSON, no other text. "
            "Do NOT include any markdown formatting, code blocks, or commentary. "
            "Be fair, objective, and thorough in your evaluations."
        )

        raw_response = self.llm_client.generate_response(
            prompt=judge_prompt,
            model=judge_model,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=8192
        )

        # First attempt to parse
        try:
            return self._parse_judge_response(raw_response, rubric)
        except ValueError:
            pass  # Fall through to retry

        # Retry with a stricter prompt
        strict_system_prompt = (
            "You are an expert AI evaluator. You MUST output ONLY a single, valid JSON object. "
            "No markdown, no code blocks, no commentary before or after the JSON. "
            "Ensure all strings are properly escaped. Do not use trailing commas. "
            "Output MUST start with { and end with }."
        )

        raw_response = self.llm_client.generate_response(
            prompt=judge_prompt,
            model=judge_model,
            system_prompt=strict_system_prompt,
            temperature=0.1,
            max_tokens=8192
        )

        return self._parse_judge_response(raw_response, rubric)

    def _build_judge_prompt(
        self,
        prompt: str,
        response_a: str,
        response_b: str,
        rubric: Dict[str, Any]
    ) -> str:
        """Build the structured prompt for the LLM judge."""

        # Build dimensions description
        dimensions_text = ""
        for dim in rubric.get("dimensions", []):
            dim_name = dim["name"]
            dim_desc = dim.get("description", "")
            dim_weight = dim.get("weight", 0)

            # Include criteria if available
            criteria = dim.get("criteria", [])
            criteria_text = ""
            if criteria:
                criteria_items = "\n".join(f"    - {c}" for c in criteria)
                criteria_text = f"\n  Criteria:\n{criteria_items}"

            # Include rating guide if available
            rating_guide = dim.get("rating_guide", {})
            guide_text = ""
            if rating_guide:
                guide_items = "\n".join(
                    f"    - {score}: {desc}" for score, desc in sorted(rating_guide.items(), reverse=True)
                )
                guide_text = f"\n  Rating Guide:\n{guide_items}"

            dimensions_text += f"""
- **{dim_name}** (Weight: {dim_weight:.3f})
  Definition: {dim_desc}{criteria_text}{guide_text}
"""

        # Build list of dimension names for JSON schema
        dim_names = [dim["name"] for dim in rubric.get("dimensions", [])]
        dim_schema = ",\n".join(
            f'        "{name}": {{"score": <1|2|3>, "comment": "<specific comment>"}}'
            for name in dim_names
        )

        prompt_text = f"""Evaluate the following two AI-generated responses to the given prompt.
Use the rubric dimensions below to score EACH response independently on a 3-point scale:
- **3 = No Issues**: Meets all criteria with no identifiable problems
- **2 = Minor Issues**: Small problems that don't significantly impact usefulness
- **1 = Major Issues**: Significant problems that severely impact usefulness

## Original Prompt

{prompt}

## Response A

{response_a}

## Response B

{response_b}

## Evaluation Rubric: {rubric.get('name', 'Evaluation Rubric')}

{rubric.get('description', '')}

### Dimensions
{dimensions_text}

## Your Task

1. Evaluate EACH response on EVERY dimension listed above
2. Provide a specific comment for each dimension referencing concrete evidence from the response
3. Determine which response is overall better
4. Write a detailed comparative justification

## Required Output Format

You MUST respond with ONLY this JSON structure (no markdown, no extra text):

{{
    "scores_a": {{
{dim_schema}
    }},
    "scores_b": {{
{dim_schema}
    }},
    "preferred_response": "A" or "B",
    "justification": "<detailed comparative justification explaining your preference, citing specific differences>"
}}"""

        return prompt_text

    def _parse_judge_response(
        self,
        raw_response: str,
        rubric: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse and validate the JSON response from the judge LLM.

        Args:
            raw_response: Raw text response from the judge
            rubric: Rubric for validation

        Returns:
            Validated evaluation data dictionary

        Raises:
            ValueError: If response cannot be parsed or validated
        """
        # Try to extract JSON from various wrapping formats
        json_str = self._extract_json(raw_response)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse judge response as JSON: {e}\n\n"
                f"Raw response:\n{raw_response[:500]}"
            )

        # Validate structure
        required_keys = {"scores_a", "scores_b", "preferred_response", "justification"}
        missing = required_keys - set(data.keys())
        if missing:
            raise ValueError(f"Judge response missing required keys: {missing}")

        # Validate preferred_response
        if data["preferred_response"] not in ("A", "B"):
            data["preferred_response"] = "A"  # Default fallback

        # Validate and normalize dimension scores
        dim_names = {dim["name"] for dim in rubric.get("dimensions", [])}

        for key in ("scores_a", "scores_b"):
            if not isinstance(data[key], dict):
                raise ValueError(f"'{key}' must be a dictionary")

            for dim_name in dim_names:
                if dim_name not in data[key]:
                    # Fill missing dimensions with default
                    data[key][dim_name] = {"score": 2, "comment": "Not evaluated"}

                dim_data = data[key][dim_name]
                if not isinstance(dim_data, dict):
                    data[key][dim_name] = {"score": int(dim_data) if dim_data else 2, "comment": ""}

                # Clamp score to valid range
                score = data[key][dim_name].get("score", 2)
                if isinstance(score, str):
                    try:
                        score = int(score)
                    except ValueError:
                        score = 2
                data[key][dim_name]["score"] = max(1, min(3, score))

                # Ensure comment is a string
                if "comment" not in data[key][dim_name]:
                    data[key][dim_name]["comment"] = ""

        # Ensure justification is a string
        if not isinstance(data.get("justification"), str):
            data["justification"] = str(data.get("justification", ""))

        return data

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from text that may be wrapped in markdown code blocks
        or contain extra text before/after the JSON.

        Args:
            text: Raw text that may contain JSON

        Returns:
            Extracted JSON string
        """
        # Try extracting from ```json ... ``` block
        json_block_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if json_block_match:
            extracted = json_block_match.group(1).strip()
            return self._clean_json_string(extracted)

        # Try finding JSON object directly using brace matching
        first_brace = text.find('{')
        if first_brace != -1:
            # Use brace-depth matching to find the correct closing brace
            depth = 0
            in_string = False
            escape_next = False
            for i in range(first_brace, len(text)):
                ch = text[i]
                if escape_next:
                    escape_next = False
                    continue
                if ch == '\\':
                    if in_string:
                        escape_next = True
                    continue
                if ch == '"' and not escape_next:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        extracted = text[first_brace:i + 1]
                        return self._clean_json_string(extracted)

            # Fallback: first { to last }
            last_brace = text.rfind('}')
            if last_brace > first_brace:
                extracted = text[first_brace:last_brace + 1]
                return self._clean_json_string(extracted)

        # Return as-is and let JSON parser handle the error
        return text.strip()

    def _clean_json_string(self, json_str: str) -> str:
        """
        Clean common JSON formatting issues from LLM output.

        Handles:
            - Trailing commas before } or ]
            - Control characters inside strings
            - BOM characters

        Args:
            json_str: Raw JSON string

        Returns:
            Cleaned JSON string
        """
        # Remove BOM
        json_str = json_str.strip().lstrip('\ufeff')

        # Remove trailing commas before } or ] (common LLM mistake)
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)

        # Remove control characters (except \n \r \t which are valid in strings)
        json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', json_str)

        return json_str
