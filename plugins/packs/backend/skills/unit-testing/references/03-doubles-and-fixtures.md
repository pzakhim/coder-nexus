# 03 — Doubles and fixtures

Detail for [unit-testing](../SKILL.md). Rules U4, U5, U6, U11.

## Order of preference

**Real > fake > stub > mock.** Move down only when the real thing is slow, non-deterministic or has side effects you cannot control. Reason: every step down removes real behavior from the test.

| Dependency | Use | Never |
|---|---|---|
| Subject under test, its own collaborators (domain objects, policies, mappers) | Real | Doubled |
| Ports owned by the service (repository, unit of work, gateway `Protocol`) | Hand-written **fake** class implementing the same `Protocol`, rows in a `dict`, raising the same domain errors | `MagicMock()` returning whatever is asked |
| Outbound HTTP | `httpx.MockTransport(handler)` with one handler per scenario; unknown URL raises | Real network, patching `httpx` internals |
| Clock, ids, randomness | Injected `Callable[[], datetime]` returning aware UTC; injected id factory; `random.Random(seed)` | `datetime.now()` inside the code under test, `time.sleep` in tests |
| SDKs without a transport hook | `unittest.mock.create_autospec(Client, instance=True)` or `monkeypatch` at the edge | Unspecced `Mock()` that accepts any attribute |
| Authorization, data-scope filters, ownership checks | Real code | A fake that always allows |
| Database | Not in unit tests at all: the service sees a fake repository; SQL is integration | A mocked `AsyncSession` |

## Rules for every double

- Learn the real method's side effects before replacing it; double the slow or external level below what the test depends on. Reason: doubling too high removes the behavior you meant to test.
- A fake keeps the real contract: same result types, same errors for the same situations, complete data shapes (every field of the real row or response, not only the ones this test reads). Reason: a looser fake lets a service pass that fails on real data.
- One handler or fixture per branch (success, each error, malformed). Reason: the wrong branch cannot satisfy the test.
- Assert calls only when the call itself is the contract (a message published, a payment requested), with exact arguments: `gateway.charge.assert_awaited_once_with(ORDER_1, Decimal("15.00"))`. Reason: call assertions elsewhere couple the test to internals.
- Mock setup larger than the test logic means the design is too coupled or the test belongs at integration level.
- Use `create_autospec` / `spec_set=` for every `unittest.mock` object. Reason: a spec turns a renamed or misspelled method into a test failure instead of a silent pass.

```python
# Shape - tests/fakes.py
class FakeOrderRepository:                      # satisfies OrderRepository Protocol
    def __init__(self, rows: list[Order] | None = None) -> None:
        self.rows = {r.id: r for r in rows or []}

    async def get(self, order_id: UUID) -> Order:
        try:
            return self.rows[order_id]
        except KeyError:
            raise OrderNotFound(order_id) from None   # same error as the SQL repository

    async def add(self, order: Order) -> None:
        if order.id in self.rows:
            raise DuplicateOrder(order.id)
        self.rows[order.id] = order


class FakeUnitOfWork:
    committed = False
    async def commit(self) -> None:
        self.committed = True
```

```python
# Shape - outbound adapter
def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/v1/stock/SKU-1":
        return httpx.Response(200, json={"sku": "SKU-1", "available": 3})
    raise AssertionError(f"unexpected call {request.method} {request.url}")

client = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://erp.test")
```

## Router tests through overrides

- `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` in `async def` tests; never `TestClient` inside an `async def` test. Reason: `TestClient` runs its own event loop.
- Override the **service** dependency with a fake service and the **authentication** dependency (`get_current_user`) with a fixed user. Keep authorization real. Reason: overriding the permission check proves nothing about 403.
- Key each override by the exact dependency function the routes use, and always `app.dependency_overrides.clear()` in the fixture's `finally`. Reason: an override on a copy is silently ignored; a leftover override leaks into every later test.
- `lifespan` does not run under `ASGITransport`; resources it would create come from overrides. Use `ASGITransport(app=app, raise_app_exceptions=False)` only in a test that asserts the 500 response shape.

Starter: [templates/conftest.py.tpl](../templates/conftest.py.tpl), [templates/test_router.py.tpl](../templates/test_router.py.tpl).

## Async setup

One async runner per suite: pytest-asyncio. Never mix it with `@pytest.mark.anyio` tests. Reason: both plugins claim `async def` tests and the suite fails or silently skips depending on plugin order.

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"      # keep "strict" if the workspace uses it; then mark tests @pytest.mark.asyncio
testpaths = ["tests"]
```

Adding these settings to a workspace that has none is a plan task, not a side effect of a test. A missing tool (`pytest-asyncio`, `httpx`) is `NOT_RUN` with the reason or `NEEDS_CONTEXT`, never installed silently. Reason: a new dependency is a design decision (`D-NN`).

## Fixtures and data

- **Function scope by default.** Reason: shared mutable fixtures make tests pass or fail by order. No `autouse` for unit fixtures; tests name what they use.
- Builders create complete valid objects with values from the design's **Pass/Default** row: `make_order(**overrides)`. **Fail** and **Empty** cases override only the field that makes them fail or empty. Reason: a partial object passes the unit test and breaks on the first real row. Use `factory_boy` / `polyfactory` only if already installed.
- Reuse the existing fixtures, fakes and builders before writing new ones (U11). Reason: two fakes of one port drift apart.
