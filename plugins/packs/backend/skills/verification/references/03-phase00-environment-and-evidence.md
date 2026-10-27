# PHASE-00 Readiness, Acceptance Environment, and Evidence Template

> Topic: Backend `PHASE-00` readiness checklist, running-service acceptance environment for Test Runner, never-production safety rules, and the copy-ready Phase Gate Evidence template.

General environment discipline (probe first, never stop processes you did not start, isolated test data, labeled mocks, `BLOCKED` on environment failure) belongs to `quality-acceptance`; this reference provides the concrete Backend rules and evidence template.

---

## 1. `PHASE-00` Readiness Checklist (Backend)

A backend work item prepares the developer toolchain, test database, migrations, seed fixtures, and outbound third-party sandboxes or Mockoon mocks (`mocks/<provider>_mockoon.json`). Each `[EXECUTE]` item in `phases/phase-00-prepare.md` is verified with an evidence row:

| Readiness Item | Verification Command (`cwd`: service root) | Expected (`PASS`) |
|---|---|---|
| **P0-00: Developer Tools** | `coder-nexus setup tools --pack backend --check` and `uv run ruff --version`, `uv run mypy --version`, `uv run pytest --version` | `TOOLS: READY` (install missing via `coder-nexus setup tools --pack backend -y`); versions recorded |
| **P0-01: Test DB Reachable & Guarded** | `uv run pytest tests/integration --collect-only -q` + guard smoke test | Collection succeeds; `conftest.py` guard rejects non-test `DATABASE_URI` |
| **P0-02: Migrations Apply Cleanly** | `G5` (`alembic heads && alembic upgrade head && alembic check`) on disposable DB | Single head; `upgrade head` exits `0`; `alembic check` clean |
| **P0-03: Seed / Fixtures for Roles** | Workspace seed command on test DB | Test accounts exist for each role named in `design.md` (record role names only, never credentials) |
| **P0-04: Outbound 3rd-Party Sandbox / Mockoon** | Sandbox key check in `.env` (`3RD_PARTY_READY`) or `mockoon-cli start --data mocks/<provider>_mockoon.json` + `curl` smoke check (`3RD_PARTY_MOCKOON`) | Matches `D-NN` mode; Mockoon runs labeled `3RD_PARTY_MOCKOON: <provider>` |

- Tick completed items in `phases/phase-00-prepare.md` as `[x] PREPARED / COMPLETED` (or `[x] PREPARED (NO_EXTERNAL_API)` with the reason). Never generate frontend mock files from a backend work item.

---

## 2. Running Service for Acceptance (`test_runner`)

When `test_runner` executes `quality-acceptance` on the `APPROVED` `REVIEW_REVISION`:

| Requirement | Verification Rule |
|---|---|
| **Revision Lock** | `git rev-parse HEAD` in the service root equals the `APPROVED` `REVIEW_REVISION`, and `git status --short` is clean |
| **Start Command** | Use the workspace's documented command (`uv run uvicorn app.main:app --port <port>`, `docker compose up api`, or `Makefile` target)—never invent an entrypoint |
| **Port & Health Probe** | Read port from `.env` / compose config; probe `curl -fsS http://127.0.0.1:<port>/health` (or documented health route). Non-200 after timeout → `BLOCKED` |
| **Database** | Dedicated test database migrated to `REVIEW_REVISION` via `alembic upgrade head`; never production, never a shared dev DB without explicit user approval |
| **Auth & Roles** | Obtain real tokens through the dev/test auth flow for each seeded role; test both authorized calls (`200`/`201`) and forbidden/cross-tenant calls (`403`/`404`) |
| **Persistence Proof** | Read back persisted state after mutations via the API or restricted-mode Postgres MCP (`backend-postgres`); developer unit/integration tests from `{{slot:unit-testing}}` are cited as prior evidence, never counted as acceptance |

---

## 3. Never-Production Safety Rules

1. **Never target production or unclassified URLs**: Any gate, seed, migration, or acceptance command whose `DATABASE_URI` or base URL cannot be proven to be local/test/disposable is immediately **`BLOCKED`**.
2. **Never mutate code to start the environment**: If `uvicorn`, Docker, or Alembic fails to start due to code or migration defects on `REVIEW_REVISION`, record `FAIL` / `BLOCKED` and return `CHANGES_REQUESTED`—never patch code during verification.
3. **Never drop or downgrade shared databases**: Only drop/truncate disposable databases created specifically for the verification run.
4. **Never leak secrets**: Replace all connection strings, passwords, and bearer tokens with `<REDACTED>` in logs and evidence tables.

---

## 4. Phase Gate Evidence Template (Copy-Ready)

Record one block per phase verification run (Code Writer in `writer-handoff.md`, Code Reviewer in `review-report.md`, and Test Runner in `verification.md`):

```markdown
## Phase Gates — <phase-id> @ <REVIEW_REVISION>

- **Service root (`cwd`)**: `<services/api>` | **Prefix**: `<uv run | poetry run | python -m>`
- **Tool versions**: Python `<x.y>` | ruff `<v>` | mypy `<v>` | pytest `<v>` | Alembic `<v>`
- **Test database**: `<db_name_only_REDACTED_url>` (guard: `<_test suffix | D-NN>`) | **Disposable DB (`G5`)**: `<name>`
- **Working tree**: `git status --short` → `<clean | explicit scope>`

| Gate / Claim | Command (+ `cwd`) | Revision | Exit Code | Key Output | Result |
|---|---|---|---:|---|---|
| G0 Tools check | `coder-nexus setup tools --pack backend --check` | `<sha>` | 0 | `TOOLS: READY` | `PASS` |
| G1 Format | `<prefix> ruff format --check .` (`cwd: <root>`) | `<sha>` | 0 | `<N files already formatted>` | `PASS` |
| G2 Lint | `<prefix> ruff check .` (`cwd: <root>`) | `<sha>` | 0 | `<All checks passed!>` | `PASS` |
| G3 Types | `<prefix> mypy <package>` (`cwd: <root>`) | `<sha>` | 0 | `<Success: no issues found in N source files>` | `PASS` |
| G4 Unit tests | `<prefix> pytest tests/unit -q` (`cwd: <root>`) | `<sha>` | 0 | `<N passed, 0 skipped>` | `PASS` |
| G5 Migrations | `<prefix> alembic heads && <prefix> alembic upgrade head && <prefix> alembic check` | `<sha>` | 0 | `<No new upgrade operations detected.>` | `PASS` |
| G6 Integration tests | `<prefix> pytest tests/integration -q` (`cwd: <root>`) | `<sha>` | 0 | `<N passed>` | `PASS` |
| G7 Coverage | `<prefix> pytest --cov=<package> --cov-report=term-missing -q` | `<sha>` | 0 | `<TOTAL ... NN% (fail_under=NN%)>` | `PASS` |
| G8 OpenAPI diff | export + `<oasdiff breaking | diff -u> <agreed.json> <evidence-dir>/openapi.review.json` | `<sha>` | 0 | `<Only changes declared in design.md>` | `PASS` |
```

- Valid **Result** tokens: `PASS` | `FAIL` | `BLOCKED` | `NOT_RUN` | `UNVERIFIED`.
- If a gate does not apply to the current phase (e.g., `G5` when no models/migrations changed), record a single note stating why it is out of scope rather than faking a `PASS` row.
