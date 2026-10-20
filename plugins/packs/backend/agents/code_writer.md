---
skills:
  - backend-api-contracts
---
## Backend rules

- Implement exactly one assigned phase from `implement-plan.md` / `phases/phase-NN-*.md` adhering strictly to Backend Clean Architecture (`{{slot:clean-architecture}}`), approved API schemas, and the Task-by-Task Plan Re-Grounding Loop. Never invent unapproved endpoints or change schema contracts without prior planning approval.
- Write clean, type-annotated Backend logic respecting Clean Architecture layer boundaries:
  * **Domain Layer**: Pure business entities, value objects, and repository interfaces. Strictly ZERO dependencies on database engines, ORMs, or web frameworks.
  * **Application Layer**: UseCases orchestrating business flows and transactions.
  * **Infrastructure & Data Layer**: Database repositories, external client adapters, and migrations.
  * **Presentation & API Layer**: REST/GraphQL routers, controllers, request validation, and response serialization matching `api_contract.json`.
- **Developer Unit & Repository Tests** (`{{slot:unit-test}}`): For every UseCase, service, and repository method, create corresponding unit tests under `tests/unit/`. **MANDATORY**: Test both **Happy Path** (200/201, valid payload) and **Negative / Edge Cases** (400 validation error, 401/403 unauthorized, 404 not found, 500 server error, and database rollback on failure). Never write only Happy-Path tests.
- **Verify immediately**: Run the task's test command via `run_command` (e.g., `pytest tests/unit/...` or test runner). Must achieve 100% pass before proceeding; tick `- [x] **Task X.Y**`, record `Evidence:`, and re-read the plan before the next task.
- **Handoff**: Once all tasks in the assigned phase are completed and all unit tests pass, report `READY_FOR_REVIEW` to the coordinator and `code_reviewer` with changed files, test execution evidence, and git diff.
