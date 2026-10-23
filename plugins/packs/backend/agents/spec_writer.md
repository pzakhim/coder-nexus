---
skills:
  - {{slot:clean-architecture}}
  - backend-api-contract-design
---
## Backend rules (Python + FastAPI + PostgreSQL)

- **Detection signature**: `pyproject.toml` (or `requirements*.txt`) with `fastapi`, an `alembic/` folder or `alembic.ini`, SQLAlchemy models  $\implies$ Target Platform: `backend`, Framework: `fastapi`. Record the package manager (`uv.lock`, `poetry.lock` or pip) as a verified fact.
- **Verified baseline facts** (`codebase-notes.md` §3): existing `APIRouter` modules and route prefixes, auth dependency and roles, SQLAlchemy models and their tables, the latest Alembic revision, existing error codes and the exception handler, realtime endpoints (WebSocket / SSE) if any.
- **Backend fields** the shared templates leave to the stack, in `brief.md` / `requirements.md` / `codebase-notes.md`:
  - **Target Service** (the package or service root that holds `pyproject.toml`);
  - endpoints with method, path and auth (who may call it, on which objects, in which data scope);
  - tables affected (new, altered, read only);
  - the handshake reference `api_contract.json` when the frontend client consumes the endpoints (`backend-api-contract-design`);
  - scenarios written as "request → response + persisted change / error response + nothing persisted";
  - `codebase-notes.md` §5: validation schemas (field, type, bounds, required) and error codes per endpoint.
- **Questions to queue** as `Q-NN` when the request does not state them:
  - *Endpoints*: idempotency of create/retry, pagination and sort, partial vs full update, which status code for "not yours" (404 or 403).
  - *Data*: ownership and data scope of each record, uniqueness rules, soft vs hard delete, what happens to existing rows when a column becomes required.
  - *Realtime*: which events are pushed, to whom (scope), delivery guarantee expected by the frontend client, behavior on reconnect.
- **Handshake requests** from the frontend client (`api_gap_report.md` / `api_contract.json`) are checked for feasibility, authorization and schema compatibility per `backend-api-contract-design` and the installed plugin's `shared_contracts/api_handshake_protocol.md`.
