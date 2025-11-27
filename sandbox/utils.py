import tempfile
from .executor import run_code_safely

def run_and_capture(code: str):
    """Write user code to a temp file and execute it safely."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
        f.write(code)  # For write permission
        f.flush() # Force changes before subprocess
        file_path = f.name

    result = run_code_safely(file_path)
    return result


def is_success(result):
    """Return True if code executed successfully."""
    return result.get("returncode") == 0 and not result.get("timed_out")

def is_timeout(result):
    """True only if wall-clock timeout occurred."""
    return result.get("timed_out") == True

def get_error_type(result):
    """Basic fallback: extract first error type from stderr."""
    stderr = result.get("stderr", "")
    if ":" in stderr:
        return stderr.split(":")[0].split("\n")[-1]
    return None

def get_traceback(result):
    """Return relevant stderr traceback."""
    return result.get("stderr", "")

def summarize_result(result):
    """Return clean dictionary for UI/logs."""
    return {
        "success": is_success(result),
        "timeout": is_timeout(result),
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr"),
        "exec_time": result.get("exec_time")
    }