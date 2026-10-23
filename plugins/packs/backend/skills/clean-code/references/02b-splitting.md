# 02b — Splitting long code

When a unit exceeds size limits or accumulates multiple responsibilities, split it cleanly without introducing pass-through layers.

## When to split

Split code when:
- It exceeds limits in [02 — Size and structure](02-size-and-structure.md).
- The unit has multiple reasons to change (e.g. database schema changes AND external API formatting).
- An honest name requires "and" or "or" (e.g. `parse_and_persist_order`).
- Mixed abstraction levels appear together (raw SQL execution mixed with presentation formatting and business validation).

## Identifying the pieces

1. Identify distinct concerns within the unit:
   - Input schema parsing / validation.
   - Domain business rules and state transition checks.
   - Persistence operations (SQL / ORM operations).
   - External service calls (HTTP client / messaging).
2. Group operations that always vary together; separate operations that vary independently.
3. Choose intention-revealing names following [01 — Naming](01-naming.md).

## Where split pieces go

- Placement follows `{{slot:clean-architecture}}`:
  - Domain rules stay in the domain layer (`domain/`).
  - Coordination and business flows stay in application services (`services/` or `use_cases/`).
  - Database queries move into dedicated repositories (`repositories/`).
  - HTTP routers handle only request parsing, dependency injection, and status code mapping (`routers/`).
- Sibling private helpers stay in the same module if used by only one class or function.
- If moving across packages, place the helper in the module that owns the concept, never in a generic `utils.py`.

## Safe refactoring protocol

1. Ensure existing unit and integration tests pass before modifying structure.
2. Extract the helper or new module.
3. Update all call sites across the codebase in the same commit.
4. Delete the original code from the old location; do not leave forwarding wrappers or re-export aliases (C1).
5. Re-run `ruff format`, `ruff check`, `mypy`, and pytest to verify that behavior remains unchanged.
