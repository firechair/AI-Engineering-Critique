"""
Rubric Builder - Interface for loading and managing evaluation rubrics.

Updated to work with markdown-based rubrics instead of YAML files.
"""

from pathlib import Path
from typing import Dict, List, Any
from utils.rubric_parser import RubricParser


class RubricBuilder:
    """Manages loading and listing of evaluation rubrics."""
    
    def __init__(self, rubrics_dir: Path):
        """
        Initialize with rubrics directory.
        
        Args:
            rubrics_dir: Path to directory containing rubric markdown files
        """
        self.rubrics_dir = Path(rubrics_dir)
        self.parser = RubricParser(self.rubrics_dir)
    
    def load_rubric(self, filename: str) -> Dict[str, Any]:
        """
        Load a rubric from markdown file.
        
        Args:
            filename: Rubric filename (with or without extension)
        
        Returns:
            Dictionary containing parsed rubric data
        """
        try:
            # Handle both .md and -rubric naming conventions
            if filename.endswith('.md'):
                filename = filename[:-3]  # Remove .md
            
            return self.parser.parse_rubric_file(filename)
        except FileNotFoundError:
            # Return empty rubric if not found
            return self.get_empty_rubric()
        except Exception as e:
            print(f"Error loading rubric {filename}: {e}")
            return self.get_empty_rubric()
    
    def list_rubrics(self) -> List[str]:
        """
        List available rubric markdown files.
        
        Returns:
            List of rubric filenames (*.md format)
        """
        markdown_files = []
        for file_path in self.rubrics_dir.glob("*-rubric.md"):
            markdown_files.append(file_path.name)
        return sorted(markdown_files)
    
    def get_rubric_display_name(self, filename: str) -> str:
        """
        Get human-readable display name from filename.
        
        Args:
            filename: Rubric filename
        
        Returns:
            Formatted display name
        """
        # Remove extension and -rubric suffix
        name = filename.replace('.md', '').replace('-rubric', '')
        # Convert to title case with spaces
        display_name = name.replace('-', ' ').title()
        return display_name
    
    def get_empty_rubric(self) -> Dict[str, Any]:
        """
        Return structure of an empty rubric.
        
        Returns:
            Empty rubric dictionary
        """
        return {
            "name": "New Rubric",
            "scenario": "General",
            "description": "",
            "dimensions": []
        }
    
    def get_empty_dimension(self) -> Dict[str, Any]:
        """
        Return structure of an empty dimension.
        
        Returns:
            Empty dimension dictionary
        """
        return {
            "name": "",
            "weight": 0.0,
            "description": "",
            "criteria": [],
            "rating_guide": {
                3: "No Issues",
                2: "Minor Issues",
                1: "Major Issues"
            }
        }
