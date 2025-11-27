def fix_off_by_one(source, issue):
    """
    Fix range(len(x) + 1) to range(len(x)).
    """
    lines = source.split("\n")
    ln = issue["line"] - 1

    lines[ln] = lines[ln].replace("+ 1", "")

    return "\n".join(lines)
