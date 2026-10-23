# 02 — Authorization and data scope

Why: broken access control and scope leaks are the costliest and most common serious flaws (SC2, SC3, SC7, SC13; OWASP API1, API2, API5).

## Authorization (SC2)

- **Authentication on the router, authorization in the service.** The router declares the auth dependency (`actor: Actor = Depends(get_current_actor)`, or the workspace's real name); the service / use case receives `actor` explicitly and decides whether this actor may do this action on this object. Reason: a check that exists only in a router is skipped by the next router, job or WebSocket handler that calls the same service.
- **Per object, not per kind.** Load the object **with** its scope, then check the actor against it (owner, tenant, capability). Reason: "may read orders" is not "may read order 42".
- **Deny by default.** No capability, no access; an exception inside the check denies (SC13).
- **Out-of-scope objects return not-found (404)** unless the contract says 403. Reason: a 403 confirms the id exists.
- **Forbidden:** `if actor.role == "admin"` scattered in routers; an `actor_id`, `tenant_id` or `role` taken from the request body or query; a service method without an `actor` or scope parameter for scoped data. Reason: the request is untrusted (SC1).
- **One capability check per function:** `require_capability(actor, Capability.REFUND)` (or the workspace's guard), with a test that a normal actor gets 403. Reason: admin routes that only check "logged in" are OWASP API5.
- Sensitive business flows (redemption, sign-up, OTP) get the per-actor limits and idempotency keys the design names; when the design is silent, ask Planning (OWASP API6).

## Roles and capabilities

The roles, capabilities and their mapping come from the approved `design.md`. Copy the workspace's RBAC table into a workspace `secure-coding-standards` override when it exists; never invent roles in code.

## Data scopes (SC3)

| Scope | Carried by | Enforced in | A leak looks like |
|---|---|---|---|
| Tenant | `actor.tenant_id` from the token → service → repository argument | `.where(Row.tenant_id == tenant_id)` on every `select`, `update`, `delete`; cache keys prefixed with the tenant | `session.get(Row, id)` on a tenant-scoped table |
| Owner / user | `actor.id` → service | Repository filter or service check `row.owner_id == actor.id` | A list endpoint returning every user's rows |
| Environment / release state | Settings or request context named in the design | Repository filter; mutations in production gated as the design says | Draft rows served by a public endpoint |

Single-tenant services still apply the owner scope. Every new query, cache key, file path, background job and event states which scopes it carries; a job never runs with a "system" default scope unless the design names it.

```python
# Unsafe: router-only check, repository loads by id alone
@router.get("/orders/{order_id}")
async def read_order(order_id: UUID, actor: Actor = Depends(get_current_actor),
                     session: AsyncSession = Depends(get_session)):
    order = await session.get(OrderRow, order_id)          # any tenant's order
    if actor.role != "admin" and order.owner_id != actor.id:
        raise HTTPException(403)                            # the next caller forgets this
    return order                                            # ORM object, every column

# Safe: scope in the repository, decision in the service, schema at the edge
class OrderRepository:
    async def get_in_scope(self, order_id: UUID, *, tenant_id: UUID) -> OrderRow | None:
        stmt = select(OrderRow).where(OrderRow.id == order_id, OrderRow.tenant_id == tenant_id)
        return (await self._session.execute(stmt)).scalar_one_or_none()

class OrderService:
    async def get_for_actor(self, actor: Actor, order_id: UUID) -> Order:
        row = await self._repo.get_in_scope(order_id, tenant_id=actor.tenant_id)
        if row is None or not actor.can_read(row):
            raise OrderNotFoundError(order_id)              # mapped to 404
        return order_from_row(row)

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def read_order(order_id: UUID, actor: Actor = Depends(get_current_actor),
                     service: OrderService = Depends(get_order_service)) -> Order:
    return await service.get_for_actor(actor, order_id)
```

Updates and deletes carry the scope in the `WHERE` clause (`update(OrderRow).where(OrderRow.id == id, OrderRow.tenant_id == tenant_id)`) and check `rowcount`.

## Authentication (SC7)

- Use the workspace's existing auth module; a new mechanism is a design decision (`D-NN`), not a task choice. Reason: hand-rolled auth is where account takeovers come from.
- Tokens: PyJWT `jwt.decode(token, key, algorithms=[settings.jwt_algorithm], audience=..., issuer=..., options={"require": ["exp", "sub"]})`. The algorithm list comes from settings, never from the token header; `verify_signature=False` never appears outside a test of the rejection. On `jwt.InvalidTokenError` → 401 with `WWW-Authenticate: Bearer`.
- Passwords: the workspace's hasher (Argon2 or bcrypt through a vetted library such as `pwdlib`); verify a dummy hash for an unknown user so timing does not reveal which usernames exist. Plain, `md5` or `sha256` password hashes are a `BLOCKER`.
- Tokens travel in the `Authorization` header or a body, never in URLs or query strings. Cookie-authenticated mutations need `Secure`, `HttpOnly`, `SameSite` and CSRF protection.

```python
# Unsafe
payload = jwt.decode(token, options={"verify_signature": False})
payload = jwt.decode(token, key, algorithms=jwt.get_unverified_header(token)["alg"])

# Safe (inside the workspace's auth module)
try:
    payload = jwt.decode(token, settings.jwt_secret.get_secret_value(),
                         algorithms=[settings.jwt_algorithm],
                         audience=settings.jwt_audience, issuer=settings.jwt_issuer,
                         options={"require": ["exp", "sub"]})
except jwt.InvalidTokenError as exc:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"}) from exc
```

## Fail closed (SC13)

- An exception in validation, authorization or a dependency fails the request (401/403/404/503 per the contract). Never `except Exception: return []`, a default object, or a fallback path that skips the guard. Reason: attackers aim for the error path, and fake success hides the outage.
- Provider or database errors are failures, not empty data (OWASP API10).
