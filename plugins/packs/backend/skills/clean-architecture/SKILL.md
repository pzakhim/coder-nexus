---
name: clean-architecture
description: Folder layout, layer roles and dependency direction for the Python FastAPI + SQLAlchemy 2 async + PostgreSQL backend - routers, Pydantic schemas, services that own the transaction, repositories, ORM models, settings and the database session - plus how to add a feature and how to split a long file. Use when creating or extending an endpoint, a service, a repository or a model, when deciding where a file goes or what may import what, when wiring dependencies with Annotated Depends, and when the Code Reviewer grades architecture.
---

# Backend Clean Architecture (FastAPI + SQLAlchemy 2 async)

The layout below is the default for a new service and the vocabulary for an existing one. **The workspace's verified layout wins** (`{{slot:clean-code}}` C11): if `codebase-notes.md` records a feature-first tree (`app/modules/<feature>/...`) or other names, map the same roles onto it and keep it. Moving an existing service to this layout is a `D-NN`, never a side effect of a task.

FastAPI API usage (Annotated, return types, `yield` dependencies, lifespan) follows `backend-fastapi`. This skill decides where code lives and what may import what.

## Before writing code

1. The phase is approved and the task lists every file in **Scope / Files** (`work-item-contract` → `plan-and-task-contract.md`). A file outside that list is out of scope.
2. Read the sibling of what you are adding (an existing router, service, repository, model) and copy its shape. Read `app/api/deps.py`, `app/db/session.py`, `app/core/settings.py` and `app/core/errors.py` before creating anything that resembles them.
3. Resolve every import from real code. A name you cannot find is not invented; it is a question or a **Consumes** line from an earlier task.

## Layout

```text
app/
  main.py                  create_app(): FastAPI(lifespan=...), include routers, register error handlers
  api/
    deps.py                shared Annotated dependencies (SessionDep, CurrentUserDep, SettingsDep)
    auth.py                get_current_user: reads the credential, returns core.security.CurrentUser
    error_handlers.py      domain error -> status code + contract error body
    routers/<resource>.py  APIRouter per resource: parse -> call one service method -> return schema
  schemas/<resource>.py    Pydantic v2 request/response models (the API contract)
  services/<resource>.py   use cases: business rules, authorization, the one commit
  repositories/<resource>.py  select()/insert/update for one aggregate; flush, never commit
  models/base.py           DeclarativeBase + naming convention
  models/<resource>.py     SQLAlchemy 2 ORM tables (Mapped[...], mapped_column)
  core/settings.py         pydantic-settings Settings + cached get_settings()
  core/errors.py           framework-free error hierarchy
  core/security.py         framework-free CurrentUser type and token/password helpers
  db/session.py            engine and session factory builders, get_session (yield)
  integrations/<provider>.py  outbound clients (httpx), only when a provider exists
alembic/                   env.py + versions/ (backend-database-migrations)
tests/                     mirrors app/: tests/api/routers, tests/services, tests/repositories
```

Folder roles, naming and the test mirror: [references/01_folder_layout.md](references/01_folder_layout.md).

## Dependency direction

```text
main -> api (routers, deps, error_handlers) -> services -> repositories -> models
                       \-> schemas <-------------/            db.session, core: used by all
```

| Layer | May import | Never imports | Why |
|---|---|---|---|
| `api/routers` | `api/deps`, `schemas`, service dependency aliases | `repositories`, `models`, `sqlalchemy` | Handlers stay thin; queries and rules are testable without HTTP |
| `services` | `repositories`, `schemas`, `models`, `core/errors`, `integrations` | `fastapi`, `starlette`, `api/*` | Workers, CLI and tests call services without a request |
| `repositories` | `models`, `core/errors`, `sqlalchemy` | `schemas`, `services`, `fastapi` | Storage does not know the API contract |
| `models` | `models/base`, `models/enums`, `sqlalchemy` | `schemas`, `services`, `fastapi`, `pydantic` | Tables change by migration only, never because a response changed |
| `schemas` | `pydantic`, `models/enums` | `models` (ORM classes), `sqlalchemy`, `fastapi` | The contract is plain data; enums are shared, tables are not |
| `core` | standard library, `pydantic`, `pydantic-settings`, crypto/token libraries | anything else in `app`, `fastapi` | Everyone depends on core, so core depends on nobody and stays importable from services |

