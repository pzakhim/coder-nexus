# Server-Sent Events (SSE) & WebSocket Implementation Patterns

> Topic: Native FastAPI SSE (`fastapi.sse` `EventSourceResponse` & `ServerSentEvent`), gap-free `Last-Event-ID` replay (`RT7`), short DB session lifecycle (`RT4`), WebSocket pre-accept authentication (`RT3`), close codes, Pydantic v2 discriminated union messages (`RT2`), and single-sender `asyncio.TaskGroup` queues (`RT6`).

## 1. Native FastAPI Server-Sent Events (`fastapi.sse`, FastAPI ≥ 0.135)

Verify FastAPI version before implementation (`uv run python -c "import fastapi; print(fastapi.__version__)"`). Native `fastapi.sse` provides `EventSourceResponse` and `ServerSentEvent`:

| Built-in `fastapi.sse` Behavior | Engineering Implication |
|---|---|
| Sets `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `X-Accel-Buffering: no` | Do not duplicate these headers manually; ensure reverse proxies disable response buffering/compression on SSE paths. |
| Emits `: ping` keep-alive comment every 15 s when idle | No custom ping loop needed for SSE; configure load-balancer idle timeout `> 15 s` in `design.md`. |
| Single-item buffer between generator and socket | Natural socket backpressure; protect upstream pub/sub fan-out with bounded `asyncio.Queue(maxsize=N)` (`RT6`). |
| Cancels generator at current `await` on client disconnect | Always place subscription cleanup inside `try ... finally:`. |

### 1.1 Finite Progress Stream vs. Resumable Event Stream

- **Finite stream (no resume ID needed)** — yield typed Pydantic response models directly so `contracts/openapi.json` documents the exact item schema:
  ```python
  @router.get("/jobs/{job_id}/progress", response_class=EventSourceResponse)
  async def job_progress(
      job_id: UUID,
      actor: Annotated[Actor, Depends(get_current_actor)],
      jobs: Annotated[JobService, Depends(get_job_service)],
  ) -> AsyncIterable[JobProgressOut]:
      await jobs.ensure_visible(job_id, actor)  # RT3: Authorize before first byte (returns HTTP 403/404 on failure)
      async for progress in jobs.watch(job_id):
          yield progress
  ```

- **Resumable event stream (`Last-Event-ID`, `RT7`)** — yield `ServerSentEvent` with durable database IDs (`id=str(event.id)`), `Enum` event names, and `data=<PydanticModel>`:
  ```python
  @router.get("/orders/events", response_class=EventSourceResponse)
  async def order_events(
      actor: Annotated[Actor, Depends(get_current_actor)],
      feed: Annotated[OrderFeed, Depends(get_order_feed)],
      last_event_id: Annotated[int | None, Header(alias="Last-Event-ID", ge=1)] = None,
  ) -> AsyncIterable[ServerSentEvent]:
      yield ServerSentEvent(comment="connected", retry=5000)
      async for event in feed.events_after(actor, last_event_id):
          if event.kind == "resync":
              yield ServerSentEvent(
                  event="resync",
                  data=ResyncNoticeOut(reason="replay_window_exceeded"),
                  retry=10000,
              )
              break
          yield ServerSentEvent(data=event, event=event.kind.value, id=str(event.id))
  ```

### 1.2 Gap-Free `Last-Event-ID` Replay & Short DB Sessions (`RT4`, `RT7`)

Never inject `session: AsyncSession = Depends(get_session)` into an SSE or WebSocket route (`RT4`), because a `yield` dependency holds the PostgreSQL connection for the entire lifetime of the stream. Instead, inject `async_sessionmaker[AsyncSession]` into the feed/service and open a short session only during the replay query:

```python
class OrderFeed:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        bus: EventBus,
    ) -> None:
        self._session_factory = session_factory
        self._bus = bus

    async def events_after(
        self,
        actor: Actor,
        last_id: int | None,
    ) -> AsyncIterator[OrderEventOut]:
        # Step 1 (RT7): Subscribe to live bus BEFORE running the DB replay query
        # so events committed between replay and live loop are buffered, never lost.
        subscription = await self._bus.subscribe(scope=actor.tenant_id)  # bounded asyncio.Queue(maxsize=N)
        try:
            high_water = last_id or 0
            if last_id is not None:
                # Step 2 (RT4): Short-lived DB session closes immediately after replay fetch
                async with self._session_factory() as session:
                    rows = await OrderEventRepository(session).fetch_after(
                        tenant_id=actor.tenant_id,
                        last_id=last_id,
                        limit=REPLAY_MAX + 1,
                    )
                    # Convert ORM rows to Pydantic DTOs inside session context before exit
                    replayed = [OrderEventOut.model_validate(r) for r in rows]

                # Step 3 (RT9): Bounded replay window — force client resync if too far behind
                if len(replayed) > REPLAY_MAX:
                    yield OrderEventOut(kind=EventKind.RESYNC, id=replayed[-1].id)
                    return

                for item in replayed:
                    yield item
                if replayed:
                    high_water = replayed[-1].id

            # Step 4 (RT7): Deduplicate live events already covered by the replay query
            async for live_event in subscription:
                if live_event.id > high_water:
                    yield live_event
        finally:
            await subscription.close()  # Guaranteed cleanup on disconnect
