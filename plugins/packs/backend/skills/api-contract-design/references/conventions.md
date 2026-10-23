# Contract conventions in FastAPI

Detail for [api-contract-design](../SKILL.md) CT2–CT6. The workspace's existing conventions win: read them from current routes and `openapi.json` before adding anything, and list endpoints that do not follow them as known drift instead of "fixing" them in an unrelated task (a change there is breaking, see [compatibility](compatibility.md)).

## 1. Schemas per direction (CT2, CT3)

```python
class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: UUID
    note: str | None = Field(default=None, max_length=500)

class OrderUpdate(BaseModel):                       # PATCH: every field optional
    model_config = ConfigDict(extra="forbid")
    note: str | None = Field(default=None, max_length=500)

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: OrderStatus
    note: str | None
    created_at: datetime

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderCreate, actor: Annotated[Actor, Depends(get_current_actor)],
                       orders: Annotated[OrderService, Depends(get_order_service)]) -> OrderRead:
    return OrderRead.model_validate(await orders.create(actor, body))
```

| Unsafe | Safe | Reason |
|---|---|---|
| One `Order` model for body and response | `OrderCreate` / `OrderUpdate` / `OrderRead` | Server-owned fields (`id`, `status`, `owner_id`) cannot be set by the client, and internal fields cannot leak |
| `-> dict` or `-> Any` with no `response_model` | `-> OrderRead`, or `response_model=OrderRead` when the function returns something else | Untyped results become an empty schema in `openapi.json`; generated clients get `unknown` |
| Returning the ORM object with no response model | `OrderRead.model_validate(entity)` or `response_model=OrderRead` | The response model filters fields; without it every column is serialized |
| PATCH applying `body.model_dump()` | `body.model_dump(exclude_unset=True)` | Otherwise an omitted field is written as `None` |
| `OrderStatus` as free `str` | `Enum` (or `Literal`) | The enum appears in the schema and clients can switch on it |

**Input/output schema split in OpenAPI.** With Pydantic v2, FastAPI's default `separate_input_output_schemas=True` publishes a model used in both directions as `Order-Input` and `Order-Output`; in the output schema a field with a default is **required** (it is always present). Separate models per direction avoid the suffixes entirely. Never flip the flag on an existing API: every schema name changes, which renames types in generated clients (breaking).

## 2. One error envelope (CT4)

Use the workspace's envelope. If the workspace uses FastAPI's defaults, the envelope is `{"detail": "<message>"}` for `HTTPException` and `HTTPValidationError` (`{"detail": [{"loc", "msg", "type"}]}`) for 422 — document that in `design.md` and keep it. If the workspace has a custom envelope:

```python
class ErrorBody(BaseModel):
    code: str                      # stable machine code, e.g. "order_not_found"
    message: str                   # human text; clients never parse it
    fields: list[FieldError] = []  # validation details
    request_id: str

class ErrorResponse(BaseModel):
    error: ErrorBody

COMMON_ERRORS: dict[int | str, dict[str, Any]] = {
    401: {"model": ErrorResponse}, 403: {"model": ErrorResponse},
    404: {"model": ErrorResponse}, 422: {"model": ErrorResponse},
}
router = APIRouter(prefix="/orders", tags=["orders"], responses=COMMON_ERRORS)
```

- Exception handlers (`app.add_exception_handler`) for `HTTPException`, `RequestValidationError` and domain errors are registered once in the app factory.
- When the 422 body is customised, declare `422` in `responses=` as above. Reason: FastAPI adds its default `HTTPValidationError` 422 schema to every operation with parameters unless the operation already declares `422`, so the contract would lie about the real body.
- Clients branch on `code`, never on `message` text; `message` and `request_id` never contain stack traces or internal names (SC6).

## 3. Status codes

| Outcome | Status | Notes |
|---|---|---|
| Read, replace, partial update | `200` | Body is the read model |
| Created | `201` | Body is the read model; add `Location` only if the workspace does |
| Accepted for async processing | `202` | Body points to a status resource |
| Deleted, no body | `204` | `status_code=204`, return `None`; no `response_model` |
| Body or parameter fails validation | `422` | FastAPI default; keep `400` only where the workspace already uses it |
| Missing or invalid credentials | `401` | From the auth dependency |
| Authenticated, action not allowed | `403` | Function-level permission |
| Object missing **or outside the actor's scope** | `404` | Do not reveal existence across scopes (`{{slot:secure-coding-standards}}`) |
| State conflict, duplicate, idempotency-key mismatch | `409` | Stable `code` per cause |
| Rate limited | `429` | With `Retry-After` when the limiter provides it |

Every status a route can return is declared (router or route `responses=`) and listed in `design.md`.

## 4. Pagination, filtering, sorting

Reuse the workspace's one style. If none exists yet, it is a `D-NN` at Gate 2; a typical page/limit shape:

```python
class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int

async def list_orders(limit: Annotated[int, Query(ge=1, le=100)] = 20,
                      offset: Annotated[int, Query(ge=0)] = 0, ...) -> Page[OrderRead]: ...
```

- `le=` on every limit parameter, and the repository applies it. Reason: an unbounded list is a resource-exhaustion path (OWASP API4).
- Ordering is deterministic (a unique tie-breaker such as `id`). Reason: clients see duplicates or gaps between pages otherwise, and ordering is observable behaviour (Hyrum's Law).
- Cursor pagination when lists change quickly or are large; the cursor is opaque to clients.
- Filters and sort fields are allow-listed (`Literal["created_at", "status"]`), never passed through to SQL.

## 5. Auth per endpoint (CT5)

- Authentication dependencies built on FastAPI security classes (`HTTPBearer`, `OAuth2PasswordBearer`, `APIKeyHeader`) through `Depends`/`Security` put a `security` requirement on the operation automatically. A dependency that reads the header by hand does not, and the contract shows the route as public.
- Router-level `dependencies=[Depends(get_current_actor)]` covers every route of the router.
- `design.md` lists each endpoint's roles and data scope; `openapi.json` shows only that auth is required. Authorization (who may touch which object) stays in the service layer and in tests, not in the spec.

## 6. Operation ids, tags, deprecation

- Every route has a tag; tags group generated client services.
- `operationId` comes from FastAPI's default (function name + path + method) or the workspace's `generate_unique_id_function` (for example `f"{route.tags[0]}-{route.name}"`). Renaming a path function changes the default id: treat it as a contract change (CT6).
- Deprecate before removal: `@router.get(..., deprecated=True)` sets `deprecated: true` on the operation; parameters take `Query(deprecated=True)`. The removal date goes in `design.md` and the change record.
- Versioning follows the workspace (`/api/v1` prefix or none). A new major version is a last resort (One-Version Rule, [compatibility](compatibility.md) §3).
