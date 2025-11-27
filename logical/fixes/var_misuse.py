def fix_var_misuse(source, issue):
    """
    Fix unassigned variable by inserting initialization above the line.
    """
    var = issue["message"].split("'")[1]  # extract variable name
    lines = source.split("\n")
    ln = issue["line"] - 1

    lines.insert(ln, f"{var} = None  # auto-init fix")

    return "\n".join(lines)
