"""
Tests for AutoEvaluator — JSON extraction, cleaning, and parsing.

Tests cover:
  - Valid JSON parsing
  - JSON wrapped in markdown code blocks
  - JSON with trailing text/commentary
  - JSON with trailing commas
  - Completely invalid JSON (raises ValueError)
  - Missing rubric dimensions (defaults applied)
  - Score clamping to 1-3 range
  - String scores converted to int
  - Brace-matched extraction with nested objects
  - BOM-prefixed JSON
  - Control characters stripped
"""

import sys
import os
import pytest

# Add parent directory to path so we can import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.auto_evaluator import AutoEvaluator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_RUBRIC = {
    "name": "Test Rubric",
    "dimensions": [
        {"name": "Accuracy", "weight": 0.5, "description": "Factual correctness"},
        {"name": "Clarity", "weight": 0.5, "description": "Clear communication"},
    ]
}

VALID_JSON = '''{
    "scores_a": {
        "Accuracy": {"score": 3, "comment": "Very accurate"},
        "Clarity": {"score": 2, "comment": "Could be clearer"}
    },
    "scores_b": {
        "Accuracy": {"score": 2, "comment": "Some inaccuracies"},
        "Clarity": {"score": 3, "comment": "Very clear"}
    },
    "preferred_response": "A",
    "justification": "Response A is more accurate overall."
}'''


def make_evaluator():
    """Create an AutoEvaluator with a dummy client (not used for parsing tests)."""
    return AutoEvaluator.__new__(AutoEvaluator)


# ---------------------------------------------------------------------------
# _extract_json tests
# ---------------------------------------------------------------------------

class TestExtractJson:
    def test_plain_json(self):
        ev = make_evaluator()
        assert ev._extract_json(VALID_JSON).startswith('{')

    def test_json_in_markdown_block(self):
        ev = make_evaluator()
        text = f"```json\n{VALID_JSON}\n```"
        result = ev._extract_json(text)
        assert result.startswith('{')
        assert '"scores_a"' in result

    def test_json_in_bare_code_block(self):
        ev = make_evaluator()
        text = f"```\n{VALID_JSON}\n```"
        result = ev._extract_json(text)
        assert result.startswith('{')

    def test_json_with_leading_commentary(self):
        ev = make_evaluator()
        text = f"Here is my evaluation:\n\n{VALID_JSON}"
        result = ev._extract_json(text)
        assert result.startswith('{')
        assert result.endswith('}')

    def test_json_with_trailing_commentary(self):
        ev = make_evaluator()
        text = f"{VALID_JSON}\n\nI hope this evaluation helps!"
        result = ev._extract_json(text)
        assert result.startswith('{')
        assert result.endswith('}')
        # Should not include the trailing text
        assert "I hope" not in result

    def test_no_json_returns_stripped_text(self):
        ev = make_evaluator()
        text = "  no json here  "
        assert ev._extract_json(text) == "no json here"


class TestCleanJsonString:
    def test_trailing_comma_before_brace(self):
        ev = make_evaluator()
        dirty = '{"key": "val",}'
        assert ev._clean_json_string(dirty) == '{"key": "val"}'

    def test_trailing_comma_before_bracket(self):
        ev = make_evaluator()
        dirty = '{"arr": [1, 2, 3,]}'
        assert ev._clean_json_string(dirty) == '{"arr": [1, 2, 3]}'

    def test_multiple_trailing_commas(self):
        ev = make_evaluator()
        dirty = '{"a": 1, "b": 2,}'
        assert ev._clean_json_string(dirty) == '{"a": 1, "b": 2}'

    def test_bom_removal(self):
        ev = make_evaluator()
        dirty = '\ufeff{"key": "val"}'
        assert ev._clean_json_string(dirty) == '{"key": "val"}'

    def test_control_char_removal(self):
        ev = make_evaluator()
        dirty = '{"key": "val\x01ue"}'
        cleaned = ev._clean_json_string(dirty)
        assert '\x01' not in cleaned
        assert '"key"' in cleaned

    def test_clean_json_unchanged(self):
        ev = make_evaluator()
        clean = '{"key": "value"}'
        assert ev._clean_json_string(clean) == clean


# ---------------------------------------------------------------------------
# _parse_judge_response tests
# ---------------------------------------------------------------------------

