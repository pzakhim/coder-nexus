### Realtime channels

<!-- One block per channel. Required whenever the work item adds or changes an SSE stream or a WebSocket path (backend-realtime RT1). Omit the section when there is none. -->

- **Transport decision**: `{{Transport}}` (polling / SSE / WebSocket) — `D-NN` {{DecisionRef}}; acceptable delay: {{AcceptableDelay}}
- **Deployment**: {{ProcessModel}} (one process / N workers / N instances) → fan-out: {{FanOut}} (in-memory / LISTEN-NOTIFY channel `<name>` / existing broker)

| Channel | Path | Auth at connect | Scope rule | Resume | Limits |
|---|---|---|---|---|---|
| `CH-01` | `GET /api/v1/<feature>/events` (SSE) | `<header / cookie / ticket>` via `<dependency>` | `<who sees which events>` | `Last-Event-ID` = `<table>.id`; replay max `<n>`; retention `<period>`; `retry` `<ms>` | conns/actor `<n>` |
| `CH-02` | `/ws/<feature>` (WebSocket) | `<ticket / header / subprotocol>` | `<rule>` | `<none / resubscribe with last id>` | frame `<bytes>`, `<n>` msg/s, conns/actor `<n>`, ping `<s>` |

**Messages** (every payload is a named Pydantic model in `<module path>`):

| Channel | Direction | `type` / `event` | Model | Fields | Sent when | AC |
|---|---|---|---|---|---|---|
| `CH-01` | server → client | `order_updated` | `OrderEventOut` | `id`, `status`, `updated_at` | after commit of a status change | AC-03 |
| `CH-02` | client → server | `subscribe` | `Subscribe` | `order_id` | client opens an order | AC-04 |
| `CH-02` | server → client | `error` | `ErrorMessage` | `code` | invalid or forbidden message | AC-05 |

**Close codes and terminal events**:

| Channel | Code / event | Meaning | Client action |
|---|---|---|---|
| `CH-02` | `1008` | auth failed / forbidden | get a new ticket or stop |
| `CH-02` | `4001` | ticket or token expired | reconnect with a new ticket |
| `CH-01` | `event: resync` | resume point too old | refetch with `GET`, reconnect without id |

**Overflow policy**: per-connection queue max `<n>`; when full: `<drop + resync / close with code>`.

**Failure modes**: listener down → `<behaviour>`; deploy → clients reconnect with backoff `<range>` and resume by id.
