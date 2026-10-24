# Backend Design Sections

Guidance for writing each section of `design.md` for a backend service (FastAPI + SQLAlchemy + PostgreSQL), ensuring conformity with `validate_proposal_spec` and Gate 2 review.

## 1. Scope Classification

Classify the work item in the document frontmatter / metadata:
- `INIT`: New service, standalone microservice, or completely new resource domain.
- `EXTEND`: Adding endpoints, models, or fields to an existing domain without breaking contracts.
- `CORE IMPACT`: Modifying core settings, database engine, auth dependency, session lifecycle, global middleware, or shared models.

## 2. Goal Alignment

Map every goal from `requirements.md` (`G-NN`) directly to architectural deliverables:
- Table listing `Goal ID`, `Endpoints / Models / Handlers`, and `Owning PHASE-NN`.
- Every element in `design.md` must trace back to at least one `G-NN`.

## 3. Architectural Decision

Document the confirmed technical approach, citing locked `D-NN` from `codebase-notes.md`:
- Technology choices (libraries, patterns, schema styles).
- **Deferred decisions**: Choices deferred to future versions, why they can wait, and trigger conditions.
- **Complexity justifications**: Deviations from Clean Architecture or standard idioms, why required, and simpler alternatives rejected.

## 4. Module and Folder Diff

List new, modified, or deleted files per layer conforming to `{{slot:clean-architecture}}`:
- Presentation: `app/api/routers/<feature>.py`, `app/schemas/<feature>.py`
- Business / Application: `app/services/<feature>.py`
- Domain & Data: `app/models/<feature>.py`, `app/repositories/<feature>.py`
- Migrations: `alembic/versions/<id>_<desc>.py`

## 5. Behavior, Data, and State

- **API Contract**: Endpoints, HTTP methods, route paths, auth dependencies, input schemas, response models, and error responses.
- **Data Model**: SQLAlchemy 2 models, primary keys, foreign keys, indexes, unique constraints, and relationships.
- **Test Data per Endpoint**: Explicit Pass, Fail, and Empty test scenarios per endpoint ([03](03_endpoint_test_data.md)).

## 6. UI Design System

For backend services, this section contains the standard non-applicability declaration to satisfy `validate_proposal_spec`:
`Not applicable. This is a backend service providing REST/OpenAPI APIs and realtime event streams.`

## 7. Integration, Errors, and Risks

- **Error Catalog**: Explicit error bodies, HTTP status codes, and error codes (`ERR_<DOMAIN>_<CODE>`).
- **Outbound Providers & Mockoon Strategy**: Sandbox credentials (`3RD_PARTY_READY`) or `Mockoon 3rd-Party Trigger & Test Data Table` (`3RD_PARTY_MOCKOON` with `mocks/<provider>_mockoon.json`).
- **Transaction Boundaries**: Multi-table operations wrapped in atomic async sessions with verified rollback.
- **Realtime Channels**: SSE or WebSocket streams, message schemas, and replay buffers.
- **Migration & Rollback**: Safe expand-contract steps, lock duration considerations, and rollback procedures.

## 8. Verification Strategy

Runnable commands with cwd:
- Lint & format: `uv run ruff check .`, `uv run ruff format --check .`
- Type checking: `uv run mypy app`
- Developer tests: `uv run pytest tests/unit -q`, `uv run pytest tests/integration -q`
- Migration verification: `uv run alembic upgrade head` on test database
