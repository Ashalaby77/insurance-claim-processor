"""
validator.py — cleans and checks the model's output.

Why: models sometimes wrap JSON in markdown code fences (```json ... ```) or add
extra text. This module strips that noise and verifies the result is real JSON.
This is our "basic content validator" (Step 3).
"""

import json
import re


def clean_json_output(text):
    """
    Remove markdown code fences and surrounding whitespace so we're left with raw JSON text.
    Turns  ```json\n{...}\n```  into  {...}
    """
    # Strip ```json or ``` fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def validate_json(text):
    """
    Try to parse the text as JSON.
    Returns (True, parsed_dict) if valid, or (False, error_message) if not.
    """
    cleaned = clean_json_output(text)
    try:
        parsed = json.loads(cleaned)
        return True, parsed
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"


def check_required_fields(data, required_fields):
    """
    Confirm the extracted data has all the fields we expect, and none are empty.
    Returns a list of problems (empty list = all good).
    """
    problems = []
    for field in required_fields:
        if field not in data:
            problems.append(f"Missing field: {field}")
        elif not str(data[field]).strip():
            problems.append(f"Empty field: {field}")
    return problems