```

---

## 2. WebSocket Endpoints (`@router.websocket`)

### 2.1 Authentication Before `websocket.accept()` (`RT3`)

Choose the handshake authentication mechanism in `design.md` (`RT1`):

| Client Type | Recommended Handshake Auth | Mandatory Security Rule |
|---|---|---|
| Native mobile / server-to-server | `Authorization: Bearer <jwt>` header on HTTP Upgrade | Reuse standard token verification dependency before `accept()`. |
| Browser WebSocket (`new WebSocket(url)`) | **Single-use short-lived ticket (`<= 60s`)** via `POST /api/v1/realtime/tickets` → `wss://.../ws/orders?ticket=<opaque>` | Never pass a long-lived JWT access token in a URL query string (logged by proxies/access logs). Tickets are single-use, bound to `(user_id, tenant_id, channel)`, and expire in `<= 60 s`. |
| Same-site Cookie session | Cookie on Upgrade request | **Must validate `websocket.headers.get("origin")`** against the configured origin allow-list before `accept()` to prevent Cross-Site WebSocket Hijacking (CSWSH). |

Raise `WebSocketException(code=status.WS_1008_POLICY_VIOLATION)` (never `HTTPException`) inside WebSocket dependencies so unauthenticated connections are rejected before `await websocket.accept()`:

```python
async def get_ws_actor(
    websocket: WebSocket,
    ticket: Annotated[str | None, Query(min_length=16, max_length=128)] = None,
    tickets: Annotated[TicketService, Depends(get_ticket_service)] = None,
) -> Actor:
    actor = await tickets.redeem_single_use(ticket, channel="orders") if ticket else None
    if actor is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return actor
```

### 2.2 Standard & Application WebSocket Close Codes (`RT1`)

| Close Code | Meaning | Required Client Behavior |
|---|---|---|
| `1000` (`WS_1000_NORMAL_CLOSURE`) | Normal completion | Do not auto-reconnect unless user re-opens view |
| `1001` (`WS_1001_GOING_AWAY`) | Server graceful shutdown / deploy | Reconnect with jittered exponential backoff |
| `1008` (`WS_1008_POLICY_VIOLATION`) | Authentication failed, invalid Origin, or unauthorized scope | Stop or request a fresh ticket after re-authenticating |
| `1009` (`WS_1009_MESSAGE_TOO_BIG`) | Inbound frame exceeds `MAX_MESSAGE_BYTES` | Do not retry the oversized payload |
| `1011` (`WS_1011_INTERNAL_ERROR`) | Unhandled server exception (logged with `trace_id`) | Reconnect with backoff |
| `1013` (`WS_1013_TRY_AGAIN_LATER`) | Rate limit, per-user connection cap, or bounded queue overflow | Back off and resync state via REST `GET` |
| `4001` (App-defined in `design.md`) | Session/ticket expired mid-connection | Fetch new ticket via `POST /realtime/tickets` and reconnect |

### 2.3 Strict Pydantic v2 Discriminated Unions for Inbound Messages (`RT2`)

Never call `await websocket.receive_json()` directly into business logic. Enforce byte-length bounds, parse with a Pydantic v2 discriminated union `TypeAdapter`, and never echo raw invalid input or stack traces back to the client:

```python
class SubscribeOrderMsg(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["subscribe"]
    order_id: UUID


class UnsubscribeOrderMsg(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["unsubscribe"]
    order_id: UUID


InboundClientMessage = Annotated[
    SubscribeOrderMsg | UnsubscribeOrderMsg,
    Field(discriminator="type"),
]
inbound_adapter: TypeAdapter[InboundClientMessage] = TypeAdapter(InboundClientMessage)
```

### 2.4 Single Writer Loop (`asyncio.TaskGroup`) & Bounded Outbox (`RT6`)

Never iterate over active sockets with `for ws in sockets: await ws.send_text(...)` (one slow client stalls the entire broadcast) and never allow multiple coroutines to call `websocket.send_text()` concurrently on the same socket. Give each connection a bounded `outbox: asyncio.Queue[ServerMessage]` (`maxsize=OUTBOX_MAX`) and run one `send_loop` + one `receive_loop` inside `asyncio.TaskGroup`:

```python
async def serve_orders_socket(websocket: WebSocket, actor: Actor, hub: OrderHub) -> None:
    await websocket.accept()
    outbox: asyncio.Queue[ServerMessage] = asyncio.Queue(maxsize=OUTBOX_MAX)
    conn_id = await hub.register(actor=actor, outbox=outbox)
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_send_loop(websocket, outbox))
            tg.create_task(_receive_loop(websocket, actor, conn_id, outbox, hub))
    except* WebSocketDisconnect:
        pass
    finally:
        await hub.unregister(conn_id)  # Always clean up registry entry on any exit
```

See [`references/02-fanout-scaling-and-security.md`](02-fanout-scaling-and-security.md) for multi-worker fan-out (`LISTEN/NOTIFY`) and security controls, and [`references/03-testing-cli-gates-and-review.md`](03-testing-cli-gates-and-review.md) for testing and review gates.
