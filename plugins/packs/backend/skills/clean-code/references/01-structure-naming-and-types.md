# 01 — Structure, Naming, and Types (Python / FastAPI)

Consolidated rules for naming (**C5**), size thresholds and splitting (**C6**), one-concept-one-place (**C1**), module-level purity (**C15**), helper locality (**C16**), explicit export surface (**C17**), Python 3.12+ static types (**C9**), Pydantic vs frozen dataclasses (**C13**), constants (**C7**), and comments (**C8**).

---

## 1. Naming Conventions (C5)

Names are primary documentation. A single clear convention per concept prevents misreadings and duplicate abstractions.

| Kind | Pattern | Example | Note |
|---|---|---|---|
| Module / package | `snake_case.py` / `snake_case/` | `order_service.py`, `orders/` | PEP 8 module and package convention. |
| Test file | `test_<module>.py` | `test_order_service.py` | Discovered automatically by pytest. |
| Migration file | `<timestamp>_<slug>.py` | `20261023_add_order_table.py` | Ordered chronologically by Alembic. |
| Class / Pydantic Model | `PascalCase` | `OrderCreateRequest`, `OrderRepository` | Noun phrase representing an entity or service. |
| Exception | `PascalCase` ending in `Error` | `OrderNotFoundError`, `InvalidStateError` | Distinguishes errors from standard entities. |
| Enum | `PascalCase` (`enum.StrEnum`) | `OrderStatus.PENDING`, `Role.ADMIN` | `UPPER_SNAKE` member names. |
| Function / method | `snake_case` (verb phrase) | `get_order()`, `create_invoice()` | Describes the action performed. |
| Boolean | `is_`, `has_`, `can_`, `should_` | `is_active`, `has_permission()`, `can_cancel` | Clearly conveys boolean semantics. |
| Module constant | `UPPER_SNAKE` | `DEFAULT_TIMEOUT_SECONDS`, `MAX_RETRIES` | True constants read by multiple functions. |
| Private module helper | `_snake_case` | `_calculate_tax()`, `_parse_token()` | Leading underscore marks file-private scope. |

- **Domain glossary**: Use business terms from requirements verbatim; never invent synonyms (`Order` vs `Purchase` vs `Booking`).
- **Include units**: Explicitly suffix non-obvious units (`timeout_seconds`, `max_payload_bytes`, `delay_ms`).
- **Banned vague names**: Never use `data`, `info`, `payload`, `item`, `obj`, `val`, `tmp`, `Manager`, `Helper`, `Utils`, `Handler`, `Processor`, `handle()`, or `process()`.

---

## 2. Size Thresholds & Decomposition (C6)

Thresholds apply to new or modified code:

| Unit | Limit | Remedy when exceeded |
|---|---|---|
| Function / method | ≤ ~30 lines | Extract cohesive private `_snake_case` steps. |
| File / module | ≤ ~300 lines | Split by responsibility into dedicated domain/service/repository modules. |
| Parameters | ≤ 3 parameters | Group cohesive inputs into a Pydantic schema or `@dataclass(frozen=True)`. |
| Nesting depth | ≤ 2 levels | Flatten control flow with early returns and guard clauses. |

### How & Where to Split Oversized Code
1. **Separate distinct concerns**: Input parsing/validation (`routers/` / schemas), domain business rules (`domain/`), orchestration (`services/` / `use_cases/`), persistence (`repositories/`), and outbound HTTP/messaging (`integrations/`).
2. **Safe refactoring**: Keep existing tests green → extract the new helper/module → update all call sites in the same commit → delete the old code without leaving forwarding wrappers or aliases (**C1**).

---

## 3. Structure, Globals, Locality, and Exports (C1, C15, C16, C17)

- **One concept, one place (C1)**:
  - **No pass-through wrappers**: Delete any function or class that merely forwards arguments without transformation, authorization, caching, or error mapping.
  - **No compatibility aliases**: Update all call sites when renaming or moving a symbol; never leave `# noqa: F401` re-export shims.
- **No mutable module globals (C15)**:
  - Module level holds only true shared constants (`UPPER_SNAKE`), `logger = logging.getLogger(__name__)`, and the dedicated settings class.
  - Never declare module-level mutable state (`_cache: dict = {}`, global lists, counters) or use the `global` keyword.
- **Helper locality (C16)**:
  - A helper used within a single module stays private (`def _validate_checksum(...)`) in that module.
  - Move it only when a second module imports it, placing it in the domain module that owns the concept—never create `utils.py`, `helpers.py`, or `common.py`.
- **Explicit export surface (C17)**:
  - `__init__.py` is empty by default.
  - If an explicit `__all__` is declared, it lists **only** the symbols other packages actually import through it (including tests).
  - Never use wildcard imports (`from .x import *`) and never export `_private` helpers or test hooks.

---

## 4. Static Types, Immutability, Constants & Comments (C7, C8, C9, C13)

- **Full Python 3.12+ Type Annotations (C9)**:
  - Annotate all function parameters and return types using built-in generics (`list[str]`, `dict[str, int]`, `str | None`).
  - Never pass business data across layers as `dict[str, Any]`.
  - Never add bare `# type: ignore`; always specify the error code (`# type: ignore[import-untyped]`) with a brief reason.
- **Pydantic vs Frozen Dataclasses (C13)**:
  - **Pydantic (`BaseModel`)**: External boundaries (HTTP request/response bodies, query params, `BaseSettings`).
  - **Frozen Dataclasses (`@dataclass(frozen=True)`)**: Internal domain value objects and immutable data transfer without validation overhead.
- **Named Constants & Enums (C7)**:
  - Use `enum.StrEnum`, `typing.Literal`, or `UPPER_SNAKE` constants instead of raw strings or magic numbers (`if status == OrderStatus.PENDING:`).
- **Comments Explain WHY (C8)**:
  - Explain non-obvious business constraints, external API quirks, or trade-offs; delete docstrings/comments that merely echo the function signature. Preserve unrelated existing comments.
