---
name: architecture-design
description: Backend Gate 2 architecture design for Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async / Alembic / PostgreSQL services - guides the 7-anchor read-only codebase scan, Socratic grilling and D-NN decision locking in codebase-notes.md, the straight-line backend design.md (API contract, data model, Pass/Fail/Empty test data per endpoint, migrations, realtime channels, risks), and PHASE-00 readiness. Use when Planning acts as Backend Tech Lead / Solution Architect for a backend work item.
---

# Architecture Design — Backend (Python / FastAPI)

Used by `planning` acting as **Backend Tech Lead / Solution Architect**. Core process and statuses come from [work-item-contract](../work-item-contract/SKILL.md), [gate-review](../gate-review/SKILL.md), and [implementation-planning](../implementation-planning/SKILL.md); layer rules from `{{slot:clean-architecture}}`; FastAPI idioms from [fastapi](../fastapi/SKILL.md); API contracts from [api-contract-design](../api-contract-design/SKILL.md); migrations from [database-migrations](../database-migrations/SKILL.md); PostgreSQL patterns from [postgres](../postgres/SKILL.md); event streams from [realtime](../realtime/SKILL.md).

## 1. Pre-Design & Gate 2 Verification Gates (`PASS` / `FAIL`)

| Gate | Command / Tool | Pass Criteria |
|---|---|---|
| **Developer Toolset Check** | `coder-nexus setup tools --pack backend --check` | `PASS` (`TOOLS: READY`) |
| **Read-Only Codebase Scan** | `rg -n` across `pyproject.toml`, `app/`, `alembic/`, `tests/` | `PASS` (all facts recorded in `codebase-notes.md` §3 with real paths) |
| **Alembic Head Check** | `uv run alembic heads` | `PASS` (single migration head; >1 head is `BLOCKED`) |
| **Proposal Spec Validator** | `validate_proposal_spec` on `codebase-notes.md` & `design.md` | `PASS` (`valid: true`, 0 `OPEN` `Q-NN`) |

`NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`.

## 2. Input Contract & 7-Anchor Read-Only Scan

Before drafting `design.md`, verify `requirements.md` and `codebase-notes.md` are approved at Gate 1 (`G-NN`, `BR-NN`, `AC-NN`, `D-NN` locked), then run the 7-anchor read-only scan ([01 — Codebase Scan & Decisions](references/01-codebase-scan-and-decisions.md)):

```text
Backend Root
├── pyproject.toml + lock file        ──> 1. Python/FastAPI/Pydantic/SQLAlchemy/Alembic versions, runner prefix, ruff/mypy/pytest config
├── app/main.py (create_app)          ──> 2. Lifespan, included routers, global exception handlers, middleware
├── app/api/ (routers, deps)          ──> 3. URL prefixes, auth dependency, session/UoW injection, error mapping
├── app/core/settings.py, .env.example──> 4. Settings field names (never secret values), DATABASE_URI, provider keys
├── app/models, app/repositories      ──> 5. Tables, tenant/owner scope columns, relationships, query patterns
├── alembic/ (env.py, versions)       ──> 6. Current head, naming convention, migration style
└── tests/ + conftest.py              ──> 7. Test database strategy, fixtures, ASGITransport/TestClient, auth helpers
```

## 3. Mandatory Architecture Design Rules (`AD1`–`AD10`)

| ID | Rule | Reference |
|---|---|---|
| **AD1** | **Verified facts only:** Every path, class, table, or command in `design.md` must come from `codebase-notes.md` §3; unverified names fail `gate-review` (`BLOCKER`). | [01 — Codebase Scan & Decisions](references/01-codebase-scan-and-decisions.md) |
| **AD2** | **Scope classification (`INIT` / `EXTEND` / `CORE IMPACT`):** Classify the work item upfront; `EXTEND` preserves existing module conventions (`C11`). | [01 — Codebase Scan & Decisions](references/01-codebase-scan-and-decisions.md) |
| **AD3** | **High-leverage `D-NN` decisions only:** Record a `Q-NN` → `D-NN` only when two independently built parts could choose incompatibly and existing code does not settle it. | [01 — Codebase Scan & Decisions](references/01-codebase-scan-and-decisions.md) |
| **AD4** | **One straight locked-in line:** Render `design.md` only after all pre-design `Q-NN` items are closed into `D-NN` (zero `Option A / Option B`, `TBD`, or open questions). | [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) |
| **AD5** | **Complete API & Data contract:** Specify path, method, auth guard, request/response schemas, error codes, and SQLAlchemy 2.x schema/constraints per endpoint. | [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) |
| **AD6** | **Adversarial test data per endpoint:** Agree with the user on **Pass/Default (`200/201`)**, **Fail (`400/401/403/404/409/422`)**, and **Empty (`[]`)** rows before Gate 2. | [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) |
| **AD7** | **3rd-Party Mockoon isolation:** External providers use sandbox (`3RD_PARTY_READY`) or `mocks/<provider>_mockoon.json` (`3RD_PARTY_MOCKOON`); `app/` implements only the real `httpx.AsyncClient`. | [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) |
| **AD8** | **Safe expand-migrate-contract migrations:** Breaking column/table/enum changes follow expand → backfill → contract with explicit rollback steps. | [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) |
| **AD9** | **`PHASE-00` readiness baseline:** Verify tools, baseline lint/tests, isolated test DB migrations, seed accounts, and 3rd-party sandbox/Mockoon before `PHASE-01`. | [03 — PHASE-00, Gates & Template](references/03-phase00-gates-and-template.md) |
| **AD10** | **Validator + Cold-Reader Gate 2 check:** Pass `validate_proposal_spec`, `gate-review` (`modes/design.md`), and `cold-reader-check` before requesting user Gate 2 approval. | [03 — PHASE-00, Gates & Template](references/03-phase00-gates-and-template.md) |

## 4. Reference Guides

| Guide | Topic |
|---|---|
| [01 — Codebase Scan & Decisions](references/01-codebase-scan-and-decisions.md) | Read-only 7-anchor Backend scan commands, `INIT`/`EXTEND`/`CORE IMPACT` classification, and `Q-NN` → `D-NN` decision rules |
| [02 — Design Sections & Test Data](references/02-design-sections-and-test-data.md) | Validated `design.md` sections, optional `###` subsections, and the Pass/Fail/Empty Endpoint Test Data table |
| [03 — PHASE-00, Gates & Template](references/03-phase00-gates-and-template.md) | Backend `PHASE-00` readiness checklist, Gate 2/3 ordering, and the copy-ready `design.md` template |
