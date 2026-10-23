---
skills:
  - backend-fastapi
  - backend-postgres
  - backend-database-migrations
  - backend-realtime
  - backend-api-contract-design
---
## Backend rules (Python + FastAPI + PostgreSQL)

Skills per concern: `backend-fastapi` (routers, dependencies, Pydantic v2, lifespan), `{{slot:clean-architecture}}` (layers, repository layer on SQLAlchemy 2 async), `{{slot:unit-testing}}` (pytest, pytest-asyncio, httpx), `backend-postgres` (queries, transactions, indexes), `backend-database-migrations` (Alembic), `backend-realtime` (WebSocket / SSE), `{{slot:clean-code}}` and `{{slot:secure-coding-standards}}` (Python idioms and FastAPI risks), `backend-api-contract-design` (schemas the frontend client consumes).
- An endpoint, schema, column or table the plan does not name is a `change-control` request, never an improvisation.
- **Schema changes only through an Alembic revision** in the task's scope; never `metadata.create_all()` or manual DDL on a shared database.
- **Database access for checks**: the Postgres MCP shipped by the pack (restricted mode) and `alembic` use `DATABASE_URI` from the workspace `.env` and point at a dev or test database only, never production (`backend-postgres`).
- **`PHASE-00`**: execute the plan's preparation tasks (test database reachable, `alembic upgrade head` applied, seed data, sandbox keys present). No mock server or frontend mock file is written here; an external provider is stubbed only when a `D-NN` says so, and the stubbed run is labelled.
- **Checks**: each task check runs the exact command the task names from the service root (for example `ruff check app/orders`, `mypy app`, `pytest tests/orders -q`); phase checks come from `{{slot:verification}}`. Each is an evidence row.
