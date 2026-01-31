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
