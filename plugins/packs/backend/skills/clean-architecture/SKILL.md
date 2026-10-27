---
name: clean-architecture
description: Folder layout, layer roles, dependency direction, and DI/transaction rules for Python FastAPI + SQLAlchemy 2 async + PostgreSQL backends - deterministic import-linter and rg boundary gates, routers, Pydantic schemas, services that own the transaction, repositories, ORM models, settings, and lifespan - plus how to add a feature and split oversized files.
---

# Backend Clean Architecture (FastAPI + SQLAlchemy 2 Async)

The layout below is the default for a new service and the canonical role map for an existing one. **The workspace's verified layout wins** (`{{slot:clean-code}}` C11): if `codebase-notes.md` records a feature-first tree (`app/modules/<feature>/...`) or custom folder names, map the same roles onto it and keep it. All check flags (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md`.

---

## 1. Deterministic Tool & Boundary Gates (`PASS` / `FAIL`)

Installed and verified via `coder-nexus setup tools --pack backend`. Every command below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)** and must pass before `READY_FOR_REVIEW`:

| Tool / Boundary Gate | Command | Enforces Rules Automatically |
|---|---|---|
| **Import Boundary Linter** | `uv run lint-imports` | Layered import direction (`api → services → repositories → models`), framework-free `services`/`core`, and schema/model separation (**A1, A2, A8**) |
| **Static Type Checker** | `uv run mypy app tests` | Typed dependency aliases (`Annotated`), schema/model contracts, and service/repository signatures (**A1, A5**) |
| **Import-Time Purity Probe** | `env -i PATH="$PATH" uv run python -c "import app.main"` | Zero environment reads, database connections, or network I/O at module import time (**A7**) |
| **Ripgrep (`rg`) Boundary Scan** | `rg -n` forbidden-import checks ([02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md)) | Fallback boundary verification when `import-linter` is not yet configured (**A1, A2, A8**) |

---

## 2. Core Architecture & Layer Principles (Mandatory Compliance)

Rules written below govern layer responsibilities, dependency direction, and transaction/session lifecycles. **Every rule is mandatory to follow**:

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **A1** | **Separate Pydantic schemas and SQLAlchemy ORM models.** Services map explicitly via `Schema.model_validate(orm_obj)` (`from_attributes=True`). Never return ORM instances directly from routers or import ORM models into `schemas`. | Prevents accidental column leaks in API responses and decouples database migrations from contract changes. | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md) |
| **A2** | **Thin routers.** Routers do three things only: receive validated input, call **one** service method, and return its response schema. No `select()`, no `commit()`, and no permission branching inside routers. | Keeps business rules and authorization testable without HTTP transport scaffolding. | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md) |
| **A3** | **Service owns the transaction commit.** The top-level service method called by the router calls `await self.session.commit()` once at the end. Repositories call `flush()` only—they never `commit()` or `rollback()`. | Guarantees one request = one atomic unit of work; partial failures roll back cleanly on session close. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A4** | **One `AsyncSession` per request.** Provide `AsyncSession` via the `yield` dependency `get_session`; never store a module-level session or share a single session across concurrent `asyncio.gather` tasks. | `AsyncSession` is not safe for concurrent coroutine access. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A5** | **Explicit `Annotated[..., Depends(...)]` DI wiring.** Define shared dependency aliases in `app/api/deps.py` (`SessionDep`, `SettingsDep`, `CurrentUserDep`, `<Resource>ServiceDep`). Never instantiate sessions inside services. | Makes every dependency explicit and replaceable via `app.dependency_overrides` in tests. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A6** | **Framework-free domain errors.** Services and repositories raise domain errors from `app/core/errors.py`; `app/api/error_handlers.py` maps them to HTTP status codes and contract error bodies. | Keeps `services`, `repositories`, and `core` independent of FastAPI/Starlette. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A7** | **Lifespan and cached settings own startup I/O.** Read settings via `@lru_cache def get_settings()` and create/dispose the database engine and `httpx.AsyncClient` inside `lifespan` (`{{slot:clean-code}}` C12). | Importing `app.main` in tests, Alembic, or CLI tools never triggers network or DB connections. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A8** | **Minimal `__init__.py` export surface.** Keep `__init__.py` empty by default (`{{slot:clean-code}}` C17), except `app/models/__init__.py` which imports model modules solely to register tables on `Base.metadata`. | Avoids circular imports and hidden coupling while ensuring Alembic discovers all ORM tables. | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md) |
| **A9** | **Explicit async relationship loading.** Declare ORM relationships with `lazy="raise"` and load related rows explicitly in repositories via `selectinload()` / `joinedload()`. | Prevents runtime `MissingGreenlet` errors and hidden N+1 queries during schema serialization. | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| **A10** | **No speculative layers or single-implementation protocols.** Add a `Protocol`, abstract base class, or folder only when required by the approved phase or when 2+ implementations exist (`{{slot:clean-code}}` C1). | Eliminates pass-through boilerplate and empty placeholder layers. | [03 — Adding, Splitting & Review](references/03-adding-splitting-and-review.md) |

---

## 3. Reference Guides

| Topic | Reference |
|---|---|
| Directory layout, layer roles, naming conventions, starter templates, and mirrored `tests/` tree | [01 — Layout & Layer Roles](references/01-layout-and-layer-roles.md) |
| Dependency matrix, `import-linter` config, `rg` boundary checks, DI/session/transaction rules, and `lifespan`/settings | [02 — Dependencies, DI & Transactions](references/02-dependencies-di-and-transactions.md) |
| Step-by-step adding a resource/endpoint, splitting oversized files, feature-first mapping, and `BLOCKER`/`MAJOR`/`MINOR` review rubric | [03 — Adding, Splitting & Review](references/03-adding-splitting-and-review.md) |
<!-- {{profile_references}} -->

---

## 4. Starter Templates

Copy only what the approved task requires and resolve every import against real workspace code:
- **Core**: [settings.py.tpl](templates/core/settings.py.tpl), [session.py.tpl](templates/core/session.py.tpl), [main.py.tpl](templates/core/main.py.tpl), [deps.py.tpl](templates/core/deps.py.tpl), [base.py.tpl](templates/core/base.py.tpl), [errors.py.tpl](templates/core/errors.py.tpl)
- **Feature**: [model.py.tpl](templates/feature/model.py.tpl), [repository.py.tpl](templates/feature/repository.py.tpl), [schemas.py.tpl](templates/feature/schemas.py.tpl), [service.py.tpl](templates/feature/service.py.tpl), [router.py.tpl](templates/feature/router.py.tpl)

## 5. Relationship with Other Skills

- **Naming & file/function size thresholds**: `{{slot:clean-code}}` (`01-structure-naming-and-types.md`).
- **FastAPI route & dependency idioms**: `backend-fastapi`.
- **PostgreSQL queries & indexing**: `backend-postgres` and `backend-database-migrations`.
- **Post-green refactoring**: `{{slot:code-simplification}}`.
