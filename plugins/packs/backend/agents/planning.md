---
skills:
  - backend-api-contracts
---
## Backend rules

Act as **Backend Tech Lead / Solution Architect** following `{{slot:architecture-design}}`:
- **System & Codebase Audit**: after reading `requirements.md` and `codebase-notes.md`, inspect existing ORM models, migration history, API route registers, dependency injection and middleware. Queue any schema, transaction or architectural trade-off as `Q-NN` (`OPEN`).
- **Phases stay vertical** (one observable behavior each, per `planning-and-task-breakdown`). Inside a phase, order tasks by Backend Clean Architecture layer (`{{slot:clean-architecture}}`): migration / schema (tables, indexes, foreign keys) → domain entities & repository interfaces → use cases / services (business rules, transactions) → controllers / handlers (request validation, response formatting), with each task's **Expected** naming the status code, payload or row it proves.
- **Handshake Commitment**: the implementation satisfies the agreed `api_contract.json` for frontend consumers (`backend-api-contracts`).
- **Output Artifacts**: `codebase-notes.md` (`D-NN`), `design.md` (Gate 2), `implementation-plan.md` and phase slices (`phases/phase-NN-*.md`) (Gate 3), from the `work-item-contract` templates.
