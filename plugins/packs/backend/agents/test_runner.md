---
skills:
  - backend-api-contract-design
  - backend-postgres
  - backend-realtime
---
## Backend rules (Python + FastAPI + PostgreSQL)

Backend acceptance runs through the real API, following `quality-acceptance` and `{{slot:verification}}`:
- **Environment**: the reviewed revision running against a test database (`DATABASE_URI` from the workspace `.env`, never production) with `alembic upgrade head` applied; record the Alembic head revision in the environment record.
- **Through the API**: calls with real tokens per role (an HTTP client or `httpx`), checking status codes, response bodies against `api_contract.json`, and a direct call with another actor's or tenant's id refused per the contract.
- **Persisted data** (`backend-postgres`): read rows back with the pack's Postgres MCP in restricted (read-only) mode or a `SELECT` against the test database; check that a failed multi-table write left nothing behind.
- **Realtime** (`backend-realtime`): connect a WebSocket / SSE client per role, trigger the event through the API and check that only in-scope clients receive it, including after a reconnect when the design names one.
- Developer unit tests are the Code Writer's and were graded in review; do not count them as acceptance evidence.
