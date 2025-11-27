from fastapi import FastAPI
from pydantic import BaseModel

from sandbox.utils import run_and_capture
from errors.parser import parse_traceback
from errors.classifier import classify_error

app = FastAPI()

class CodeInput(BaseModel):
    code: str

@app.post("/run")
def run_code(payload: CodeInput):
    # 1️⃣ Run the code in sandbox
    result = run_and_capture(payload.code)

    # 2️⃣ Parse traceback (only if error)
    stderr = result.get("stderr", "")
    parsed = parse_traceback(stderr) if stderr else {}

    # 3️⃣ Classify error type
    category = classify_error(parsed) if parsed else "NO_ERROR"


    return {
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr"),
        "parsed": parsed,
        "category": category,
        "success": result.get("returncode") == 0
    }
