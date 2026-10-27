# Workspace Detection and Task Checks

> Topic: Service-root signal detection (`pyproject.toml`, lockfiles, `alembic.ini`), monorepo `cwd` discipline, and task-level Acceptance Criteria command examples for `implementation-plan.md`.

Planning reads this reference during codebase readiness (`implementation-planning`) to write task **Acceptance Criteria** and phase **Verification** commands; Code Writer and Code Reviewer read it before running their first gate. Folder and layer conventions belong to `{{slot:clean-architecture}}`.

---

## 1. Workspace Signals and What They Decide

| File / Signal | What It Decides |
|---|---|
| Lockfile (`uv.lock`, `poetry.lock`, `requirements*.txt`) | Command prefix (`uv run`, `poetry run`, or `python -m` in activated `venv`) |
| `pyproject.toml` `[project]` / `[tool.poetry]` | Package name for `mypy <package>` and `--cov=<package>`; Python version |
| `[tool.ruff]` / `ruff.toml` | `G1` (format) and `G2` (lint) apply; line length and rule set follow workspace config |
| `[tool.mypy]` / `mypy.ini` | `G3` target (`files`, `packages`), strictness flags, and plugins (`pydantic.mypy`) |
| `[tool.pytest.ini_options]` | `testpaths`, `addopts` (may already include `--cov`), `asyncio_mode`, loop scopes, markers |
| `[tool.coverage.*]` / `.coveragerc` | `G7` threshold enforcement (`fail_under`) |
| `[tool.importlinter]` | Architectural layer-boundary gate (`uv run lint-imports`) |
| `alembic.ini` + `alembic/env.py` | `G5` migration gate and the environment variable carrying the database URL |
| `.env.example` | Names of `DATABASE_URI`, `TEST_DATABASE_URL` (values are never copied into documents) |
| `docker-compose*.yml` | Local PostgreSQL service and port for test / disposable databases |
| `Makefile` / `justfile` / CI workflow | Team's existing command spelling; reuse only when it runs the same underlying tools |
| Committed `openapi.json` / `api_contract.json` | `G8` OpenAPI contract baseline |

- **Missing readiness prerequisite**: If the workspace lacks a test database guard, `ruff` config, or migration setup required by the plan, record it as a readiness gap in `codebase-notes.md` and schedule a `PHASE-00` task or open a `Q-NN` → `D-NN`. Never leave it for Code Writer to discover mid-phase.

---

## 2. Monorepo `cwd` Discipline

- A repository with multiple services has multiple service roots.
- Every gate command must explicitly state its working directory (`cwd: services/api`), and its command prefix comes from that service root's lockfile.
- Running `pytest`, `mypy`, or `alembic` from the wrong root collects the wrong service's tests or exits `5` (`no tests ran`).

---

## 3. Task Check Examples for `implementation-plan.md`

Each task in `implementation-plan.md` / `phases/phase-XX-<slug>.md` gets a narrow, deterministic check plus the expected output that proves it ([plan-and-task-contract](../../work-item-contract/references/plan-and-task-contract.md)).

| Task Kind | Acceptance Criteria Command (`cwd: services/api`) | Expected Output |
|---|---|---|
| **New domain/service rule** | `uv run pytest tests/unit/services/test_orders.py::test_cancel_order_when_already_shipped_raises_order_not_cancellable -q` | `1 passed` (RED first: `1 failed ... OrderNotCancellable not raised`) |
| **Schema validation** | `uv run pytest tests/unit/schemas/test_orders.py -q` | `6 passed, 0 skipped` |
| **Repository query** | `uv run pytest tests/integration/repositories/test_orders.py -q` | `4 passed` against the guarded test DB |
| **Router + authZ** | `uv run pytest tests/integration/api/test_orders.py -k "other_owner" -q` | `2 passed` (`403` / `404` cases verified) |
| **New migration** | `uv run alembic heads && uv run alembic upgrade head && uv run alembic check` (on disposable DB) | Single head; `No new upgrade operations detected.` |
| **Type-only contract** | `uv run mypy app/services/orders.py` | `Success: no issues found in 1 source file` |
| **Route / schema contract** | `G8` OpenAPI export + `oasdiff breaking` / `diff -u` | Only the additions/changes declared in `design.md` |

- **Task vs. Phase Scope**: `-k` or single-file targeting is allowed in a **task** check to isolate the task's behavior. **Phase-end gates** always run the full `G1`–`G8` scope (`G1`–`G4` always; `G5`–`G6` when models, migrations, repositories, or routers changed; `G7` at phase end; `G8` when routes or schemas changed; all applicable gates on the closing phase).
