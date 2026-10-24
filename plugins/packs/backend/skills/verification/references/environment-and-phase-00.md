# Environment and PHASE-00 for a backend item

Detail for [backend verification](../SKILL.md) §4–§5. The rules (probe first, never stop what you did not start, isolated data, labelled stubs, `BLOCKED` on environment failure) belong to `quality-acceptance` (environment mode); this file gives the backend facts they need.

## PHASE-00 readiness (backend)

A backend item prepares test database, migrations, fixtures, and third-party provider sandboxes or Mockoon mocks (`mocks/<provider>_mockoon.json`). Typical `[EXECUTE]` items the plan may list, each with its evidence row:

| Item | Check (cwd: service root) | Expected |
|---|---|---|
| Test database reachable and guarded | `uv run pytest tests/integration --collect-only -q` then one smoke test | collection succeeds; guard rejects a non-test URL (proved by the guard's own test) |
| Migrations apply from empty | G5 on a disposable database | one head; `upgrade head` exit 0; `alembic check` clean |
| Seed / fixtures for acceptance roles | the workspace's seed command on the test database | one account per role the plan names (role names only in evidence) |
| Provider sandbox or Mockoon mock | presence of sandbox key in `.env` (if `3RD_PARTY_READY`), or `mockoon-cli start --data mocks/<provider>_mockoon.json` + `curl` smoke test (if `3RD_PARTY_MOCKOON`) | `D-NN` covers external provider mode (`3RD_PARTY_READY` vs `3RD_PARTY_MOCKOON`); results labelled `mockoon: <provider>` when mocked |
| Gate tools present | `coder-nexus setup tools --pack backend --check` and `uv run ruff --version`, `uv run mypy --version`, `uv run pytest --version` | `TOOLS: READY` (install missing via `coder-nexus setup tools --pack backend -y`); versions recorded in the pre-flight table |

Tick per `plan-and-task-contract` (`[x] PREPARED / COMPLETED`, or `[x] PREPARED (NO_EXTERNAL_API)` with the reason). A frontend client's mock files are never written from the backend item.

## Running service for acceptance (Test Runner)

| Fact | Where it comes from |
|---|---|
| Start command | the workspace's own (`uv run uvicorn app.main:app --port <port>`, `docker compose up api`, a `make` target); never invented |
| Port | `.env` / compose file; probe first (`curl -fsS http://127.0.0.1:<port>/health` or the documented health route) |
| Database | the test database, migrated to the reviewed revision with `alembic upgrade head`; never production, never a shared dev database without the user's approval |
| Revision | the `APPROVED` `REVIEW_REVISION`: `git rev-parse HEAD` in the service root equals it, tree clean |
| Accounts | seeded test users per role; tokens obtained through the real auth flow of the dev environment |
| Readiness | health route returns 200 within the agreed timeout; otherwise `BLOCKED` |
| Logs | the uvicorn process you started, written beside the evidence |

Acceptance calls go through the real HTTP API (`curl`, `httpx` script, the workspace's API test suite marked for acceptance), with real auth per role, a direct forbidden call returning 403/404 per contract, and persisted data read back. Developer tests from `{{slot:unit-testing}}` are cited, never counted as acceptance.

## Never

- Point any gate, seed or acceptance run at a production URL, or at a URL whose environment you cannot classify.
- Change application code, tests or `alembic/` to get the environment up; that is `BLOCKED` with the owner named.
- Drop, truncate or downgrade a database you did not create.
- Paste `DATABASE_URI`, passwords or tokens into evidence.
