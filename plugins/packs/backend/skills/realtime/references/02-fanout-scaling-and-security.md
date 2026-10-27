# Multi-Worker Fan-Out, Scaling & Realtime Security

> Topic: Single-process vs. multi-worker fan-out (`RT8`), PostgreSQL `LISTEN/NOTIFY` with `asyncpg` and transactional `pg_notify`, Redis/broker pub/sub, anti-IDOR `(tenant_id, object_id)` scope isolation (`RT3`), short-lived tickets, CSWSH `Origin` checks, and rate/size/connection caps (`RT9`).

## 1. Single-Process vs. Multi-Worker Fan-Out (`RT8`)

An in-memory connection registry (`dict[ScopeKey, set[Queue]]`) only sees clients connected to that single OS process. When running `uvicorn --workers N`, Gunicorn workers, or multiple container replicas, an event published in Worker 1 will silently miss clients connected to Worker 2 unless fanned out through a shared pub/sub backbone:

| Deployment Topology (recorded in `design.md` `D-NN`) | Required Fan-Out Architecture |
|---|---|
| **Single process (`workers=1`, `replicas=1`)** explicitly locked by `D-NN` | In-memory scoped `Hub` with bounded per-connection `asyncio.Queue(maxsize=N)`. |
| **Multi-worker / Multi-replica (`workers > 1` or horizontal scaling)** | Shared Pub/Sub listener in every worker feeding its local in-memory `Hub`:<br>1. **PostgreSQL `LISTEN / NOTIFY`** (zero extra infra when Postgres is already primary DB and event rate is moderate).<br>2. **Redis Pub/Sub or Streams** (when Redis is already in the stack or high-throughput fan-out is required).<br>3. **Existing message broker** (RabbitMQ / NATS / Kafka when already carrying domain events). |

> **Rule**: Never introduce a new infrastructure dependency (Redis, Kafka, `encode/broadcaster`) inside an implementation task without an approved Gate 2 Decision Record (`D-NN`).

---

## 2. Transactional PostgreSQL `LISTEN / NOTIFY` Pattern (`RT7`, `RT8`)

PostgreSQL `NOTIFY` executed inside a database transaction is delivered **only after the transaction commits** — guaranteeing clients never receive notifications for rolled-back changes. Because `NOTIFY` payloads are capped at 8000 bytes and are ephemeral while a listener is disconnected, always combine `NOTIFY` with a durable outbox/event table (`RT7`):

### 2.1 Publishing Inside the Write Transaction

Use parameterized `SELECT pg_notify(:channel, :payload)` (never SQL string interpolation):

```python
# Inside the Application/Infrastructure unit of work before commit:
notice = EventNotice(id=event_row.id, tenant_id=actor.tenant_id, object_id=order.id)
await session.execute(
    text("SELECT pg_notify(:channel, :payload)"),
    {"channel": "order_events", "payload": notice.model_dump_json()},
)
await session.commit()
```

### 2.2 Dedicated `asyncpg` Listener with Backoff Reconnect

Acquire a dedicated `asyncpg.Connection` at FastAPI `lifespan` startup (do **not** borrow a connection permanently from the SQLAlchemy request pool):

```python
class PostgresRealtimeListener:
    def __init__(self, dsn: str, hub: OrderHub) -> None:
        self._dsn = dsn.replace("postgresql+asyncpg://", "postgresql://", 1)
        self._hub = hub
        self._conn: asyncpg.Connection | None = None

    async def start(self) -> None:
        self._conn = await asyncpg.connect(self._dsn)
        await self._conn.add_listener("order_events", self._on_notify)

    def _on_notify(
        self,
        conn: asyncpg.Connection,
        pid: int,
        channel: str,
        payload: str,
    ) -> None:
        notice = EventNotice.model_validate_json(payload)
        # Non-blocking fan-out into local bounded queues keyed by (tenant_id, object_id)
        self._hub.publish_nowait(
            scope_key=(notice.tenant_id, notice.object_id),
            notice=notice,
        )

    async def stop(self) -> None:
        if self._conn is not None and not self._conn.is_closed():
            await self._conn.remove_listener("order_events", self._on_notify)
            await self._conn.close()
```

---

## 3. Realtime Security & Anti-IDOR Controls (`RT3`, `RT9`, `RT10`)

Long-lived connections introduce security risks beyond standard REST requests. Enforce every control below:

| Threat | Vulnerable Pattern | Mandatory Defense (`RT2`, `RT3`, `RT6`, `RT9`) |
|---|---|---|
| **Auth only at connect (Broken Object Level Authorization / IDOR)** | Socket is authenticated at handshake, then trusts any `{"type": "subscribe", "order_id": "..."}` sent by the client. | Authorize **every** inbound `Subscribe` and action in the Application service against `(actor.user_id, actor.tenant_id, order_id)` before adding the subscription. |
| **Cross-Tenant Fan-Out Leak** | Hub dictionary keyed only by `order_id` (`dict[UUID, set[Queue]]`). | Key the Hub by **`(tenant_id, object_id)`** and verify `event.tenant_id == connection.actor.tenant_id` before enqueueing. |
| **Stale Authorization / Revoked Session** | User's token expires or role is revoked while socket stays open for hours. | Record `actor.expires_at` in connection state; re-verify on each event or timer tick and close with `4001` (WS) or `event: revoked` (SSE) when expired. |
| **Long-Lived Access Token in URL** | `wss://api.example.com/ws?token=<jwt>` (leaked in proxy/CDN logs and browser history). | Issue a **single-use, channel-scoped ticket (`<= 60 s` TTL)** via `POST /api/v1/realtime/tickets` and redeem it atomically on connect. |
| **Cross-Site WebSocket Hijacking (CSWSH)** | Cookie-authenticated WebSocket accepts upgrade from any website. | Validate `websocket.headers.get("origin")` against settings `ALLOWED_ORIGINS` before `websocket.accept()`; reject mismatches with `1008`. |
| **Memory Exhaustion via Slow Client (`OWASP API4`)** | Unbounded `asyncio.Queue()` or `await ws.send_text()` inside broadcast loop. | Bounded `asyncio.Queue(maxsize=OUTBOX_MAX)` per connection; on `QueueFull`, drop and send `resync` or close with `1013`. |
| **Frame Flooding & Connection Exhaustion (`OWASP API4`)** | Unlimited connections per user, unlimited messages/sec, or 16 MiB frames. | Set `--ws-max-size`, check `len(raw) <= MAX_MESSAGE_CHARS` (`1009`), enforce a per-connection token bucket (e.g. `10 msg/s` → `1008`/`1013`), and cap concurrent connections per `actor.user_id` (`1013` on WS, `429` on SSE). |
| **Unbounded Replay DoS** | Client sends `Last-Event-ID: 1` and triggers a 500,000-row table scan. | Enforce `LIMIT :replay_max + 1` and retention window; if exceeded, emit a single `event: resync` and close so the client refetches current state via REST `GET`. |
| **SSE Header/Frame Injection** | Building SSE `event:` or `id:` from raw user strings containing `\n` or `\r`. | Restrict SSE `event` names to a server-side `Enum` and `id` to integer/UUID database identifiers. |

See [`references/01-sse-and-websocket-patterns.md`](01-sse-and-websocket-patterns.md) for SSE/WebSocket handler code and [`references/03-testing-cli-gates-and-review.md`](03-testing-cli-gates-and-review.md) for testing recipes, CLI gates, and review severities.
