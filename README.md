# Autonomous AI Software Engineer

A safe, local-first coding-agent reference app. It turns a GitHub-style issue into a structured implementation plan, stages proposed file changes inside a dedicated workspace, and runs only explicitly allow-listed checks. Every write is gated by an approval flag.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs. Run `pytest`.

## Safety model
- Workspace is restricted to `./workspace` by default.
- No arbitrary shell execution; validation commands are selected from an allow-list.
- File changes require `approved: true`.
- This is a deterministic agent scaffold; connect an LLM planner through the Planner interface for model-driven plans. It does not autonomously open PRs or claim to solve arbitrary issues.
