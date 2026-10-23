# 03 — Errors and logging

Swallowed errors and untyped exceptions cause silent data corruption and difficult production debugging.

## Error contract (C4, C11)

- **Domain exceptions**: Define specific exceptions subclassing a common base (e.g. `DomainError` or `AppError`).
  ```python
  class DomainError(Exception):
      """Base exception for all business domain errors."""

  class EntityNotFoundError(DomainError):
      def __init__(self, entity_type: str, entity_id: str | int) -> None:
          super().__init__(f"{entity_type} {entity_id} not found")
          self.entity_type = entity_type
          self.entity_id = entity_id
  ```
- **Boundary translation**: Domain and repository layers raise domain exceptions. Translation to HTTP response codes (e.g. 404 Not Found, 409 Conflict) happens exclusively at the edge:
  - Inside dedicated FastAPI exception handlers registered on the application (`@app.exception_handler(EntityNotFoundError)`).
  - Or within the HTTP route handler if specific to a single endpoint.

## Catching rules (C4)

- **Catch specific exceptions**: Always catch the exact exception expected (e.g. `sqlalchemy.exc.IntegrityError`, `httpx.TimeoutException`).
- **Chain causes**: When re-raising or translating an exception, preserve the root cause:
  ```python
  try:
      await session.commit()
  except IntegrityError as exc:
      await session.rollback()
      raise DuplicateOrderError(order_id) from exc
  ```
- **Prohibited practices**:
  - Bare `except:` or `except Exception: pass`.
  - Returning `None`, `[]`, or `False` to hide an underlying failure.
  - Catching `Exception` outside the application global error handler or background worker loop.

## Logging standards (C3)

- **Module logger**: Use `logger = logging.getLogger(__name__)` defined at module level.
- **Structured arguments**: Pass context as extra fields or positional arguments; never use eager f-strings that evaluate even if the log level is disabled:
  ```python
  # Good
  logger.info("Order processed successfully", extra={"order_id": order.id, "duration_ms": elapsed})
  # Bad
  logger.info(f"Order processed {order.id}")
  ```
- **Log exceptions with tracebacks**: Use `logger.exception("Failed to process payment")` inside an `except` block to capture the full traceback automatically.
- **No secrets in logs**: Never log tokens, passwords, session cookies, or raw authorization headers (see `{{slot:secure-coding-standards}}`).
- **No debug artifacts**: `print()`, `breakpoint()`, and `import pdb` must never be committed.
