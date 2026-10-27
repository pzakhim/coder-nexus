# Route Conventions, Input/Output Schemas, Pagination & Idempotency

> Topic: FastAPI route naming, HTTP methods and status codes (`CT4`), strict Pydantic v2 input/output DTO separation (`CT2`), single `ErrorResponse` envelope (`CT3`), bounded pagination (`CT6`), and atomic `Idempotency-Key` mutations (`CT10`).

## 1. Resource Naming, Path Hierarchy & `APIRouter` Conventions (`CT4`, `CT9`)

1. **Versioned prefix & plural kebab-case nouns**:
   - Mount versioned routers under `/api/v1/<plural-kebab-resource>` (e.g., `/api/v1/work-orders`, `/api/v1/inventory-adjustments`).
   - Limit path nesting to **at most 2 levels** (`/api/v1/work-orders/{work_order_id}/line-items`). Deeper associations belong on their own top-level resource with a query filter (`GET /api/v1/inspections?work_order_id=...`).
   - Use sub-resource action nouns only for explicit domain state transitions that cannot be modeled as CRUD (`POST /api/v1/work-orders/{work_order_id}/cancel`).
2. **Deterministic `operation_id` and `tags` (`CT9`)**:
   - Every `@router.<method>` declares an explicit `operation_id="<resource>_<action>"` and inherits a single canonical `tags=["<resource>"]` from its `APIRouter`. Never rely on FastAPI's auto-generated function+path concatenation.
3. **Wire naming & format conventions**:
   - JSON keys and query parameters use `snake_case`.
   - Path identifiers use explicit typed UUIDs/ULIDs (`work_order_id: UUID`).
   - Timestamps are always timezone-aware UTC (`datetime` serialized as ISO-8601 `2026-10-25T08:30:00Z`).
   - Monetary amounts and exact quantities use string-encoded `Decimal` or integer minor units (`amount_minor: int`, `currency: Literal["VND", "USD"]`) — never IEEE-754 `float`.

---

## 2. Separate Input and Output Schemas (`CT2`)

Never share a single Pydantic model across request and response, and never return a SQLAlchemy model or `dict[str, Any]` from a route handler:

```python
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class WorkOrderCreateRequest(BaseModel):
    """Strict input DTO for POST /api/v1/work-orders (CT2)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str = Field(..., min_length=3, max_length=64, pattern=r"^[A-Z0-9_-]+$")
    title: str = Field(..., min_length=1, max_length=200)
    priority: Literal["low", "normal", "high", "urgent"] = "normal"
    planned_quantity: Decimal = Field(..., gt=Decimal("0"), max_digits=12, decimal_places=3)


class WorkOrderUpdateRequest(BaseModel):
    """Partial update DTO for PATCH /api/v1/work-orders/{work_order_id} (CT2)."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    priority: Literal["low", "normal", "high", "urgent"] | None = None


class WorkOrderResponse(BaseModel):
    """Public output DTO (CT2) — never exposes internal audit columns or tenant secrets."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    title: str
    priority: Literal["low", "normal", "high", "urgent"]
    status: Literal["draft", "released", "completed", "cancelled"]
    planned_quantity: Decimal
    created_at: datetime
    updated_at: datetime
```

### Mandatory DTO Separation Rules (`CT2`)

- **Input DTOs (`*CreateRequest`, `*UpdateRequest`)**:
  - Must set `model_config = ConfigDict(extra="forbid")` so misspelled or unauthorized mass-assignment fields (`role`, `is_admin`, `tenant_id`, `status`) fail immediately with `422 Unprocessable Entity`.
  - In `PATCH` handlers, extract only caller-supplied fields via `payload.model_dump(exclude_unset=True)` so omitted fields are distinguished from explicit `null`.
- **Output DTOs (`*Response`, `*SummaryResponse`)**:
  - Set `model_config = ConfigDict(from_attributes=True)` when mapping from Application/Domain read models.
  - Never expose password hashes, refresh tokens, internal integer surrogates (when UUID is public), or soft-delete internals (`deleted_at`).

---

## 3. Single Structured Error Envelope & Status Codes (`CT3`, `CT4`)

All `4xx` and `5xx` responses across the service — including FastAPI's built-in `RequestValidationError` (`422`), `StarletteHTTPException`, and domain exceptions — must be normalized by global exception handlers into a single `ErrorResponse` schema:

```python
from pydantic import BaseModel, Field


class ErrorFieldDetail(BaseModel):
    field: str | None = Field(default=None, description="Dot-path to the offending request field")
    code: str = Field(..., description="Machine-readable field error code")
    message: str = Field(..., description="Safe human-readable explanation")


class ErrorBody(BaseModel):
    code: str = Field(..., examples=["RESOURCE_NOT_FOUND", "VALIDATION_ERROR"])
    message: str = Field(..., examples=["Work order was not found."])
    details: list[ErrorFieldDetail] = Field(default_factory=list)
    trace_id: str = Field(..., description="Request correlation / OpenTelemetry trace ID")


class ErrorResponse(BaseModel):
    error: ErrorBody
```

### HTTP Method & Status Code Matrix (`CT4`)

