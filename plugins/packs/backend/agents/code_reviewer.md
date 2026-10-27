---
skills:
  - backend-api-contract-design
  - backend-fastapi
  - backend-postgres
  - backend-database-migrations
  - backend-realtime
---
## Backend rules (Python + FastAPI + PostgreSQL)

Grade the phase with `{{slot:code-review}}` inside the `review-workflow` passes, using `{{slot:clean-architecture}}`, `{{slot:unit-testing}}`, `{{slot:clean-code}}` and `{{slot:secure-coding-standards}}` for their axes, plus:
- `backend-api-contract-design` for request/response schemas, status codes and error shapes against `api_contract.json` / `design.md`;
- `backend-database-migrations` for every Alembic revision (reversible `downgrade`, safe on existing rows, matches the models);
- `backend-postgres` for query scope, transactions and indexes; `backend-realtime` for event scope and connection handling; `backend-fastapi` for dependency and lifespan wiring;
- When reviewing `PHASE-00` with `3RD_PARTY_MOCKOON`, audit `mocks/<provider>_mockoon.json` against the trigger table in `design.md`, verify via `mockoon-cli` / `curl`, and confirm application code uses real `httpx.AsyncClient` without fake provider classes.
- Rerun the checks yourself from the service root with the workspace's prefix (`ruff check`, `mypy`, `pytest` on the phase's test paths) via `run_command`; migrations are applied only to a dev or test database.
