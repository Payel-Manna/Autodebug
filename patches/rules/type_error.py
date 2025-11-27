# patches/rules/type_error.py

import re
from typing import Dict, Optional

def fix_type_error(parsed: Dict, original_code: str) -> Optional[Dict]:
    msg = (parsed.get("message") or "")
    msg_lower = msg.lower()

    # 1) Missing positional argument
    m = re.search(r"missing (\d+) required positional argument[s]?: ['\"]?(.+?)['\"]?$", msg_lower)
    if m:
        missing_args = m.group(2)
        return {
            "id": "type_missing_argument",
            "hint": f"Add missing argument(s): {missing_args}",
            "patched_code": original_code
        }

    # 2) Unsupported operand types
    m = re.search(
        r"unsupported operand type\(s\) for .+: ['\"](\w+)['\"] and ['\"](\w+)['\"]",
        msg_lower
    )
    if m:
        left, right = m.group(1), m.group(2)
        return {
            "id": "type_operand_mismatch",
            "hint": f"Operand types incompatible: {left} vs {right}. Convert one with int()/str()/float().",
            "patched_code": original_code
        }

    # 3) NoneType issues
    if "nonetype" in msg_lower:
        return {
            "id": "type_nonetype",
            "hint": "A variable is None unexpectedly. Check return values or conditions.",
            "patched_code": original_code
        }

    # fallback
    return {
        "id": "type_general",
        "hint": f"General TypeError: {msg}",
        "patched_code": original_code
    }
