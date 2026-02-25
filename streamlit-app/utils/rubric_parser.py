"""
Rubric Parser Utility

Parses markdown rubric files to extract structured evaluation data.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class RubricParser:
    """Parser for markdown-based rubric files."""
    
    def __init__(self, rubrics_dir: Path):
        """
        Initialize parser with rubrics directory.
        
        Args:
            rubrics_dir: Path to directory containing rubric markdown files
        """
        self.rubrics_dir = Path(rubrics_dir)
    
    def list_available_rubrics(self) -> List[str]:
        """
        List all available rubric markdown files.
        
        Returns:
            List of rubric filenames (without extension)
        """
        rubric_files = []
        for file_path in self.rubrics_dir.glob("*-rubric.md"):
            rubric_files.append(file_path.stem)
        return sorted(rubric_files)
    
    def parse_rubric_file(self, rubric_name: str) -> Dict[str, Any]:
        """
        Parse a rubric markdown file into structured data.
        
        Args:
            rubric_name: Name of rubric file (with or without extension)
        
        Returns:
            Dictionary containing rubric structure compatible with app
        """
        # Normalize filename
        if not rubric_name.endswith('.md'):
            if not rubric_name.endswith('-rubric'):
                rubric_name = f"{rubric_name}-rubric"
            rubric_name = f"{rubric_name}.md"
        
        file_path = self.rubrics_dir / rubric_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {file_path}")
        
        content = file_path.read_text(encoding='utf-8')
        
        # Extract metadata and dimensions
        rubric_data = {
            'name': self._extract_title(content, file_path.stem),
            'scenario': self._extract_scenario(file_path.stem),
            'description': self._extract_description(content),
            'use_case': self._extract_use_case(content),
            'scale_type': '3-point',
            'dimensions': self._extract_dimensions(content)
        }
        
        return rubric_data
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract document title from markdown header."""
        # Look for first H1 heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Fallback to formatted filename
        return filename.replace('-', ' ').replace('rubric', 'Rubric').title()
    
    def _extract_scenario(self, filename: str) -> str:
        """Extract scenario name from filename."""
        # Remove -rubric suffix and format nicely
        scenario = filename.replace('-rubric', '')
        scenario = scenario.replace('-', ' ').title()
        return scenario
    
    def _extract_description(self, content: str) -> str:
        """Extract overview description."""
        # Look for Overview section
        pattern = r'##\s+Overview\s+(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            desc = match.group(1).strip()
            # Get first paragraph
            first_para = desc.split('\n\n')[0]
            return first_para.strip()
        return "Evaluation rubric using a 3-point rating scale."
    
    def _extract_use_case(self, content: str) -> str:
        """Extract use case information."""
        # Look for "Use Case Examples" or "Perfect for evaluating" section
        pattern = r'\*\*Perfect for evaluating\*\*:?\s+(.*?)(?=\n\*\*|\n\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            use_cases = match.group(1).strip()
            # Clean up list markers
            use_cases = re.sub(r'\n\s*-\s*', ', ', use_cases)
            return use_cases.strip()
        return "Various evaluation scenarios"
    
    def _extract_dimensions(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract evaluation dimensions from markdown.
        
        Returns:
            List of dimension dictionaries
        """
        dimensions = []
        
        # Find all dimension sections (### 1. Dimension Name)
        pattern = r'###\s+(\d+)\.\s+(.+?)\n\n\*\*Definition\*\*:\s*(.+?)\n\n####\s+What to Evaluate:(.*?)####\s+Rating Guidelines:(.*?)(?=\n###|\n##\s+Overall|\Z)'
        
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            dim_number = int(match.group(1))
            dim_name = match.group(2).strip()
            definition = match.group(3).strip()
            criteria_section = match.group(4).strip()
            rating_section = match.group(5).strip()
            
            # Extract criteria
            criteria = self._extract_criteria(criteria_section)
            
            # Extract rating guide
            rating_guide = self._extract_rating_guide(rating_section)
            
            dimension = {
                'name': dim_name,
                'description': definition,
                'weight': 0.0,  # Will be calculated later
                'criteria': criteria,
                'rating_guide': rating_guide
            }
            
            dimensions.append(dimension)

        # Extract priority mappings and calculate weights
        priorities = self._extract_dimension_priorities(content)

        if priorities:
            self._calculate_priority_weights(dimensions, priorities)
        else:
            # Fallback to equal weights (sum to 10)
            if dimensions:
                weight = 10.0 / len(dimensions)
                for dim in dimensions:
                    dim['weight'] = round(weight, 2)

        return dimensions
    
    def _extract_criteria(self, criteria_section: str) -> List[str]:
        """Extract evaluation criteria from section."""
        criteria = []
        # Look for list items starting with - or •
        for line in criteria_section.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                criterion = line.lstrip('-•').strip()
                if criterion:
                    criteria.append(criterion)
        return criteria
    
    def _extract_rating_guide(self, rating_section: str) -> Dict[int, str]:
        """Extract rating guide table."""
        rating_guide = {}
        
        # Try to extract from markdown table
        # Pattern: | **3 - No Issues** | Description text | Examples... |
        pattern = r'\|\s*\*\*(\d+)\s*-\s*([^*]+)\*\*\s*\|\s*([^|]+)\|'
        matches = re.finditer(pattern, rating_section)
        
        for match in matches:
            score = int(match.group(1))
            level = match.group(2).strip()
            description = match.group(3).strip()
            rating_guide[score] = f"{level}: {description}"
        
        # Fallback: ensure we have all 3 levels
        if len(rating_guide) != 3:
            rating_guide = {
                3: "No Issues: Meets all criteria with no identifiable problems",
                2: "Minor Issues: Small problems that don't significantly impact usefulness",
                1: "Major Issues: Significant problems that severely impact usefulness"
            }
        
        return rating_guide

    def _extract_dimension_priorities(self, content: str) -> Dict[str, str]:
        """
        Extract dimension priority mappings from rubric.

        Returns:
            Dict mapping dimension names to priority levels
        """
        priorities = {}

        # Find priority section (handles "Step 2" and "Step 3" variants)
        pattern = r'###\s+Step\s+\d+:\s+Prioritize.*?Dimensions.*?\n(.*?)(?=\n###|\n---|\n##\s+[A-Z]|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

        if not match:
            return priorities

        priority_section = match.group(1)

        # Extract: - **Critical**: Dim1, Dim2
        priority_pattern = r'-\s*\*\*(\w+(?:-to-\w+)?)\*\*:\s*(.+?)(?=\n-|\Z)'

        for level_match in re.finditer(priority_pattern, priority_section, re.DOTALL):
            level = level_match.group(1).strip()
            dims_text = level_match.group(2).strip()

            # Split by comma and "&"
            dims_text = dims_text.replace(' & ', ', ')
            dim_names = [d.strip() for d in dims_text.split(',')]

            for dim_name in dim_names:
                if dim_name:
                    priorities[dim_name] = level

        return priorities

    def _calculate_priority_weights(
        self,
        dimensions: List[Dict[str, Any]],
        priorities: Dict[str, str]
    ) -> None:
        """
        Calculate weights based on dimension priorities.

        Multipliers: Critical=2.0, Important=1.0, Nice-to-have=0.5
        Weights are normalized to sum to 10 (for direct contribution to 0-10 final score)
        """
        if not dimensions:
            return

        WEIGHT_MULTIPLIERS = {
            'Critical': 2.0,
            'Important': 1.0,
            'Nice-to-have': 0.5
        }

        raw_weights = []
        for dim in dimensions:
            dim_name = dim['name']
            priority = priorities.get(dim_name)

            # Fuzzy match for slight name variations
            if priority is None:
                priority = self._fuzzy_match_priority(dim_name, priorities)

            multiplier = WEIGHT_MULTIPLIERS.get(priority, 1.0)
            raw_weights.append(multiplier)

        # Normalize to sum to 10 (not 1)
        total = sum(raw_weights)
        for i, dim in enumerate(dimensions):
            dim['weight'] = round((raw_weights[i] / total) * 10, 2)

    def _fuzzy_match_priority(
        self,
        dim_name: str,
        priorities: Dict[str, str]
    ) -> Optional[str]:
        """
        Fuzzy match dimension name to priority.
        Handles variations like "Scalability & NFRs" vs full name.
        """
        dim_lower = dim_name.lower()

        for priority_dim, level in priorities.items():
            priority_lower = priority_dim.lower()

            # Check containment
            if priority_lower in dim_lower or dim_lower in priority_lower:
                return level

            # Check first word match
            if dim_lower.split()[0] == priority_lower.split()[0]:
                return level

        return None


def load_rubric(rubric_name: str, rubrics_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Convenience function to load a rubric.
    
    Args:
        rubric_name: Name of the rubric
        rubrics_dir: Optional path to rubrics directory
    
    Returns:
        Parsed rubric dictionary
    """
    if rubrics_dir is None:
        # Default to relative path from this file
        rubrics_dir = Path(__file__).parent.parent / 'rubrics'
    
    parser = RubricParser(rubrics_dir)
    return parser.parse_rubric_file(rubric_name)


def list_rubrics(rubrics_dir: Optional[Path] = None) -> List[str]:
    """
    Convenience function to list available rubrics.
    
    Args:
        rubrics_dir: Optional path to rubrics directory
    
    Returns:
        List of available rubric names
    """
    if rubrics_dir is None:
        rubrics_dir = Path(__file__).parent.parent / 'rubrics'
    
    parser = RubricParser(rubrics_dir)
    return parser.list_available_rubrics()
