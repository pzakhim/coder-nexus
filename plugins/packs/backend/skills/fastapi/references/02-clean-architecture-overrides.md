# Clean Architecture and Async Overrides (`O1`–`O8`)

> Topic: Mandatory Backend Pack overrides (`O1`–`O8`) where our layered SQLAlchemy 2 async + Pydantic v2 architecture overrides the generic single-file advice in the official FastAPI skill.

Rules **O1**, **O2**, **O3**, **O4**, **O5**, **O6**, **O7**, and **O8**.

---

## O1. SQLAlchemy 2 Async ORM + Repositories + Separate Pydantic v2 Schemas (Never `SQLModel`)

- **Official skill says**: Prefer `SQLModel` so one class acts as both the DB table and the API schema.
- **This pack enforces**: SQLAlchemy 2 ORM (`DeclarativeBase`, `Mapped[...]`, `mapped_column`) with `asyncpg`, repository classes for queries, and separate Pydantic v2 schemas (`app/schemas/`) for request and response payloads.
- **Why**: API contracts and DB tables evolve independently. Sharing a single class risks leaking sensitive columns (`password_hash`, `internal_note`, `tenant_id`) into responses (`{{slot:secure-coding-standards}}`) and couples schema migrations to API shapes.

```python
# UNSAFE (BLOCKER): One SQLModel class used as both DB table and API response
class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int
    internal_note: str  # Leaks into every API response returning Order

# SAFE: Table in app/models/, public contract in app/schemas/
class Order(Base):  # app/models/orders.py
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    internal_note: Mapped[str | None]

class OrderRead(BaseModel):  # app/schemas/orders.py
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int  # internal_note is never exposed
```

---

## O2. `mypy` (with `pydantic.mypy`) Instead of `ty`

- **Official skill says**: Use `ty` for type checking when available.
- **This pack enforces**: `mypy` configured in `pyproject.toml` (`[tool.mypy]`, `plugins = ["pydantic.mypy"]`), executed via `<prefix> mypy app`. If a workspace already standardizes on `ty` and not `mypy`, record it in `codebase-notes.md` and confirm via `D-NN` at Gate 2 rather than running two competing type checkers.

---

## O3 & O4. `async def` on All I/O Paths + `anyio.to_thread.run_sync` (No `Asyncer` Without `D-NN`)

- **Official skill says**: Write sync `def` path operations when unsure, and use `Asyncer` for sync/async mixing.
- **This pack enforces**: Every path operation and dependency touching `AsyncSession`, `asyncpg`, Redis, or `httpx` must be `async def`. Never call blocking CPU/file I/O directly inside `async def` — offload via `anyio.to_thread.run_sync` (which ships with FastAPI/Starlette). Never add `Asyncer` or any new package without an approved `D-NN`.

```python
# UNSAFE (BLOCKER): Blocking call inside async def stalls the entire worker event loop
@router.post("/{order_id}/invoice")
async def create_invoice(order_id: int, service: InvoiceServiceDep) -> InvoiceRead:
    pdf = render_pdf_blocking(order_id)
    return await service.attach_invoice(order_id, pdf)

# SAFE: Offload sync CPU/file work via anyio.to_thread.run_sync
@router.post("/{order_id}/invoice")
async def create_invoice(order_id: int, service: InvoiceServiceDep) -> InvoiceRead:
    pdf = await anyio.to_thread.run_sync(render_pdf_blocking, order_id)
    return await service.attach_invoice(order_id, pdf)
```

---

## O5 & O6. Lockfile Package Manager + Strict Layer Delegation (`Router → Service → Repository`)

- **Official skill says**: Query `session` directly inside the path operation (and use legacy `session.query(...)`).
- **This pack enforces**:
  - Router parses HTTP input, calls **one** service method, and returns its Pydantic schema.
  - Service owns business rules, authorization checks, and the single transaction (`async with session.begin():` or `await session.commit()`).
  - Repository owns SQLAlchemy 2 `select(...)` queries (`session.scalars()` / `session.execute()`) and never calls `commit()`.

```python
# UNSAFE (BLOCKER): Query, business rule, and commit inside router
@router.post("/")
async def create_order(body: OrderCreate, session: SessionDep) -> OrderRead:
    if (await session.scalar(select(func.count()).where(Order.customer_id == body.customer_id))) > 10:
        raise HTTPException(409)
    order = Order(**body.model_dump())
    session.add(order)
    await session.commit()
    return OrderRead.model_validate(order)

# SAFE: Router delegates to Service
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderCreate, service: OrderServiceDep, user: CurrentUserDep) -> OrderRead:
    return await service.create_order(body, actor=user)
```

---

## O7 & O8. Domain Error Mapping (`app/api/error_handlers.py`) & Explicit Schema Returns

- **O7 (Framework-Free Domain Errors)**: Services and repositories raise domain exceptions from `app/core/errors.py` (`NotFoundError`, `ConflictError`, `PermissionDeniedError`). Register centralized exception handlers in `app/api/error_handlers.py` that map domain exceptions to the exact HTTP status codes and error envelope defined in `api_contract.json` (`backend-api-contract-design`). Routers never wrap service calls in `try/except` to re-raise `HTTPException`.
- **O8 (Never Return ORM Models)**: Services and routers return explicit Pydantic v2 schemas (`-> OrderRead`), never raw SQLAlchemy ORM instances relying on `response_model` filtering (which hides return type mismatches from `mypy` and risks `MissingGreenlet` lazy-load errors outside the session).
- **Out-of-Scope Features Without `D-NN`**: Do not enable `app.frontend()`, OpenTelemetry auto-instrumentation, or repo-wide Ruff rule changes unless approved via `D-NN`.
