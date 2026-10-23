---
skills:
  - backend-api-contracts
---
## Backend rules

- Build the assigned phase against Backend Clean Architecture (`{{slot:clean-architecture}}`) and the approved API schemas in `design.md` / `api_contract.json` (`backend-api-contracts`). An endpoint, schema or table the plan does not name is a `plan-change-request`, never an improvisation.
- Respect layer boundaries:
  * **Domain**: entities, value objects, repository interfaces; zero dependencies on database engines, ORMs or web frameworks.
  * **Application**: use cases orchestrating business flows and transactions.
  * **Infrastructure & Data**: repositories, external client adapters, migrations.
  * **Presentation & API**: routers/controllers, request validation, response serialization matching `api_contract.json`.
- **Developer tests** (`{{slot:unit-test}}`, `test-first`): for every use case, service and repository method, cover the happy path (200/201) and the negative paths the design names: 400 validation, 401/403 authorization, 404 not found, server error, and rollback of a multi-table write on failure.
- **`PHASE-00` for a backend item**: there is no mock-server step. `[EXECUTE]` items are the preparation tasks the plan lists (for example a migration applied to a disposable database, seed data, a provider sandbox key confirmed present); a frontend consumer's Mockoon file is never written here. External providers are stubbed only when a `D-NN` says so, and a stubbed run is labelled as such.
- Task checks and phase checks use the commands from `{{slot:verification}}` (for example a targeted `pytest` path); record them as evidence rows, not as an `Evidence:` note.
