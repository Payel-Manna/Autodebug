import re

def parse_traceback(stderr: str):
    """
    Parses Python traceback stderr into structured fields.

    Returns:
    {
        "has_error": bool,
        "error_type": str | None,
        "message": str | None,
        "line": int | None,
        "column": int | None,
        "file": str | None,
        "code": str | None,
        "raw": stderr
    }
    """

    # ---------------------------------------------------------
    # CASE 1: No traceback → it's not a Python exception
    # ---------------------------------------------------------
    if not stderr or "Traceback (most recent call last)" not in stderr:
        return {
            "has_error": False,
            "error_type": None,
            "message": stderr.strip() or None,
            "line": None,
            "column": None,
            "file": None,
            "code": None,
            "raw": stderr
        }

    lines = stderr.strip().split("\n")

    # --------------------------------------------------------------------
    # 1. Extract FINAL ERROR LINE (most important)
    #    Example: "SyntaxError: invalid syntax"
    # --------------------------------------------------------------------
    last_line = lines[-1]

    # Accept ANYTHING ending with Error or Exception, including custom classes
    match = re.match(r"([\w\.]+(?:Error|Exception)):\s*(.*)", last_line)
    if match:
        error_type = match.group(1)
        message = match.group(2)
    else:
        # fallback: entire last line is message
        error_type = None
        message = last_line

    # --------------------------------------------------------------------
    # 2. Extract file + line number from traceback
    # --------------------------------------------------------------------
    file_info_pattern = r'File "(.+?)", line (\d+)(?:, in .*)?'
    file_match = re.findall(file_info_pattern, stderr)

    file_path = None
    line_number = None

    if file_match:
        file_path, line_number = file_match[-1]
        line_number = int(line_number)

    # --------------------------------------------------------------------
    # 3. Extract column offset (only SyntaxError and similar)
    # --------------------------------------------------------------------
    column = None
    caret_index = None

    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("File "):
            if i + 3 < len(lines) and lines[i+3].strip().startswith("^"):
                caret_index = lines[i+3].index("^")
                column = caret_index + 1  # 1-based indexing

    # --------------------------------------------------------------------
    # 4. Extract code line that triggered error
    # --------------------------------------------------------------------
    code_line = None

    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("File "):
            if i + 1 < len(lines):
                code_line = lines[i+1].strip()

    return {
        "has_error": True,
        "error_type": error_type,
        "message": message if message else None,
        "line": line_number,
        "column": column,
        "file": file_path,
        "code": code_line,
        "raw": stderr
    }
