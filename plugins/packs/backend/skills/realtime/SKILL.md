---
name: realtime
description: "Design, implement, scale, secure, and test real-time server-to-client channels in Python + FastAPI + PostgreSQL: transport selection (Polling vs. SSE vs. WebSockets), native FastAPI SSE (`fastapi.sse` `EventSourceResponse` & `ServerSentEvent` with `Last-Event-ID` durable replay), WebSocket endpoints (pre-accept auth, close codes, Pydantic v2 discriminated unions, single-sender `TaskGroup`), short DB session lifecycle, multi-worker fan-out via PostgreSQL `LISTEN/NOTIFY` or Redis, anti-IDOR scope isolation, and deterministic CLI/review gates."
---

# Backend Realtime (FastAPI + PostgreSQL)

This skill governs real-time server push channels in the Backend pack. It works alongside `{{slot:clean-architecture}}` (layer boundaries), `backend-api-contract-design` (HTTP/DTO contracts & `api_contract.json`), `{{slot:secure-coding-standards}}` (OWASP security controls), and `{{slot:unit-testing}}` (async/sync test harnesses).

---

## 1. Choose the Simplest Transport First (Gate 2 `D-NN`)

Pick the simplest transport that satisfies the latency and directionality requirement, and record the choice as a `D-NN` Decision Record in `design.md`:

| Requirement | Transport Choice | Rationale |
|---|---|---|
| Delay of 10–60 s is acceptable, or updates are infrequent | **HTTP Polling** (`GET` with `ETag` / `If-None-Match` or `updated_after` cursor) | Stateless, works through every proxy/CDN, covered by standard OpenAPI contracts and HTTP tests. |
| **Server → Client only**: live notifications, status boards, job progress, AI token streams | **SSE (`fastapi.sse`, FastAPI ≥ 0.135)** | Standard HTTP: reuses FastAPI dependencies/middleware, built-in `: ping` keep-alive, automatic `Last-Event-ID` resume, and appears in `contracts/openapi.json`. |
| **Bidirectional (`Client ↔ Server`) at high frequency**: live chat, collaborative editing, operator control, presence | **WebSocket (`@router.websocket`)** | Single persistent connection carries low-latency client-to-server frames without HTTP request overhead per message. |
| One-off result of a slow background task | **`202 Accepted` + Polling or SSE progress** | Opening a stateful bidirectional WebSocket for a single completion signal adds security and scaling complexity with zero benefit. |

---

## 2. Mandatory Channel Invariants (`RT1`–`RT10`, Mandatory Compliance)

Every invariant below is **mandatory compliance** — never invent per-rule severity columns or mark any invariant as `"not adopted"`:

