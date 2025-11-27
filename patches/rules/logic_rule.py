from logical.analyzer import analyze_logic_errors
from logical.patch_generator import generate_logic_patch


def logic_rule_applies(error):
    """
    Determines if logic fixing should be applied.

    Conditions:
    - Error must contain source code
    - No syntax/type/runtime crash
    - Logic analyzer finds at least one issue
    """
    code = error.get("code")
    if not code:
        return False

    issues = analyze_logic_errors(code)
    return len(issues) > 0


def apply_logic_patch(code, error):
    """
    Generates a logic-fix patch using purely functional style.
    """

    issues = analyze_logic_errors(code)
    patch = generate_logic_patch(code, issues)

    return {
        "reason": "Logical errors detected",
        "issues_detected": issues,
        "diff": patch["diff"],
        "patched_code": patch["patched_code"],
        "applied_fixes": patch["applied_fixes"]
    }
