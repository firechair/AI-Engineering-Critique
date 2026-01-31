import yaml
from pathlib import Path
from typing import Dict, List, Any
import streamlit as st

class RubricBuilder:
    def __init__(self, rubrics_dir: Path):
        self.rubrics_dir = rubrics_dir

    def load_rubric(self, filename: str) -> Dict[str, Any]:
        """Loads a rubric from a YAML file."""
        path = self.rubrics_dir / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def save_rubric(self, filename: str, rubric_data: Dict[str, Any]) -> bool:
        """Saves a rubric to a YAML file."""
        try:
            path = self.rubrics_dir / filename
            with open(path, "w") as f:
                yaml.dump(rubric_data, f, sort_keys=False)
            return True
        except Exception:
            return False

    def list_rubrics(self) -> List[str]:
        """Lists available rubric files."""
        return [f.name for f in self.rubrics_dir.glob("*.yaml")]

    def get_empty_rubric(self) -> Dict[str, Any]:
        """Returns the structure of an empty rubric."""
        return {
            "name": "New Rubric",
            "description": "",
            "dimensions": []
        }
    
    def get_empty_dimension(self) -> Dict[str, Any]:
        """Returns the structure of an empty dimension."""
        return {
            "name": "",
            "weight": 0.0,
            "description": "",
            "criteria": []
        }
