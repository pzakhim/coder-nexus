---
name: architecture-design
description: Backend Gate 2/Gate 3 design — service codebase audit (ORM models, migrations, routes, DI, middleware), straight-line design.md and Clean Architecture layer slicing (Migration, Domain, Use Cases, Controllers).
---

# Backend Architecture Design

Used by `planning` acting as **Backend Tech Lead / Solution Architect**. Layer rules: `{{slot:clean-architecture}}`; contracts: `backend-api-contracts`.

## 1. System & Codebase Audit (with `grilling`)

- Read `requirements.md` and `codebase-notes.md` (`D-NN`, Glossary, Verified Baseline Facts) first, then inspect existing ORM models, migration history, API route registers, dependency injection, and middleware.
- Queue any schema, transaction, or architectural trade-off as `Q-NN` (`OPEN`) in `codebase-notes.md`, ask the user 1 question at a time, and close confirmed choices into `D-NN` (`Owner: planning`).
- For a real choice between viable approaches, present 2-3 technical options with trade-offs via `solution-options`, recommended first.
- Record a decision only when two independently built parts (two phases, a handler and a repository, this service and its consumers) could otherwise choose incompatibly, and the answer is not obvious from existing code. Reason: obvious decisions bloat `design.md` and still need review.

## 2. Straight-Line `design.md` (Gate 2)

- Write `design.md` in one straight locked-in line citing `D-NN` (never writing `Option A / Option B` or `Open Questions`).
- Optional `###` subsections, only when they apply, inside the existing sections (never new `##` sections, never a renamed heading):

| Subsection | Inside section | Content |
|---|---|---|
| Deferred decisions | `## Architectural decision` | Choices this version's goals do not need: decision, why it can wait, revisit trigger. An unknown that blocks an AC is resolved before Gate 2, never deferred |
| Complexity justifications | `## Architectural decision` | One row per deviation from the established layers, ORM patterns or shared components; the cited `D-NN` records **Violation**, **Why needed**, **Simpler alternative rejected because** |
| Risk → Mitigation | `## Integration, errors, and risks` | Risk, affected AC / G, mitigation or check, owning `PHASE-NN` |
| Migration plan and rollback | `## Integration, errors, and risks` | When tables, columns, indexes or stored formats change: expand → migrate → contract steps, effect on running consumers and existing rows, lock and volume concerns, rollback and its check |

- Before Gate 2: run `validate_proposal_spec`, then `gate-review` with `modes/design.md`, then `cold-reader-check` on `design.md`. Minor questions are Planning's call and marked as such; user's-call questions become `Q-NN`, asked one at a time and closed into `D-NN`. Present Gate 2 only with 0 `OPEN` `Q-NN`.

## 3. Layered Slicing (Gate 3)

Inside each vertical phase, order tasks according to Backend Clean Architecture:
1. Migration / Schema changes (tables, indexes, foreign keys).
2. Domain Entities & Repository Interfaces.
3. Use Cases / Services (Core business rules, transactions).
4. Presentation / Controllers / Handlers (HTTP/gRPC request validation & response formatting).

A schema or contract change that running consumers use follows expand → migrate → contract across phases, as in `planning-and-task-breakdown`.

## 4. Handshake Commitment

Ensure the implementation satisfies the agreed `api_contract.json` for frontend consumers.
