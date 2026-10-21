# Preset: Python / FastAPI

> A starting point, not a final answer. Always tailor to the project and confirm with the user.

## Detect

`pyproject.toml` / `requirements*.txt` containing `fastapi`. Check for `sqlalchemy`/`sqlmodel`, `alembic`, `pydantic-settings`.

## Framework-enforced conventions

Very few. FastAPI only needs an app instance and routers (`APIRouter`). DI is `Depends`. Everything else is our choice.

## Concept mapping

| Concept | In this stack |
|---|---|
| Presentation | `APIRouter` endpoints + Pydantic request/response schemas |
| Use case | Plain class or function in `application/` |
| Domain entity | `dataclass` (keep Pydantic/ORM out of domain at `full`) |
| Repository interface | `typing.Protocol` or `abc.ABC` in `domain/` |
| Repository implementation | SQLAlchemy-based class in `infrastructure/` |
| Input validation | Pydantic models in `api/schemas.py` |
| DI / composition root | `Depends` providers in each module's `dependencies.py`; app assembly in `main.py` |
| Config | `pydantic-settings` `Settings` in `core/config.py` |

## Standard tree (feature-first)

```
src/<app_name>/
  main.py                    # create FastAPI app, include module routers
  core/                      # config, db session, security, logging (technical shared)
  shared/                    # base errors, common types used by ≥ 3 modules
  modules/
    orders/
      api/
        router.py            # endpoints only: parse → call use case → map response
        schemas.py           # Pydantic request/response models
      application/
        create_order.py      # one use case per file
      domain/
        entities.py
        repository.py        # Protocol
        errors.py
      infrastructure/
        models.py            # ORM models
        repository.py        # SQLAlchemy implementation
      dependencies.py        # Depends wiring for this module
      __init__.py            # public API
tests/
  unit/modules/orders/
  integration/
alembic/
```

## Lite / full variations

- **lite:** `app/main.py`, `app/routers/`, `app/services/`, `app/models/`, `app/schemas/` — no interfaces.
- **full:** domain entities are pure dataclasses with behavior; explicit mappers between ORM models and entities; domain events.

## Naming

| Kind | Pattern |
|---|---|
| Module / file | `snake_case.py` |
| Use case | `verb_noun.py` → `class CreateOrder` |
| Schema | `CreateOrderRequest`, `OrderResponse` |

## Enforcing import rules

`import-linter` (`pyproject.toml`):
```toml
[tool.importlinter]
root_package = "app_name"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Domain stays pure"
type = "forbidden"
source_modules = ["app_name.modules.orders.domain"]
forbidden_modules = ["fastapi", "sqlalchemy", "app_name.modules.orders.infrastructure", "app_name.modules.orders.api"]
```
Add one contract per module, or use a `layers` contract with `containers`.

## Stack-specific pitfalls

- Business logic inside route functions.
- Returning ORM objects directly from endpoints.
- Opening DB sessions inside use cases instead of injecting them.
- Circular imports between modules' `models.py` (ORM relationships) — use string references.

## Reference sources

Verify current versions during research; candidates: FastAPI official "Bigger Applications" docs, `zhanymkanov/fastapi-best-practices` on GitHub.
