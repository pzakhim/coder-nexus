---
name: verification
description: "Execute and verify deterministic backend quality gates for a Python + FastAPI + PostgreSQL service (`G0`–`G8`: `ruff format --check`, `ruff check`, `mypy`, `pytest` unit/integration/coverage, `alembic` disposable-DB migration checks, OpenAPI contract diff, `lint-imports`, and `pip-audit`). Use when Planning defines task Acceptance Criteria commands, Code Writer verifies phase completion (`READY_FOR_REVIEW`), Code Reviewer re-runs checks on `REVIEW_REVISION` (`APPROVED` / `CHANGES_REQUESTED`), or Test Runner prepares the environment and runs acceptance checks (`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`)."
---

# Backend Verification (Python)

This skill is `{{slot:verification}}` for the Backend pack. Claim proof rules belong to `evidence-standard`; unified flags, severities, and handoff statuses belong to [handoff-and-status](../work-item-contract/references/handoff-and-status.md) and `shared_contracts/flags_and_statuses.md`.

## 1. Detect Workspace Tooling First (Never Assume)

Before running any gate, inspect from the service root (`cwd`): `pyproject.toml`, the lockfile, `alembic.ini`, `ruff.toml` / `mypy.ini` / `setup.cfg`, `.env.example`, and existing `Makefile` / `justfile` targets.

| Lockfile | Command Prefix | Example |
|---|---|---|
| `uv.lock` | `uv run` | `uv run ruff check .` |
| `poetry.lock` | `poetry run` | `poetry run mypy app` |
| `requirements*.txt` only | activated `venv` | `python -m pytest -q` |

See [01-workspace-detection-and-task-checks.md](references/01-workspace-detection-and-task-checks.md) for signal detection and how Planning writes task-level **Acceptance Criteria** commands.

## 2. Deterministic Backend Gate Matrix (`G1`–`G8`)

Run in order from the service root holding `pyproject.toml`. A later gate never replaces an earlier one (`evidence-standard` §2).

| Gate | Purpose | Command (`uv` shown) | Runs When |
|---|---|---|---|
| **G0** | Developer Tools Check | `coder-nexus setup tools --pack backend --check` | Pre-flight (`PHASE-00`) & before first phase gate (`PASS` when `TOOLS: READY`) |
| **G1** | Format Check | `uv run ruff format --check .` | `ruff` is configured or listed as a dev dependency |
| **G2** | Static Lint | `uv run ruff check .` | `ruff` is configured or listed as a dev dependency |
| **G3** | Type Check | `uv run mypy <package>` (or `files` in `[tool.mypy]`) | `mypy` is configured or listed as a dev dependency |
| **G4** | Unit Tests | `uv run pytest tests/unit -q` | Always when `tests/unit` exists (`pytest-asyncio` & `pytest-randomly` active) |
| **G5** | Migrations (Disposable DB) | `uv run alembic heads && uv run alembic upgrade head && uv run alembic check` (plus `uv run pytest --test-alembic -q` if configured) | Phase adds/changes models or migrations; always on closing phase |
| **G6** | Integration Tests | `uv run pytest tests/integration -q` (against guarded test DB) | Repositories, routers, or migrations changed |
| **G7** | Coverage | `uv run pytest --cov=<package> --cov-report=term-missing -q` | Phase end to inspect uncovered branches; enforces `fail_under` when configured |
| **G8** | OpenAPI Contract Diff | Export `app.openapi()` to `<evidence-dir>/openapi.review.json` and diff against agreed contract ([02](references/02-gate-commands-and-results.md#g8-openapi-contract-diff)) | Route, schema, or status code changed |

- **Additional stack gates**: Run `uv run lint-imports` when `[tool.importlinter]` is present in `pyproject.toml` (`{{slot:clean-architecture}}`), and `uvx pip-audit` / `uv run pip-audit` when dependencies change (`{{slot:secure-coding-standards}}`).

## 3. Canonical Gate Results & Role Verdicts

| Gate Flag | Meaning | Rule |
|---|---|---|
| **`PASS`** | Command ran on `REVIEW_REVISION`, exited `0`, and output confirms non-empty scope (file count, test count, `All checks passed!`) | Record command, `cwd`, revision, exit code, and key output. |
| **`FAIL`** | Command ran and reported a defect (`exit != 0`, coverage below `fail_under`, drift in `alembic check`, unapproved breaking OpenAPI diff) | Blocks `READY_FOR_REVIEW`, `APPROVED`, and `ACCEPTED`. Diagnose via `{{slot:root-cause-debugging}}`. |
| **`BLOCKED`** | External/environment blocker (missing tool, config error `exit 2`, unreachable test DB, no disposable DB allowed) | Never counts as `PASS`. Name the exact blocker and owner. |
| **`NOT_RUN`** | Not executed, or exited `5` (`no tests ran`), or required tests were skipped/deselected | Never counts as `PASS`. |
| **`UNVERIFIED`** | Claim made without an executed command or verifiable evidence row | Treated as a failure to verify; never counts as `PASS`. |

- **Role Verdicts (`shared_contracts/flags_and_statuses.md` §4–§5)**:
  - **Code Writer**: `READY_FOR_REVIEW` (all applicable `G0`–`G8` `PASS` on committed revision) or `BLOCKED`.
  - **Code Reviewer**: Independently re-runs `G1`–`G8` on `REVIEW_REVISION` → `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED`.
  - **Test Runner**: Runs acceptance against a running service on `REVIEW_REVISION` → `ACCEPTED`, `CHANGES_REQUESTED`, or `BLOCKED` (developer unit/integration tests are cited, never counted as acceptance).

## 4. Mandatory Rules (`V1`–`V8`)

| ID | Mandatory Rule |
|---|---|
| **V1** | **Detect, never assume** — Read workspace config files before choosing prefix, package target, or test path. |
| **V2** | **Exit code + output together** — `exit 0` with `collected 0 items` or skipped phase tests is `NOT_RUN`, never `PASS`. |
| **V3** | **Never bend a gate** — Never add `--fix`, `--exit-zero`, `|| true`, `--deselect`, lowered `fail_under`, `# noqa`, or `# type: ignore` to force green. |
| **V4** | **Leave the verified tree clean** — Write OpenAPI exports and logs to `<evidence-dir>`, never inside the service source tree. |
| **V5** | **Never run against production** — Every DB gate (`G5`, `G6`, seed, acceptance) requires a verified test/disposable database (`_test` suffix or local Docker). Unclassified `DATABASE_URI` is `BLOCKED`. |
| **V6** | **Redact secrets in evidence** — Never print `DATABASE_URI`, passwords, API keys, or tokens in evidence rows; write `<REDACTED>`. |
| **V7** | **Revision invalidation** — Any code, test, migration, or config change creates a new revision and invalidates prior gate evidence. |
| **V8** | **Strict status vocabulary** — Use only `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `UNVERIFIED` for checks and `APPROVED` / `ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED` for verdicts. |

## 5. Reference Guides

| Topic | Reference File |
|---|---|
| Workspace signal detection, monorepo `cwd` rules, and task check examples for Planning | [01-workspace-detection-and-task-checks.md](references/01-workspace-detection-and-task-checks.md) |
| Detailed exit codes, command flags, and output rules for `G1`–`G8`, `lint-imports`, and `pip-audit` | [02-gate-commands-and-results.md](references/02-gate-commands-and-results.md) |
| `PHASE-00` backend readiness, running-service acceptance environment, never-production guard, and evidence template | [03-phase00-environment-and-evidence.md](references/03-phase00-environment-and-evidence.md) |
