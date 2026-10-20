---
name: architecture-design
description: Backend Gate 2/Gate 3 design — service codebase audit (ORM models, migrations, routes, DI, middleware), straight-line design.md and Clean Architecture layer slicing (Migration, Domain, Use Cases, Controllers).
---

# Backend Architecture Design

Used by `planning` acting as **Backend Tech Lead / Solution Architect**. Layer rules: `{{slot:clean-architecture}}`; contracts: `backend-api-contracts`.

## 1. System & Codebase Audit (with `grill-me`)

- Read `requirements.md` and `codebase-notes.md` (`D-NN`, Glossary, Verified Baseline Facts) first, then inspect existing ORM models, migration history, API route registers, dependency injection, and middleware.
- Queue any schema, transaction, or architectural trade-off as `Q-NN` (`OPEN`) in `codebase-notes.md`, ask the user 1 question at a time, and close confirmed choices into `D-NN` (`Owner: planning`).

## 2. Straight-Line `design.md` (Gate 2)

- Write `design.md` in one straight locked-in line citing `D-NN` (never writing `Option A / Option B` or `Open Questions`).

## 3. Layered Slicing (Gate 3)

Slice tasks according to Backend Clean Architecture, in this order:
1. Migration / Schema changes (tables, indexes, foreign keys).
2. Domain Entities & Repository Interfaces.
3. Use Cases / Services (Core business rules, transactions).
4. Presentation / Controllers / Handlers (HTTP/gRPC request validation & response formatting).

## 4. Handshake Commitment

Ensure the implementation satisfies the agreed `api_contract.json` for frontend consumers.
