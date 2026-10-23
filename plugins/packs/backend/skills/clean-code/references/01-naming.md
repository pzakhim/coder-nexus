# 01 — Naming

Names are primary documentation. A single clear convention per concept prevents misreadings and duplicate abstractions.

## Files and folders

| Kind | Pattern | Example | Reason |
|---|---|---|---|
| Module file | `snake_case.py` | `order_service.py`, `models.py` | Standard Python module convention (PEP 8). |
| Package folder | `snake_case/` | `orders/`, `auth/` | Valid Python package identifier. |
| Test file | `test_<module>.py` | `test_order_service.py` | Discovered automatically by pytest. |
| Migration file | `<timestamp>_<slug>.py` | `20261023_add_order_table.py` | Ordered chronologically by Alembic. |

## Types, functions, variables

| Kind | Convention | Example | Note |
|---|---|---|---|
| Class / Pydantic Model | `PascalCase` | `OrderCreateRequest`, `OrderRepository` | Noun phrase representing an entity or service. |
| Exception | `PascalCase` ending in `Error` | `OrderNotFoundError`, `InvalidStateError` | Distinguishes errors from standard entities. |
| Enum | `PascalCase` with `UPPER_SNAKE` values | `OrderStatus.PENDING`, `Role.ADMIN` | Subclass `enum.StrEnum` for string values. |
| Function / method | `snake_case` (verb) | `get_order()`, `create_invoice()` | Describes the action performed. |
| Boolean variable / function | `is_`, `has_`, `can_`, `should_` | `is_active`, `has_permission()`, `can_cancel` | Clearly conveys boolean semantics. |
| Constant (module-level) | `UPPER_SNAKE` | `DEFAULT_TIMEOUT_SECONDS`, `MAX_RETRIES` | True constants read by multiple functions. |
| Private module helper | `_snake_case` | `_calculate_tax()`, `_parse_token()` | Leading underscore marks file-private scope. |
| TypeVar / Generic | `PascalCase` ending in `T` | `ModelT`, `SchemaT` | Clearly marks type variables. |

## Words and concepts

- **Domain glossary**: Use business terms from requirements and domain specifications verbatim. Never invent synonyms (e.g., if domain says `Order`, do not name variables `Purchase`, `Booking`, or `Txn`).
- **Units in names**: Explicitly include measurement units when not obvious: `timeout_seconds`, `max_payload_bytes`, `delay_ms`.
- **Banned vague names**:
  - `data`, `info`, `payload`, `item`, `obj`, `val`, `tmp`: State what the object represents (`user_profile`, not `user_info`).
  - `Manager`, `Helper`, `Utils`, `Handler`, `Processor`: Use role-focused nouns or service names (`PaymentGateway`, `TaxCalculator`, `OrderService`).
  - `handle()`, `process()`: Use specific action verbs (`dispatch_event()`, `execute_step()`).
