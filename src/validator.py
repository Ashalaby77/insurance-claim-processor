"""
validator.py — cleans and checks the model's output.
Models sometimes wrap JSON in markdown code fences or add extra text;
this strips that noise and verifies the result is real JSON.
"""
import json
import re


def clean_json_output(text):
    """Remove markdown code fences and surrounding whitespace."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def validate_json(text):
    """Try to parse text as JSON. Returns (True, dict) or (False, error_message)."""
    cleaned = clean_json_output(text)
    try:
        return True, json.loads(cleaned)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_required_fields(data, required_fields):
    """Confirm the extracted data has all expected fields, none empty. Returns list of problems."""
    problems = []
    for field in required_fields:
        if field not in data:
            problems.append(f"Missing field: {field}")
        elif not str(data[field]).strip():
            problems.append(f"Empty field: {field}")
    return problems
