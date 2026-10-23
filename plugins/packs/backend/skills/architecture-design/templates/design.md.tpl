# Design: {{FeatureTitle}} — {{Version}}

> **Document type**: DESIGN  
> **Feature**: {{module}}/{{feature}}  
> **Version**: {{Version}}  
> **Created**: {{CreatedDate}}  
> **Source references**: {{SourceReferences}}  
> **Status**: PENDING_REVIEW  
> **Approval reference**: NONE

- **Requirements reference**: [requirements.md](requirements.md)
- **Context reference**: [codebase-notes.md](codebase-notes.md)
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

### Deferred decisions

| Decision deferred | Why it can wait | Revisit trigger |
|---|---|---|
| {{DeferredDecision}} | {{ReasonNotNeededInThisVersion}} | {{TriggerEvent}} |

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
  - Errors: `400` Bad Request, `401` Unauthorized, `409` Conflict, `422` Validation Error

### Data model

- Table `{{table_name}}`:
  - `id`: UUID / Integer (Primary Key)
  - `created_at`: DateTime(timezone=True)
  - `updated_at`: DateTime(timezone=True)
  - Foreign keys, constraints, and indexes.

### Test data per endpoint

| Endpoint | Scenario | Role | Precondition | Input | Expected Status | Expected Output |
|---|---|---|---|---|---|---|
| `POST /api/v1/{{resource}}` | Nominal create | `user` | Valid authenticated session | `{"name": "test"}` | `201 Created` | `{"id": "...", "name": "test"}` |
| `POST /api/v1/{{resource}}` | Invalid input | `user` | None | `{"name": ""}` | `422 Unprocessable` | Validation error details |

## UI design system

Not applicable. This is a backend service providing REST/OpenAPI APIs and realtime event streams.

## Integration, errors, and risks

- **Error handling**: Uniform error envelope `{"error": {"code": "...", "message": "...", "details": ...}}`.
- **Database transactions**: Multi-statement operations wrapped in `async with session.begin():`.
- **Migration & rollback**: Reversible Alembic migration script verified against test database.

## Verification strategy

- `uv run ruff check .` (cwd: service root)
- `uv run ruff format --check .` (cwd: service root)
- `uv run mypy app` (cwd: service root)
- `uv run pytest tests/unit -q` (cwd: service root)
- `uv run pytest tests/integration -q` (cwd: service root)
- `uv run alembic upgrade head` (cwd: service root)

## Gate 2 approval

Pending user review.
