# Backend rules (framework-agnostic)

Knowledge used to fill the backend branch (`be/` in the fullstack layout, or the flat layout for a BE-only project). Every rule must be expressed with the project's real paths and stack syntax. Mark a rule "not adopted" instead of inventing structure the project does not need.

| # | Topic | Rule | Goes into |
|---|---|---|---|
| B1 | Transactions / Unit of Work | The use case owns the transaction (`with uow:` + commit). Repositories never commit. One use case = one transaction boundary. | 08-runtime, 05 |
| B2 | Error flow | Domain/application raise framework-free errors (a base `DomainError` hierarchy). One global handler maps them to HTTP. Routers neither remap with try/except nor raise HTTP errors for business/permission rules. | 08-runtime, 05, 07 |
| B3 | Authorization placement | Permission/capability guards run in the application layer (or a shared dependency), never as `if role ==` in routers. FE visibility is UX only. | 08-runtime, 05 |
| B4 | External services via ports | LLM, payment, email, ERP, storage, queues are ports in application with adapters in infrastructure. Use cases never import SDKs or HTTP clients. | 02, 05, 08-runtime |
| B5 | No ORM leaks | Mappers turn ORM rows into entities/DTOs; ORM objects never cross into application/domain. | 02, 05, 07 |
| B6 | Workers / jobs / CLI | Background entrypoints are another presentation edge: they get use cases from the composition root and call them; no business SQL, no skipped guards. | 01, 02, 08-runtime |
| B7 | Module communication | A module reaches another only through its application API. Only the composition root wires adapters across modules. The shared kernel never imports modules. | 05 |
| B8 | Read side (CQRS-lite) | Heavy list/report reads may use a query port + query class returning DTOs directly; query classes never write. | 04, 08-runtime |
| B9 | Splitting big repositories | Split per aggregate (`repositories/<aggregate>_repository`), read SQL into `queries/`, one port per class, wired in the composition root. | 04 |
| B10 | Config, secrets, migrations | One settings object read in one place; no env/DB/network at import time. Migrations have one location and one owner. Secrets never logged. | 02, 08-runtime |
| B11 | Multi-tenancy / scope (optional) | Where tenant/environment/version context is resolved and how it is passed down; infrastructure never guesses a default scope. | 08-runtime, shared/integration-contract |
| B12 | Testing per layer | Domain: pure unit tests. Application: unit tests with fake ports. Infrastructure/presentation: integration tests on the real DB. Architecture tests as gate. Never mock authorization to pass. | 08-runtime |
| B13 | Thin entrypoint | The process entry only builds the app (`create_app()`); app assembly lives in the composition root. | 01, 02 |

## Stack notes

- Python/FastAPI: `Protocol` ports, `dataclass(frozen=True, slots=True)` entities, `Depends` providers, `pydantic-settings`, gates via `import-linter` or pytest AST tests.
- TypeScript/NestJS: abstract-class ports as DI tokens, module files as composition roots, exception filters as the global handler, `dependency-cruiser` gates.
- Other stacks: map each row to the closest idiom in `stacks/<stack>.md`.
