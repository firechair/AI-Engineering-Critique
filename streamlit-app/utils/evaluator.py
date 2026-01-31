from typing import Dict, Any, List

class Evaluator:
    def __init__(self):
        pass

    def calculate_score(self, rubric: Dict[str, Any], ratings: Dict[str, float]) -> float:
        """
        Calculates the weighted score based on rubric and user ratings.
        Ratings is a dict of dimension_name -> score (0-10 or 0-1)
        """
        total_score = 0.0
        total_weight = 0.0

        for dim in rubric.get("dimensions", []):
            name = dim["name"]
            weight = dim["weight"]
            
            if name in ratings:
                score = ratings[name]
                total_score += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        # Normalize to 0-100 or keep as is? Let's assume input scores are 0-10
        # and we return a 0-10 weighted average.
        return total_score / total_weight

    def format_results(self, rubric: Dict[str, Any], ratings: Dict[str, float]) -> Dict[str, Any]:
        """
        Formats the evaluation results for display or export.
        """
        final_score = self.calculate_score(rubric, ratings)
        
        details = []
        for dim in rubric.get("dimensions", []):
            name = dim["name"]
            val = ratings.get(name, 0.0)
            details.append({
                "dimension": name,
                "score": val,
                "weight": dim["weight"],
                "weighted_score": val * dim["weight"]
            })
            
        return {
            "final_score": final_score,
            "details": details
        }
