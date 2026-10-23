# 01 — Trust boundaries and input

Why: every injection, overflow and logic abuse starts with input nobody checked at the place it entered (SC1). Anything from outside the process is untrusted.

## Where untrusted data enters

Paths are conventions; record the workspace's real ones in `codebase-notes.md`.

| Boundary | Conventional path | Validated by |
|---|---|---|
| HTTP API (path, query, body, headers) | `app/**/router*.py`, `APIRouter` path functions | Pydantic request schemas, `Path(...)` / `Query(...)` constraints |
| Webhooks from third parties | webhook routers | Signature check first (provider secret from settings, `hmac.compare_digest`), then a Pydantic schema |
| Background jobs and queue messages | worker / consumer modules | `Model.model_validate(payload)` on every message; the job carries actor or scope explicitly |
| File uploads and imports | upload routers, import services | Size and type limits, safe parser ([04](04-stack-risks.md#file-uploads-sc10)) |
| External provider responses (HTTP APIs, identity provider) | `app/**/clients/` or adapters | `ProviderModel.model_validate(resp.json())`; errors are failures, never empty data |
| Stored user content read back | repositories | Treated as untrusted when rendered, parsed or used in a query |
| Settings and environment | `Settings(BaseSettings)` | Typed fields; the app refuses to start on a missing required value |

## Rules

- **Validate at the boundary with Pydantic v2.** Types, required fields, allow-lists (`Literal[...]`, `Enum`), length and size limits (`Field(max_length=...)`, `conint(ge=..., le=...)` or `Annotated[int, Field(ge=1, le=100)]`), list bounds (`Field(max_length=100)`). Reason: the schema is the one place every caller passes.
- **Inputs forbid unknown fields:** `model_config = ConfigDict(extra="forbid")` on request schemas. Reason: an unknown field is a client bug or a probe; silently ignoring it hides mass-assignment attempts (OWASP API3).
- **Separate input and output schemas** (`OrderCreate`, `OrderUpdate`, `OrderResponse`); server-owned fields (`id`, `tenant_id`, `owner_id`, `role`, `is_admin`, `status`, `created_by`) never appear in an input schema. Reason: one shared schema lets the client set what only the server may decide.
- **`response_model` on every route.** Reason: returning an ORM row exposes every column, including ones added later.
- **Bound every collection:** `limit: int = Query(20, ge=1, le=MAX_PAGE_SIZE)`, and the repository applies `.limit()`. Reason: unbounded fetches are resource exhaustion (OWASP API4).
- **Reject, do not repair.** Invalid input returns the contract's validation error (FastAPI's 422 or the workspace's mapped shape, see `api-contract-design`); never trim, coerce or guess silently. Reason: a guessed value is an unreviewed business decision.
- **Identifiers from the request** (sort column, filter field) map through an allow-list dict; they cannot be bound parameters. Reason: SQL identifiers are code ([04](04-stack-risks.md#injection-sc4)).
- **Client validation is UX only.** A frontend or mobile check never replaces the server schema.

## Unsafe next to safe

```python
# Unsafe: one schema for input and output, client may set server-owned fields
class Order(BaseModel):
    id: UUID | None = None
    tenant_id: UUID | None = None
    status: str = "draft"
    total: Decimal

row = OrderRow(**body.model_dump())                     # status, tenant_id from the client

# Safe: the input schema rejects unknown and server-owned fields; output lists what may leave
class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: UUID
    note: str | None = Field(default=None, max_length=500)
    lines: list[OrderLineIn] = Field(min_length=1, max_length=100)

class OrderResponse(BaseModel):
    id: UUID
    status: OrderStatus
    total: Decimal

row = OrderRow(tenant_id=actor.tenant_id, customer_id=body.customer_id,
               note=body.note, status=OrderStatus.DRAFT, created_by=actor.id)
```

Partial updates: an `OrderUpdate` schema with only editable fields, `body.model_dump(exclude_unset=True)`, then assign field by field or through an allow-listed set.

Names (`Order`, `Actor`) are illustrative; use the workspace's real types.
