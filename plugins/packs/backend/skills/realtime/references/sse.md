# Server-Sent Events with native FastAPI

Detail for [realtime](../SKILL.md). Applies to FastAPI ≥ 0.135, where `fastapi.sse` ships `EventSourceResponse` and `ServerSentEvent`. Check the installed version first: `uv run python -c "import fastapi; print(fastapi.__version__)"` (or `poetry run` / the active virtualenv).

## 1. What FastAPI already does

| Built in | Consequence for our code |
|---|---|
| `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `X-Accel-Buffering: no` | Do not set them again; do check that the workspace's reverse proxy does not buffer or compress the path |
| A `: ping` comment every 15 s when the generator yields nothing | No hand-written keep-alive loop. A proxy idle timeout below 15 s still closes the stream: record the proxy timeout in `design.md` |
| Items pass through a buffer of one between the generator and the socket | Natural backpressure: the generator waits while a slow client reads. The risk moves to the source that feeds the generator (§5) |
| Plain yielded objects are validated against the declared item type and documented in `openapi.json` | `AsyncIterable[OrderEvent]` documents the payload; `AsyncIterable[ServerSentEvent]` documents only a generic `data/event/id/retry` event (RT1) |
| On disconnect the response stops and the generator's task is cancelled at its current `await` | Cleanup goes in `try/finally`; never rely on code after the loop |

## 2. Shapes

A finite stream whose events need no id (progress of one job) may yield the model directly, so `openapi.json` carries its schema:

```python
@router.get("/jobs/{job_id}/progress", response_class=EventSourceResponse)
async def job_progress(job_id: UUID, actor: Actor = Depends(get_current_actor),
                       jobs: JobService = Depends(get_job_service)) -> AsyncIterable[JobProgress]:
    await jobs.ensure_visible(job_id, actor)          # authorize before the first byte
    async for progress in jobs.watch(job_id):          # ends when the job ends
        yield progress
```

A resumable stream yields `ServerSentEvent` so it can set `id`, `event` and `retry`; `data` is still a response model:

```python
@router.get("/orders/events", response_class=EventSourceResponse)
async def order_events(
    actor: CurrentUserDep,
    feed: Annotated[OrderFeed, Depends(get_order_feed)],
    last_event_id: Annotated[int | None, Header()] = None,   # header "Last-Event-ID"
) -> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(comment="order events", retry=5000)
    async for event in feed.events_after(actor, last_event_id):
        if event.kind == "resync":
            yield ServerSentEvent(event="resync", data={"reason": "replay_overflow"}, retry=10000)
            break
        yield ServerSentEvent(data=event, event=event.kind, id=str(event.id))
```

| Unsafe | Safe | Reason |
|---|---|---|
| `yield {"id": o.id, "secret_note": o.note}` | `yield OrderEventOut.model_validate(o)` | A dict skips the response model; every field in it is sent (SC6) |
| `id=str(counter)` with `counter += 1` in memory | `id=str(event.id)` from an outbox or event table | The counter restarts after a deploy; `Last-Event-ID` then points at the wrong event (RT7) |
| `ServerSentEvent(raw_data=json.dumps(obj))` | `ServerSentEvent(data=model)` | `raw_data` is for preformatted text and sentinels; it bypasses Pydantic serialization |
| `event="order\nupdate"` or ids from user input | Fixed event names from an `Enum`; ids from the database | `event` and `id` must be single-line; user input there can inject fields |
| `return EventSourceResponse(generator())` | `response_class=EventSourceResponse` and `yield` in the path function | The decorator form gets validation, keep-alive, documentation and dependency handling |
| `def` generator with `time.sleep` | `async def` generator with `await` | A sync generator runs in the threadpool and keeps a thread after the client leaves (RT5) |
| `sse-starlette` in new code | `fastapi.sse` | Native support covers it; keep `sse-starlette` only where existing code uses it, and migrate in its own planned task |

## 3. Resume with `Last-Event-ID`

1. Ids are strictly increasing per stream and come from storage: a `bigint` identity column on an event/outbox table, filtered by the actor's scope.
2. On connect, replay `WHERE id > :last_event_id AND <scope> ORDER BY id LIMIT :replay_max` in a short session, then switch to live events. Subscribe to the live source **before** running the replay query and drop live events whose id is ≤ the last replayed id. Reason: events committed between the replay and the subscription are otherwise lost.
3. If `last_event_id` is older than the retention window or more than `replay_max` events behind, send one `event: resync` and close; the client refetches through the normal `GET`. Reason: an unbounded replay is a resource-exhaustion path (RT9).
4. `retry` (milliseconds) is set once at the start; pick it from `design.md` (for example 5000) so thousands of clients do not reconnect in the same second after a deploy.
5. `Last-Event-ID` is client input: declare it as `int | None` so FastAPI rejects garbage with 422, and never use it without the scope filter.

## 4. Database sessions and disconnect

```python
# Unsafe: the yield dependency keeps this session (and its pool connection) until the stream ends
async def order_events(session: AsyncSession = Depends(get_session)) -> AsyncIterable[ServerSentEvent]: ...

# Safe: one short session per replay or per lookup, serializing within session
class OrderFeed:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], bus: EventBus) -> None: ...

    async def events_after(self, actor: CurrentUser, last_id: int | None) -> AsyncIterator[OrderEventOut]:
        subscription = await self._bus.subscribe(actor.customer_id)        # bounded queue, RT6
        try:
            async with self._session_factory() as session:
                replayed_orm = await OrderEventRepository(session).after(actor.customer_id, last_id, limit=REPLAY_MAX + 1)
                # Map models to schemas inside session context before exit (BUG-01)
                replayed = [OrderEventOut.model_validate(e) for e in replayed_orm]

            # Replay overflow detection: emit resync instead of dropping events (BUG-02)
            if len(replayed) > REPLAY_MAX:
                yield OrderEventOut(kind="resync", id=replayed[-1].id, payload={})
                return

            for event in replayed:
                yield event
            high_water = replayed[-1].id if replayed else (last_id or 0)
            async for event in subscription:
                if event.id > high_water:
                    yield event
        finally:
            await subscription.close()                                 # runs on disconnect
```

- Authentication and the first authorization run in dependencies or before the first `yield`, so a refusal is a normal 401/403/404 response, not an error event mid-stream.
- If authorization can change during the stream (membership revoked), re-check it on each event or on a timer and end the stream with an `event: revoked`. Reason: SSE has no inbound channel to notice it otherwise.
- `request.is_disconnected()` is only needed in a loop that never awaits anything cancellable; prefer `await` points (queue reads, `asyncio.sleep`).

## 5. Backpressure at the source

The SSE buffer protects the socket, not the producer. When a pub/sub listener pushes into per-client queues, each queue is `asyncio.Queue(maxsize=N)`; on `QueueFull` apply the policy in `design.md`: drop the event and let the client resync through `Last-Event-ID`, or end the stream. See [fan-out and scaling](fanout-and-scaling.md).

## 6. Clients and transport limits (record in `design.md`)

- A browser `EventSource` cannot set an `Authorization` header: it sends cookies only. A browser client therefore needs cookie auth or a short-lived single-purpose ticket in the query string ([security](security.md)); a non-browser client can send the normal header.
- Over HTTP/1.1 a browser opens at most about six connections per origin, shared with normal requests; HTTP/2 at the proxy removes the limit. One stream per client carrying several event types beats one stream per screen.
- SSE works with `POST` too (a body describing what to stream), but `EventSource` only does `GET`; a `POST` stream needs a client that reads `text/event-stream` itself.
