# 03 — Backend `PHASE-00`, Gate 2/3 Ordering, and `design.md` Template

> Topic: PHASE-00 readiness checklist, Gate 2 validation workflow, Gate 3 vertical task ordering, and copy-ready design.md template (`AD9`, `AD10`)

## 1. Backend `PHASE-00` Readiness Checklist (`AD9`)

Before feature implementation begins in `PHASE-01`, `PHASE-00` (`phases/phase-00-prepare.md`) establishes a verified environment and test baseline:

| Task ID | Scope | Verification Command (`cwd`: service root) | Gate Criteria |
|---|---|---|---|
| `P0-00` | Developer tools gate | `coder-nexus setup tools --pack backend --check` | `PASS` (`TOOLS: READY`) |
| `P0-01` | Baseline lint & test health | `uv run ruff check . && uv run pytest -q` | `PASS` (baseline green or pre-existing failures recorded) |
| `P0-02` | Isolated test DB & migrations | `docker compose up -d postgres && uv run alembic upgrade head` | `PASS` (migrations apply cleanly to test DB head) |
| `P0-03` | OpenAPI contract snapshot | Export base OpenAPI schema (`contracts/openapi.base.json`) | `PASS` (snapshot recorded) |
| `P0-04` | Seed accounts & test fixtures | `uv run python scripts/seed_test_data.py` (or test fixtures) | `PASS` (actors/roles from Test Data table seeded) |
| `P0-05` | Outbound 3rd-party provider | Sandbox probe (`3RD_PARTY_READY`) or `mockoon-cli start --data mocks/<provider>_mockoon.json` (`3RD_PARTY_MOCKOON`) | `PASS` (reachable & trigger rules verified) |

Never connect test runs or `PHASE-00` commands to a production database. If a required service or sandbox is unavailable, mark `PHASE-00` as `BLOCKED` with exact command output.

---

## 2. Gate 2 Validation & Gate 3 Layer Ordering (`AD10`)

1. **Gate 2 Validation Workflow:**
   - Run `validate_proposal_spec` on both `codebase-notes.md` and `design.md` (`PASS` required).
   - Run `gate-review` (`modes/design.md`) and `cold-reader-check` on `design.md`.
   - Resolve any remaining user-choice items via `Q-NN` → `D-NN`. Present Gate 2 to the user via `ask_question` only when `OPEN` `Q-NN` count is **0**.
2. **Gate 3 Phase & Task Ordering (`implementation-planning`):**
   - Each phase after `PHASE-00` delivers one vertical observable behavior, scheduling the highest-risk behavior first.
   - Inside each phase, order tasks from inner to outer layers (`{{slot:clean-architecture}}`): **Domain entity/interfaces → ORM model & Alembic migration → Repository implementation → Pydantic schemas → Application service/use case → FastAPI router & DI wiring**, pairing each behavior with unit/integration tests covering the Pass, Fail, and Empty rows from `design.md`.

---

## 3. Copy-Ready Backend `design.md` Template

```markdown
# Design: {{FeatureTitle}} — {{Version}}

> **Document type**: DESIGN
> **Feature**: {{module}}/{{feature}}
> **Version**: {{Version}}
> **Created**: {{CreatedDate}}
> **Source references**: {{SourceReferences}}
> **Status**: PENDING_REVIEW
> **Approval reference**: NONE

- **Requirements reference**: `requirements.md`
- **Context reference**: `codebase-notes.md`
- **Gate 1 approval reference**: {{ActualUserApprovalReference}}
- **Scope classification**: {{INIT_OR_EXTEND_OR_CORE_IMPACT}}

## Architecture profile

```yaml
architecture_profile:
  mode: {{imespro_or_external_structured_or_external_standard}}
  core_source: {{VerifiedPackageOrClientSourceOrNone}}
  evidence: {{ActualDependencyBaseAndConsumerPaths}}
```

- **Selection rationale / existing approval**: {{ProfileEvidenceAndApprovalReference}}

## Goal alignment

| Goal | Endpoints, models and handlers that deliver it | Owning PHASE |
|---|---|---|
| G-01 | {{DeliverablesDeliveringG01}} | PHASE-01 |

## Architectural decision

- **Confirmed architecture (`D-NN`)**: {{ConfirmedArchitectureSummary}}
- **Decision log reference**: Evaluated trade-offs and decisions are locked in `codebase-notes.md` (`## 1. Decision Log (D-NN)`).

## Module and folder diff

- **Current structure and owners**: {{CurrentExistingPaths}}
- **Proposed structure and owners**:
  - `app/api/routers/{{feature}}.py`
  - `app/schemas/{{feature}}.py`
  - `app/services/{{feature}}.py`
  - `app/models/{{feature}}.py`
  - `app/repositories/{{feature}}.py`
  - `alembic/versions/{{migration_id}}.py`
- **Shared consumers affected**: {{AffectedConsumersOrNone}}

## Behavior, data, and state

### API contract

- `POST /api/v1/{{resource}}`: Create {{resource}}
  - Auth: `Depends(get_current_user)` (Roles: `user`, `admin`)
  - Request: `{{Resource}}Create`
  - Response `201`: `{{Resource}}Read`
  - Errors: `400` Bad Request, `401` Unauthorized, `403` Forbidden, `404` Not Found, `409` Conflict, `422` Validation Error

### Data model

- Table `{{table_name}}`:
  - `id`: UUID / BigInteger (Primary Key)
  - `owner_id` / `tenant_id`: Indexed scope column
  - `created_at`: DateTime(timezone=True)
  - `updated_at`: DateTime(timezone=True)
  - Foreign keys, unique/check constraints, and indexes.

### Test data per endpoint

| Endpoint | Scenario | Role | Precondition | Input | Expected Status | Expected Output |
|---|---|---|---|---|---|---|
| `POST /api/v1/{{resource}}` | Pass nominal | `user` | Valid authenticated session | `{"name": "test"}` | `201 Created` | `{"id": "...", "name": "test"}` |
| `POST /api/v1/{{resource}}` | Fail validation | `user` | Valid authenticated session | `{"name": ""}` | `422 Unprocessable` | Validation error details |
| `POST /api/v1/{{resource}}` | Fail unauthenticated | `guest` | No bearer token | `{"name": "test"}` | `401 Unauthorized` | Auth error details |

## UI design system

Not applicable. This is a backend service providing REST/OpenAPI APIs and realtime event streams.

## Integration, errors, and risks

- **Error handling**: Uniform error envelope `{"error": {"code": "...", "message": "...", "details": ...}}`.
- **Outbound providers & mocking**: {{SandboxCredentialsOrMockoon3rdPartyTable}}
- **Database transactions**: Multi-statement operations wrapped in `async with session.begin():` (or `UnitOfWork`) with verified rollback on error.
- **Migration & rollback**: Reversible Alembic migration script verified against test database.

## Verification strategy

- `uv run ruff check .` (cwd: service root)
- `uv run ruff format --check .` (cwd: service root)
- `uv run mypy app` (cwd: service root)
- `uv run pytest tests/unit -q` (cwd: service root)
- `uv run pytest tests/integration -q` (cwd: service root)
- `uv run alembic upgrade head` (cwd: service root)

## Gate 2 approval

- **Decision summary**: {{UserFacingDesignSummary}}
- **Approved response**: NONE
- **Approved document revision**: NONE
```
