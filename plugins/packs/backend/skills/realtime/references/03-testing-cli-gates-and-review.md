# Testing Realtime Channels, CLI Gates & Code Review Rubric

> Topic: Mandatory test matrix for SSE and WebSocket channels, `httpx` SSE streaming tests, Starlette `TestClient` WebSocket tests, deterministic CLI `PASS`/`FAIL` verification gates, and `BLOCKER`/`MAJOR`/`MINOR` review rubric.

## 1. Mandatory Test Matrix for Every Realtime Channel

Every channel declared in `design.md` (`RT1`) must have automated integration tests covering these 8 scenarios:

| Scenario | SSE Assertion (`httpx.AsyncClient.stream`) | WebSocket Assertion (`TestClient.websocket_connect`) |
|---|---|---|
| **1. Missing or invalid credentials** | HTTP `401 Unauthorized` before first byte | `pytest.raises(WebSocketDisconnect)` with `code == 1008` before `accept()` |
| **2. Cross-tenant / unauthorized object (`RT3` anti-IDOR)** | HTTP `403` or `404` before first byte | Error frame or close `1008`; events for Tenant B **never** arrive on Tenant A's socket |
| **3. Ordered happy path (`RT2`)** | Exact `id:`, `event:`, and Pydantic-decoded `data:` in sequence | Exact Pydantic-validated outbound messages in sequence |
| **4. Gap-free resume (`RT7`)** | `Last-Event-ID: 2` replays only events with `id > 2` followed by live events | Re-subscribe with `last_event_id` replays only newer events |
| **5. Replay window overflow (`RT9`)** | Emits `event: resync` and closes stream cleanly | Emits `resync` frame or closes with `1013` / documented `4xxx` code |
| **6. Malformed / unknown inbound payload (`RT2`)** | `422 Unprocessable Entity` on invalid `Last-Event-ID` header | Returns structured `ErrorMessage(code="invalid_message")` without echoing raw input |
| **7. Oversized frame / rate limit exceeded (`RT9`)** | HTTP `429 Too Many Requests` when connection cap exceeded | Closes socket with `1009` (oversized) or `1008`/`1013` (rate/connection cap) |
| **8. Disconnect cleanup (`RT4`, `RT6`)** | `finally:` block unsubscribes queue from hub | `finally:` block unregisters socket from hub |

---

## 2. Testing SSE Streams with `httpx.AsyncClient`

Inject a finite scripted event feed via `app.dependency_overrides` so `httpx.ASGITransport` finishes cleanly inside `asyncio.timeout`:

```python
async def test_order_events_sse_resumes_after_last_event_id(
    async_client: AsyncClient,
    scripted_order_feed: ScriptedOrderFeed,
) -> None:
    scripted_order_feed.seed([
        make_order_event(id=1, status="created"),
        make_order_event(id=2, status="paid"),
        make_order_event(id=3, status="shipped"),
    ])

    async with asyncio.timeout(2.0):
        async with async_client.stream(
            "GET",
            "/api/v1/orders/events",
            headers={"Last-Event-ID": "2"},
        ) as response:
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream")
            raw_lines = [line async for line in response.aiter_lines()]

    events = parse_sse_frames(raw_lines)
    assert [e.id for e in events if e.id] == ["3"]
    payload = OrderEventOut.model_validate_json(events[-1].data)
    assert payload.status == "shipped"
```

---

## 3. Testing WebSockets with Starlette `TestClient`

