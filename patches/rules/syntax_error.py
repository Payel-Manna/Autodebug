def fix_syntax_error(parsed, original_code):
    msg = parsed.get("message","")
    lineno = parsed.get("lineno")
    line = parsed.get("line","")

    suggestions = []
    ...
    return {
        "id": "syntax_hint",
        "hint": "; ".join(suggestions),
        "patched_code": original_code
    }
