from pathlib import Path

ALLOWED_CHECKS = {"python -m pytest", "python -m compileall ."}


def plan_issue(issue: str) -> dict:
    text = issue.strip()
    if not text:
        raise ValueError("Issue description cannot be empty")
    return {
        "goal": text,
        "steps": [
            "Inspect the affected modules and existing tests",
            "Implement the smallest change that satisfies the issue",
            "Add or update regression tests",
            "Run an approved validation command and review the diff",
        ],
        "approval_required": True,
        "note": "Deterministic starter planner; replace with an LLM-backed Planner adapter for autonomous reasoning.",
    }


def stage_change(workspace: Path, relative_path: str, content: str, approved: bool) -> str:
    if not approved:
        raise PermissionError("Explicit approval is required before writing files")
    root = workspace.resolve()
    target = (root / relative_path).resolve()
    if target != root and root not in target.parents:
        raise ValueError("Path escapes the configured workspace")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return str(target.relative_to(root))


def validate_command(command: str) -> str:
    if command not in ALLOWED_CHECKS:
        raise ValueError(f"Command is not allow-listed: {command}")
    return command
