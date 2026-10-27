# 02 — Errors, Lifecycle, and Logging (Python / FastAPI)

Consolidated rules for domain exceptions and error chaining (**C4, C11**), import-time and lifespan purity (**C12**), and structured logging without debug leftovers (**C3**).

---

## 1. Domain Error Contract & Boundary Translation (C4, C11)

Swallowed errors and untyped exceptions cause silent data corruption and opaque production incidents.

- **Specific domain exceptions**:
  - Define domain exceptions inheriting from a common base (`DomainError` / `AppError`):
    ```python
    class DomainError(Exception):
        """Base exception for business domain errors."""

    class EntityNotFoundError(DomainError):
        def __init__(self, entity_type: str, entity_id: str | int) -> None:
            super().__init__(f"{entity_type} {entity_id} not found")
            self.entity_type = entity_type
            self.entity_id = entity_id
    ```
- **Edge translation**:
  - Domain and repository layers raise domain exceptions (never `fastapi.HTTPException`).
  - Translation to HTTP status codes (`404`, `409`, `422`) happens exclusively in FastAPI exception handlers (`@app.exception_handler(...)`) or route handlers.
- **Catch specific exceptions & chain causes**:
  - Always catch the exact expected exception (`sqlalchemy.exc.IntegrityError`, `httpx.TimeoutException`) and re-raise with `from exc`:
    ```python
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise DuplicateOrderError(order_id) from exc
    ```
  - **Prohibited**: Bare `except:`, `except Exception: pass`, or returning `None`/`False` to hide an operational failure. `except Exception` is permitted only at top-level worker/middleware boundaries where the error is logged with full traceback.

---

## 2. Import-Time Purity & Lifespan Management (C12)

- **Zero import-time I/O**:
  - Never open database connections, instantiate live HTTP clients, perform file I/O, or read `os.environ` at module import time.
  - Import-time side effects break unit test collection, Alembic migration discovery, and deterministic startup.
- **Lifespan & Dependency Injection**:
  - Load configuration via `pydantic-settings` (`BaseSettings`) injected through FastAPI `Depends` or cached factory functions.
  - Manage database engines, connection pools, Redis clients, and `httpx.AsyncClient` instances inside the FastAPI `lifespan` async context manager, closing them cleanly on shutdown.

---

## 3. Structured Logging & No Debug Leftovers (C3)

- **Module logger**: Declare `logger = logging.getLogger(__name__)` at module level.
- **Structured context**: Pass structured key-value fields via `extra={...}` so log aggregators can index them:
  ```python
  # GOOD: structured context
  logger.info("Order processed", extra={"order_id": str(order.id), "duration_ms": elapsed})

  # BAD: unstructured f-string interpolation
  logger.info(f"Order processed {order.id}")
  ```
- **Exception tracebacks**: Use `logger.exception("Payment gateway call failed", extra={"order_id": str(order.id)})` inside `except` blocks to capture the traceback automatically.
- **No secrets or PII**: Never log passwords, bearer tokens, API keys, session cookies, or raw personal data (`{{slot:secure-coding-standards}}`).
- **No debug leftovers**: Never commit `print()`, `breakpoint()`, or `import pdb` (enforced by `ruff` rules `T10` and `T20`).
