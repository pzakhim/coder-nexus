# 02 — Size and structure

Structure rules prevent complexity drift before code spreads across the service.

## Thresholds

Thresholds apply to new or modified code. Legacy files exceeding thresholds are refactored only when the phase explicitly touches them.

| Unit | Limit | Why |
|---|---|---|
| Function / method | ≤ ~30 lines | Units readable without scrolling; single responsibility. |
| File / module | ≤ ~300 lines | Prevents junk-drawer modules that attract multiple reasons to change. |
| Parameters | ≤ 3 parameters | Positional arguments beyond 3 hide call-site mistakes. Use Pydantic schema or dataclass. |
| Nesting | ≤ 2 levels | Deep indentation obscures control flow; use early returns and guard clauses. |

When a function or module exceeds thresholds or performs multiple distinct jobs, follow [02b — Splitting](02b-splitting.md).

## One concept, one place (C1)

- **No pass-through wrappers**: A function, service or class that only forwards arguments to an underlying method without transformation, authorization, caching, or error mapping is deleted. Callers invoke the target directly.
- **No aliases or compatibility shims**: When renaming or moving a function, class, or module, update all call sites across the repository in the same task. Never leave compatibility imports (`from .new_module import Target # noqa: F401`).

## Module-level variables and globals (C15)

- Module level holds only:
  1. True shared constants (`UPPER_SNAKE`) read by two or more functions and never reassigned.
  2. The module's logger: `logger = logging.getLogger(__name__)`.
  3. The settings configuration instance (in its dedicated config module).
- **Prohibited**:
  - Mutable state at module level: `_cache: dict = {}`, global lists, in-memory counters.
  - The `global` keyword.
  - Instantiating database engines, HTTP clients, or reading `os.environ` at import time (C12). Engines and clients are managed via the FastAPI lifespan context.

## Helper locality (C16)

- A helper function used only within one module must be marked file-private with a leading underscore (`def _validate_checksum(...)`).
- It remains in that module until a second module explicitly needs it.
- When shared, move it into the domain module that owns the concept, named for what it does. Never create generic `utils.py`, `helpers.py`, or `common.py`.

## Export surface and package entry files (C17)

- `__init__.py` is empty by default.
- An `__init__.py` may declare an explicit `__all__`, listing only the symbols other packages actually import through it (tests included). A name nobody imports through the package is removed from `__all__` (and its import line), not kept "for later".
- Never export private helpers (`_name`), implementation details or test hooks.

```python
# app/integrations/payments/__init__.py — good: callers import these two from the package
from .client import PaymentClient
from .errors import PaymentDeclined

__all__ = ["PaymentClient", "PaymentDeclined"]

# bad: every public symbol "just in case", plus an internal helper
__all__ = ["PaymentClient", "PaymentDeclined", "RetryPolicy", "build_headers", "_sign"]
```

- Never use wildcard imports (`from .x import *`). Wildcards obscure symbol origin and leak private helpers into public API surface.
