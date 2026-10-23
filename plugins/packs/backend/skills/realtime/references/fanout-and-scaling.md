# Fan-out and scaling

Detail for [realtime](../SKILL.md) RT6–RT8. Decide this in `design.md` before writing the hub, because it changes where events come from.

## 1. One process or many

| Deployment (from the workspace's run command, Dockerfile, compose or deploy files) | Registry and fan-out |
|---|---|
| Exactly one process, one instance, and `design.md` says so | In-memory hub (dict of scope → connections) is enough |
| `uvicorn --workers N`, `gunicorn -w N`, more than one container or pod, or autoscaling | Every process listens to a shared pub/sub and delivers to its own connections |

Reason: an in-memory hub sees only the clients connected to its own process (RT8). "We only run one worker" must be a recorded `D-NN`, not an assumption.

## 2. Pub/sub options

| Option | Use when | Notes |
|---|---|---|
| **PostgreSQL `LISTEN` / `NOTIFY`** | The service already runs PostgreSQL and the rate is moderate | `NOTIFY` inside the business transaction is delivered only on commit, so no event for rolled-back data. Payload limit is about 8000 bytes: send the event id and scope, and load the full event from the database. No storage: events sent while a listener is down are lost, so durable ids and replay (RT7) are required anyway |
| Redis pub/sub or streams | The workspace already runs Redis | Pub/sub has no storage (same replay rule); streams keep history but add consumer-group handling |
| A broker the workspace already uses (RabbitMQ, NATS, Kafka) | It already carries domain events | Reuse it; do not add a second broker for realtime |
| `encode/broadcaster` | Suggested by FastAPI's docs for multi-process broadcast | Check its maintenance and supported backends before adopting; a new dependency needs SC10 justification |

Never add infrastructure (Redis, a broker) inside a task: it is a `D-NN` approved at Gate 2.

## 3. LISTEN/NOTIFY with asyncpg

```python
# infrastructure/realtime/pg_listener.py
class PgListener:
    def __init__(self, dsn: str, hub: Hub) -> None:
        self._dsn, self._hub = dsn, hub
        self._conn: asyncpg.Connection | None = None

    async def start(self) -> None:                       # called from lifespan startup
        self._conn = await asyncpg.connect(self._dsn)     # dedicated connection, not from the SQLAlchemy pool
        await self._conn.add_listener("order_events", self._on_notify)

    def _on_notify(self, conn, pid, channel, payload: str) -> None:
        note = EventNotice.model_validate_json(payload)   # {"id": 123, "scope": "..."} only
        self._hub.notify(note)                            # non-blocking: puts into bounded queues

    async def stop(self) -> None:                          # lifespan shutdown
        if self._conn is not None:
            await self._conn.close()
```

```python
# in the service, inside the same transaction as the change
await session.execute(text("SELECT pg_notify('order_events', :payload)"),
                      {"payload": EventNotice(id=event.id, scope=event.scope).model_dump_json()})
```

- The DSN comes from settings (`DATABASE_URL` in the workspace `.env`), converted from the SQLAlchemy URL form (`postgresql+asyncpg://`) to the plain form asyncpg expects.
- A dropped listener connection must reconnect with backoff and log it; while it is down, clients rely on resume/replay. Record this in the channel's failure modes.
- Use bound parameters for the payload (`pg_notify` with `:payload`), never an f-string `NOTIFY` (SC4).
- The channel name is a constant, never user input.

## 4. Sizing notes for `design.md`

- Expected concurrent connections per instance, and the database pool size: with RT4 the pool is not tied to connections, but replay queries on reconnect storms are; cap `replay_max`.
- Load balancer: WebSockets need upgrade support and an idle timeout above the ping interval; SSE needs response buffering off for the path. Sticky sessions are not needed when every instance listens to the pub/sub.
- Deploys close every connection on the old instances: clients reconnect with jittered backoff and resume by id.
