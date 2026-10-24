---
name: architecture-design
description: Backend Gate 2 design for a Python FastAPI + SQLAlchemy 2 async + PostgreSQL service - the read-only codebase scan (pyproject, app factory and lifespan, routers, dependencies, settings, models, repositories, Alembic, tests), the backend design.md (API contract per endpoint with schemas, errors and auth, data model with migration and rollback, realtime channels, risks), the Pass/Default/Fail/Empty test data per endpoint, PHASE-00 readiness for the database, seed data and test accounts, and the layer order of tasks at Gate 3. Use when Planning acts as Backend Tech Lead / Solution Architect for a backend work item.
---

# Backend Architecture Design

Used by `planning` acting as **Backend Tech Lead / Solution Architect**. Process, statuses and formats come from core ([delivery-workflow](../delivery-workflow/SKILL.md), [work-item-contract](../work-item-contract/SKILL.md), [gate-review](../gate-review/SKILL.md), [implementation-planning](../implementation-planning/SKILL.md)); this skill adds the backend content. Layout and layer rules: `{{slot:clean-architecture}}`. FastAPI usage: [fastapi](../fastapi/SKILL.md). Contracts: [api-contract-design](../api-contract-design/SKILL.md). Schema changes: [database-migrations](../database-migrations/SKILL.md). Database access and the Postgres MCP: [postgres](../postgres/SKILL.md). Streams: [realtime](../realtime/SKILL.md).

## 1. Input contract

Before drafting `design.md`:

1. `requirements.md` and `codebase-notes.md` are approved at Gate 1 (or `brief.md` for phase-free items), with `G-NN`, `BR-NN`, `AC-NN` and `D-NN` locked.
2. Who calls the API is known: the frontend client, another service, a worker. Their required fields and error handling are in `requirements.md`, not guessed here.

## 2. Codebase scan and decisions (with `grilling`)

Scan the backend read-only before naming any file, class, table or command. Recipe, commands and what to record: [references/01_backend_codebase_scan.md](references/01_backend_codebase_scan.md).

```text
Backend root
├── pyproject.toml + lock file   ──> 1. Python version, FastAPI / Pydantic / SQLAlchemy / Alembic versions, package manager, ruff/mypy/pytest config
├── app/main.py (create_app)     ──> 2. Lifespan, included routers, error handlers, middleware
├── app/api/ (routers, deps)     ──> 3. URL prefixes, auth dependency, service builders, error mapping
├── app/core/settings.py, .env.example ──> 4. Settings fields, DATABASE_URI, provider keys (names only)
├── app/models, app/repositories ──> 5. Tables, scope columns, relationships, query patterns
├── alembic/ (env.py, versions)  ──> 6. Current head, naming convention, migration style
└── tests/ + conftest.py         ──> 7. Test database, fixtures, factories, auth helpers
```

Then decide, exactly as core prescribes:

- Every verified fact goes to `codebase-notes.md` → `## 3. Verified Baseline Facts` with its path. An unverified name in `design.md` is a `gate-review` finding.
- A schema, transaction, contract or layering trade-off becomes a `Q-NN` (`OPEN`) in `codebase-notes.md`, asked one at a time; a real choice between approaches goes through `solution-options` (2-3 options, recommended first); the user's answer closes into `D-NN` (`Owner: planning`).
- Record a decision only when two independently built parts (two phases, a service and a repository, this API and the frontend client) could otherwise choose incompatibly, and the answer is not obvious from existing code. Reason: obvious decisions bloat `design.md` and still need review.
- Backend divergence points that always need a `D-NN` when new: error body and error codes, pagination shape, id type, timestamp format and time zone, auth scheme and roles, data-scope column, enum values stored in the database.

## 3. `design.md` (Gate 2)

Render [templates/design.md.tpl](templates/design.md.tpl) only after every pre-design `Q-NN` is closed. One straight locked-in line citing `D-NN`: no alternative-option headings, no open-question or assumption sections, no unresolved markers.

The template keeps the headings `validate_proposal_spec` checks; backend content goes inside them:

