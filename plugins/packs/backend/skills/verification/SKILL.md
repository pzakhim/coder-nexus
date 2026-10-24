---
name: verification
description: The exact gate commands for a Python + FastAPI + PostgreSQL service, detected from the workspace (uv, poetry or pip; pyproject.toml settings) - ruff check, ruff format --check, mypy, pytest -q with the coverage threshold only when the workspace sets one, alembic upgrade head and alembic check on a disposable database, and an OpenAPI diff against the agreed contract - with what counts as PASS, FAIL, BLOCKED and NOT_RUN for each, evidence rows, the never-production rule, PHASE-00 readiness for a backend item and task check examples for plans. Use when the Code Writer runs phase checks, when the Code Reviewer re-runs them on REVIEW_REVISION, when the Test Runner prepares a backend environment, and when Planning writes Acceptance Criteria commands for backend tasks.
---

# Backend Verification (Python)

This is `{{slot:verification}}` for the backend pack. How a claim is proven and recorded belongs to `evidence-standard`; the evidence row, status words and report shapes to [handoff-and-status](../work-item-contract/references/handoff-and-status.md). This file names the backend commands and how to read their results.

Detail: [gate commands and results](references/gates.md), [workspace detection and task checks](references/workspace-detection.md), [environment and PHASE-00](references/environment-and-phase-00.md), [sources](references/sources.md). Evidence block: [templates/phase-gate-evidence.md.tpl](templates/phase-gate-evidence.md.tpl).

## 1. Detect, never assume

Before the first gate, read from the service root: `pyproject.toml`, the lock file, `alembic.ini`, `ruff.toml` / `mypy.ini` / `setup.cfg` if present, `.env.example`, and any `Makefile` / `justfile` target the team already uses for the same checks. Reason: a command guessed from another project runs the wrong tool or the wrong scope and still exits 0.

| Lock file | Prefix | Example |
|---|---|---|
| `uv.lock` | `uv run` | `uv run ruff check .` |
| `poetry.lock` | `poetry run` | `poetry run mypy app` |
| `requirements*.txt` only | activated venv | `python -m pytest -q` |

A workspace target (`make check`) is used only if it runs the same tools; record the expanded commands in the evidence row. Detection detail and how Planning writes task checks: [workspace detection](references/workspace-detection.md).

## 2. The gates

cwd = the service root holding `pyproject.toml`. Run in this order; a later gate never replaces an earlier one (`evidence-standard` §2).

| # | Gate | Command (uv shown) | Runs when |
|---|---|---|---|
| G1 | Format | `uv run ruff format --check .` | ruff is configured or listed as a dev dependency |
| G2 | Lint | `uv run ruff check .` | same |
| G3 | Types | `uv run mypy <package>` (or the `files` set in `[tool.mypy]`) | mypy is configured or a dev dependency |
| G4 | Unit tests | `uv run pytest tests/unit -q` (runs with `pytest-asyncio` and `pytest-randomly` installed by `setup tools`) | always when `tests/unit` exists |
| G5 | Migrations | on a disposable DB: `uv run alembic upgrade head`, `uv run alembic check`, and `uv run pytest --test-alembic -q` (when configured) | the phase adds or changes models or migrations; always on the closing phase |
| G6 | Integration tests | `uv run pytest tests/integration -q` against the test database | repositories, routers or migrations changed |
| G7 | Coverage | `uv run pytest --cov=<package> --cov-report=term-missing -q` (`pytest-cov` installed by `setup tools`) | always on phase end to inspect uncovered branches; enforces `fail_under` when configured |
| G8 | OpenAPI diff | export `app.openapi()` and diff against the agreed contract ([gates](references/gates.md#g8-openapi-diff)) | a route, schema or status code changed |

Additional standard tools installed by `coder-nexus setup tools --pack backend` (`uv run lint-imports` from `import-linter` when `[tool.importlinter]` is present in `pyproject.toml`, and `uvx pip-audit` / `uv run pip-audit` when dependencies change per `{{slot:secure-coding-standards}}`) run alongside G1–G8. Never invent a custom threshold the workspace does not have. Reason: verification proves the agreed bar, it does not move it.

## 3. Reading results

| Result | When | Example |
|---|---|---|
| `PASS` | The gate ran on the stated revision, exit 0, and the output shows the scope ran (file count, test count, `Success: no issues found`) | `ruff check .` → `All checks passed!` |
| `FAIL` | The gate ran and reported a defect in the code under check | ruff exit 1; mypy exit 1; pytest exit 1; coverage under `fail_under`; `alembic check` reports new upgrade operations; breaking OpenAPI change not in `design.md` |
| `BLOCKED` | The gate could not execute for a reason outside the code: tool missing from the environment, config error (ruff/mypy exit 2), test database unreachable, no disposable database allowed | `connection refused` in a session fixture |
| `NOT_RUN` | Not attempted, or ran but proved nothing: pytest exit 5 ("no tests ran"), the changed tests reported as skipped or deselected | `0 passed, 3 skipped` for the phase's tests |

- Exit code and output are read together. Reason: exit 0 with `collected 0 items` proves nothing; exit 1 from a fixture `ConnectionRefusedError` is an environment problem (`BLOCKED`), not a code defect.
- A `FAIL` goes back through `root-cause-debugging`; the gate is never edited, narrowed or given `--exit-zero`, `|| true`, `--deselect` / `-k` narrowing, a lowered `fail_under`, new `# type: ignore` or `per-file-ignores` to turn green. Reason: a bent gate hides the defect it exists to show.
- `NOT_RUN`, `BLOCKED` and `UNVERIFIED` never count as `PASS` in any summary.

Full per-gate result table: [gates](references/gates.md).

## 4. Never against production

- Every database gate runs on a database whose name or host matches the agreed test rule (for example a `_test` suffix or a local Docker service), checked before the command runs. Reason: `alembic upgrade` and test fixtures write; one wrong `DATABASE_URI` is data loss.
- `DATABASE_URI` comes from the workspace `.env` and must point to a dev or test database. A URL you cannot classify is `BLOCKED`; never "try it and see".
- The Postgres MCP (`crystaldba/postgres-mcp`, restricted mode, shipped by the pack) may be used to inspect the dev/test schema and plans (`backend-postgres`). Schema changes happen only through Alembic (`backend-database-migrations`).
- Never print or paste the URL, password or tokens in evidence; write `<REDACTED>`.

## 5. Evidence

One row per gate in the format of `evidence-standard` §3, revision = the commit the gates ran on:

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| G2 lint clean | `uv run ruff check .` (cwd `services/api`) | `a1b2c3d` | 0 | `All checks passed!` | PASS |
| G6 integration tests | `uv run pytest tests/integration -q` (cwd `services/api`) | `a1b2c3d` | 1 | `1 failed, 41 passed` | FAIL |
| G5 migrations | not run: no disposable database (`D-04` forbids shared dev DB) | `a1b2c3d` | - | - | BLOCKED |

Per role: the Code Writer runs G1–G8 that apply at phase end and on the committed `REVIEW_REVISION`; the Code Reviewer re-runs them itself (`review-workflow` pass 1); the Test Runner runs the acceptance checks of `quality-acceptance` against a running service prepared per [environment and PHASE-00](references/environment-and-phase-00.md), never counting developer tests as acceptance.
