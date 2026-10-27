# 01 — Folder Layout, Layer Roles, and Naming

Default directory tree for a FastAPI + SQLAlchemy 2 async + PostgreSQL service. An existing workspace keeps its verified layout and maps these layer responsibilities onto it ([../SKILL.md](../SKILL.md)).

---

## 1. Canonical Directory Tree

```text
.
├── app/
│   ├── main.py                       # create_app(): FastAPI(lifespan=...), include routers, register error handlers
│   ├── api/
│   │   ├── deps.py                   # shared Annotated dependencies (SessionDep, CurrentUserDep, SettingsDep)
│   │   ├── auth.py                   # get_current_user: reads credential, returns core.security.CurrentUser
│   │   ├── error_handlers.py         # domain error -> HTTP status code + contract error body
│   │   └── routers/
│   │       └── <resource>.py         # APIRouter per resource: parse -> call one service method -> return schema
│   ├── schemas/
│   │   └── <resource>.py             # Pydantic v2 request/response models (the API contract)
│   ├── services/
│   │   └── <resource>.py             # use cases: business rules, authorization, and the single transaction commit
│   ├── repositories/
│   │   └── <resource>.py             # select()/insert/update for one aggregate; flush, never commit
│   ├── models/
│   │   ├── base.py                   # DeclarativeBase + constraint naming convention
│   │   ├── enums.py                  # Shared StrEnum values
│   │   └── <resource>.py             # SQLAlchemy 2 ORM tables (Mapped[...], mapped_column)
│   ├── core/
│   │   ├── settings.py               # pydantic-settings Settings + cached get_settings()
│   │   ├── errors.py                 # framework-free domain error hierarchy
│   │   └── security.py               # framework-free CurrentUser type and token/password helpers
│   ├── db/
│   │   └── session.py                # engine and session factory builders, get_session (yield)
│   └── integrations/
│       └── <provider>.py             # outbound clients (httpx), added only when an external provider exists
├── alembic/
│   ├── env.py                        # async migration runner wired to Base.metadata
│   └── versions/                     # schema revisions (backend-database-migrations)
└── tests/                            # mirrors app/ structure
```

---

## 2. Layer Responsibilities & Ownership (**A1, A2, A8, A10**)

| Path | Owns | Must Never Contain |
|---|---|---|
| `app/main.py` | `create_app()`: builds `FastAPI(lifespan=lifespan)`, includes routers, registers error handlers | Settings reads at import time, DB queries, business logic |
| `app/api/deps.py` | Shared `Annotated` aliases (`SessionDep`, `SettingsDep`, `CurrentUserDep`) and `<Resource>ServiceDep` builders | Queries, business rules |
| `app/api/auth.py` | `get_current_user`: extracts and verifies credentials via `app/core/security.py`, returns `CurrentUser` | Per-resource authorization rules (owned by services) |
| `app/api/error_handlers.py` | `register_error_handlers(app)`: translates `app/core/errors.py` exceptions into HTTP status codes and contract bodies | Business error detection |
| `app/api/routers/<resource>.py` | One `APIRouter(prefix=..., tags=[...])` per resource; delegates to one service method and returns response schema | `select()`, `commit()`, permission logic, ORM-to-schema mapping |
| `app/schemas/<resource>.py` | Request payloads (`<Resource>Create`, `<Resource>Update`), responses (`<Resource>Read`, `<Resource>Page`), filter params | ORM classes, database access |
| `app/services/<resource>.py` | One class per resource (`OrderService`): business rules, authorization, data-scope checks, `await self.session.commit()`, ORM-to-schema mapping | FastAPI/Starlette types (`Request`, `HTTPException`), raw SQL |
| `app/repositories/<resource>.py` | One class per aggregate (`OrderRepository`): persistence queries, `flush()`, translating `IntegrityError` to `ConflictError` | `commit()`, `rollback()`, business rules, Pydantic schemas |
| `app/models/base.py` | `class Base(DeclarativeBase)` with deterministic `MetaData(naming_convention=...)` and `eager_defaults=True` | Domain tables |
| `app/models/<resource>.py` | ORM tables (`Mapped[...]`, `mapped_column`), relationships with `lazy="raise"` | API input validation, response serialization |
| `app/models/enums.py` | `enum.StrEnum` values stored in columns and shared with `schemas` | SQLAlchemy or Pydantic imports |
| `app/models/__init__.py` | `from app.models import orders, customers  # noqa: F401` to register tables on `Base.metadata` | Re-exporting classes for application code |
| `app/core/settings.py` | `Settings(BaseSettings)` and `@lru_cache def get_settings()` | Module-level `settings = Settings()` instantiation |
| `app/core/errors.py` | `AppError` and subclasses (`NotFoundError`, `ConflictError`, `PermissionDeniedError`, `ValidationFailedError`) | HTTP status codes |
| `app/core/security.py` | Framework-free `CurrentUser` and token/password helpers (`{{slot:secure-coding-standards}}`) | FastAPI imports |
| `app/db/session.py` | `build_engine(settings)`, `build_session_factory(engine)`, `get_session(request)` | Queries or business rules |
| `app/integrations/<provider>.py` | Outbound HTTP client (`httpx.AsyncClient`), translating provider errors into `app/core/errors.py` | Domain business rules |

Add a directory only when the first file for it is required (**A10**).

---

## 3. Architectural Naming & Mirrored Test Tree

| Kind | Pattern | Example |
|---|---|---|
| Module | `snake_case.py`, plural resource name | `orders.py` |
| Router object | `router` inside each router module | `from app.api.routers import orders` → `app.include_router(orders.router)` |
| Schema | `<Resource><Purpose>` | `OrderCreate`, `OrderUpdate`, `OrderRead`, `OrderPage` |
| Service / method | `<Resource>Service`, verb + noun | `OrderService.cancel_order` |
| Repository / method | `<Resource>Repository`, query intent | `OrderRepository.get_for_customer` |
| ORM class / table | Singular `PascalCase` class, plural `snake_case` table | `Order` / `orders` |
| Dependency alias | `<Thing>Dep` | `OrderServiceDep` |

### Mirrored `tests/` Layout
```text
tests/
├── conftest.py                       # test settings, engine on test DB, session per test, httpx AsyncClient
├── api/
│   └── routers/
│       └── test_orders.py            # HTTP status codes, contract bodies, auth per role
├── services/
│   └── test_orders.py                # business rules, authorization, commit/rollback effects
└── repositories/
    └── test_orders.py                # queries against the migrated PostgreSQL test database
```
Repository and API tests run against a real PostgreSQL test database migrated with `alembic upgrade head`, never SQLite (`{{slot:unit-testing}}`).
