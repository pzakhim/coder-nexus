# Sources

Ideas rewritten in this repo's vocabulary (core `clean-code` CC rules, `D-NN`, tasks and evidence rows). Nothing is copied. Stars as of 2026-10.

Internal base inputs (read-only): the previous `plugins/packs/backend/skills/clean-architecture/SKILL.md` (Domain / UseCases / Infrastructure / Presentation layers) and `src/skill_factory/library/generators/create-clean-architecture-skill/` (`references/backend-rules.md` B1-B13, `stacks/python-fastapi.md`).

| Source (pinned link or doc URL, date read) | Stars | Idea taken | Where used |
|---|---|---|---|
| [wshobson/agents `plugins/api-scaffolding/skills/fastapi-templates/SKILL.md`](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/api-scaffolding/skills/fastapi-templates/SKILL.md) (2026-10-23) | 42k | Layered `app/` tree (api, core, models, schemas, services, repositories); async SQLAlchemy + asyncpg; `dependency_overrides` for the session in API tests; `httpx.ASGITransport` client | [../SKILL.md](../SKILL.md) Layout, [01](01_folder_layout.md), [03](03_di_sessions_transactions.md) §6 |
| [fastapi/fastapi official skill `SKILL.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/SKILL.md) and [`references/dependencies.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/dependencies.md) (2026-10-23) | 104k | `Annotated` aliases, function dependencies building services, router-level prefix/tags | [03](03_di_sessions_transactions.md) §2, [templates/feature/router.py.tpl](../templates/feature/router.py.tpl), [templates/core/deps.py.tpl](../templates/core/deps.py.tpl) |
| https://fastapi.tiangolo.com/tutorial/bigger-applications/ (2026-10-23) | - | One router module per resource exposing `router`, imported as the module to avoid name clashes; `[tool.fastapi] entrypoint` | [01](01_folder_layout.md) §2, [templates/core/main.py.tpl](../templates/core/main.py.tpl) |
| https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ (2026-10-23) | - | `yield` session with cleanup; re-raise, never swallow; exit code runs after the response, so the commit belongs in the service | [03](03_di_sessions_transactions.md) §1, §3 |
| https://fastapi.tiangolo.com/advanced/settings/ (2026-10-23) | - | `BaseSettings` + `lru_cache` `get_settings()`, no global instance, override in tests | [04](04_settings_and_startup.md) §1, [templates/core/settings.py.tpl](../templates/core/settings.py.tpl) |
| https://fastapi.tiangolo.com/advanced/events/ (2026-10-23) | - | `lifespan` owns startup/shutdown; `on_event` is ignored when `lifespan` is set | [04](04_settings_and_startup.md) §2 |
| https://docs.pydantic.dev/latest/concepts/pydantic_settings/ (redirects to pydantic.dev, 2026-10-23) | - | Required fields fail at instantiation; source priority; `extra` default `forbid`; DSN types | [04](04_settings_and_startup.md) §1 |
| https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html (2026-10-23) | - | One `AsyncSession` per task; `async_sessionmaker(expire_on_commit=False)`; no implicit IO (`selectinload`, `lazy="raise"`); `engine.dispose()` at shutdown | [03](03_di_sessions_transactions.md) §1, §5, [templates/core/session.py.tpl](../templates/core/session.py.tpl) |
| skill-factory `create-clean-architecture-skill` `backend-rules.md` (internal) | - | B1 service owns the transaction, repositories never commit; B2 framework-free errors + one handler; B3 authorization in services; B9 split repositories per aggregate; B10 one settings object, no I/O at import; B13 thin entrypoint | [../SKILL.md](../SKILL.md) A3, A6, A7; [05](05_adding_and_splitting.md) §2 |
| skill-factory `stacks/python-fastapi.md` (internal) | - | import-linter contracts; pitfalls (logic in routes, ORM objects returned, sessions opened in use cases, model import cycles) | [02](02_dependency_rules.md) §2, [templates/feature/model.py.tpl](../templates/feature/model.py.tpl) (`TYPE_CHECKING` import) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Separate pure domain layer (dataclass entities + `Protocol` repository ports + mappers) for every feature | previous backend skill, generator `full` level, `rules/backend_clean_architecture_rules.md` | One implementation per port is a pass-through layer (`{{slot:clean-code}}` C1); business rules live in services, tables in models, contract in schemas. A `Protocol` is added when a second implementation exists (A10) |
| Feature-first `modules/<feature>/{api,application,domain,infrastructure}` as the default | generator `stacks/python-fastapi.md` | The approved layout is layered by role; a workspace that already uses feature folders keeps them ([05](05_adding_and_splitting.md) §3) |
| `api/v1/endpoints/` nesting by default | wshobson fastapi-templates | Versioning is a contract decision ([api-contract-design](../../api-contract-design/SKILL.md)); add a version prefix only when the design requires it |
| SQLite in-memory test database and `metadata.create_all` in fixtures | wshobson fastapi-templates | PostgreSQL types, constraints and locking differ; tests run on a migrated PostgreSQL test database |
| Commit inside the `yield` session dependency after the handler | common tutorials | Exit code runs after the response is sent; a failed commit would follow a success response |
| SQLModel shared table/API classes | official FastAPI skill | Approved decision: SQLAlchemy 2 async + separate Pydantic schemas ([fastapi](../../fastapi/SKILL.md) overrides O1) |
| Asyncer for blocking calls | official FastAPI skill | `anyio.to_thread.run_sync` is already installed; new dependency needs a `D-NN` |
