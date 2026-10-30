---
skills:
  - backend-api-contract-design
  - backend-postgres
  - backend-database-migrations
  - backend-realtime
  - backend-fastapi
---
## Backend rules (Python + FastAPI + PostgreSQL)

Design with `{{slot:architecture-design}}`; layer placement from `{{slot:clean-architecture}}`.
- **Codebase audit**: read `pyproject.toml`, the app factory and lifespan, router registration, dependency functions (`Depends`), settings, SQLAlchemy models, the Alembic revision chain and existing tests. A schema, transaction or layering trade-off becomes `Q-NN` (`OPEN`).
- **`design.md` backend sections**: endpoints (method, path, auth dependency, request/response Pydantic schemas, status codes, error codes) consistent with `api_contract.json` when the frontend client consumes them (`backend-api-contract-design`); tables, columns, indexes and constraints (`backend-postgres`); the migration plan with expand/backfill/contract steps and rollback (`backend-database-migrations`); realtime channels and their scope (`backend-realtime`); FastAPI wiring (routers, dependencies, lifespan resources) per `backend-fastapi`.
- **Inside a phase**, order tasks by layer: Alembic migration → SQLAlchemy model and repository → service (authorization, transaction) → router and schemas → tests per layer. Each task's **Expected** names the status code, response body or row it proves.
- **Task check commands** are real invocations with their cwd (the service root), prefixed as the workspace runs tools (`uv run`, `poetry run` or the virtualenv), for example `ruff check app/orders`, `mypy app`, `pytest tests/orders/test_order_service.py -q`, `alembic upgrade head` against the test database. Take the commands from `{{slot:verification}}`; never invent a tool the workspace does not have.
- **`PHASE-00`** for a backend item lists real preparation: test database reachable through `DATABASE_URI` from the workspace `.env`, migrations applied to it, seed data, provider sandbox keys confirmed present (`3RD_PARTY_READY`), or `mocks/<provider>_mockoon.json` with agreed Pass/Fail triggers when external providers are mocked (`3RD_PARTY_MOCKOON`).
- **Gate 3 Backend `test-plan.md` (`E2E-01..E2E-N`) & `final_qa` L3 Escalation**:
  - Author `.superpowers/work-items/<slug>/vN/test-plan.md` defining sequential `E2E-01..E2E-N` scenarios for `test_runner` across the **Backend Verification Ladder**: (1) disposable/test DB schema & migration gate (`alembic upgrade head` against `DATABASE_URI`), (2) live HTTP/REST endpoint requests per role (`httpx`, status codes, `api_contract.json` schema compliance, and cross-actor/cross-tenant `403` refusal), (3) persisted database state & multi-table transaction rollback verification (`backend-postgres` read-only MCP / `SELECT`), and (4) WebSocket / SSE realtime event delivery & reconnection (`backend-realtime`).
  - When `bug_fixer` raises an `L3` `PCR-NN.md` during `final_qa` (e.g., an Alembic schema/migration flaw, a breaking `api_contract.json` / OpenAPI contract mismatch, an auth/tenant-scope dependency issue, or a shared `app/core/` transaction/session wiring flaw), resolve it via `change-control` before `test_runner` re-verifies `E2E-01..E2E-N` from start to finish.
