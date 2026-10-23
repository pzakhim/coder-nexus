# 04 — Test quality

Detail for [unit-testing](../SKILL.md). Rules U1, U3, U7, U8, U9, U14. A test is only useful if it fails for the right reason and passes reliably.

## Right-reason failure

| Red run shows | Means | Do |
|---|---|---|
| `AssertionError` or the expected `pytest.raises` miss, message names the missing behavior | Right reason | Write the code |
| Test passes | Behavior already exists, or the test checks nothing | Re-read the break you named; fix the test |
| `ImportError`, `NameError`, `AttributeError`, fixture not found, collection error | Not red yet | Fix the error, run again |
| Fails on a different assertion than intended | Wrong setup or a second defect | Fix setup; a real second defect gets its own test |
| `0 tests collected`, `skipped`, deselected by `-k` / marker, exit code 5 | Not run | Fix the selection; never record it as red or green |

Compare the red run with the red run the task's **Expected** states ([plan-and-task-contract §2](../../work-item-contract/references/plan-and-task-contract.md)). A stub that raises `NotImplementedError` gives a red for the wrong reason; prefer a minimal signature that returns a wrong value so the assertion fails.

## Name the break

Before the body, answer: which realistic production change fails this test, and is that change a defect or a deliberate decision? Cannot name one → the test checks nothing; pick an observable behavior.

| Answer | Action |
|---|---|
| A defect (wrong branch, lost field, missing guard) | Write the test |
| Only a deliberate decision (constant value, message wording) | Change detector: test the behavior that depends on the decision |
| "The source text changed" | Run the code and assert its effect |
| Nothing | Redesign around an observable result |

```python
# BAD - change detector
assert MAX_RETRIES == 5

# GOOD - behavior that depends on the decision
async def test_sync_when_gateway_always_fails_stops_after_five_attempts() -> None:
    gateway = FailingGateway()
    with pytest.raises(RetryExhausted):
        await sync(gateway)
    assert gateway.calls == 5
```

## Independent expectations

```python
# BAD - tautological: expected computed the way the code computes it
expected = sum(item.price for item in items)
assert order_total(items) == expected

# GOOD - literal from the design's Pass/Default row
assert order_total([make_item(price=Decimal("10")), make_item(price=Decimal("5"))]) == Decimal("15")
```

Expected values come from an independent source: a literal from the design, a worked example, the spec. Never from the code under test or its helpers. Parametrized tables with literal expected values are the preferred shape for the design's Pass/Default, Fail and Empty rows; repetition in tests is fine when it makes each case obvious.

## Assertions

- Assert exact values, error types and emitted state: `assert result.status is OrderStatus.CANCELLED`, `assert exc.value.code == "order_not_cancellable"`.
- `pytest.raises(SpecificError)`, never `pytest.raises(Exception)`; add `match=` only for a message the contract fixes, and keep one statement inside the block. Reason: a broad or multi-statement block passes on the wrong error (ruff `PT011`, `PT012`, `B017` flag these when enabled).
- Never only `is not None`, never `assert True`, never a test without an assertion. Reason: a weak assertion passes on wrong output.
- Pydantic errors: assert `exc.value.errors()[0]["loc"]` and `["type"]`, not the English message. Reason: messages change between Pydantic releases.
- Large snapshot or `model_dump()` equality nobody reviews is a change detector; assert the fields the behavior depends on.

## Structure

Arrange → Act → Assert, separated by blank lines; one behavior per test. Reason: a failure points to one broken behavior without debugging the test.

## Behavior, not implementation

- Assert results, raised errors, persisted state through the port and data visible through the public interface.
- Verify through the interface, not a side channel: create then read back through the service or fake repository API, not by poking private attributes.
- A refactor that keeps behavior must not break the test. If it would, the test is coupled to internals.
- Test your contract at its boundary (the payload you send, the status you return), not the library's mechanics.

## Determinism

| Need | Do | Reason |
|---|---|---|
| Time | Inject `clock: Callable[[], datetime]`, pass `lambda: FIXED_NOW` (aware UTC); `freezegun` / `time-machine` only if already installed | A real clock makes date logic pass or fail by the hour |
| Ids | Inject the id factory when the id appears in an assertion; otherwise assert on returned ids | Random UUIDs cannot be compared to literals |
| Randomness | `random.Random(seed)` injected | Unseeded randomness makes failures unreproducible |
| Async | `await` every coroutine; `asyncio.timeout(2)` around anything that waits | A forgotten `await` passes silently; a hang blocks the suite |
| Order | Sort before comparing unordered collections | `set` and dict-built lists have no contract order |
| State | No module-level mutable state; `app.dependency_overrides` cleared per test | Leaked state makes tests depend on run order |

A flaky test is a defect in the test: fix the cause, never rerun until green.

## Mutation check

Before hand-off, mentally change the production code; at least one test should fail for each:

- wrong constant or argument;
- wrong branch taken, or a refusal rule removed;
- missing state change, missing `commit`, or `commit` on the failure path;
- empty or default return (`[]`, `None`);
- missing validation for zero, empty, missing, unauthorized or malformed input;
- owner / scope check removed.

A mutation nothing catches is an unprotected behavior: add the test, or record why it is out of scope (for example SQL-only, left to `{{slot:verification}}`).
