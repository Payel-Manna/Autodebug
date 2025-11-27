from logical.fixes.op_misuse import fix_op_misuse
from logical.fixes.wrong_return import fix_wrong_return
from logical.fixes.var_misuse import fix_var_misuse
from logical.fixes.unreachable_code import fix_unreachable_code
from logical.fixes.off_by_one import fix_off_by_one


FIX_MAP = {
    "op_misuse": fix_op_misuse,
    "wrong_return": fix_wrong_return,
    "var_misuse": fix_var_misuse,
    "unreachable_code": fix_unreachable_code,
    "off_by_one_logic": fix_off_by_one,
}


def generate_logic_patch(source, issues):
    applied = []
    patched = source

    for issue in issues:
        fix_fn = FIX_MAP.get(issue["rule"])
        if not fix_fn:
            continue

        try:
            new_code = fix_fn(patched, issue)
            if new_code != patched:
                applied.append(issue["rule"])
                patched = new_code
        except Exception:
            continue  # isolated, no crash

    diff = _make_diff(source, patched)

    return {
        "patched_code": patched,
        "applied_fixes": applied,
        "diff": diff
    }


def _make_diff(old, new):
    import difflib
    diff = difflib.unified_diff(
        old.split("\n"),
        new.split("\n"),
        lineterm=""
    )
    return "\n".join(diff)
