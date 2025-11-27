# patches/rules/index_error.py
import re
from typing import Dict, Optional

def fix_index_error(parsed: Dict, original_code: str) -> Optional[Dict]:
    """
    Attempt conservative fix for IndexError:

    1. Corrects off-by-one in `range(len(arr)+1)` → `range(len(arr))`.
    2. Wraps simple arr[idx] access in safe bounds check:
       arr[idx] -> (arr[idx] if 0 <= idx < len(arr) else None)
    """
    code_line = parsed.get("code") or ""
    if not code_line:
        return None

    patched_code = original_code

    # ------------------------------
    # 1) Fix range(len(arr)+1)
    # ------------------------------
    range_pattern = r"range\(\s*len\(\s*([A-Za-z_]\w*)\s*\)\s*\+\s*1\s*\)"
    range_match = re.search(range_pattern, code_line)
    if range_match:
        arr = range_match.group(1)
        patched_code = patched_code.replace(f"len({arr})+1", f"len({arr})")
        return {
            "id": "index_off_by_one_range_fix",
            "hint": f"Adjusted `range(len({arr})+1)` -> `range(len({arr}))` to prevent IndexError.",
            "patched_code": patched_code
        }

    # ------------------------------
    # 2) Safe-access for arr[idx]
    # ------------------------------
    # Match simple expressions like arr[idx] or arr[0]
    bracket_pattern = r"([A-Za-z_]\w*)\s*\[\s*([A-Za-z_]\w*|\d+)\s*\]"
    bracket_match = re.search(bracket_pattern, code_line)
    if bracket_match:
        arr = bracket_match.group(1)
        idx = bracket_match.group(2)
        safe_expr = f"({arr}[{idx}] if isinstance({idx}, int) and 0 <= {idx} < len({arr}) else None)"
        patched_code = patched_code.replace(f"{arr}[{idx}]", safe_expr)
        return {
            "id": "index_safe_access",
            "hint": f"Replaced `{arr}[{idx}]` with safe-bound check to prevent IndexError.",
            "patched_code": patched_code
        }

    # ------------------------------
    # No patch found
    # ------------------------------
    return None
