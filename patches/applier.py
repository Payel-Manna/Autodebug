# patches/applier.py
import ast
from typing import Dict, Optional

def apply_patch(original_code: str, patch: Optional[Dict]) -> str:
    """
    If patch is None -> return original_code.
    If patch has 'patched_code' -> validate and return it.
    Otherwise return original_code.
    """
    if not patch:
        return original_code

    patched_code = patch.get("patched_code")
    if not patched_code:
        return original_code

    # validate patched code
    try:
        ast.parse(patched_code)
    except Exception:
        # invalid patch — return original to be safe
        return original_code

    return patched_code
