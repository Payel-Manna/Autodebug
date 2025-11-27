import ast

from .fixes.op_misuse import detect_op_misuse
from .fixes.wrong_return import detect_wrong_return
from .fixes.off_by_one import detect_off_by_one
from .fixes.var_misuse import detect_var_misuse
from .fixes.unreachable_code import detect_unreachable_code


LOGIC_RULES = [
    detect_op_misuse,
    detect_wrong_return,
    detect_off_by_one,
    detect_var_misuse,
    detect_unreachable_code,
]


def analyze_logic_errors(source: str):
    """
    Runs all AST-based logic error detectors.
    Returns a list of detected issues with:
      {
        "rule": str,
        "line": int,
        "col": int,
        "message": str,
        "suggestion": str
      }
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    issues = []
    for rule in LOGIC_RULES:
        try:
            issues.extend(rule(tree, source))
        except Exception as ex:
            # Rule isolation: do not allow one rule to break the analyzer.
            issues.append({
                "rule": rule.__name__,
                "line": 0,
                "col": 0,
                "message": f"Rule failed: {ex}",
                "suggestion": "Internal logic rule error."
            })

    return issues
