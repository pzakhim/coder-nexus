---
name: realtime
description: How a Python + FastAPI + PostgreSQL service pushes data to the frontend client in real time - choosing polling, Server-Sent Events or WebSockets; native FastAPI SSE (fastapi.sse EventSourceResponse and ServerSentEvent with yield, durable event ids, retry, Last-Event-ID resume, keep-alive, disconnect, short database sessions, backpressure); WebSocket endpoints (auth at connect, close codes, heartbeat, per-connection state, one sender per connection, broadcast through PostgreSQL LISTEN/NOTIFY or another pub/sub when there is more than one process); Pydantic message schemas; documenting channels in design.md; realtime security (authorization per message, rate and size limits); and how to test both. Use when a requirement says live updates, push, notifications, progress, streaming, chat, presence or "without refresh", when Planning designs a channel, when the Code Writer touches an EventSourceResponse or @router.websocket path, and when the Code Reviewer reviews one.
---

# Backend Realtime (FastAPI)

An extra skill of the backend pack. It adds stack knowledge only: the process (gates, tasks, unit testing, review, evidence) stays in the core skills linked below. Layer placement comes from `{{slot:clean-architecture}}`; schemas and errors from [api-contract-design](../api-contract-design/SKILL.md); security rules from `{{slot:secure-coding-standards}}`.

Detail: [SSE](references/sse.md) · [WebSockets](references/websockets.md) · [fan-out and scaling](references/fanout-and-scaling.md) · [security](references/security.md) · [testing](references/testing.md) · [sources](references/sources.md). The `design.md` section: [templates/realtime-channels.md.tpl](templates/realtime-channels.md.tpl).

## 1. Choose the transport first (Planning, before Gate 2)

Pick the simplest transport that meets the requirement; the choice is a `D-NN` with its reason.

| Need | Choose | Reason |
|---|---|---|
| Data changes rarely, or a delay of 10–60 s is acceptable | **Polling** a normal `GET` (with `ETag` / `If-None-Match` or an `updated_after` cursor) | No long-lived connection, works through every proxy, already covered by the OpenAPI contract and normal tests |
| Server → client only: notifications, progress, feeds, token streams | **SSE** (`fastapi.sse`, FastAPI ≥ 0.135) | Plain HTTP: same auth dependencies, same middleware, automatic reconnect with `Last-Event-ID`, appears in `openapi.json` |
| Both directions at high frequency: chat, collaborative editing, presence, live control | **WebSocket** | One connection carries client → server messages without a request per message |
| A one-off result of a slow job | `202 Accepted` + status endpoint (polling) or SSE progress | A socket for a single answer adds state with no benefit |

Ask the user (`Q-NN`) when the requirement does not state the acceptable delay or who sends messages. Never pick WebSocket "for future flexibility": every extra direction is extra auth, rate-limit and test surface.

## 2. Rules for every channel

| # | Rule | Reason |
|---|---|---|
| RT1 | Every channel is documented in `design.md` with the [channel template](templates/realtime-channels.md.tpl): path, transport, auth, scope, message types with their Pydantic models, ids and resume, close codes, limits | WebSocket messages never appear in `openapi.json`, and SSE payloads sent through `ServerSentEvent` appear only as a generic event; the design is the contract the frontend client and the reviewer check |
| RT2 | Every message is a named Pydantic model; inbound WebSocket messages are one discriminated union validated with a `TypeAdapter`; outbound payloads are built from response models, never from ORM objects or raw dicts | Validation at the boundary (SC1) and no accidental field leaks (SC6) |
| RT3 | Authenticate before streaming or `accept()`, through the workspace's auth dependency; authorize every subscription and every inbound action in the service layer, per object and data scope | A socket accepted without auth holds resources for anyone; a check only at connect lets a user act on objects of another scope later (SC2, SC3) |
| RT4 | Never hold a request-scoped database session for the life of a stream or socket; open a short `async with session_factory() as session:` per unit of work | A `yield` dependency stays open until the stream or socket ends, so each idle client pins one pool connection and the pool runs dry |
| RT5 | Long-lived handlers are `async def`; blocking calls go through the async driver or `anyio.to_thread.run_sync` | A sync generator or blocking call holds a worker thread (default limit 40) until it returns, and cannot be stopped on disconnect |
| RT6 | Every per-connection buffer is bounded and has a stated overflow policy (drop and ask the client to resync, or close with a code) | An unbounded queue behind a slow client grows until the process runs out of memory |
| RT7 | Events that a client must not miss carry a durable, ordered id (a database sequence or outbox id), and resume replays from the database | An in-memory counter restarts at 1 after a deploy and the client silently skips or repeats events |
| RT8 | In-memory connection registries are valid for one process only; more than one process or instance needs a pub/sub decided in `design.md` | `uvicorn --workers 4` or two pods each see a quarter of the clients; broadcasts silently miss the rest |
| RT9 | Limits are explicit: max message size, messages per second per connection, connections per user, idle timeout | Unbounded realtime endpoints are an easy resource-exhaustion target (OWASP API4) |
| RT10 | No fake events: a channel whose source is not built yet is `BLOCKED` or out of scope, never fed by a timer that invents data | A fake source passes the demo and hides that the real integration does not exist (core "no fake fallbacks") |

## 3. Code placement

| Layer | Owns |
|---|---|
| Router (`api/`) | `@router.get(..., response_class=EventSourceResponse)` or `@router.websocket(...)`; auth dependency; parsing messages into models; mapping domain errors to close codes or error events |
| Service | Authorization per subscription and per action; the business effect of an inbound message; publishing a domain event after the commit |
| Realtime adapter (`app/api/realtime.py` or `app/core/realtime.py`) | Connection registry, pub/sub listener (LISTEN/NOTIFY, Redis), per-connection queues |
| Repository | Replay queries (`WHERE id > :last_id AND <scope> ORDER BY id LIMIT :n`) |

Reason: the router stays thin and the same service rules apply to HTTP, SSE and WebSocket callers.

## 4. Planning and tasks

- Split a realtime feature into vertical phases like any other behavior (`implementation-planning`): first the event source and its replay query, then the channel endpoint, then fan-out across processes if needed.
- Task checks use real commands with cwd, detected from the workspace (`uv run`, `poetry run` or the active virtualenv): `pytest tests/integration/test_order_events.py -q`, `ruff check app/api/realtime`, `mypy app`.
- **Expected** names the observable result: event names and ids received, the close code for a refused connection, the resume starting after the given id.

## 5. Review focus (Code Reviewer adds to the core rubric)

- RT1–RT10 above, then the [security checklist](references/security.md#review-checklist).
- A broadcast that awaits each socket in turn, `receive_text()` without size or rate limits, `except Exception: pass` around the loop, a missing `WebSocketDisconnect` cleanup: each is a finding with a failure scenario.

## Related skills

[unit-testing](../unit-testing/SKILL.md) · [incremental-implementation](../incremental-implementation/SKILL.md) · [root-cause-debugging](../root-cause-debugging/SKILL.md) · [evidence-standard](../evidence-standard/SKILL.md) · [review-workflow](../review-workflow/SKILL.md) · [secure-coding-standards](../secure-coding-standards/SKILL.md).
