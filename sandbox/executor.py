import subprocess
import sys
import resource
import time
from pathlib import Path

# Maximum CPU time allowed for the child process (in seconds)
CPU_TIME_LIMIT = 5  

# Maximum memory allowed to the child process (in bytes)
# 100 MB here
MEMORY_LIMIT = 100 * 1024**2  # 100 MB

def set_limits():
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_TIME_LIMIT, CPU_TIME_LIMIT))
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))

def run_code_safely(file_path: str):
    start_time = time.time()   # Track how long the child execution takes

    try:
        # Run the user's code in an isolated child process
        result = subprocess.run(
            [sys.executable, file_path],
            text=True,
            capture_output=True,
            preexec_fn=set_limits,
            timeout=CPU_TIME_LIMIT + 1
        )
    except subprocess.TimeoutExpired:
        # Python killed the process because 'timeout' was reached
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "returncode": -1,
            "timed_out": True,
            "exec_time": CPU_TIME_LIMIT
        }
    except Exception as e:
        # Any unexpected error from subprocess itself (rare)
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -2,
            "timed_out": False,
            "exec_time": time.time() - start_time
        }
    
     # If we reach this point → execution was NORMAL (no timeout or crash)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "timed_out": False,
        "exec_time": time.time() - start_time
    }
