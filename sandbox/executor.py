import subprocess
import sys
import resource
import time
from pathlib import Path

CPU_TIME_LIMIT = 5          # seconds
MEMORY_LIMIT = 100 * 1024**2  # 100 MB

def set_limits():
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_TIME_LIMIT, CPU_TIME_LIMIT))
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))

def run_code_safely(file_path: str):
    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            text=True,
            capture_output=True,
            preexec_fn=set_limits,
            timeout=CPU_TIME_LIMIT + 1
        )
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "returncode": -1,
            "exec_time": CPU_TIME_LIMIT
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -2,
            "timed_out": False,
            "exec_time": time.time() - start_time
        }

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "timed_out": False,
        "exec_time": time.time() - start_time
    }
