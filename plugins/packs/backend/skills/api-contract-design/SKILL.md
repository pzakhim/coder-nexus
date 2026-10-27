---
name: api-contract-design
description: "Design, version, and verify FastAPI/Pydantic v2 HTTP & OpenAPI 3.1 contracts: route conventions, strict input/output DTOs, single error envelope, per-endpoint auth/RBAC/anti-IDOR scopes, bounded pagination, idempotency keys, additive-first compatibility, and committed OpenAPI snapshot diffing."
---

<!-- Generated from create-api-contract-design-skill@1.1.0 -->

# API Contract Design (FastAPI + Pydantic v2 + OpenAPI 3.1)

This skill governs every HTTP route, request/response DTO, authentication/authorization scope declaration, pagination contract, idempotency key flow, and OpenAPI 3.1 snapshot check in the Backend pack. It works alongside `backend-fastapi` (FastAPI runtime & DI), `backend-clean-architecture` (Presentation → Application → Domain boundaries), `backend-secure-coding-standards` (OWASP defense-in-depth), and `backend-realtime` (SSE / WebSocket event contracts).

---

## 1. Core Contract Invariants (`CT1`–`CT10`, Mandatory Compliance)

Every invariant below is **mandatory compliance** — never invent per-rule severity columns or mark any invariant as `"not adopted"`:

| ID | Invariant | FastAPI + Pydantic v2 Enforcement | Reference |
|---|---|---|---|
| `CT1` | **Contract Snapshot Is Reviewable Evidence** | Export `app.openapi()` deterministically to `contracts/openapi.json` and commit alongside route/schema changes. | [03-openapi-snapshot-diff-and-review.md](references/03-openapi-snapshot-diff-and-review.md) |
| `CT2` | **Separate Input and Output Schemas** | Distinct `<Resource>CreateRequest`, `<Resource>UpdateRequest` (`ConfigDict(extra="forbid")`), and `<Resource>Response` (`ConfigDict(from_attributes=True)`). Never expose SQLAlchemy models or `dict[str, Any]` on the wire. | [01-conventions-schemas-and-idempotency.md](references/01-conventions-schemas-and-idempotency.md) |
| `CT3` | **Single Structured Error Envelope** | Every `4xx`/`5xx` (including `RequestValidationError` `422` and `HTTPException`) returns `ErrorResponse` (`error.code`, `error.message`, `error.details`, `error.trace_id`). | [01-conventions-schemas-and-idempotency.md](references/01-conventions-schemas-and-idempotency.md) |
| `CT4` | **Explicit Status Codes & Response Contracts** | Every `@router.<method>` declares explicit `response_model=`, `status_code=`, and `responses={401: ..., 403: ..., 404: ..., 409: ..., 422: ...}`. | [01-conventions-schemas-and-idempotency.md](references/01-conventions-schemas-and-idempotency.md) |
| `CT5` | **Explicit Auth, RBAC Scopes & Anti-IDOR** | Declare `Security(require_scopes(...))` / `Depends(get_current_principal)` in route signatures so OpenAPI `security` is populated; scope every query by `principal.tenant_id` and return `404` on cross-tenant IDs. | [02-compatibility-and-versioning.md](references/02-compatibility-and-versioning.md) |
| `CT6` | **Bounded Pagination, Deterministic Sort & Allow-Listed Filters** | `Query(default=20, ge=1, le=100)`, `PaginatedResponse[T]`, `Literal`/`Enum` sort & filter fields, and unique tie-breaker sort (`ORDER BY created_at DESC, id DESC`). | [01-conventions-schemas-and-idempotency.md](references/01-conventions-schemas-and-idempotency.md) |
| `CT7` | **Additive Changes by Default; Breaking Changes Require `D-NN`** | Never remove/rename fields, tighten input bounds, or change types/status codes without an approved `D-NN` Decision Record in `design.md` and Expand-and-Contract plan. | [02-compatibility-and-versioning.md](references/02-compatibility-and-versioning.md) |
| `CT8` | **One-Version Rule & Explicit Deprecation** | Evolve `/api/v1/...` additively; mark retiring routes `deprecated=True` with `Deprecation` and `Sunset` headers before removal. | [02-compatibility-and-versioning.md](references/02-compatibility-and-versioning.md) |
| `CT9` | **Deterministic `operationId`s, Tags & Handshake** | Explicit `operation_id="<resource>_<action>"`, `tags=["<resource>"]`, and synchronized `api_contract.json` (`shared_contracts/api_handshake_protocol.md`). | [03-openapi-snapshot-diff-and-review.md](references/03-openapi-snapshot-diff-and-review.md) |
| `CT10` | **Idempotency & Safe Retries (`Idempotency-Key`)** | Non-idempotent `POST` mutations accept `Idempotency-Key: str = Header(...)`, persist `(key, request_hash, status_code, response_body)` atomically, replay matching retries, and return `409` on payload mismatch. | [01-conventions-schemas-and-idempotency.md](references/01-conventions-schemas-and-idempotency.md) |

