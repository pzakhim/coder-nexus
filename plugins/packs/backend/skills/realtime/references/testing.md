# Testing realtime channels

Detail for [realtime](../SKILL.md). Test fixtures, auth overrides and loop rules follow [unit-testing](../../unit-testing/SKILL.md). This page lists what a channel's tests must prove and the realtime-specific techniques.

## 1. Cases every channel needs

Derived from the channel's row in `design.md` (RT1), each with a decisive assertion:

| Case | SSE assertion | WebSocket assertion |
|---|---|---|
| No or invalid credentials | 401 before any event | `WebSocketDisconnect` with code `1008` on connect |
| Object outside the actor's scope | 403/404 before any event | Error message or `1008`; no event of that object ever arrives |
| Happy path | Exact `event:`, `id:` and decoded `data:` per scripted event, in order | Exact message models in order |
| Resume | Request with `Last-Event-ID: 2` yields only ids > 2 | Reconnect with the last id (if the channel supports it) |
| Resume too old | One `event: resync`, then the stream ends | Documented resync message or close code |
| Invalid inbound message | n/a | `error` message with the documented code, connection stays open (or the documented close) |
| Oversized / too many messages | n/a | `1009` / rate-limit close code |
| Source ends or authorization revoked | Stream ends with the documented event | Documented close code |

## 2. SSE through httpx

```python
async def test_order_events_resume_after_last_id(client, feed_with_events):
    feed_with_events([event(1), event(2), event(3)])           # fake source that ENDS after these
    async with asyncio.timeout(2):
        async with client.stream("GET", "/orders/events", headers={"Last-Event-ID": "2"}) as response:
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream")
            lines = [line async for line in response.aiter_lines()]

    events = parse_sse(lines)                                   # small helper in tests/support/
    assert [e.id for e in events if e.id] == ["3"]
    assert OrderEventOut.model_validate_json(events[-1].data).status == "shipped"
```

- The fake source must end: `httpx.ASGITransport` collects the body before returning, so an endless stream never returns. Inject the source through `app.dependency_overrides` on the feed dependency.
- `parse_sse` splits on blank lines and reads `id:`, `event:`, `data:`, ignoring `:` comment lines. Assert ids and event names exactly; decode `data` with the payload model, so a contract change fails the test.
- Keep-alive is FastAPI's behavior, not ours: do not test the ping. If a channel adds its own comment lines, test those only.
- To see real streaming behaviour (proxy buffering, disconnect cleanup), use the Test Runner's run against a started service ([quality-acceptance](../../quality-acceptance/SKILL.md)), for example `curl -N -H "Accept: text/event-stream" <base-url>/orders/events`, not a unit test.

## 3. WebSockets through TestClient

```python
def test_orders_socket_refuses_missing_ticket():
    with TestClient(app) as client:
        with pytest.raises(WebSocketDisconnect) as refused:
            with client.websocket_connect("/ws/orders"):
                pass
    assert refused.value.code == status.WS_1008_POLICY_VIOLATION


def test_orders_socket_delivers_only_own_scope(fake_hub, ticket_for):
    # the fake hub replays this script, in order, once the subscription is registered
    fake_hub.script([order_event(ORDER_B, scope=TENANT_B),      # must NOT arrive
                     order_event(ORDER_A, scope=TENANT_A)])
    with TestClient(app) as client, client.websocket_connect(f"/ws/orders?ticket={ticket_for(USER_A)}") as ws:
        ws.send_text(Subscribe(type="subscribe", order_id=ORDER_A).model_dump_json())
        message = ServerMessageAdapter.validate_json(ws.receive_text())
    assert message.order_id == ORDER_A
```

- `TestClient` tests are sync `def` tests and run the app on their own loop: provide services and the hub through overrides (fakes), as the [unit-testing](../../unit-testing/SKILL.md) reference says. Test the hub, the listener and the services with the async fixtures separately.
- `with TestClient(app) as client:` runs the lifespan; use it when the hub or listener starts there.
- `receive_text()` blocks forever when nothing is sent: design the test so the expected message is the next one, and assert "never arrives" by scripting the forbidden event first and checking that the next received message is the allowed one.
- Script fake events before connecting instead of publishing from the test body: the test thread is not the app's loop, and `asyncio.Queue` is not thread-safe.

## 4. Commands and evidence

Run with the workspace's runner and cwd (detected from `pyproject.toml` / `uv.lock` / `poetry.lock`), for example `uv run pytest tests/integration/test_order_events.py -q` (cwd: service root). Evidence rows follow [evidence-standard](../../evidence-standard/SKILL.md): command, cwd, exit code, test count. A skipped realtime test is `NOT_RUN`, never `PASS`.