class TestParseJudgeResponse:
    def test_valid_response(self):
        ev = make_evaluator()
        result = ev._parse_judge_response(VALID_JSON, SAMPLE_RUBRIC)
        assert result['preferred_response'] == 'A'
        assert result['scores_a']['Accuracy']['score'] == 3
        assert result['scores_b']['Clarity']['score'] == 3
        assert isinstance(result['justification'], str)

    def test_json_in_code_block(self):
        ev = make_evaluator()
        text = f"```json\n{VALID_JSON}\n```"
        result = ev._parse_judge_response(text, SAMPLE_RUBRIC)
        assert result['preferred_response'] == 'A'

    def test_json_with_trailing_commas(self):
        ev = make_evaluator()
        dirty = '''{
            "scores_a": {
                "Accuracy": {"score": 3, "comment": "Good",},
                "Clarity": {"score": 2, "comment": "OK",},
            },
            "scores_b": {
                "Accuracy": {"score": 1, "comment": "Bad",},
                "Clarity": {"score": 3, "comment": "Great",},
            },
            "preferred_response": "B",
            "justification": "B is better",
        }'''
        result = ev._parse_judge_response(dirty, SAMPLE_RUBRIC)
        assert result['preferred_response'] == 'B'
        assert result['scores_a']['Accuracy']['score'] == 3

    def test_completely_invalid_json_raises(self):
        ev = make_evaluator()
        with pytest.raises(ValueError, match="Failed to parse"):
            ev._parse_judge_response("This is not JSON at all.", SAMPLE_RUBRIC)

    def test_missing_dimensions_get_defaults(self):
        ev = make_evaluator()
        # Only has Accuracy, missing Clarity
        partial = '''{
            "scores_a": {
                "Accuracy": {"score": 3, "comment": "Good"}
            },
            "scores_b": {
                "Accuracy": {"score": 2, "comment": "OK"}
            },
            "preferred_response": "A",
            "justification": "A is better"
        }'''
        result = ev._parse_judge_response(partial, SAMPLE_RUBRIC)
        # Missing Clarity should get default score of 2
        assert result['scores_a']['Clarity']['score'] == 2
        assert result['scores_b']['Clarity']['score'] == 2
        assert result['scores_a']['Clarity']['comment'] == "Not evaluated"

    def test_score_clamping_high(self):
        ev = make_evaluator()
        bad = '''{
            "scores_a": {
                "Accuracy": {"score": 5, "comment": "Overshot"},
                "Clarity": {"score": 3, "comment": "Fine"}
            },
            "scores_b": {
                "Accuracy": {"score": 3, "comment": "OK"},
                "Clarity": {"score": 3, "comment": "OK"}
            },
            "preferred_response": "A",
            "justification": "A"
        }'''
        result = ev._parse_judge_response(bad, SAMPLE_RUBRIC)
        assert result['scores_a']['Accuracy']['score'] == 3  # Clamped to max

    def test_score_clamping_low(self):
        ev = make_evaluator()
        bad = '''{
            "scores_a": {
                "Accuracy": {"score": 0, "comment": "Zero"},
                "Clarity": {"score": -1, "comment": "Negative"}
            },
            "scores_b": {
                "Accuracy": {"score": 1, "comment": "OK"},
                "Clarity": {"score": 1, "comment": "OK"}
            },
            "preferred_response": "B",
            "justification": "B"
        }'''
        result = ev._parse_judge_response(bad, SAMPLE_RUBRIC)
        assert result['scores_a']['Accuracy']['score'] == 1  # Clamped to min
        assert result['scores_a']['Clarity']['score'] == 1   # Clamped to min

    def test_string_scores_converted(self):
        ev = make_evaluator()
        str_scores = '''{
            "scores_a": {
                "Accuracy": {"score": "3", "comment": "Good"},
                "Clarity": {"score": "2", "comment": "OK"}
            },
            "scores_b": {
                "Accuracy": {"score": "1", "comment": "Bad"},
                "Clarity": {"score": "3", "comment": "Great"}
            },
            "preferred_response": "A",
            "justification": "A is better"
        }'''
        result = ev._parse_judge_response(str_scores, SAMPLE_RUBRIC)
        assert result['scores_a']['Accuracy']['score'] == 3
        assert isinstance(result['scores_a']['Accuracy']['score'], int)

    def test_invalid_preferred_defaults_to_a(self):
        ev = make_evaluator()
        bad_pref = VALID_JSON.replace('"preferred_response": "A"', '"preferred_response": "C"')
        result = ev._parse_judge_response(bad_pref, SAMPLE_RUBRIC)
        assert result['preferred_response'] == 'A'

    def test_missing_required_keys_raises(self):
        ev = make_evaluator()
        incomplete = '{"scores_a": {}, "scores_b": {}}'
        with pytest.raises(ValueError, match="missing required keys"):
            ev._parse_judge_response(incomplete, SAMPLE_RUBRIC)

    def test_nested_json_with_surrounding_text(self):
        ev = make_evaluator()
        text = f"Here is my analysis:\n\n{VALID_JSON}\n\nThank you for the opportunity."
        result = ev._parse_judge_response(text, SAMPLE_RUBRIC)
        assert result['preferred_response'] == 'A'
        assert result['scores_a']['Accuracy']['score'] == 3