| ID | Invariant | Enforcement Summary | Reference |
|---|---|---|---|
| `RT1` | **Explicit Channel Contract in `design.md`** | Document every SSE/WebSocket channel in `design.md` using [`templates/realtime-channels.md.tpl`](templates/realtime-channels.md.tpl) (path, transport, auth, tenant scope, Pydantic models, replay rules, close codes, limits). | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT2` | **Strict Pydantic v2 Message Schemas** | Validate inbound WebSocket messages via a single discriminated union `TypeAdapter` (`ConfigDict(extra="forbid")`); serialize outbound SSE/WS payloads from explicit `*Out` / `*Event` Pydantic models (never ORM entities or raw `dict`). | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT3` | **Authenticate Before Streaming/`accept()` & Authorize Every Scope** | Authenticate before the first SSE byte or before `websocket.accept()`; authorize every subscription/action in the service layer per `(tenant_id, object_id)` (anti-IDOR). | [02-fanout-scaling-and-security.md](references/02-fanout-scaling-and-security.md) |
| `RT4` | **Never Hold a DB Session Across a Long-Lived Connection** | Never inject a `yield`-based `Depends(get_session)` into a long-lived stream/socket; open short `async with session_factory() as session:` blocks per query/replay so idle clients never exhaust the PostgreSQL pool. | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT5` | **Non-Blocking `async def` Handlers Only** | All stream generators and socket loops are `async def`; offload any unavoidable CPU/sync work via `anyio.to_thread.run_sync`. | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT6` | **Bounded Per-Connection Queues & Single Socket Writer** | Every connection uses `asyncio.Queue(maxsize=N)` with an explicit `QueueFull` policy (`event: resync` or close `1013`), and exactly one `send_loop` task writes to each WebSocket. | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT7` | **Durable Ordered Event IDs & Gap-Free Replay** | Resumable streams use durable database sequence/outbox IDs (never in-memory counters); subscribe to the live bus **before** running the replay query and filter `event.id > high_water`. | [01-sse-and-websocket-patterns.md](references/01-sse-and-websocket-patterns.md) |
| `RT8` | **Multi-Worker Fan-Out via Shared Pub/Sub** | In-memory hubs are valid only for single-process deployments (`D-NN`); multi-worker/multi-pod deployments must fan out via PostgreSQL `LISTEN/NOTIFY` or Redis/broker. | [02-fanout-scaling-and-security.md](references/02-fanout-scaling-and-security.md) |
| `RT9` | **Explicit Frame Size, Rate, Connection & Replay Limits** | Enforce `--ws-max-size`, per-connection message rate limits, per-actor connection caps, and `replay_max` bounds (`OWASP API4`). | [02-fanout-scaling-and-security.md](references/02-fanout-scaling-and-security.md) |
| `RT10` | **No Fake Timer/Mock Streams in Production Code** | If the real event source is not built yet, mark the channel `BLOCKED` or out of scope — never ship a timer that fabricates demo events. | [03-testing-cli-gates-and-review.md](references/03-testing-cli-gates-and-review.md) |

---

## 3. Clean Architecture Layer Placement

| Layer | Responsibility |
|---|---|
| **Presentation (`api/routers/`)** | `@router.get(..., response_class=EventSourceResponse)` or `@router.websocket(...)`, handshake auth dependency, `TypeAdapter` frame parsing, mapping domain errors to WS close codes / SSE terminal events. |
| **Application (`application/services/`)** | Per-subscription and per-action authorization (`ensure_visible`), business command execution, emitting domain events after transaction commit. |
| **Infrastructure (`infrastructure/realtime/`)** | Scoped connection hub (`(tenant_id, topic)` → bounded queues), PostgreSQL `LISTEN/NOTIFY` (`asyncpg`) or Redis subscriber, outbox/replay repository queries. |

---

## 4. Reference Routing Table

| Reference / Template | Topic & Coverage | Load When |
|---|---|---|
| [`references/01-sse-and-websocket-patterns.md`](references/01-sse-and-websocket-patterns.md) | Native FastAPI SSE (`EventSourceResponse`, `ServerSentEvent`), gap-free `Last-Event-ID` replay (`RT7`), short DB sessions (`RT4`), WebSocket handshake auth, close codes (`1000`–`4999`), discriminated union `TypeAdapter` (`RT2`), and single-sender `asyncio.TaskGroup` (`RT6`). | Implementing or refactoring an SSE stream or WebSocket endpoint. |
| [`references/02-fanout-scaling-and-security.md`](references/02-fanout-scaling-and-security.md) | Single-process vs. multi-worker fan-out (`RT8`), PostgreSQL `LISTEN/NOTIFY` with `asyncpg` & transactional `pg_notify`, single-use short-lived tickets (`<= 60s`), `Origin` CSWSH checks, `(tenant_id, object_id)` anti-IDOR hub isolation (`RT3`), and resource caps (`RT9`). | Designing multi-worker fan-out, wiring `LISTEN/NOTIFY` or Redis, or hardening realtime auth and rate limits. |
| [`references/03-testing-cli-gates-and-review.md`](references/03-testing-cli-gates-and-review.md) | Mandatory channel test matrix, `httpx` SSE streaming tests, Starlette `TestClient` WebSocket tests, deterministic CLI `PASS`/`FAIL` gates, and `BLOCKER`/`MAJOR`/`MINOR` review rubric. | Writing realtime integration tests, running CLI verification gates, or reviewing a realtime PR. |
| [`templates/realtime-channels.md.tpl`](templates/realtime-channels.md.tpl) | Standard `design.md` specification template for `CH-NN` channels. | Authoring or updating `design.md` (Gate 2) for any realtime feature. |
<!-- {{profile_references}} -->

---

## 5. Deterministic CLI Verification Gates (`PASS` / `FAIL`)

All automated checks report strictly **`PASS`** or **`FAIL`** (`shared_contracts/flags_and_statuses.md`; `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`):

| Gate | Command | Pass Criterion |
|---|---|---|
| **G1 — Long-Lived DB Session Leak Scan (`RT4`)** | `rg -n "websocket.*Depends\(get_session\)|EventSourceResponse[\s\S]{0,160}Depends\(get_session\)" app/ src/ -g "*.py"` | `0` matches (`PASS`) — streams/sockets use `session_factory` per unit of work |
| **G2 — Unbounded Queue Scan (`RT6`)** | `rg -n "asyncio\.Queue\(\s*\)" app/ src/ -g "*.py"` | `0` matches (`PASS`) — every `asyncio.Queue` sets `maxsize=` |
| **G3 — Unvalidated `receive_json()` Scan (`RT2`)** | `rg -n "\.receive_json\(\)" app/ src/ -g "*.py"` | `0` matches (`PASS`) — use `receive_text()` + size check + `TypeAdapter.validate_json()` |
| **G4 — Realtime Integration Test Suite** | `uv run pytest -q -k "sse or websocket or realtime"` | Exit `0` (`PASS`) |
