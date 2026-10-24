# 02 — Dependency rules and how to check them

The direction is `main → api → services → repositories → models`, with `schemas` used by `api` and `services` only, and `core` / `db` depended on by everyone and depending on nothing above them. The table with reasons is in [../SKILL.md](../SKILL.md).

## 1. Why each boundary exists

| Boundary | Failure it prevents |
|---|---|
| Routers never import repositories or models | A handler with its own query bypasses the service's authorization and data-scope check; the next endpoint copies it |
| Services never import FastAPI | A worker or CLI command cannot call the use case; tests need a fake request; `HTTPException` codes drift from the contract |
| Repositories never import schemas | A response change forces a query change; repositories start shaping API output |
| Models never import schemas or Pydantic | A response change turns into a migration; circular imports between tables and schemas |
| Schemas never import ORM classes | The contract silently follows the table (a new column appears in responses) |
| Core imports nothing from `app` | Import cycles at startup; settings that depend on business code |

## 2. Enforce with import-linter (default via `setup tools`)

`import-linter` is installed by default via `coder-nexus setup tools --pack backend`. Keep these contracts in `pyproject.toml` and run `lint-imports` (with the workspace prefix, for example `uv run lint-imports`; cwd: backend root) to verify layer boundaries automatically.

```toml
[tool.importlinter]
root_package = "app"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Layers: api above services above repositories above models"
type = "layers"
layers = ["app.main", "app.api", "app.services", "app.repositories", "app.models"]

[[tool.importlinter.contracts]]
name = "Services are framework-free"
type = "forbidden"
source_modules = ["app.services", "app.repositories", "app.models", "app.schemas", "app.core"]
forbidden_modules = ["fastapi", "starlette"]

[[tool.importlinter.contracts]]
name = "Storage does not know the API contract"
type = "forbidden"
source_modules = ["app.repositories", "app.models"]
forbidden_modules = ["app.schemas", "pydantic"]

[[tool.importlinter.contracts]]
name = "Schemas are plain data (enums excepted)"
type = "forbidden"
source_modules = ["app.schemas"]
forbidden_modules = ["app.models", "sqlalchemy"]
ignore_imports = ["app.schemas.* -> app.models.enums"]

[[tool.importlinter.contracts]]
name = "Core depends on nothing in app"
type = "forbidden"
source_modules = ["app.core"]
forbidden_modules = ["app.api", "app.services", "app.repositories", "app.models", "app.schemas", "app.db"]
```

`Expected`: `Contracts: N kept, 0 broken.` A broken contract names the importing line; fix the import, never the contract (weakening a check is not allowed, `{{slot:unit-testing}}` / `{{slot:root-cause-debugging}}`).

## 3. Fallback check without import-linter

Run from the backend root; each command must print nothing.

```bash
rg -n "^\s*(from|import) (fastapi|starlette)" app/services app/repositories app/models app/schemas app/core
rg -n "^\s*from app\.(repositories|models)(\.| )" app/api/routers
rg -n "^\s*from app\.schemas" app/repositories app/models
rg -n "^\s*from app\.models(\.| )" app/schemas | rg -v "app\.models\.enums"
rg -n "^\s*from app\.(api|services|repositories|models|schemas|db)" app/core
```

Record the command and its empty output as the evidence row for an architecture check (`evidence-standard`). A hit outside the task's scope is legacy debt: report it in Concerns, do not fix it in this task (`{{slot:clean-code}}` C10).

## 4. Allowed shortcuts (and the ones that are not)

| Situation | Allowed? | Rule |
|---|---|---|
| A read-only list endpoint with no business rule | Router still calls a service method | The service is where authorization and data scope live; a missing check is invisible in a router-only path |
| A service needs another resource's data | Call that resource's **repository** from this service, or its service method when a rule applies | Never import another service's private helpers; never let the router stitch two services together |
| Two services need the same rule | Move it into the service that owns the concept; the other calls it | No `utils.py` / `helpers.py` (`{{slot:clean-code}}` C16) |
| A background job or CLI command | Builds the session and services itself and calls the same service method | Jobs are another entry edge, like routers; no business SQL in jobs |
| Raw SQL for a heavy report | Inside a repository, as `text()` with bound parameters, returning plain rows mapped by the service | Never string-formatted SQL (`{{slot:secure-coding-standards}}`) |
