# patches/rules/name_error.py
import re
from typing import Dict, Optional

def fix_name_error(parsed: Dict, original_code: str) -> Optional[Dict]:
    """
    Conservative fix for NameError:
    - find missing name from message like "name 'x' is not defined"
    - prepend `x = None` at the top of the file (or near top)
    Returns dict with patched_code, hint, id
    """
    msg = (parsed.get("message") or "").strip()
    m = re.search(r"name '?\"?([A-Za-z_]\w*)'?\"? is not defined", msg)
    if not m:
        # try alternate formats
        m = re.search(r"name '?\"?([A-Za-z_]\w*)'?\"? is not defined", msg.lower())
    if not m:
        return None

    name = m.group(1)
    # create a conservative initializer
    init_line = f"{name} = None  # auto-added to fix NameError\n"

    # If original already defines the name (rare), abort
    pattern = rf"(^|\n){name}\s*="
    if re.search(pattern, original_code):
        return None

    patched_code = init_line + original_code

    return {
        "id": "name_error_prepend_none",
        "hint": f"Inserted `{name} = None` at top of file to fix NameError.",
        "patched_code": patched_code
    }
