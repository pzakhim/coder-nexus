# 04 — Types, constants, comments

Explicit types and clean constants remove ambiguity and enable static verification.

## Full type annotations (C9)

- Annotate all function signatures (parameters and return types).
- Use modern Python 3.12+ syntax:
  - `list[str]`, `dict[str, int]`, `tuple[int, ...]` (built-in generic types, no `typing.List` or `typing.Dict`).
  - `str | None` instead of `Optional[str]`.
  - Type unions: `int | float` instead of `Union[int, float]`.
- **Prohibited**:
  - Raw untyped dictionaries (`dict[str, Any]` or `dict`) to pass business data across layer boundaries. Use Pydantic models or dataclasses.
  - Unexplained `# type: ignore`. When an ignore is strictly necessary due to an untyped third-party library, name the specific rule code: `# type: ignore[import-untyped]`.

## Pydantic models vs dataclasses

- **Pydantic models (`BaseModel`)**: Use for external boundary contracts: HTTP request/response payloads, configuration settings (`BaseSettings`), query parameter schemas.
- **Dataclasses (`@dataclass(frozen=True)`)**: Use for internal domain value objects and lightweight data transfer where schema validation overhead is unnecessary.

## Constants and magic values (C7)

- Replace string and numeric literals with named constants or enums:
  ```python
  # Good: StrEnum or Literal for domain states
  class OrderStatus(enum.StrEnum):
      PENDING = "pending"
      CONFIRMED = "confirmed"
      CANCELLED = "cancelled"

  # Good: Named constant for limits
  MAX_PAGE_SIZE = 100
  DEFAULT_PAGE_SIZE = 20
  ```
- Never compare against raw literal strings (`if status == "pending":`) or hardcode HTTP status codes in business logic.

## Meaningful comments (C8)

- **Explain why, not what**: Code shows *what* is happening; comments explain *why* a particular non-obvious approach was chosen, citing business constraints, external API quirks, or performance trade-offs.
- **No signature echo**: Avoid redundant docstrings:
  ```python
  # Bad
  def get_order(order_id: UUID) -> Order:
      """Get order by order id."""
      ...
  ```
- **Preserve existing comments**: Never delete unrelated existing comments or docstrings when modifying a file.
