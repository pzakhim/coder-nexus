# 01 — Trust Boundaries, Input Validation, Authentication, Authorization & Data Scope

> Scope: Untrusted input validation (`SC1`, `SC5`), end-to-end authentication flow (`SC7`), object-level service authorization (`SC2`), explicit tenant/owner/environment scope isolation (`SC3`), and fail-closed error handling (`SC13`).

---

## 1. Trust Boundaries & Input Validation (`SC1`, `SC5`)

Every payload entering the process from outside is untrusted:

| Boundary | Conventional Path | Mandatory Validation Contract |
|---|---|---|
| **HTTP API (path, query, body, headers)** | `app/api/routers/*.py` | Pydantic v2 request schemas (`ConfigDict(extra="forbid")`), `Path(...)` / `Query(...)` bounds |
| **Third-party Webhooks** | Webhook routers | Verify HMAC signature first (`hmac.compare_digest` against `SecretStr`), then validate payload via Pydantic schema |
| **Background Jobs & Queue Messages** | Worker / consumer modules | `PayloadSchema.model_validate(raw)` on every message; pass `user_id` and `tenant_id` explicitly |
| **File Uploads & Imports** | Upload routers / import services | Byte-size cap, magic-byte content sniffing, and safe parser ([03](03-runtime-risks-deps-and-review.md#2-code-examples-injection-ssrf--file-uploads)) |
| **External Provider Responses** | `app/integrations/*.py` | `ProviderSchema.model_validate(resp.json())`; upstream errors raise typed domain errors, never empty fallback data |

### Mandatory Schema Rules
1. **Forbid unknown fields (`extra="forbid"`):** Put `model_config = ConfigDict(extra="forbid")` on every request input schema to block mass-assignment probes (OWASP API3).
2. **Separate input and output schemas:** Define distinct `*Create`, `*Update`, and `*Read` schemas. Server-owned fields (`id`, `tenant_id`, `owner_id`, `role`, `is_admin`, `status`, `created_by`) must never appear in an input schema.
3. **Declare return types / `response_model=` on every route:** Never return raw SQLAlchemy ORM rows directly (`{{slot:clean-architecture}}` `A1`).
4. **Bound every collection query:** Require `limit: int = Query(20, ge=1, le=MAX_PAGE_SIZE)` and apply `.limit(limit)` in the repository (OWASP API4).
5. **Reject, never repair:** Return `422` / contract validation errors on invalid input; never silently coerce or guess business values.

```python
# Unsafe: shared schema allows client to overwrite server-owned tenant_id and status
class OrderSchema(BaseModel):
    id: UUID | None = None
    tenant_id: UUID | None = None
    status: str = "draft"
    total: Decimal

row = Order(**body.model_dump())

# Safe: strict input schema forbids extra fields and excludes server-owned columns
class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: UUID
    note: str | None = Field(default=None, max_length=500)
    lines: list[OrderLineIn] = Field(min_length=1, max_length=100)

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: OrderStatus
    total: Decimal
```

---

## 2. End-to-End Authentication Architecture (`SC7`)

> **Workspace Convention Rule (`C11` / `SC7`):**
> - **Existing workspace (`EXTEND`):** Always inspect and reuse the project's existing auth dependency, principal/user class, and session/token mechanism recorded in `codebase-notes.md` and `design.md`. **Never** create a parallel auth flow or force-rename existing project classes to `CurrentUser`.
> - **New service bootstrap (`INIT`):** When scaffolding a new FastAPI service from scratch and `design.md` does not specify custom class names, use the reference pattern below so `app/services/` stays 100% free of FastAPI imports (`{{slot:clean-architecture}}` `A5`):
> - **Mandatory security invariants (apply to ALL projects regardless of class names):**
>   1. Pin allowed JWT algorithms, issuer, audience, and required claims (`exp`, `sub`) from configuration—never trust the token header's `alg` or set `verify_signature=False`.
>   2. Authenticate at the HTTP router boundary, pass a framework-free caller identity object into the Service, and enforce object-level authorization + scope filtering inside Service/Repository.

```text
HTTP Header (Authorization: Bearer <jwt>)
  │
  ▼
1. app/core/security.py   → Defines pure-Python `CurrentUser` dataclass + `decode_access_token()` / `pwdlib` hashing
  │
  ▼
2. app/api/auth.py        → FastAPI `get_current_user()` extracts Bearer token, calls `decode_access_token()`, returns `CurrentUser`
  │
  ▼
3. app/api/deps.py        → Defines `CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]`
  │
  ▼
4. Router → Service       → Router injects `current_user: CurrentUserDep` and passes `current_user` (pure Python) into Service
```

### Concrete Implementation Across the 3 Files (`SC7`)

```python
# 1. app/core/security.py — Pure Python (NO FastAPI imports; safe for Services to import)
from dataclasses import dataclass
from uuid import UUID
import jwt
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()  # Argon2id by default

@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: UUID
    tenant_id: UUID
    roles: frozenset[str]

    def has_role(self, role: str) -> bool:
        return role in self.roles

def decode_access_token(token: str, settings: Settings) -> CurrentUser:
    # Always pin algorithms, audience, issuer, and required claims from Settings (never from token header)
    payload = jwt.decode(
        token,
        settings.jwt_secret.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
        options={"require": ["exp", "sub", "tenant_id"]},
    )
    return CurrentUser(
        id=UUID(payload["sub"]),
        tenant_id=UUID(payload["tenant_id"]),
        roles=frozenset(payload.get("roles", [])),
    )
```

```python
# 2. app/api/auth.py — FastAPI HTTP boundary (translates JWT errors into 401 HTTPException)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from app.core.security import CurrentUser, decode_access_token
from app.core.settings import Settings, get_settings

bearer_scheme = HTTPBearer(auto_error=True)

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    try:
        return decode_access_token(creds.credentials, settings)
    except (jwt.InvalidTokenError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
```

```python
# 3. app/api/deps.py — Reusable Annotated dependency aliases for Routers
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth import get_current_user
from app.core.security import CurrentUser
from app.db.session import get_session

CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

---

## 3. Object-Level Authorization (`SC2`), Data-Scope Isolation (`SC3`) & Fail-Closed (`SC13`)

### Authorization & Scope Rules
1. **Authenticate on the router (`CurrentUserDep`), authorize in the service (`CurrentUser`):**
   - Routers only declare `current_user: CurrentUserDep` and forward `current_user` to the Service.
   - Services (`app/services/`) check whether `current_user` has permission on the specific record.
2. **Enforce Data Scopes in every Repository query (`SC3`):**
   - Never call unscoped `await session.get(Order, order_id)` on a tenant-scoped or user-scoped table.
   - Pass `tenant_id=current_user.tenant_id` into Repository methods so every `select`, `update`, and `delete` includes `.where(Order.tenant_id == tenant_id)`.
3. **Deny by default & hide existence (`SC2`, `SC13`):**
   - Raise `NotFoundError` (`404`) when a record does not exist in `current_user.tenant_id`, and `PermissionDeniedError` (`403`) when `current_user` lacks the required role/ownership.
   - **Fail closed (`SC13`):** Any exception in validation, authentication, or permission checks denies the request—never catch and return `[]` or fallback data.

```python
# Unsafe: router checks role strings + unscoped session.get() leaks other tenants' orders
@router.get("/orders/{order_id}")
async def get_order(order_id: UUID, current_user: CurrentUserDep, session: SessionDep):
    order = await session.get(Order, order_id)  # BUG: loads ANY tenant's order!
    if "admin" not in current_user.roles and order.owner_id != current_user.id:
        raise HTTPException(403)
    return order

# Safe: Repository filters by tenant_id; Service checks object ownership/role; Router stays thin
class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id_and_tenant(self, order_id: UUID, *, tenant_id: UUID) -> Order | None:
        stmt = select(Order).where(Order.id == order_id, Order.tenant_id == tenant_id)
        return (await self._session.execute(stmt)).scalar_one_or_none()

class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = OrderRepository(session)

    async def get_order(self, current_user: CurrentUser, order_id: UUID) -> OrderRead:
        row = await self._repo.get_by_id_and_tenant(order_id, tenant_id=current_user.tenant_id)
        if row is None:
            raise NotFoundError("order", order_id)  # Mapped to 404 by app/api/error_handlers.py
        if row.owner_id != current_user.id and not current_user.has_role("admin"):
            raise PermissionDeniedError("Not allowed to view this order")  # Mapped to 403
        return OrderRead.model_validate(row)

@router.get("/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: UUID,
    current_user: CurrentUserDep,
    service: OrderServiceDep,
) -> OrderRead:
    return await service.get_order(current_user, order_id)
```
