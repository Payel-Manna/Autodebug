def fix_op_misuse(source, issue):
    """
    Replaces bitwise '&' with 'and' in boolean conditions.
    """
    lines = source.split("\n")
    ln = issue["line"] - 1

    if "&" in lines[ln]:
        lines[ln] = lines[ln].replace("&", "and")

    return "\n".join(lines)
