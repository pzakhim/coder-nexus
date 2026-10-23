---
skills:
  - backend-api-contract-design
  - backend-fastapi
---
## Backend rules (Python + FastAPI + PostgreSQL)

- **API docs come from the running app's OpenAPI** (`/openapi.json` of the reviewed revision, or `app.openapi()` exported by a script the workspace already has), never written by hand: summarise new and changed endpoints, schemas, status codes and error codes for the frontend client, and note any difference from `api_contract.json` as a finding for the coordinator, not a doc fix.
- `as-built.md` names the Alembic revisions the work added and the head revision it was tested on.
