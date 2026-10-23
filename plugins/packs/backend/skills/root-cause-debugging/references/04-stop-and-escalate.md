# 04 — Stop and escalate

Rules D10 and D12 of [root-cause-debugging](../SKILL.md). Why this file exists: code changes for environment problems break things for everyone, and endless attempts burn time and drift out of scope. Status words: [handoff-and-status §3](../../work-item-contract/references/handoff-and-status.md).

## Environment, not code

| Sign | Check | Report |
|---|---|---|
| `ConnectionRefusedError`, `OSError: Connect call failed`, `asyncpg` `CannotConnectNowError` | `pg_isready -h <host> -p <port>`; `lsof -i :5432` | `BLOCKED` — database not reachable |
| `KeyError` / Pydantic `ValidationError` from the settings class at startup, missing `DATABASE_URL` or secret | Compare required settings with what is set (names only, never print values) | `BLOCKED` — missing env var or credential |
| `UndefinedTableError` / `UndefinedColumnError` while models and migrations agree | `uv run alembic current` vs `uv run alembic heads` | `BLOCKED` — migrations not applied on that database |
| `ModuleNotFoundError` / `ImportError` for a declared dependency, versions differ from `uv.lock` | `uv sync --locked --dry-run` (or the workspace's equivalent); `uv run python -V` | `BLOCKED` — stale or drifted virtualenv / wrong Python |
| Port already in use, uvicorn not answering | `lsof -i :<port>` | `BLOCKED` — another process owns the port |
| Stale cache or generated files (`.pytest_cache`, `__pycache__`, `.mypy_cache`) suspected | Rerun with `-p no:cacheprovider`; `uv run mypy --no-incremental <file>` | Code if it still fails; otherwise note the cache in the hand-off |
| Shared stack (Docker Compose database, staging service) started by someone else misbehaves | Observe only | `BLOCKED` — do not stop, restart or reconfigure it |
| Failure reproduces on a clean, correct environment | — | It is code: continue in [02](02-isolate-and-hypothesize.md) |

Never stop or restart a stack you did not start, never change shared configuration (`.env`, Compose files, database settings) to get past an environment problem, and never patch code around it. Why: the next person inherits a hidden workaround, and the real problem stays. A `BLOCKED` names the blocker and carries the evidence row of the check above.

## Time-box

After **3 failed fix attempts** (a fix whose reproduction still fails) with a code cause still unfixed, stop. Do not try a fourth. Return `BLOCKED` to the coordinator with the report block ([06](06-report.md)): reproduction, hypotheses tried and ruled out, current best guess, what evidence is missing. The coordinator decides the next step (Planning or the user). Why: three failures usually mean the model of the problem or the design is wrong, not the fourth patch.

Missing information (a redacted payload, access to an environment, the intended behaviour) → `NEEDS_CONTEXT`, stating what you tried and exactly what is needed.

## Back to the gate

A fix that is not a debugging fix stops here and goes to `change-control`. Never decide it yourself.

| The fix would… | Class (Planning decides) |
|---|---|
| Need a file outside the task's Scope / Files, a reordered task, or a corrected check command | `TASK_DETAIL` |
| Change an endpoint path, status code, request/response schema or error shape (see `api-contract-design`) | `DESIGN_CHANGE` |
| Add, upgrade or pin a dependency in `pyproject.toml` / `uv.lock` | `DESIGN_CHANGE` |
| Change the database schema beyond what the task approves (table, column, constraint, index) | `DESIGN_CHANGE` |
| Move responsibility between layers or contradict a `D-NN` | `DESIGN_CHANGE` |
| Change user-visible behaviour or an approved AC | `SCOPE_CHANGE` |

Why: these change what was approved at a gate; a Code Writer fixing a bug has no authority over them.
