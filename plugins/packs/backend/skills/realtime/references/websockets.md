# WebSocket endpoints

Detail for [realtime](../SKILL.md). FastAPI's `WebSocket` is Starlette's; the server needs a WebSocket implementation installed (`websockets` or `wsproto`, usually through `uvicorn[standard]`). Check it in the lockfile before planning a socket task; adding it is a dependency change (SC10).

## 1. Authentication at connect

Choose one method in `design.md` (RT1). In every case the token is validated by the workspace's auth code, never parsed by hand (SC7).

| Method | Use when | Risks and handling |
|---|---|---|
| `Authorization` header on the upgrade request | The client can set headers (server-to-server, most native HTTP libraries) | Best option; same dependency as HTTP routes |
| Short-lived **ticket** in the query: `wss://…/ws?ticket=…`, issued by an authenticated `POST /realtime/tickets` | Browser clients (the browser WebSocket API cannot set headers) | URLs are logged by proxies: the ticket is single-use, scoped to this channel, expires in ≤ 60 s, and is never the long-lived access token |
| Token in `Sec-WebSocket-Protocol` | A browser client when tickets are not possible | The server must `accept(subprotocol=<the protocol name>)` and never echo the token back; still visible to every proxy that logs headers |
| Cookie session | The client already uses cookie sessions on the same site | Check `Origin` against the allow-list: browsers send cookies on cross-site upgrades and CORS does not apply to WebSockets (cross-site WebSocket hijacking) |
| First message after `accept()` | Only when none of the above is possible | Unauthenticated sockets hold resources: require the auth message within a few seconds or close with `1008` |

```python
async def get_ws_actor(websocket: WebSocket, ticket: Annotated[str | None, Query()] = None,
                       tickets: TicketService = Depends(get_ticket_service)) -> Actor:
    actor = await tickets.redeem(ticket, channel="orders") if ticket else None
    if actor is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)   # before accept → handshake refused
    return actor


@router.websocket("/ws/orders")
async def orders_socket(websocket: WebSocket, actor: Annotated[Actor, Depends(get_ws_actor)]) -> None:
    await websocket.accept()
    ...
```

- Raise `WebSocketException`, never `HTTPException`, inside a WebSocket route. Closing before `accept()` refuses the handshake (the client sees HTTP 403).
- A dependency with `yield` stays open for the whole connection: never inject a database session that way (RT4).
- Token expiry during a long connection: store `expires_at` in the connection state and close with the application code from `design.md` (for example `4001`) when it passes, so the client reconnects with a fresh ticket.

## 2. Close codes

| Code | Use for |
|---|---|
| `1000` | Normal close (client or server finished) |
| `1001` | Server shutting down (deploy); the client reconnects with backoff |
| `1008` | Policy violation: authentication or authorization failed, forbidden action |
| `1009` | Message too big |
| `1011` | Unexpected server error (after logging it with a request id) |
| `1013` | Try again later: overload, connection limit reached |
| `4000–4999` | Application codes, each listed in `design.md` with what the client must do (refresh ticket, resync, stop) |

Reason: the close code is the only error signal the client gets once the socket is open; undocumented codes leave the client guessing whether to reconnect.

## 3. Messages as Pydantic models

```python
class Subscribe(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["subscribe"]
    order_id: UUID

class Unsubscribe(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["unsubscribe"]
    order_id: UUID

ClientMessage = Annotated[Subscribe | Unsubscribe, Field(discriminator="type")]
client_message = TypeAdapter(ClientMessage)

raw = await websocket.receive_text()
if len(raw) > MAX_MESSAGE_CHARS:
    await websocket.close(code=status.WS_1009_MESSAGE_TOO_BIG)
    return
try:
    message = client_message.validate_json(raw)
except ValidationError:
    await outbox.put(ErrorMessage(type="error", code="invalid_message"))   # no echo of the input
    continue
```

- Outbound messages are models too (`OrderUpdated`, `ErrorMessage`) with a `type` literal; send with `websocket.send_text(model.model_dump_json())`.
- Never `receive_json()` straight into business code: it accepts any JSON shape (SC1).
- An error message never echoes the raw input or a stack trace (SC6).
- Also cap the frame size at the server: `uvicorn --ws-max-size <bytes>` (default 16 MiB) to the value in `design.md`. Reason: the check in code runs only after the whole frame is in memory.

## 4. Per-connection state and one sender

Python ≥ 3.11 (`asyncio.TaskGroup`, `except*`); on older versions use an `anyio` task group the same way.

```python
async def serve(websocket: WebSocket, actor: Actor, hub: OrderHub) -> None:
    outbox: asyncio.Queue[ServerMessage] = asyncio.Queue(maxsize=OUTBOX_MAX)    # RT6
    connection = await hub.register(actor, outbox)
    try:
        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(send_loop(websocket, outbox))
            tasks.create_task(receive_loop(websocket, actor, connection, hub))
    except* WebSocketDisconnect:
        pass                                   # normal end; nothing to report
    finally:
        await hub.unregister(connection)       # always remove the registry entry
```

| Unsafe (common example code) | Safe | Reason |
|---|---|---|
| `for ws in active: await ws.send_text(msg)` | `hub.publish(scope, msg)` puts into each connection's bounded `outbox` with `put_nowait`; one `send_loop` per connection writes to its socket | One slow or dead client blocks the loop for everyone; an exception from one socket aborts the broadcast |
| Several tasks calling `websocket.send_*` on the same socket | Only `send_loop` sends | One writer per socket keeps frames ordered and makes backpressure visible in one place |
| `active.remove(ws)` only in `except WebSocketDisconnect` | `finally: await hub.unregister(...)` | Other exceptions leak registry entries and later broadcasts hit closed sockets |
| `except Exception: pass` around the receive loop | Let unexpected errors close with `1011` after logging | Swallowed errors leave a half-dead connection that still counts toward limits |
| Subscription list taken from the client and trusted | Each `Subscribe` goes through the service: `await orders.ensure_visible(msg.order_id, actor)` | Authorization per message, not only at connect (RT3) |

On `QueueFull` apply the policy in `design.md`: drop and send a `resync` message, or close with `1013`/an application code.

## 5. Heartbeat and idle connections

- The server answers and sends protocol-level pings: uvicorn's `--ws-ping-interval` and `--ws-ping-timeout` (20 s each by default) close dead peers. Set them in the run command from `design.md`; do not add an application ping only for liveness.
- Add an application-level `{"type": "ping"}` only when the client needs to see liveness itself (browsers cannot send protocol pings), and document it as a message type.
- Load balancers close idle connections (often after 60 s): the ping interval must be below that timeout, and the proxy must pass the `Upgrade` and `Connection` headers.

## 6. Shutdown and deploys

On shutdown, close open sockets with `1001` from the app's `lifespan` exit (the hub keeps the list). Clients reconnect with jittered backoff stated in `design.md`. Reason: without it every client of a restarted instance reconnects in the same second.
