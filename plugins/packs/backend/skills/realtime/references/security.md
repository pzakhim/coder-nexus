# Realtime security

Detail for [realtime](../SKILL.md). General security rules, the severity scale and the verdict impact belong to [secure-coding-standards](../../secure-coding-standards/SKILL.md). This page lists only what is specific to long-lived connections.

| Risk | Unsafe | Safe | Core rule |
|---|---|---|---|
| Auth only at connect | Socket accepted, then every `Subscribe` / action trusted | Service call authorizes each subscription and each action against the actor and data scope | SC2, SC3 |
| Stale authorization | Membership revoked, socket keeps receiving the group's events | Re-check on each delivery or on a short timer; close with the documented application code | SC2, SC8 |
| Long-lived token in the URL | `?token=<access token>` | Single-use, channel-scoped ticket with ≤ 60 s expiry; header auth when the client can set headers | SC5 |
| Cross-site WebSocket hijacking | Cookie-authenticated socket with no `Origin` check | Compare `websocket.headers["origin"]` with the settings allow-list before `accept()`; refuse with `1008` | SC2 |
| Cross-scope fan-out | Hub keyed by object id only; event for tenant A delivered to tenant B's subscriber of the same id | Hub keyed by `(scope, object id)`; the event carries its scope and delivery compares it with the connection's actor | SC3 |
| Unbounded input | `receive_text()` with no size cap, no rate limit | `--ws-max-size`, length check, per-connection token bucket (for example 10 messages/s, from `design.md`), close with `1008` or `1013` on abuse | SC1, OWASP API4 |
| Connection flooding | Unlimited sockets or streams per user | Per-actor connection cap in the hub; refuse new ones with `1013` (WebSocket) or 429 (SSE, before the first byte) | OWASP API4 |
| Unbounded replay | `Last-Event-ID: 0` replays the whole table | `replay_max` and a retention window; beyond them send `resync` and close | SC1 |
| Data leak in events | ORM object or dict serialized into `data` | Response models only; no internal ids, tokens or personal data the subscriber may not see | SC6 |
| Error leaks | Exception text sent in an error message or close reason | Generic error code; details logged server-side with a request id | SC6 |
| Header injection in SSE fields | `event` or `id` built from user input | Event names from an `Enum`, ids from the database | SC4 |
| Fake source | Timer that emits sample events "until the backend is ready" | Channel `BLOCKED` until the real source exists | SC8 |

## Review checklist

Walk this over every changed `@router.websocket` path, `EventSourceResponse` route and realtime adapter:

- [ ] Authentication happens before `accept()` or before the first event, through the workspace's auth dependency.
- [ ] Every inbound message type is a model in one discriminated union; unknown types are rejected.
- [ ] Every subscription and action is authorized in the service, per object and scope.
- [ ] Hub keys and delivery checks include the data scope.
- [ ] Size limit, rate limit, connection cap and replay limit exist and match `design.md`.
- [ ] No database session from a `yield` dependency lives for the connection.
- [ ] Every per-connection queue is bounded with the documented overflow policy.
- [ ] Close codes match the `design.md` table; errors never echo input or stack traces.
- [ ] Tickets are single-use and short-lived; no access token in a URL.
- [ ] Cookie-authenticated sockets check `Origin`.
- [ ] Tests prove refusal without credentials and that another scope's events never arrive ([testing](testing.md)).
