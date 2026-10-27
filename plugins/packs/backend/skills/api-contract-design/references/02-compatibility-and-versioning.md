# Authentication Scopes, Compatibility & Versioning Policy

> Topic: OpenAPI security scheme declarations, RBAC (`403`) vs. Anti-IDOR tenant ownership (`404`) (`CT5`), Additive vs. Breaking change classification (`CT7`), the 4-step `D-NN` breaking change protocol, and One-Version deprecation (`CT8`).

## 1. Explicit Authentication, Authorization Scopes & Anti-IDOR (`CT5`)

Authentication and authorization are part of the public OpenAPI contract — never hide security checks inside opaque middleware that leaves `contracts/openapi.json` without `security` metadata, and never trust identity fields from the request body.

### 1.1 Declaring Security Schemes in FastAPI OpenAPI (`CT5`)

Use FastAPI's `Security(...)` or `Depends(...)` wrapping `HTTPBearer` / `OAuth2PasswordBearer` so every protected route emits `security` and `components.securitySchemes` into `contracts/openapi.json`:

```python
from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from pydantic import BaseModel

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    description="JWT access token issued by the identity provider.",
    auto_error=False,
)


class AuthenticatedPrincipal(BaseModel):
    user_id: UUID
    tenant_id: UUID
    scopes: frozenset[str]


async def get_current_principal(
    security_scopes: SecurityScopes,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)],
) -> AuthenticatedPrincipal:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHENTICATED", "message": "Missing bearer token."},
            headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
        )
    principal = await verify_jwt_and_extract_principal(credentials.credentials)
    for required_scope in security_scopes.scopes:
        if required_scope not in principal.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "PERMISSION_DENIED",
                    "message": f"Missing required scope: {required_scope}",
                },
            )
    return principal
```

### 1.2 `401` vs. `403` vs. `404` (Anti-IDOR Tenant Ownership, `CT5`)

| Scenario | Required Status & Error Code | Why |
|---|---|---|
| Missing, malformed, expired, or revoked token | `401 Unauthorized` (`UNAUTHENTICATED`) | Client must re-authenticate or refresh token. |
| Valid token, but caller lacks route scope/role (e.g., `work_orders:write`) | `403 Forbidden` (`PERMISSION_DENIED`) | Principal is known; operation itself is not permitted for their role. |
| Valid token + valid scope, but `{work_order_id}` belongs to **another `tenant_id` or unauthorized owner** | **`404 Not Found` (`RESOURCE_NOT_FOUND`)** | Returning `403` leaks that the UUID exists in another tenant's workspace (IDOR enumeration). Scoping SQL `WHERE id = :id AND tenant_id = :tenant_id` naturally yields `None` → `404`. |

- **Never accept `tenant_id`, `organization_id`, or `actor_user_id` from request bodies or query strings** on tenant-scoped endpoints. Always bind them from `principal.tenant_id` and `principal.user_id`.
- **Public endpoints** (`/healthz`, `/api/v1/auth/token`, signed webhooks) must be explicitly allow-listed in contract tests; webhook endpoints must require cryptographic HMAC signature headers (`X-Webhook-Signature`, `X-Webhook-Timestamp`).

---

## 2. Additive vs. Breaking Contract Changes (`CT7`)

Under **Hyrum's Law**, any observable change in paths, query parameters, request/response schemas, status codes, or `error.code` values can break deployed clients (mobile apps, web frontends, partner integrations). Classify every contract modification using the table below:

