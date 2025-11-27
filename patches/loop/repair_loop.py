from patches.rules.syntax_error import SyntaxErrorRule
from patches.rules.type_error import TypeErrorRule
from patches.rules.name_error import NameErrorRule
from patches.rules.recursion_error import RecursionErrorRule

# NEW LOGIC RULE (functional style)
from patches.rules.logic_rule import logic_rule_applies, apply_logic_patch


# All class-based patch rules
PATCH_RULES = [
    SyntaxErrorRule(),
    TypeErrorRule(),
    NameErrorRule(),
    RecursionErrorRule(),
]


def repair_code(code, error):
    """
    Main repair loop that tries:
    1. Syntax errors
    2. Type errors
    3. Name errors
    4. Recursion errors
    5. Logical errors (functional)
    """

    # Attach code into the error dictionary so rules can see it
    error = dict(error)
    error["code"] = code

    # 1–4: class-based rules
    for rule in PATCH_RULES:
        if rule.applies(error):
            return rule.generate_patch(code, error)

    # 5: function-based logic rule LAST
    if logic_rule_applies(error):
        return apply_logic_patch(code, error)

    # Nothing matched
    return {
        "reason": "No applicable patch rule",
        "patched_code": code,
        "applied_fixes": [],
        "diff": None
    }
