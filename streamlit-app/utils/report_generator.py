"""
Report Generator for AI Evaluation Sessions

This module generates comprehensive markdown reports from evaluation sessions,
including LLM-powered analysis and enhanced response versions.
"""

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from utils.llm_client import LLMClient


class ReportGenerator:
    """Generates comprehensive evaluation reports with LLM-powered analysis."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize the report generator.
        
        Args:
            llm_client: LLMClient instance for generating analysis
        """
        self.llm_client = llm_client
    
    def generate_report(self, session_data: Dict[str, Any], analysis_model: str) -> str:
        """
        Generate a complete evaluation report from session data.
        
        Args:
            session_data: Dictionary containing all evaluation session data
            analysis_model: Model ID to use for generating analysis
        
        Returns:
            Complete markdown report as string
        """
        # Generate LLM-powered reasoning analysis
        llm_reasoning = self._generate_llm_reasoning(session_data, analysis_model)
        
        # Format into markdown report
        report = self._format_markdown(session_data, llm_reasoning)
        
        return report
    
    def _generate_enhanced_response(self, session_data: Dict[str, Any], model: str) -> str:
        """
        Generate an enhanced version of the stronger response.
        
        Args:
            session_data: Session data containing responses and evaluations
            model: Model ID for generation
        
        Returns:
            Enhanced response text
        """
        # Determine which response is stronger
        preferred = session_data['preferred_response']
        stronger_response = session_data['response_a'] if preferred == 'A' else session_data['response_b']
        stronger_scores = session_data['scores_a'] if preferred == 'A' else session_data['scores_b']
        
        # Build prompt for enhancement
        prompt = self._build_enhancement_prompt(
            stronger_response,
            stronger_scores,
            session_data['rubric'],
            session_data['user_justification']
        )
        
        # Generate enhanced version
        enhanced = self.llm_client.generate_response(
            prompt=prompt,
            model=model,
            system_prompt="You are an expert code reviewer and technical writer. Your task is to improve AI-generated responses based on specific critiques.",
            temperature=0.3,
            max_tokens=4096
        )
        
        return enhanced
    
    def _generate_llm_reasoning(self, session_data: Dict[str, Any], model: str) -> str:
        """
        Generate LLM reasoning about the evaluation.
        
        Args:
            session_data: Session data containing responses and evaluations
            model: Model ID for generation
        
        Returns:
            LLM reasoning text
        """
        prompt = self._build_reasoning_prompt(session_data)
        
        reasoning = self.llm_client.generate_response(
            prompt=prompt,
            model=model,
            system_prompt="You are an expert AI evaluator. Analyze evaluation results and identify additional issues or insights that might have been missed.",
            temperature=0.5,
            max_tokens=2048
        )
        
        return reasoning
    
    def _build_enhancement_prompt(
        self,
        response: str,
        scores: Dict[str, Any],
        rubric: Dict[str, Any],
        user_justification: str
    ) -> str:
        """Build prompt for generating enhanced response."""
        
        # Identify problematic dimensions (scores < 3 for 3-point scale, or < 7 for 10-point scale)
        issues = []
        for dim in rubric.get('dimensions', []):
            dim_name = dim['name']
            score_data = scores.get(dim_name, {'score': 0, 'comment': ''})
            if not isinstance(score_data, dict):
                score_data = {'score': score_data, 'comment': ''}
            
            score = score_data.get('score', 0)
            comment = score_data.get('comment', '')
            
            # 1-3 scale: 3=No Issues, 2=Minor, 1=Major
            if score < 3:
                severity = "Major Issues" if score == 1 else "Minor Issues"
                issue_desc = f"- **{dim_name}** ({severity}): {dim['description']}"
                if comment:
                    issue_desc += f"\n  - *User Comment:* {comment}"
                issues.append(issue_desc)
        
        issues_text = "\n".join(issues) if issues else "No major issues identified"
        
        prompt = f"""You are tasked with improving an AI-generated response based on specific evaluation critiques.

**Original Response:**
```
{response}
```

**Issues Identified by Evaluator:**
{issues_text}

**Evaluator's Justification:**
{user_justification}

**Your Task:**
Rewrite or improve the response to address the identified issues. Fix the specific problems mentioned (e.g., poor formatting, bad coding practices, incomplete explanations, etc.). Maintain the core approach but enhance quality.

Provide ONLY the improved response, without meta-commentary."""

        return prompt
    
    def _build_reasoning_prompt(self, session_data: Dict[str, Any]) -> str:
        """Build prompt for generating LLM reasoning."""
        
        is_auto_eval = 'LLM-as-Judge' in session_data.get('evaluator', '')
        
        # Format dimension scores comparison with comments
        dimensions_comparison = []
        for dim in session_data['rubric'].get('dimensions', []):
            dim_name = dim['name']
            score_data_a = session_data['scores_a'].get(dim_name, {'score': 0, 'comment': ''})
            score_data_b = session_data['scores_b'].get(dim_name, {'score': 0, 'comment': ''})
            
            def get_val(data):
                return data.get('score', 0) if isinstance(data, dict) else data
            def get_comment(data):
                return data.get('comment', '') if isinstance(data, dict) else ''
                
            val_a = get_val(score_data_a)
            val_b = get_val(score_data_b)
            comment_a = get_comment(score_data_a)
            comment_b = get_comment(score_data_b)
            
            line = f"- **{dim_name}**: A={val_a}/3, B={val_b}/3"
            if comment_a:
                line += f"\n  - A comment: {comment_a}"
            if comment_b:
                line += f"\n  - B comment: {comment_b}"
            dimensions_comparison.append(line)
        
        dimensions_text = "\n".join(dimensions_comparison)
        
        if is_auto_eval:
            evaluator_label = "LLM Judge's"
            task_instruction = """**Your Task:**
An LLM judge already performed the primary evaluation above. Your role is to provide an independent second opinion:

1. **Validation**: Do you agree or disagree with the judge's scores and preferred response? Cite specific evidence.
2. **Missed Issues**: Identify any problems, bugs, or improvements that the judge might have missed in EITHER response.
3. **Deeper Insights**: What patterns, trade-offs, or subtle differences exist between the responses that add nuance beyond the judge's analysis?

Be constructive, specific, and add genuine value beyond what the judge already stated."""
        else:
            evaluator_label = "User's"
            task_instruction = """**Your Task:**
Carefully review the user's evaluation. Provide:

1. **Agreement/Disagreement**: Do you agree with the user's assessment? Why or why not?
2. **Additional Issues**: Identify any problems, bugs, or improvements that the user might have missed in BOTH responses.
3. **Deeper Insights**: What patterns, trade-offs, or subtle differences exist between the responses?

Be constructive and specific. Cite evidence from the responses."""
        
        prompt = f"""You are an expert AI evaluator reviewing an evaluation session.

**Prompt Given:**
{session_data['prompt']}

**Response A:**
```
{session_data['response_a']}
```

**Response B:**
```
{session_data['response_b']}
```

**Dimension Scores:**
{dimensions_text}

**Final Scores:**
- Response A: {session_data['final_score_a']:.2f}/10
- Response B: {session_data['final_score_b']:.2f}/10

**Preferred Response:** Response {session_data['preferred_response']}

**{evaluator_label} Justification:**
{session_data['user_justification']}

{task_instruction}"""

        return prompt
    
    def _format_markdown(
        self,
        session_data: Dict[str, Any],
        llm_reasoning: str
    ) -> str:
        """
        Format all data into markdown report.
        
        Args:
            session_data: Session data
            llm_reasoning: LLM-generated reasoning
        
        Returns:
            Complete markdown report
        """
        timestamp = session_data['timestamp']
        rubric = session_data['rubric']
        evaluator_type = session_data.get('evaluator', 'User')
        evaluator_prefix = "Judge's" if 'LLM-as-Judge' in evaluator_type else "User's"
        
        # Format dimension evaluation tables
        table_a = self._format_dimension_table(
            rubric.get('dimensions', []),
            session_data['scores_a']
        )
        table_b = self._format_dimension_table(
            rubric.get('dimensions', []),
            session_data['scores_b']
        )
        
        report = f"""# AI Response Evaluation Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Evaluator:** {session_data.get('evaluator', 'User')}  
**Rubric:** {rubric.get('name', 'Unknown')}  
**Report Analysis Model:** {session_data.get('report_model', 'N/A')}

---

## Original Prompt

{session_data['prompt']}

---

## Response A

**Model:** `{session_data['model_a']}`  
**Parameters:** Temperature: {session_data['params_a']['temperature']}, Top-P: {session_data['params_a']['top_p']}, Max Tokens: {session_data['params_a']['max_tokens']}

### Full Response

{session_data['response_a']}

### {evaluator_prefix} Dimension Evaluations

{table_a}

**Final Score:** {session_data['final_score_a']:.2f}/10

---

## Response B

**Model:** `{session_data['model_b']}`  
**Parameters:** Temperature: {session_data['params_b']['temperature']}, Top-P: {session_data['params_b']['top_p']}, Max Tokens: {session_data['params_b']['max_tokens']}

### Full Response

{session_data['response_b']}

### {evaluator_prefix} Dimension Evaluations

{table_b}

**Final Score:** {session_data['final_score_b']:.2f}/10

---

## Comparison & User Evaluation

**Preferred Response:** Response {session_data['preferred_response']}

### Evaluator's Comparative Justification

{session_data['user_justification']}

---

## LLM Reasoning & Additional Insights

{llm_reasoning}

---

## Report Metadata

- **Timestamp:** `{timestamp}`
- **Session ID:** `eval_{timestamp}`
- **Rubric Version:** {rubric.get('name', 'N/A')}

"""
        return report
    
    def _format_dimension_table(
        self,
        dimensions: list,
        scores: Dict[str, Any]
    ) -> str:
        """Format dimension scores as a markdown table with a dedicated Comment column."""
        
        if not dimensions:
            return "*No dimensions available*"
        
        header = "| Dimension | Score | Comment | Weight |\n|-----------|-------|---------|--------|"
        rows = []
        
        for dim in dimensions:
            name = dim['name']
            score_data = scores.get(name, {'score': 0, 'comment': ''})
            if not isinstance(score_data, dict):
                score_data = {'score': score_data, 'comment': ''}
            
            score = score_data.get('score', 0)
            comment = score_data.get('comment', '')
            
            score_label = "Unknown"
            if score == 3: score_label = "✅ No Issues"
            elif score == 2: score_label = "⚠️ Minor Issues"
            elif score == 1: score_label = "❌ Major Issues"
            
            weight = dim.get('weight', 0)
            
            # Escape pipe characters in comment to avoid breaking table layout
            comment_safe = comment.replace('|', '\\|') if comment else '—'
            
            rows.append(f"| {name} | **{score_label}** | {comment_safe} | {weight:.2f} |")
        
        return header + "\n" + "\n".join(rows)
    
    def save_report(self, content: str, timestamp: str) -> Path:
        """
        Save report to evaluations folder.
        
        Args:
            content: Report markdown content
            timestamp: Timestamp string for filename
        
        Returns:
            Path to saved report
        """
        eval_dir = Path('evaluations')
        eval_dir.mkdir(exist_ok=True)
        
        report_path = eval_dir / f"evaluation_report_{timestamp}.md"
        report_path.write_text(content, encoding='utf-8')
        
        return report_path