| Modification | Classification | Allowed Without `D-NN`? |
|---|---|---|
| Add a new route (`POST /api/v1/work-orders/{id}/notes`) | **Additive** | Yes — export updated `contracts/openapi.json` |
| Add an **optional** request field with a backward-compatible default (`notes: str | None = None`) | **Additive** | Yes — existing clients omitting `notes` behave identically |
| Add an **optional** query parameter (`include_archived: bool = False`) | **Additive** | Yes |
| Add a new field to a response DTO (`completed_at: datetime | None`) | **Additive** | Yes — JSON clients must ignore unknown keys |
| Relax input validation bounds (`max_length=100` → `max_length=200`) | **Additive** | Yes |
| Add a new allowed value to a **request** `Literal` / `Enum` | **Additive** | Yes |
| Add a new value to a **response** `Literal` / `Enum` | **Breaking for strict clients** | Requires checking `api_contract.json` consumers or `D-NN` if clients decode enums exhaustively without an `unknown` fallback |
| Remove or rename an endpoint, path parameter, query parameter, request field, or response field | **Breaking** | **No** — requires approved `D-NN` in `design.md` |
| Make an optional request field or query parameter **required** | **Breaking** | **No** — requires approved `D-NN` in `design.md` |
| Change a field's type or nullability (`str` → `int`, `str` → `str | None` on response) | **Breaking** | **No** — requires approved `D-NN` in `design.md` |
| Tighten input validation bounds (`max_length=200` → `100`, `le=100` → `le=50`) | **Breaking** | **No** — requires approved `D-NN` in `design.md` |
| Change success status code (`200` → `202`) or machine-readable `error.code` string | **Breaking** | **No** — requires approved `D-NN` in `design.md` |
| Change authentication scheme or add a newly required scope to an existing endpoint | **Breaking** | **No** — requires approved `D-NN` in `design.md` |

---

## 3. The 4-Step Breaking Change Protocol (`D-NN`, `CT7`)

Never ship a stealth breaking change. When a breaking change is genuinely required:

1. **Step 1 — Record Decision `D-NN` in `design.md` and get user approval**:
   - State what is changing, why an additive change is insufficient, which clients (`api_contract.json` consumers) are affected, and the rollout/sunset plan.
2. **Step 2 — Apply Expand-and-Contract whenever feasible**:
   - **Expand**: Introduce the new field (`assigned_user_ids: list[UUID]`) or new endpoint alongside the legacy field (`assigned_user_id: UUID | None = Field(default=None, deprecated=True)`). Populate both in responses; accept either in requests.
   - **Migrate**: Update `api_contract.json` (`shared_contracts/api_handshake_protocol.md`) so downstream clients switch to the new contract.
   - **Contract**: Remove the deprecated field/route only in a subsequent release after all consumers have migrated.
3. **Step 3 — Document in `contracts/contract-change.md`**:
   - Explicitly list every breaking diff entry and cite `D-NN` in `design.md`.
4. **Step 4 — Synchronize `contracts/openapi.json` and `api_contract.json`**:
   - Re-export the OpenAPI snapshot and update the handshake file in the same commit/PR.

---

## 4. Deprecation & Versioning Policy (`CT8`)

- **One-Version Rule within `/api/v1`**: Do not create `/api/v2` for routine schema changes. Keep all additive and Expand-and-Contract evolutions inside `/api/v1`.
- **When `/api/v2` is justified**: Only when replacing an entire resource domain model under an approved `D-NN` where dual-field support on `/api/v1` is structurally impossible. Mount `/api/v2/<resource>` as a separate `APIRouter` while keeping `/api/v1/<resource>` operational until its sunset date.
- **RFC 8594 Deprecation Metadata**:
  - Set `deprecated=True` on the FastAPI route decorator or Pydantic `Field(..., deprecated=True)`.
  - Emit `Deprecation: true`, `Sunset: Wed, 11 Nov 2026 00:00:00 GMT`, and `Link: </api/v1/replacement>; rel="successor-version"` headers on deprecated route responses.

See [`references/01-conventions-schemas-and-idempotency.md`](01-conventions-schemas-and-idempotency.md) for route/DTO conventions and [`references/03-openapi-snapshot-diff-and-review.md`](03-openapi-snapshot-diff-and-review.md) for OpenAPI snapshot export, diffing, and review gates.
