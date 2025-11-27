# patches/generator.py
import ast
from typing import Optional, Dict, Callable
import difflib

# import all rule functions from patches/rules
from patches.rules.name_error import fix_name_error
from patches.rules.index_error import fix_index_error
from patches.rules.syntax_error import fix_syntax_error
from patches.rules.type_error import fix_type_error
from patches.rules.recursion_error import fix_recursion_error

# Map error categories to rule functions
ROUTING: Dict[str, Callable] = {
    "UNDECLARED_VARIABLE": fix_name_error,
    "NAME_ERROR": fix_name_error,
    "INDEX_OUT_OF_RANGE": fix_index_error,
    "INDEX_ERROR": fix_index_error,
    "SYNTAX_MISSING_COLON": fix_syntax_error,
    "SYNTAX_INVALID": fix_syntax_error,
    "TYPE_MISMATCH": fix_type_error,
    "CALLING_NON_CALLABLE": fix_type_error,
    "RECURSION_NO_BASE_CASE": fix_recursion_error,
}

def _validate_code(code: str) -> bool:
    """
    Returns True if the code is valid Python.
    """
    try:
        ast.parse(code)
        return True
    except Exception:
        return False

def generate_patch(parsed: dict, category: str, original_code: str) -> Optional[Dict]:
    """
    Generate a patch for the given parsed error and category.

    Returns:
        dict with keys: id, category, hint, patch_type, diff, patched_code
        or None if no patch is available / code invalid
    """
    # Early exit if no error
    if not parsed or not parsed.get("has_error"):
        return None

    # Get the rule function
    rule_fn: Callable = ROUTING.get(category)
    if not rule_fn:
        return None

    # Apply the rule function
    patched_result = rule_fn(parsed, original_code)
    if not patched_result:
        return None

    # Ensure consistent dictionary format
    if isinstance(patched_result, str):
        patched_code = patched_result
        hint = "Automated fix applied"
        rule_id = f"rule_{category}"
    elif isinstance(patched_result, dict) and patched_result.get("patched_code"):
        patched_code = patched_result["patched_code"]
        hint = patched_result.get("hint") or "Automated fix applied"
        rule_id = patched_result.get("id") or f"rule_{category}"
    else:
        return None

    # Validate patched code
    if not _validate_code(patched_code):
        return None

    # Generate unified diff for review/logging
    try:
        diff_text = "\n".join(difflib.unified_diff(
            original_code.splitlines(),
            patched_code.splitlines(),
            fromfile="original.py",
            tofile="patched.py",
            lineterm=""
        ))
    except Exception:
        diff_text = ""

    # Final patch dictionary
    return {
        "id": rule_id,
        "category": category,
        "hint": hint,
        "patch_type": "text",
        "diff": diff_text,
        "patched_code": patched_code
    }
