import pytest
from pathlib import Path
from app.agent import plan_issue, stage_change, validate_command

def test_plan(): assert len(plan_issue("Add health endpoint")["steps"]) >= 3
def test_requires_approval(tmp_path):
    with pytest.raises(PermissionError): stage_change(tmp_path, "a.txt", "x", False)
def test_rejects_path_escape(tmp_path):
    with pytest.raises(ValueError): stage_change(tmp_path, "../outside.txt", "x", True)
def test_command_allowlist():
    with pytest.raises(ValueError): validate_command("rm -rf /")
