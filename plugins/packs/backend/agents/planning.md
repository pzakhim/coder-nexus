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
- **`PHASE-00`** for a backend item lists only real preparation: test database reachable through `DATABASE_URI` from the workspace `.env`, migrations applied to it, seed data, provider sandbox keys confirmed present. No mock server is planned on the backend side.
