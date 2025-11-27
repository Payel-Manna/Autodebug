# patches/rules/recursion_error.py
from typing import Dict, Optional

def fix_recursion_error(parsed: Dict, original_code: str) -> Optional[Dict]:
    """
    Provide a suggestion for RecursionError.
    Automatic code modification is unsafe; only hints are returned.
    """
    message = (parsed.get("message") or "").lower()

    hint = "Ensure your recursive function has a proper base case."

    if "maximum recursion depth exceeded" in message:
        hint = (
            "Recursion depth exceeded. Likely missing or incorrect base case. "
            "Consider adding a base case or converting to iterative logic."
        )

    return {
        "id": "recursion_error_hint",
        "hint": hint,
        "patched_code": original_code  # no automatic change
    }
