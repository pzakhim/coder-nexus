---
name: clean-code
description: Python clean-code rules for a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async) service - no wrappers, no aliases or kept compatibility shims, module-level only for shared constants and settings, leading-underscore private helpers local to their module until a second module needs them, __init__.py exporting only what other packages import, intention-revealing snake_case naming, small focused units with guard clauses, no swallowed exceptions or bare except, typed models over raw dicts, no magic values, visible side effects, and self-checks with ruff, mypy and pytest. Use while the Code Writer implements or refactors Python code in a task, during the self-check before READY_FOR_REVIEW, and when the Code Reviewer grades code craft on a backend diff.
---

# Backend Clean Code (Python / FastAPI)

Goal: Python code a newcomer reads correctly on first pass and changes in exactly one place. Every rule carries its reason; a finding without a technical reason is not a finding.

Rules follow the C1–C17 baseline of `create-clean-code-skill` (carrying over core CC1–CC15). Graded on the rule-violation scale of [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md).

## Rules

| # | Rule | Why | Severity | Enforced by |
|---|---|---|---|---|
| C1 | **One concept, one place.** No wrappers forwarding without behavior; no aliases or re-export shims kept for old names. | Every hop adds files to open for nothing; two names for one concept never converge. | P1 | Review; `rg` check |
| C2 | **No dead code.** Remove unused functions, imports (ruff `F401`), variables (`F841`), orphan `TODO`, commented-out code. | Dead code is read, maintained and trusted as if it ran. | P1 | `ruff check` |
| C3 | **No debug code.** No `print()`, `breakpoint()`, `import pdb`, temporary debug flags. | Noise in logs, data leakage, and a sign of an unverified change. | P1 | `ruff check` (`T10`, `T20`) |
| C4 | **No swallowed errors.** Catch specific exceptions (`IntegrityError`, `httpx.TimeoutException`); re-raise with `from exc`. `except Exception` only at edges. | Swallowed errors turn loud failures into silent wrong data. | P1 | Review; `rg` check |
| C5 | **Intention-revealing names.** `snake_case` modules, functions, variables; `PascalCase` classes; `UPPER_SNAKE` constants; verbs for functions. | Names are primary documentation; vague names duplicate concepts. | P2 | Review |
| C6 | **Small, focused units.** Function ≤ ~30 lines, file ≤ ~300 lines, ≤ 3 parameters (or Pydantic model), nesting ≤ 2 with guard clauses. | Short units are easier to read, test and review. | P2 | `ruff` (C901, PLR09xx); Review |
| C7 | **No magic values.** Use `enum.StrEnum`, `typing.Literal` or named module constants for statuses, roles, limits. | Scattered literals drift and break silently when one copy changes. | P2 | Review |
| C8 | **Comments say why.** Explain non-obvious reasons and external constraints; never restate what the Python code clearly expresses. | "What" comments rot; "why" comments save the next reader an investigation. | P3 | Review |
| C9 | **Full types.** Mypy-clean type hints for signatures and models; no bare `Any`; no unexplained `# type: ignore`. | Type hints catch structural mismatches without executing tests. | P2 | `mypy` |
| C10 | **Change only task scope.** No drive-by renames, reformatting or refactoring of untouched files. Debt outside diff goes to Concerns. | Unrelated edits bury the real change in review. | P2 | Review |
| C11 | **Workspace contracts win.** The workspace's configured tools, line length, error hierarchy, DI, and conventions override generic advice. | Generic advice against a verified workspace contract creates two competing styles. | P1 | Review |
| C12 | **Visible side effects.** No database connection, network call, file I/O or `os.environ` read at import/module load (except settings object). | Import-time I/O breaks unit tests, Alembic migrations, and startup order. | P2 | Review |
| C13 | **Explicit state changes.** Prefer immutable Pydantic models / frozen dataclasses; mutate only where ownership is explicit. | Mutable global or shared state causes order-dependent test failures and race conditions. | P3 | Review |
| C14 | **Self-check before done.** Run formatter, linter, type checker, targeted greps, and affected unit tests; report each evidence row. | A rule without an executed check is a wish; an unrun check is NOT_RUN. | P1 | `evidence-standard` |
| C15 | **No meaningless globals.** Module level holds only shared constants and the settings object; no mutable caches, registries or `global`. | Global mutable state leaks between test cases and async request workers. | P1 mutable, else P2 | `rg` check; Review |
| C16 | **Helper locality.** Helper used in one module is `_snake_case` in that module. Move only when a second module imports it. Never `utils.py`. | Underscore signals internal scope; generic buckets become junk drawers. | P1 public internal, else P2 | Review |
| C17 | **Export surface.** `__init__.py` is empty by default; an explicit `__all__` lists only the symbols other packages actually import (tests included); no wildcard imports (`from .x import *`); never export private helpers or test hooks. | Every export is a contract to maintain; wildcards hide origins and leak internals. | P1 leaked internal, else P2 | `ruff check` (`F403`); each `__all__` name has an importer outside the package; Review |

## Which file to read

| Topic | Reference |
|---|---|
| Naming conventions and glossary | [01 — Naming](references/01-naming.md) |
| Thresholds, wrappers, globals, locality, exports | [02 — Size and structure](references/02-size-and-structure.md) |
| Splitting functions or modules over limit | [02b — Splitting](references/02b-splitting.md) |
| Exceptions, error contracts, structured logging | [03 — Errors and logging](references/03-errors-and-logging.md) |
| Types, Pydantic vs dataclass, magic values, comments | [04 — Types, constants, comments](references/04-types-constants-comments.md) |
| Step-by-step commands before hand-off | [05 — Self-check](references/05-self-check.md) |
| Review severity and grading | [06 — Review severity](references/06-review-severity.md) |

## Relationship with other skills

- **Placement and layers**: `{{slot:clean-architecture}}` decides where split pieces go (modules, domains, ports).
- **Simplifying code**: `{{slot:code-simplification}}` handles smell removal after tests pass.
- **Security risks**: `{{slot:secure-coding-standards}}` handles authorization, SQL injection, secrets, and sanitization.
- **Debugging and tests**: `{{slot:root-cause-debugging}}` fixes failing checks; `{{slot:unit-testing}}` drives unit tests.
