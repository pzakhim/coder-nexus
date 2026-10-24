# 01 — Folder layout and roles

Default tree for a FastAPI + SQLAlchemy 2 async + PostgreSQL service. An existing workspace keeps its verified tree and maps these roles onto it ([../SKILL.md](../SKILL.md)).

## 1. Roles

| Path | Owns | Does not own |
|---|---|---|
| `app/main.py` | `create_app()`: builds `FastAPI(lifespan=lifespan)`, includes every router, registers error handlers; module-level `app = create_app()` for the `fastapi` CLI entrypoint | Settings reads, DB connections, business logic |
| `app/api/deps.py` | Shared `Annotated` aliases: `SessionDep`, `SettingsDep`, `CurrentUserDep`, and one `get_<resource>_service` + `<Resource>ServiceDep` per service | Queries, rules |
| `app/api/auth.py` | `get_current_user` (FastAPI security dependency): reads the credential, verifies it with `app/core/security.py`, returns `CurrentUser` | Per-resource permission decisions (those are in services) |
| `app/api/error_handlers.py` | `register_error_handlers(app)`: maps each `app/core/errors.py` class to the status code and error body of the API contract | Deciding *whether* something is an error |
| `app/api/routers/<resource>.py` | One `APIRouter(prefix=..., tags=[...])` per resource; one function per HTTP method; return type = response schema | `select`, `commit`, permission logic, mapping ORM objects |
| `app/schemas/<resource>.py` | Request bodies (`<Resource>Create`, `<Resource>Update`), responses (`<Resource>Read`, `<Resource>Page`), query objects | ORM classes, database access |
| `app/services/<resource>.py` | One class per resource (`OrderService`) with one public method per use case; business rules, authorization, data-scope checks, the commit, ORM → schema mapping | HTTP types (`Request`, `HTTPException`), raw SQL strings |
| `app/repositories/<resource>.py` | One class per aggregate (`OrderRepository`): `get`, `list_for_customer`, `add`, ...; `flush()` to surface constraint errors; translating `IntegrityError` into `ConflictError` | Commit/rollback, business rules, schemas |
| `app/models/base.py` | `class Base(DeclarativeBase)` with a `MetaData(naming_convention=...)` so constraint names are stable across Alembic revisions; `eager_defaults` for server-generated columns | Tables |
| `app/models/<resource>.py` | ORM tables with `Mapped[...]`; relationships with `lazy="raise"` | Validation for API input, serialization |
| `app/models/enums.py` | `enum.StrEnum` values stored in columns and shared with schemas | Anything importing SQLAlchemy or Pydantic |
| `app/models/__init__.py` | `from app.models import orders, customers  # noqa: F401` - registers every table on `Base.metadata` | Re-exporting classes |
| `app/core/settings.py` | `Settings(BaseSettings)` and `get_settings()` (cached) | Reading settings at import time elsewhere |
| `app/core/errors.py` | `AppError` and subclasses (`NotFoundError`, `ConflictError`, `PermissionDeniedError`, `ValidationFailedError`), each with a stable `code` used by the contract | Status codes (those live in `api/error_handlers.py`) |
| `app/core/security.py` | Framework-free `CurrentUser` (id, roles, scope ids) and token/password helpers; rules in `{{slot:secure-coding-standards}}` | FastAPI imports (so services can depend on `CurrentUser`) |
| `app/db/session.py` | `build_engine(settings)`, `build_session_factory(engine)`, `get_session(request)` | Queries |
| `app/integrations/<provider>.py` | One outbound client per provider (`httpx.AsyncClient`), base URL and key from settings, provider errors translated to `app/core/errors.py` | Business rules |
| `alembic/env.py`, `alembic/versions/` | Migrations; `env.py` imports `app.models` and uses `Base.metadata` | Data seeding for tests (seeding is a PHASE-00 task, `{{slot:architecture-design}}`) |

Add a folder only when the first file for it is needed. A service with no provider has no `integrations/`.

## 2. Naming

| Kind | Pattern | Example |
|---|---|---|
| Module | `snake_case.py`, plural resource name | `orders.py` |
| Router object | `router` in every router module; imported as the module | `from app.api.routers import orders` → `app.include_router(orders.router)` |
| Schema | `<Resource><Purpose>` | `OrderCreate`, `OrderUpdate`, `OrderRead`, `OrderPage` |
| Service / method | `<Resource>Service`, verb + noun | `OrderService.cancel_order` |
| Repository / method | `<Resource>Repository`, what it returns | `OrderRepository.get_for_customer` |
| ORM class / table | singular class, plural table | `Order` / `orders` |
| Dependency alias | `<Thing>Dep` | `OrderServiceDep` |

Names follow the domain glossary in `codebase-notes.md` (`## 2. Glossary`); a second word for the same concept is a finding (`{{slot:clean-code}}` C5).

## 3. Tests mirror `app/`

```text
tests/
  conftest.py                    test settings, engine on the test database, session per test, httpx client
  api/routers/test_orders.py     HTTP behavior: status codes, contract bodies, auth per role
  services/test_orders.py        business rules, authorization, commit/rollback effects
  repositories/test_orders.py    queries against the real test PostgreSQL database
```

- A test file sits at the mirrored path of the module it tests, so a reviewer finds both from one name.
- Repository and API tests run against a real PostgreSQL test database migrated with `alembic upgrade head`, never SQLite and never `Base.metadata.create_all` (PostgreSQL types, constraints and locks differ). Fixtures, factories and required cases: `{{slot:unit-testing}}`.