| Validated section | Backend content | Detail |
|---|---|---|
| Header + `Scope classification` | `INIT` (new resource/router), `EXTEND` (existing resource) or `CORE IMPACT` (settings, session, auth, error handling, shared tables) | [02](references/02_design_sections.md) §1 |
| `## Goal alignment` | Each `G-NN` → endpoints, tables, channels that deliver it | [02](references/02_design_sections.md) §2 |
| `## Architectural decision` | Confirmed approach with `D-NN`; `### Deferred decisions`, `### Complexity justifications` when they apply | [02](references/02_design_sections.md) §3 |
| `## Module and folder diff` | Current and proposed files per layer (`app/api/routers/...`, `app/services/...`) | [02](references/02_design_sections.md) §4 |
| `## Behavior, data, and state` | `### API contract` (per endpoint: path, auth, request, responses, errors), `### Data model`, `### Test data per endpoint`, business rules → service methods | [02](references/02_design_sections.md) §5, [03](references/03_endpoint_test_data.md) |
| `## UI design system` | Fixed text: not applicable to a backend service (kept because the validator requires the section) | [02](references/02_design_sections.md) §6 |
| `## Integration, errors, and risks` | Error mapping, transactions, providers, `### Realtime channels`, `### Risk → Mitigation`, `### Migration plan and rollback` | [02](references/02_design_sections.md) §7 |
| `## Verification strategy` | Real commands (ruff, mypy, pytest, alembic) with cwd, test levels, live-integration checks kept separate from fixtures | [02](references/02_design_sections.md) §8 |
| `## Gate 2 approval` | Unchanged from core | - |

Optional `###` subsections (only when they apply, never as new `##` sections, never renaming a heading):

| Subsection | Inside section | Content |
|---|---|---|
| Deferred decisions | `## Architectural decision` | Choices this version's goals do not need: decision, why it can wait, revisit trigger. An unknown that blocks an AC is resolved before Gate 2, never deferred |
| Complexity justifications | `## Architectural decision` | One row per deviation from the established layers, ORM patterns or shared components; the cited `D-NN` records **Violation**, **Why needed**, **Simpler alternative rejected because** |
| Realtime channels | `## Integration, errors, and risks` | Only when the work item streams events (SSE or WebSocket) |
| Risk → Mitigation | `## Integration, errors, and risks` | Risk, affected AC / G, mitigation or check, owning `PHASE-NN` |
| Migration plan and rollback | `## Integration, errors, and risks` | When tables, columns, indexes, enums or stored formats change: expand → migrate → contract, effect on running consumers and existing rows, locks and volume, downgrade and its check |

## 4. Test data per endpoint

Every endpoint gets Pass/Default, Fail and (for lists) Empty rows agreed with the user before Gate 2: actor and role, input, seeded precondition, expected status, body or error code, and persisted effect. The same table feeds the seed task in `PHASE-00`, the developer tests (`{{slot:unit-testing}}`), acceptance cases (`quality-acceptance`) and the frontend client's handshake. Format and rules: [references/03_endpoint_test_data.md](references/03_endpoint_test_data.md).

## 5. Gate 2 review

1. Validate `codebase-notes.md` and `design.md` with `validate_proposal_spec`.
2. Run `gate-review` with `modes/design.md` (it starts from the validator result), then `cold-reader-check` on `design.md`.
3. Fix findings you own; minor questions are Planning's call and marked as such; user's-call questions become `Q-NN`, asked one at a time and closed into `D-NN`. Present Gate 2 only with 0 `OPEN` `Q-NN`.

## 6. Gate 3: phases and task order

- Phases stay vertical (one observable behavior each, `implementation-planning`); the first behavior after `PHASE-00` is the riskiest.
- Inside a phase, tasks follow the layer order of `{{slot:clean-architecture}}`: model → migration → repository → schemas → service → router + wiring, each with a test, each **Expected** naming the status code, body, row or test name it proves.
- A schema or contract change that running consumers use follows expand → migrate → contract across phases.
- Task checks are real invocations with cwd, detected from the workspace (prefix `uv run` / `poetry run` / venv): `ruff check .`, `mypy app`, `pytest tests/services/test_orders.py -q`, `alembic upgrade head`.
- `PHASE-00` prepares the database, migrations, seed data, test accounts, and provider sandboxes or Mockoon mocks: [references/04_phase00_backend.md](references/04_phase00_backend.md).

## 7. Handshake commitment

The implementation satisfies the API contract recorded in `design.md` and agreed with the frontend client ([api-contract-design](../api-contract-design/SKILL.md), plugin-root `shared_contracts/api_handshake_protocol.md`). Fixture or contract checks never prove live integration; live ACs stay `NOT_RUN` or `BLOCKED` until exercised against the running service.

## Sources

[references/sources.md](references/sources.md)
