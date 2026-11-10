from pathlib import Path
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.agent import plan_issue, stage_change, validate_command

app = FastAPI(title="Autonomous AI Software Engineer", version="0.1.0")
WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)
class PlanRequest(BaseModel): issue: str = Field(min_length=1)
class ChangeRequest(BaseModel): path: str; content: str; approved: bool = False
class CheckRequest(BaseModel): command: str
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/plan")
def plan(req: PlanRequest):
    try: return plan_issue(req.issue)
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc
@app.post("/workspace/change")
def change(req: ChangeRequest):
    try: return {"written": stage_change(WORKSPACE, req.path, req.content, req.approved)}
    except (ValueError, PermissionError) as exc: raise HTTPException(400, str(exc)) from exc
@app.post("/workspace/check")
def check(req: CheckRequest):
    try: command = validate_command(req.command)
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc
    result = subprocess.run(command.split(), cwd=WORKSPACE, capture_output=True, text=True, timeout=60, check=False)
    return {"command":command,"returncode":result.returncode,"stdout":result.stdout[-8000:],"stderr":result.stderr[-8000:]}