Prove both handshake rejection (`1008`) and cross-tenant isolation (script a forbidden Tenant B event followed by an allowed Tenant A event, and assert that the first message received is Tenant A's event):

```python
def test_orders_websocket_rejects_missing_ticket(app: FastAPI) -> None:
    with TestClient(app) as client:
        with pytest.raises(WebSocketDisconnect) as exc_info:
            with client.websocket_connect("/api/v1/ws/orders"):
                pass
    assert exc_info.value.code == status.WS_1008_POLICY_VIOLATION


def test_orders_websocket_isolates_tenant_scope(
    app: FastAPI,
    scripted_hub: ScriptedOrderHub,
    issue_ticket: Callable[..., str],
) -> None:
    # Script Tenant B event first, then Tenant A event:
    scripted_hub.script_on_subscribe([
        make_order_event(order_id=ORDER_B, tenant_id=TENANT_B, status="cancelled"),
        make_order_event(order_id=ORDER_A, tenant_id=TENANT_A, status="released"),
    ])
    ticket_a = issue_ticket(user_id=USER_A, tenant_id=TENANT_A, channel="orders")

    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/ws/orders?ticket={ticket_a}") as ws:
            ws.send_text(
                SubscribeOrderMsg(type="subscribe", order_id=ORDER_A).model_dump_json()
            )
            frame = OutboundServerAdapter.validate_json(ws.receive_text())

    # Tenant B's event must never be delivered to Tenant A:
    assert frame.order_id == ORDER_A
    assert frame.status == "released"
```

---

## 4. Deterministic CLI Verification Gates (`PASS` / `FAIL`)

All automated checks report strictly **`PASS`** or **`FAIL`** (`shared_contracts/flags_and_statuses.md`; `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`):

| Gate | Command | `PASS` Criterion | `FAIL` Resolution |
|---|---|---|---|
| **G1 — Long-Lived DB Session Scan (`RT4`)** | `rg -n "websocket.*Depends\(get_session\)|EventSourceResponse[\s\S]{0,160}Depends\(get_session\)" app/ src/ -g "*.py"` | `0` matches | Replace `Depends(get_session)` with `session_factory` short sessions inside the feed/service (`RT4`) |
| **G2 — Unbounded Queue Scan (`RT6`)** | `rg -n "asyncio\.Queue\(\s*\)" app/ src/ -g "*.py"` | `0` matches | Pass explicit `maxsize=OUTBOX_MAX` to every `asyncio.Queue` (`RT6`) |
| **G3 — Unvalidated `receive_json()` Scan (`RT2`)** | `rg -n "\.receive_json\(\)" app/ src/ -g "*.py"` | `0` matches | Use `receive_text()`, check byte length (`1009`), and validate via Pydantic `TypeAdapter.validate_json()` (`RT2`) |
| **G4 — Raw SQL Interpolation in `NOTIFY` (`RT8`)** | `rg -n "NOTIFY\s+.*\{|f[\"'].*pg_notify" app/ src/ -g "*.py"` | `0` matches | Use parameterized `SELECT pg_notify(:channel, :payload)` |
| **G5 — Realtime Integration Test Suite** | `uv run pytest -q -k "sse or websocket or realtime"` | Exit `0` | Fix failing SSE/WebSocket auth, scope isolation, or replay tests |

---

## 5. Code Review Severity Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

Reviewer findings use the unified 3-tier scale from `shared_contracts/flags_and_statuses.md` (never use `P0`–`P3`):

| Severity | Realtime Finding Criteria |
|---|---|
| **`BLOCKER`** | • Missing pre-accept/pre-stream authentication, or missing per-subscription `(tenant_id, object_id)` authorization allowing cross-tenant event leakage (`RT3`).<br>• Injecting a request-scoped `Depends(get_session)` into a long-lived SSE or WebSocket route (`RT4` connection pool exhaustion).<br>• Accepting long-lived JWT access tokens in WebSocket/SSE URL query parameters instead of short-lived single-use tickets, or omitting `Origin` validation on cookie-authenticated WebSockets (`RT3`).<br>• Multi-worker deployment using an in-memory-only hub without PostgreSQL `LISTEN/NOTIFY` or Redis/broker fan-out (`RT8`).<br>• Serializing ORM models or raw unvalidated dicts onto SSE/WebSocket frames (`RT2`), or shipping fake timer-generated events (`RT10`). |
| **`MAJOR`** | • Unbounded `asyncio.Queue()` or sequential `for ws in sockets: await ws.send_text(...)` broadcast loop where one slow client stalls all peers (`RT6`).<br>• Using in-memory counters for SSE `id:` instead of durable DB sequence/outbox IDs, or subscribing to the live bus *after* the replay query (creating an event-loss window) (`RT7`).<br>• Missing frame size limit (`1009`), message rate limit, per-actor connection cap, or `replay_max` cap (`RT9`).<br>• Missing `try ... finally:` hub unregister/unsubscribe cleanup on disconnect, or swallowing exceptions with `except Exception: pass`.<br>• Channel omitted from `design.md` (`RT1`). |
| **`MINOR`** | • Using legacy `sse-starlette` in new code on FastAPI ≥ 0.135 instead of native `fastapi.sse`.<br>• Non-standard or undocumented application close code (`4xxx`) not listed in `design.md`.<br>• Redundant manual `Content-Type: text/event-stream` header on `EventSourceResponse`. |

See [`references/01-sse-and-websocket-patterns.md`](01-sse-and-websocket-patterns.md) for SSE/WebSocket patterns and [`references/02-fanout-scaling-and-security.md`](02-fanout-scaling-and-security.md) for fan-out and security architecture.
