# Workspace detection and task checks

Detail for [backend verification](../SKILL.md) §1. Planning reads this during readiness (core `implementation-planning`, codebase readiness reference) to write task **Acceptance Criteria** commands; the Code Writer and Code Reviewer read it before their first gate. Folder and layer conventions belong to `{{slot:clean-architecture}}`.

## What to read, and what it decides

| File / signal | Decides |
|---|---|
| Lock file (`uv.lock`, `poetry.lock`, `requirements*.txt`) | Command prefix ([SKILL §1](../SKILL.md#1-detect-never-assume)) |
| `pyproject.toml` `[project]` / `[tool.poetry]` | Package name for `mypy <package>` and `--cov=<package>`; Python version |
| `[tool.ruff]` / `ruff.toml` | G1/G2 apply; line length and rule set are the workspace's |
| `[tool.mypy]` / `mypy.ini` | G3 target (`files`, `packages`), strictness, plugins |
| `[tool.pytest.ini_options]` | `testpaths`, `addopts` (may already include `--cov`), `asyncio_mode` and loop scopes, markers |
| `[tool.coverage.*]` / `.coveragerc` | G7 applies only with `fail_under` |
| `[tool.importlinter]` | extra layer-contract gate `lint-imports` |
| `alembic.ini` + `alembic/env.py` | G5; which variable carries the database URL |
| `.env.example` | names of `DATABASE_URI`, `TEST_DATABASE_URL`; values never copied into documents |
| `docker-compose*.yml` | local PostgreSQL service and port for test / disposable databases |
| `Makefile` / `justfile` / CI workflow | the team's existing command spelling; the plan reuses it when it runs the same tools |
| Committed `openapi.json` / `api_contract.json` | G8 baseline |

Missing piece the plan needs (no test database, no ruff config while the plan demands lint) → record it as a readiness gap in `codebase-notes.md` and plan a `PHASE-00` task or ask for a `D-NN`. Never let the Code Writer discover it mid-phase.

## Monorepo

A repo with several services has several service roots. Every command names its cwd (`services/api`), and the prefix comes from that root's lock file. Reason: the same command from the repo root collects other services' tests or none.

## Task check examples (for `implementation-plan.md`)

Each task gets one narrow, runnable check plus the output that proves it ([plan-and-task-contract](../../work-item-contract/references/plan-and-task-contract.md)).

| Task kind | Acceptance Criteria (cwd: `services/api`) | Expected |
|---|---|---|
| New service rule | `uv run pytest tests/unit/services/test_orders.py::test_cancel_order_when_already_shipped_raises_order_not_cancellable -q` | `1 passed` (red first: `1 failed … OrderNotCancellable not raised`) |
| Schema validation | `uv run pytest tests/unit/schemas/test_orders.py -q` | `6 passed, 0 skipped` |
| Repository query | `uv run pytest tests/integration/repositories/test_orders.py -q` | `4 passed` against the test DB |
| Router + authZ | `uv run pytest tests/integration/api/test_orders.py -k "other_owner" -q` | `2 passed` (403/404 cases) |
| New migration | `uv run alembic upgrade head && uv run alembic check` on the disposable DB | `No new upgrade operations detected.` |
| Type-only change | `uv run mypy app/services/orders.py` | `Success: no issues found in 1 source file` |
| Route / schema contract | G8 export + `oasdiff breaking` / `diff -u` | only the differences named in `design.md` |

`-k` is allowed in a **task** check to point at the task's own tests; phase gates always run the full G4/G6 scope. Reason: a task check is narrow by design; the phase gate shows interactions.

## Phase checks (end of every phase)

G1–G4 always; G5 and G6 when the phase touched models, migrations, repositories or routers; G7 when configured; G8 when routes or schemas changed. The closing phase runs every applicable gate.