| Operation | Method & Status | Required FastAPI Decorator Metadata |
|---|---|---|
| Read single resource | `GET` → `200 OK` | `response_model=WorkOrderResponse`, `responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}` |
| List collection | `GET` → `200 OK` | `response_model=PaginatedResponse[WorkOrderSummaryResponse]`, `responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}}` |
| Create resource | `POST` → `201 Created` | `status_code=status.HTTP_201_CREATED`, `response_model=WorkOrderResponse`, `responses={401: ..., 403: ..., 409: ..., 422: ...}` |
| Async command / job | `POST` → `202 Accepted` | `status_code=status.HTTP_202_ACCEPTED`, `response_model=JobAcceptedResponse` |
| Partial update | `PATCH` → `200 OK` | `response_model=WorkOrderResponse`, `responses={401: ..., 403: ..., 404: ..., 409: ..., 422: ...}` |
| Delete resource | `DELETE` → `204 No Content` | `status_code=status.HTTP_204_NO_CONTENT`, `response_class=Response` (empty body) |
| Validation failure | `422 Unprocessable Entity` | Normalized via `@app.exception_handler(RequestValidationError)` to `ErrorResponse` (`code="VALIDATION_ERROR"`) |
| Rate limit exceeded | `429 Too Many Requests` | `ErrorResponse` (`code="RATE_LIMITED"`) + `Retry-After` response header |

---

## 4. Bounded Pagination, Deterministic Sort & Allow-Listed Filtering (`CT6`)

Every collection endpoint must enforce an upper bound on page size and a deterministic tie-breaker sort:

```python
from typing import Generic, Literal, TypeVar
from pydantic import BaseModel, Field
from fastapi import Depends, Query

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        limit: int = Query(default=20, ge=1, le=100, description="Max items per page (1..100)"),
        cursor: str | None = Query(default=None, max_length=256, description="Opaque pagination cursor"),
        offset: int = Query(default=0, ge=0, le=10_000, description="Bounded offset when cursor is not used"),
    ) -> None:
        self.limit = limit
        self.cursor = cursor
        self.offset = offset


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int | None = Field(default=None, description="Optional total count for offset tables")
    limit: int
    next_cursor: str | None = None
    has_more: bool
```

- **Never accept unbounded `limit`**: Omitting `le=100` (or allowing `limit=-1` / `limit=0` to mean "all rows") is a `MAJOR` contract violation (`CT6`).
- **Deterministic tie-breaker sort**: When sorting by a non-unique column (`created_at`, `priority`, `status`), always append the primary key as tie-breaker (`ORDER BY created_at DESC, id DESC`).
- **Allow-listed sort & filter fields**: Declare filter and sort parameters using `Literal[...]` or `Enum` (`sort_by: Literal["created_at", "priority"] = "created_at"`). Never accept arbitrary column names from query strings.

---

## 5. Idempotency & Safe Retries for State-Changing Operations (`CT10`)

Every non-idempotent state-changing endpoint (`POST /api/v1/work-orders`, `POST /api/v1/payments`, `POST /api/v1/work-orders/{id}/release`) must support safe network retries via `Idempotency-Key`:

```python
from fastapi import Header

@router.post(
    "",
    operation_id="work_orders_create",
    status_code=status.HTTP_201_CREATED,
    response_model=WorkOrderResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "Duplicate code or Idempotency-Key conflict"},
        422: {"model": ErrorResponse},
    },
)
async def create_work_order(
    payload: WorkOrderCreateRequest,
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
        min_length=8,
        max_length=128,
        description="Client-generated UUID/ULID for safe retry deduplication (CT10).",
    ),
    principal: AuthenticatedPrincipal = Depends(require_scopes("work_orders:write")),
    use_case: CreateWorkOrderUseCase = Depends(get_create_work_order_use_case),
) -> WorkOrderResponse:
    return await use_case.execute(
        tenant_id=principal.tenant_id,
        actor_id=principal.user_id,
        idempotency_key=idempotency_key,
        command=payload.to_command(),
    )
```

### Mandatory Idempotency Contract Behavior (`CT10`)

1. **Fingerprint**: Compute `request_hash = sha256(f"{principal.tenant_id}:{route_id}:{canonical_json(payload)}")`.
2. **Atomic reservation**: Insert `(tenant_id, idempotency_key, request_hash, status="IN_PROGRESS", expires_at=now + 24h)` under a unique constraint `(tenant_id, idempotency_key)`.
3. **Outcome handling**:
   - **Existing completed record with identical `request_hash`**: Return the stored `status_code` and `response_body` immediately without re-running the use case.
   - **Existing record with different `request_hash`**: Raise `409 Conflict` with `error.code = "IDEMPOTENCY_KEY_CONFLICT"`.
   - **Existing `IN_PROGRESS` record**: Raise `409 Conflict` with `error.code = "IDEMPOTENCY_REQUEST_IN_PROGRESS"`.

See [`references/02-compatibility-and-versioning.md`](02-compatibility-and-versioning.md) for authentication scopes, anti-IDOR rules, and compatibility policy, and [`references/03-openapi-snapshot-diff-and-review.md`](03-openapi-snapshot-diff-and-review.md) for OpenAPI snapshot diffing and review gates.
