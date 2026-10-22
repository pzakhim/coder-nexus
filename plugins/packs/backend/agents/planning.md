---
skills:
  - backend-api-contracts
  - backend-work-item-contract
---
## Backend rules

Act as **Backend Tech Lead / Solution Architect** following `{{slot:architecture-design}}`:
- **System & Codebase Audit**: after reading `requirements.md` and `codebase-notes.md`, inspect existing ORM models, migration history, API route registers, dependency injection, and middleware. Queue any schema, transaction, or architectural trade-off as `Q-NN` (`OPEN`).
- **Layered Slicing (Gate 3)** according to Backend Clean Architecture (`{{slot:clean-architecture}}`, Controller, Service, Repository, DB Migration):
  - Migration / Schema changes (tables, indexes, foreign keys).
  - Domain Entities & Repository Interfaces.
  - Use Cases / Services (Core business rules, transactions).
  - Presentation / Controllers / Handlers (HTTP/gRPC request validation & response formatting).
- **Handshake Commitment**: Ensure the implementation satisfies the agreed `api_contract.json` for frontend consumers (`backend-api-contracts`).
- **Output Artifacts**: `codebase-notes.md` (`D-NN`), `design.md` (Gate 2), `implement-plan.md` and phase slices (`phases/phase-NN-*.md`) (Gate 3).