Checks, the import-linter contract and the ripgrep (`rg`) fallback: [references/02_dependency_rules.md](references/02_dependency_rules.md).

## Golden rules

| # | Rule | Why |
|---|---|---|
| A1 | Pydantic schemas and SQLAlchemy models are separate classes. Services map with `OrderRead.model_validate(order)` (`from_attributes=True`) | Each exposed field is a decision; nothing leaks because a column was added |
| A2 | Routers do three things: receive validated input, call **one** service method, return its schema. No `select`, no `commit`, no `if role ==` | One place for each rule; handlers carry no logic to test |
| A3 | The service method called by the router owns the transaction: it calls `await self.session.commit()` once at the end. Repositories `flush()`; they never commit or roll back | One request = one unit of work; a failure leaves nothing half-written |
| A4 | One `AsyncSession` per request from the `yield` dependency `get_session`; never a module-level session, never shared across tasks | `AsyncSession` is not safe for concurrent use |
| A5 | Dependencies are wired with `Annotated[..., Depends(...)]` aliases; services are built by a function dependency (`get_order_service`) | Explicit construction; tests replace one dependency with `app.dependency_overrides` |
| A6 | Services raise errors from `app/core/errors.py`; `app/api/error_handlers.py` maps them to the contract's status codes and body | Services stay framework-free; every endpoint returns the same error shape |
| A7 | Settings come from `get_settings()` (cached); engine and session factory are created in `lifespan` and disposed after it | No environment read, connection or file I/O at import (`{{slot:clean-code}}` C12) |
| A8 | `__init__.py` follows `{{slot:clean-code}}` C17: empty by default, an explicit `__all__` only for symbols other packages import through it. Extra exception: `app/models/__init__.py` imports each model module and nothing else | One export rule, owned by clean-code; Alembic and relationship strings need every table registered |
| A9 | Relationships load explicitly (`selectinload`) and default to `lazy="raise"` | An implicit lazy load under async raises at runtime instead of failing in review |
| A10 | Add a `Protocol` or base class only when a second implementation exists (a provider sandbox client and a test fake) | One-implementation interfaces are pass-through layers (`{{slot:clean-code}}` C1) |

Sessions, transactions and DI in detail: [references/03_di_sessions_transactions.md](references/03_di_sessions_transactions.md). Settings, lifespan and startup: [references/04_settings_and_startup.md](references/04_settings_and_startup.md).

## Add a feature or split a file

Order inside a phase (each step its own task with a check, `incremental-implementation`): model → migration → repository → schemas → service → router + `include_router` → tests per layer. Steps, check commands and the split rules for long routers, services, repositories and schemas: [references/05_adding_and_splitting.md](references/05_adding_and_splitting.md).

## Starter templates

Copy only what the task needs and rename to the real resource; resolve every import against the workspace.

| Template | Becomes |
|---|---|
| [templates/core/settings.py.tpl](templates/core/settings.py.tpl) | `app/core/settings.py` |
| [templates/core/session.py.tpl](templates/core/session.py.tpl) | `app/db/session.py` |
| [templates/core/main.py.tpl](templates/core/main.py.tpl) | `app/main.py` |
| [templates/core/deps.py.tpl](templates/core/deps.py.tpl) | `app/api/deps.py` |
| [templates/core/base.py.tpl](templates/core/base.py.tpl) | `app/models/base.py` |
| [templates/core/errors.py.tpl](templates/core/errors.py.tpl) | `app/core/errors.py` |
| [templates/feature/model.py.tpl](templates/feature/model.py.tpl) | `app/models/<resource>.py` |
| [templates/feature/repository.py.tpl](templates/feature/repository.py.tpl) | `app/repositories/<resource>.py` |
| [templates/feature/schemas.py.tpl](templates/feature/schemas.py.tpl) | `app/schemas/<resource>.py` |
| [templates/feature/service.py.tpl](templates/feature/service.py.tpl) | `app/services/<resource>.py` |
| [templates/feature/router.py.tpl](templates/feature/router.py.tpl) | `app/api/routers/<resource>.py` |

Never add placeholder files, empty layers or settings fields the task does not need. Never invent endpoints, credentials or default values for required data: missing required data fails loudly.

## Sources

[references/sources.md](references/sources.md)
