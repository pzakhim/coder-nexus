# 02 — Backend `design.md` Sections and Endpoint Test Data

> Topic: Validated design.md sections, optional subsections, 3rd-party Mockoon isolation, and Pass/Fail/Empty test data per endpoint (`AD4`–`AD8`)

Render `design.md` only after every pre-design `Q-NN` in `codebase-notes.md` is closed into `D-NN`. Write in **one straight locked-in line** citing `D-NN` (`AD4`): zero `Option A / Option B` headings, zero open questions, and zero `TBD` markers.

## 1. Validated `design.md` Sections (`validate_proposal_spec`)

Keep the exact `##` headings required by `validate_proposal_spec`:

| Section Heading | Required Backend Content |
|---|---|
| Header + `Scope classification` | `INIT` (new resource/module), `EXTEND` (existing resource), or `CORE IMPACT` (settings, session, auth, error handling, shared tables) |
| `## Architecture profile` | `mode`, `core_source`, `evidence` paths from `codebase-notes.md`, and selection rationale |
| `## Goal alignment` | Table mapping each `G-NN` from `requirements.md` → delivering endpoints, models, and handlers → owning `PHASE-NN` |
| `## Architectural decision` | Confirmed technical approach citing `D-NN` in `codebase-notes.md` |
| `## Module and folder diff` | Current verified paths, proposed files per layer (`app/api/routers/...`, `app/schemas/...`, `app/services/...`, `app/models/...`, `app/repositories/...`, `alembic/versions/...`), and affected shared consumers |
| `## Behavior, data, and state` | `### API contract` (method, path, auth dependency, request/response schemas, status/error codes), `### Data model` (SQLAlchemy 2.x tables, PK/FK, indexes, unique/check constraints, scope columns), and `### Test data per endpoint` (Section 3 below) |
| `## UI design system` | Fixed non-applicability text required by validator: `Not applicable. This is a backend service providing REST/OpenAPI APIs and realtime event streams.` |
| `## Integration, errors, and risks` | Uniform error envelope & domain error mapping, transaction boundaries (`async with session.begin():` / `UnitOfWork`), outbound providers (`3RD_PARTY_READY` vs `3RD_PARTY_MOCKOON`), plus optional `###` subsections (Section 2 below) |
| `## Verification strategy` | Runnable CLI commands with `cwd` (`ruff check`, `ruff format --check`, `mypy`, `pytest tests/unit`, `pytest tests/integration`, `alembic upgrade head`), keeping fixture/contract checks distinct from live integration checks |
| `## Gate 2 approval` | Decision summary, approved user response reference, and approved document revision |

---

## 2. Optional `###` Subsections (Include Only When Applicable; Delete Otherwise)

Add these **only** as `###` subsections inside the designated `##` section (never add new `##` headings or rename validated headings):

| `###` Subsection | Parent `##` Section | When to Include & Required Content |
|---|---|---|
| `### Deferred decisions` | `## Architectural decision` | Choices this version's goals do not need: `Decision deferred`, `Why it can wait`, `Revisit trigger`. Never defer an unknown that blocks an AC of the current version. |
| `### Complexity justifications` | `## Architectural decision` | One row per deviation from established layers, ORM patterns, or shared components; cites `D-NN` with `Violation`, `Why needed`, and `Simpler alternative rejected because`. |
| `### Realtime channels` | `## Integration, errors, and risks` | Only when streaming events via SSE or WebSocket (`realtime` skill): channel path, auth, event schema, heartbeats, and backpressure/replay policy. |
| `### Risk → Mitigation` | `## Integration, errors, and risks` | Known technical/operational risks threatening an AC or goal: `Risk`, `Affects (AC / G)`, `Mitigation / check`, `Owning PHASE-NN`. |
| `### Migration plan and rollback` | `## Integration, errors, and risks` | Whenever tables, columns, indexes, enums, or stored formats change (`AD8`): expand → migrate/backfill → contract steps, lock/volume impact (`postgresql_concurrently`), compatibility with running consumers, and verified `downgrade()` / rollback procedure. |

---

## 3. Test Data per Endpoint (`AD6`) & 3rd-Party Mockoon Strategy (`AD7`)

Every endpoint in `design.md` must specify deterministic **Pass / Default**, **Fail**, and (for list/search endpoints) **Empty** scenarios agreed with the user before Gate 2:

1. **Pass / Default (`200` / `201` / `204`):** Nominal valid request with authenticated actor and seeded precondition.
2. **Fail — Validation (`400` / `422`):** Missing required fields, invalid types, boundary violations, or domain rule breaches.
3. **Fail — Auth & Scope (`401` / `403` / `404`):** Unauthenticated caller (`401`), insufficient role/capability (`403`), or foreign-owner / cross-tenant IDOR attempt (`403` / `404`).
4. **Fail — Conflict / State (`404` / `409`):** Missing target resource (`404`) or duplicate key / invalid state transition (`409`).
5. **Empty (`200 OK` with `[]`):** List or filter query matching 0 rows (returns `200` with empty collection, never `404`).

```markdown
### Test data per endpoint

| Endpoint | Scenario | Role / Actor | Precondition | Input Payload / Query | Expected Status | Expected Body / Code |
|---|---|---|---|---|---|---|
| `POST /api/v1/orders` | Pass nominal | `buyer` | User balance >= 100, `item_1` stock >= 1 | `{"item_id": "item_1", "qty": 1}` | `201 Created` | `{"id": "...", "status": "pending"}` |
| `POST /api/v1/orders` | Fail out of stock | `buyer` | `item_2` stock == 0 | `{"item_id": "item_2", "qty": 1}` | `400 Bad Request` | `{"error": {"code": "ERR_ORDER_OUT_OF_STOCK"}}` |
| `POST /api/v1/orders` | Fail unauthenticated | `guest` | No bearer token | `{"item_id": "item_1", "qty": 1}` | `401 Unauthorized` | `{"error": {"code": "ERR_AUTH_REQUIRED"}}` |
| `GET /api/v1/orders/{id}` | Fail foreign owner | `buyer_b` | Order owned by `buyer_a` | `GET /api/v1/orders/ord_1` | `404 Not Found` | `{"error": {"code": "ERR_ORDER_NOT_FOUND"}}` |
| `GET /api/v1/orders` | Empty list | `buyer` | User has 0 orders | `page=1&limit=20` | `200 OK` | `{"items": [], "total": 0}` |
```

- **Outbound 3rd-Party Providers (`AD7`):** When the service calls an external API (ERP, payment, LLM), record either `3RD_PARTY_READY` (real sandbox credentials in `.env`) or `3RD_PARTY_MOCKOON` (a **Mockoon 3rd-Party Trigger & Test Data Table** mapped to `mocks/<provider>_mockoon.json` in `PHASE-00`). In both modes, `app/` implements only the real `httpx.AsyncClient` reading base URLs from `Settings`—never create fake in-memory provider classes in `app/`.
