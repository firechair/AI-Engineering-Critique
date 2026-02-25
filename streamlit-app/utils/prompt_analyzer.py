import json
from pathlib import Path
from typing import List, Dict, Any

class PromptAnalyzer:
    def __init__(self, techniques_path: Path):
        self.techniques_path = techniques_path
        self.techniques = self._load_techniques()

    def _load_techniques(self) -> List[Dict[str, Any]]:
        path = self.techniques_path / "techniques.json"
        if not path.exists():
            return []
        with open(path, "r") as f:
            data = json.load(f)
            return data.get("techniques", [])

    def analyze(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Analyzes the prompt and suggests improvements based on techniques.
        Simple keyword/heuristic based analysis for demonstration.
        """
        suggestions = []
        prompt_lower = prompt.lower()

        # Check for context
        if len(prompt.split()) < 10 or "context" not in prompt_lower:
             suggestions.append(self._get_suggestion("add_context"))

        # Check for format
        format_keywords = ["json", "markdown", "list", "code", "format", "output"]
        if not any(k in prompt_lower for k in format_keywords):
            suggestions.append(self._get_suggestion("specify_format"))

        # Check for examples
        if "example" not in prompt_lower:
            suggestions.append(self._get_suggestion("provide_examples"))

        # Check for constraints
        constraint_keywords = ["do not", "limit", "bound", "only", "constraint"]
        if not any(k in prompt_lower for k in constraint_keywords):
            suggestions.append(self._get_suggestion("clarify_constraints"))
            
        return [s for s in suggestions if s]

    def _get_suggestion(self, technique_id: str) -> Dict[str, Any]:
        for tech in self.techniques:
            if tech["id"] == technique_id:
                return tech
        return None
    def analyze_with_llm(self, prompt: str, llm_client, model_id: str) -> str:
        """
        Analyzes the prompt using an LLM, referencing the techniques.json file.
        """
        # Build techniques context
        techniques_context = ""
        for tech in self.techniques:
            techniques_context += f"- **{tech['name']}**: {tech['description']}\n"
            techniques_context += f"  Checklist: {', '.join(tech['checklist'])}\n"
            techniques_context += f"  Example: {tech['example_enhancement']}\n\n"

        system_prompt = (
            "You are an expert AI Prompt Engineer. Your task is to analyze the user's prompt "
            "and suggest how it can be improved, based *only* on the following prompt techniques:\n\n"
            f"{techniques_context}\n"
            "Provide a detailed, structured critique of the prompt, highlighting which techniques are missing or "
            "could be applied better, and provide a revised, enhanced version of the prompt at the end."
        )

        response = llm_client.generate_response(
            prompt=f"Here is the prompt to analyze:\n\n{prompt}",
            model=model_id,
            system_prompt=system_prompt,
            temperature=0.7
        )
        return response
