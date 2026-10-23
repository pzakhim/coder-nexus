# Sources

Ideas were rewritten in this pack's vocabulary (`D-NN`, `AC-NN`, RT rules, SC rules, `BLOCKED` / `NOT_RUN`); nothing is vendored. Links are pinned to a commit or are official documentation pages read on 2026-10-23. Stars as of 2026-10.

| Source | Stars | Idea taken | Where used |
|---|---|---|---|
| [fastapi/fastapi `fastapi/.agents/skills/fastapi/references/streaming.md`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/.agents/skills/fastapi/references/streaming.md) | 104k | `response_class=EventSourceResponse` + `yield` with a declared item type; `ServerSentEvent` for `event`/`id`/`retry`/`comment`; `raw_data` for preformatted text; prefer the decorator form over returning a streaming response | [sse](sse.md) §2 |
| [fastapi/fastapi `fastapi/sse.py`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/sse.py) and [`fastapi/routing.py`](https://github.com/fastapi/fastapi/blob/69ddc2badf9da1123bba4d360225ae6b085985f6/fastapi/routing.py) (0.161.1) | 104k | Keep-alive `: ping` every 15 s; buffer of one between generator and socket (backpressure); `ServerSentEvent` items skip item-type validation and are not documented in OpenAPI; `yield` dependencies stay open until the response finishes | [sse](sse.md) §1, §4; SKILL RT1, RT4 |
| [FastAPI tutorial: Server-Sent Events](https://fastapi.tiangolo.com/tutorial/server-sent-events/) (read 2026-10-23) | — | Added in 0.135; `Last-Event-ID` read as a header parameter; SSE over `POST`; built-in `Cache-Control: no-cache` and `X-Accel-Buffering: no` | [sse](sse.md) §1, §3, §6 |
| [FastAPI reference: SSE](https://fastapi.tiangolo.com/reference/sse/) (read 2026-10-23) | — | Field rules: `data` vs `raw_data` mutually exclusive, single-line `event`/`id`, `retry` in ms, comments for proxies | [sse](sse.md) §2 |
| [FastAPI advanced: WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) (read 2026-10-23) | — | Dependencies, `Query`/`Cookie` in WebSocket routes; `WebSocketException(code=WS_1008_POLICY_VIOLATION)` instead of `HTTPException`; `WebSocketDisconnect` cleanup; in-memory manager valid for one process only | [websockets](websockets.md) §1, §4; [fan-out](fanout-and-scaling.md) §1 |
| [FastAPI advanced: Testing WebSockets](https://fastapi.tiangolo.com/advanced/testing-websockets/) (read 2026-10-23) | — | `TestClient.websocket_connect` as a context manager | [testing](testing.md) §3 |
| [Starlette: WebSockets](https://starlette.dev/websockets/) (read 2026-10-23) | — | `accept(subprotocol=...)`; closing before `accept()` refuses the handshake with 403; `iter_*` stop on disconnect; use `send`/`receive` wrappers to keep state | [websockets](websockets.md) §1 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Broadcast loop that awaits each connection in turn | FastAPI WebSockets docs `ConnectionManager` | One slow or dead socket stalls or aborts the broadcast; replaced by bounded per-connection queues and one sender per socket (RT6) |
| Plain item yields as the default SSE shape | FastAPI SSE tutorial | Fine for finite streams; streams that must survive reconnects need durable ids, so they yield `ServerSentEvent` (RT7) |
| Sync `def` generators for SSE | FastAPI SSE tutorial | Supported, but a long-lived stream would hold a threadpool thread and cannot stop on disconnect (RT5) |
| `encode/broadcaster` as the default multi-process answer | FastAPI WebSockets docs | Adds a dependency; PostgreSQL `LISTEN`/`NOTIFY` is already available in this stack. Allowed only as a recorded `D-NN` after a maintenance check |
| `sse-starlette` | Pre-0.135 practice | Native `fastapi.sse` covers it; existing usage is migrated only in a planned task |
| Testing keep-alive by patching `fastapi.sse._PING_INTERVAL` | `fastapi/sse.py` comment | Private attribute that tests framework behavior, not ours |
| AsyncAPI documents for channels | Common practice | No tooling assumed in the workspace; the `design.md` channel table carries the same facts and is reviewed at Gate 2 |
