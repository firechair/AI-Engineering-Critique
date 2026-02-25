from typing import Dict, Any, List, Union

class Evaluator:
    def __init__(self):
        pass

    def calculate_score(self, rubric: Dict[str, Any], ratings: Dict[str, Any]) -> float:
        """
        Calculates the weighted score based on rubric and user ratings.
        Ratings is a dict of dimension_name -> {'score': int (1-3), 'comment': str}
        """
        total_score = 0.0
        total_weight = 0.0

        for dim in rubric.get("dimensions", []):
            name = dim["name"]
            weight = dim["weight"]
            
            if name in ratings:
                # Handle both new object structure and potential legacy float/int
                rating_data = ratings[name]
                if isinstance(rating_data, dict):
                    raw_score = rating_data.get('score', 0)
                else:
                    raw_score = rating_data
                
                # Normalize 1-3 scale to 0-10 scale for final score calculation if desired
                # 3 -> 10, 2 -> 5, 1 -> 0 ? Or just keep as 1-3 average?
                # Let's normalize to 0-10 for consistency with previous mental model
                # 3 (No Issues) -> 10
                # 2 (Minor Issues) -> 5
                # 1 (Major Issues) -> 0
                
                normalized_score = 0.0
                normalized_score = 0.0
                if raw_score == 3:
                    normalized_score = 10.0
                elif raw_score == 2:
                    normalized_score = 9.0  # Minor issue = 9.0 (User's math preference: small penalty)
                else:
                    normalized_score = 5.0  # Major issue = 5.0 (Significant penalty)
                    
                total_score += normalized_score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        # Normalize to 0-100 or keep as is? Let's assume input scores are 0-10
        # and we return a 0-10 weighted average.
        return total_score / total_weight

    def format_results(self, rubric: Dict[str, Any], ratings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formats the evaluation results for display or export.
        Ratings: {dim_name: {'score': 1-3, 'comment': '...'}}
        """
        final_score = self.calculate_score(rubric, ratings)
        
        details = []
        for dim in rubric.get("dimensions", []):
            name = dim["name"]
            rating_data = ratings.get(name, {'score': 0, 'comment': ''})
            if not isinstance(rating_data, dict):
                 rating_data = {'score': rating_data, 'comment': ''}
                 
            raw_score = rating_data.get('score', 0)
            comment = rating_data.get('comment', '')
            
            # Text label for score
            score_label = "Unknown"
            if raw_score == 3:
                score_label = "No Issues"
            elif raw_score == 2:
                score_label = "Minor Issues"
            elif raw_score == 1:
                score_label = "Major Issues"

            # Normalize for weighted score calculation
            normalized_val = 0.0
            if raw_score == 3:
                normalized_val = 10.0
            elif raw_score == 2:
                normalized_val = 9.0
            elif raw_score == 1:
                normalized_val = 5.0
            
            details.append({
                "dimension": name,
                "score": raw_score,
                "score_label": score_label,
                "comment": comment,
                "weight": dim["weight"],
                "weighted_score": normalized_val * dim["weight"]
            })
            
        return {
            "final_score": final_score,
            "details": details
        }
