import traceback
import re

def parse_traceback(stderr: str):
    if not stderr or "Traceback(most recent call last)" not in stderr:
        return {
            "has_error": False,
            "error_type": None,
            "message": stderr.strip(),
            "line": None,
            "file": None,
            "raw": stderr
        }
    
    # Extracting the last line
    last_line = stderr.strip().split("\n")[-1]

    # Pattern splits
    match = re.match(r"(\w+Error|Exception):\s*(.*)", last_line)
    if match:
        error_type = match.group(1)
        message = match.group(2)
    else:
        error_type = None
        message = last_line


    file_path = None
    line_number = None
    code_line = None
    column_number = None

    # Extract the line number and file
    file_line_re = re.search(r'File "(.+?)", line (\d+)', stderr)

    if file_line_re:
        file_path = file_line_re.group(1)
        line_number = int(file_line_re.group(2))
    else:
        file_path = None
        line_number = None

    # Extract the line that caused the error
    code_line = None
    lines = stderr.split("\n")
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("File ") and i + 2 < len(lines):
            # Next next line is code snippet
            code_line = lines[i + 2].strip()

    return {
        "has_error": True,
        "error_type": error_type,
        "message": message,
        "line": line_number,
        "file": file_path,
        "code": code_line,
        "raw": stderr
    }