---

## 2. Reference Routing Table

| Reference Guide | Topic & Coverage | Load When |
|---|---|---|
| [`references/01-conventions-schemas-and-idempotency.md`](references/01-conventions-schemas-and-idempotency.md) | Route naming, HTTP method & status code matrix (`CT4`), input/output Pydantic v2 DTO separation (`CT2`), single `ErrorResponse` envelope (`CT3`), bounded pagination (`CT6`), and atomic `Idempotency-Key` handling (`CT10`). | Designing or implementing FastAPI routes, Pydantic request/response schemas, pagination, error handlers, or idempotent mutations. |
| [`references/02-compatibility-and-versioning.md`](references/02-compatibility-and-versioning.md) | OpenAPI security declarations (`HTTPBearer` / `OAuth2PasswordBearer` / `Security` scopes), RBAC (`403`) vs. Anti-IDOR (`404` on cross-tenant access) (`CT5`), Additive vs. Breaking change table (`CT7`), the 4-step `D-NN` protocol, and One-Version deprecation (`CT8`). | Wiring route authentication/authorization, modifying existing endpoints or DTOs, or planning a deprecation/breaking change. |
| [`references/03-openapi-snapshot-diff-and-review.md`](references/03-openapi-snapshot-diff-and-review.md) | Exporting `contracts/openapi.json` (`CT1`), extracting `contracts/openapi.base.json`, diffing with `oasdiff` / `jq` / `diff -u`, authoring `contracts/contract-change.md`, updating `api_contract.json` (`CT9`), CLI `PASS`/`FAIL` gates, and `BLOCKER`/`MAJOR`/`MINOR` review rubric. | Exporting or diffing OpenAPI snapshots, syncing FE–BE contracts, running verification gates, or reviewing an API change. |
<!-- {{profile_references}} -->

---

## 3. Deterministic CLI Verification Gates (`PASS` / `FAIL`)

All automated contract gates report strictly **`PASS`** or **`FAIL`** (`shared_contracts/flags_and_statuses.md`; `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`):

| Gate | Command | Pass Criterion |
|---|---|---|
| **G1 — OpenAPI Snapshot Drift** | `uv run python scripts/export_openapi.py && git diff --exit-code contracts/openapi.json` | Exit `0` (`PASS`) — `contracts/openapi.json` matches live FastAPI app |
| **G2 — Raw Dict / Untyped Response Scan** | `rg -n "response_model\s*=\s*(dict|Any|None)" app/ src/ -g "*.py"` | `0` unapproved matches (`PASS`) — `204` uses `status_code=204, response_class=Response` |
| **G3 — Unbounded Limit Parameter Scan** | `rg -n "limit:\s*int\s*=\s*(Query\(\s*\)|[0-9]+)" app/ src/ -g "*router*.py" -g "*routes*.py"` | `0` matches without `le=` bound (`PASS`) |
| **G4 — Breaking Change Diff Gate** | `oasdiff breaking contracts/openapi.base.json contracts/openapi.json` (or `jq -S` diff in [Reference 03](references/03-openapi-snapshot-diff-and-review.md)) | Exit `0` (`PASS`), or every breaking item cites an approved `D-NN` in `design.md` |
| **G5 — Contract & Schema Pytest Suite** | `uv run pytest -q -k "contract or openapi"` | Exit `0` (`PASS`) |
