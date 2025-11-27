def fix_unreachable_code(source, issue):
    """
    Comments out unreachable code.
    """
    lines = source.split("\n")
    ln = issue["line"] - 1
    lines[ln] = "# unreachable: " + lines[ln]
    return "\n".join(lines)
