---
name: clean-code
description: Python clean-code standard for a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async) service - deterministic CLI gates (ruff, mypy) plus mandatory design and semantic rules (no pass-through wrappers or aliases, module locality, explicit export surface, specific exceptions, pure imports, immutable value objects). Use while implementing, refactoring, self-checking before READY_FOR_REVIEW, and reviewing backend code.
---

# Backend Clean Code (Python / FastAPI)

Goal: Python code a newcomer reads correctly on first pass and changes in one place.
All check flags (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

---

## 1. Deterministic Tool Gates (`PASS` / `FAIL`)

Installed and configured by `coder-nexus setup tools --pack backend`. Every check below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)** and must pass before `READY_FOR_REVIEW`:

| Tool Gate | Command | Enforces Rules Automatically |
|---|---|---|
| **Linter & Complexity** | `uv run ruff check .` | Unused imports/variables (**C2**: `F401`, `F841`), debug `print`/`breakpoint` (**C3**: `T10`, `T20`), bare/blind except (**C4**: `E722`, `BLE001`), naming (**C5**: `N`), cyclomatic complexity (**C6**: `C90`), wildcard imports (**C17**: `F403`) |
| **Formatter** | `uv run ruff format --check .` | Consistent formatting across touched files |
| **Static Type Checker** | `uv run mypy .` | Full type annotations, no unguarded `Any`, no unused `# type: ignore` (**C9**) |

---

## 2. Core Design & Craft Principles (Mandatory Compliance)

Rules written below govern design and semantics that static linters cannot infer automatically. When writing or reviewing code, **every rule below is mandatory to follow**:

| # | Principle | Why | Verification |
|---|---|---|---|
| **C1** | **One concept, one place.** No pass-through wrappers forwarding without behavior; no compatibility aliases or re-export shims kept for old names. | Every hop adds files to open for nothing; two names for one concept never converge. | Review; `rg` check |
| **C2** | **No dead code.** Remove unused functions, imports, variables, orphan `TODO`s, and commented-out code blocks. | Dead code is read, maintained, and trusted as if it ran. | `ruff check` (`F401`, `F841`) + Review |
| **C3** | **No debug leftovers.** No `print()`, `breakpoint()`, `import pdb`, or temporary debug flags in committed code. | Noise in logs, potential data leakage, and sign of an unverified change. | `ruff check` (`T10`, `T20`) |
| **C4** | **No swallowed errors.** Catch specific exceptions (`IntegrityError`, `httpx.TimeoutException`); re-raise domain errors with `from exc`. `except Exception` only at top-level worker/middleware boundaries with structured logging. | Swallowed errors turn loud failures into silent corrupted data. | `ruff check` (`E722`, `BLE001`) + Review |
| **C5** | **Intention-revealing names.** `snake_case` modules, functions, variables; `PascalCase` classes; `UPPER_SNAKE` constants; verb phrases for functions, `is_/has_/can_/should_` for booleans. | Names are primary documentation; vague names (`data`, `info`, `process`) hide intent. | `ruff check` (`N`) + Review |
| **C6** | **Small, focused units.** Function ≤ ~30 lines, file ≤ ~300 lines, ≤ 3 parameters (group cohesive inputs into a Pydantic model/dataclass), nesting ≤ 2 using guard clauses. | Short units with flat control flow are easier to read, test, and review. | `ruff check` (`C90`) + Review |
| **C7** | **No magic values.** Use `enum.StrEnum`, `typing.Literal`, or named constants for statuses, roles, limits, and timeouts. | Scattered literals drift and break silently when one copy changes. | Review |
| **C8** | **Comments explain WHY.** Document non-obvious business rationale, invariants, and external constraints; never restate what the Python syntax already says. | "What" comments rot; "why" comments save future readers an investigation. | Review |
| **C9** | **Full static types.** Explicit type hints on all signatures and models; no bare `Any`; no `# type: ignore[code]` without an inline justification. | Type hints catch contract mismatches before runtime. | `mypy` |
| **C10** | **Scope discipline.** Modify only files within the approved task/phase scope. Record out-of-scope legacy debt in `Concerns` instead of doing drive-by edits. | Unrelated edits bury the real change in review and create merge conflicts. | `git diff` + Review |
| **C11** | **Workspace contracts win.** Honor the workspace's configured `pyproject.toml`, error hierarchy, DI (`Depends`), and logging conventions over generic advice. | Competing styles fragment the codebase. | Review |
| **C12** | **Import-time purity.** No database connection, network call, file I/O, or `os.environ` read at module import time (settings load via `pydantic-settings` + DI). | Import-time side effects break unit test collection, Alembic migrations, and startup order. | Review |
| **C13** | **Explicit state changes.** Use `frozen=True` dataclasses / immutable Pydantic models for value objects; mutate state only where ownership is explicit. | Shared mutable state causes order-dependent test failures and async race conditions. | Review |
| **C14** | **Self-check before handoff.** Execute all CLI gates (`ruff`, `mypy`, `rg`, `pytest`) on the committed revision and record each evidence row (`PASS` / `FAIL`). | An unrun check is `NOT_RUN`, never `PASS`. | `evidence-standard` |
| **C15** | **No mutable module globals.** Module level holds only true constants (`Final`) and logger; never module-level mutable dicts/lists/caches/registries or `global`. | Mutable module state leaks across async workers and test cases. | `rg` check + Review |
| **C16** | **Helper locality.** A helper used in one module stays private (`_snake_case`) in that module. Move only when a second module imports it, into the owning domain module—never create `utils.py` or `helpers.py`. | Leading underscore enforces internal scope; generic utility buckets become junk drawers. | Review |
| **C17** | **Explicit export surface.** `__init__.py` is empty by default; if an explicit `__all__` is used, it lists only the symbols other packages actually import; no wildcard imports (`from .x import *`); never export `_private` helpers or test hooks. | Every export is a public contract to maintain; wildcards hide origins and leak internals. | `ruff check` (`F403`) + `rg` check + Review |

---

## 3. Reference Guides

| Topic | Reference |
|---|---|
| Naming, size thresholds, splitting, wrappers, globals, helper locality, exports, static types, constants, and comments | [01 — Structure, Naming & Types](references/01-structure-naming-and-types.md) |
| Domain exceptions, error chaining, import-time/lifespan purity, and structured logging | [02 — Errors, Lifecycle & Logging](references/02-errors-lifecycle-and-logging.md) |
| Pre-handoff CLI gates (`PASS` / `FAIL`) and review grading (`BLOCKER` / `MAJOR` / `MINOR`) | [03 — Self-Check & Review](references/03-self-check-and-review.md) |

## 4. Relationship with Other Skills

- **Layer boundaries & placement**: `{{slot:clean-architecture}}` (enforced via `uv run lint-imports`).
- **Post-green refactoring**: `{{slot:code-simplification}}`.
- **Security rules**: `{{slot:secure-coding-standards}}` (and `uv run pip-audit`).
- **Debugging & unit tests**: `{{slot:root-cause-debugging}}` and `{{slot:unit-testing}}`.
