# Writing tests that catch defects

Detail for [test-first](../SKILL.md). Examples are neutral pseudocode; the stack's real syntax, test paths and commands come from `{{slot:unit-test}}`.

## Right-reason failure

| Red run shows | Means | Do |
|---|---|---|
| Assertion fails, message names the missing behavior | Right reason | Write the code |
| Test passes | Behavior already exists, or the test checks nothing | Re-read the break you named; fix the test |
| Compile / import / setup error | Not red yet | Fix the error, run again |
| Fails on a different assertion than intended | Wrong setup or a second defect | Fix setup; a real second defect gets its own test |
| Not collected, skipped, filtered out | Not run | Fix the runner selection; never record it as red or green |

## Name the break

Before the body, answer: which realistic production change fails this test, and is that change a defect or a deliberate decision?

| Answer | Action |
|---|---|
| A defect (wrong branch, lost field, missing guard) | Write the test |
| Only a deliberate decision (constant value, message wording) | Change detector: test the behavior that depends on the decision instead |
| "The source text changed" | Run the artifact and assert its effect |
| Nothing | Redesign around an observable result |

```
# BAD - change detector
assert MAX_RETRIES == 5

# GOOD - behavior that depends on the decision
given a gateway that always fails
when sync() runs
then the gateway was called 5 times and sync returns RetryExhausted
```

## Independent expectations

```
# BAD - tautological: expected computed the way the code computes it
expected = sum(item.price for item in items)
assert total(items) == expected

# GOOD - literal from the design's Pass/Default row
assert total([price 10, price 5]) == 15
```

Table-driven cases with literal expected values are the preferred shape for the design's Pass/Default, Fail and Empty rows. Keep each case readable on its own; repetition in tests is fine when it makes the case obvious.

## Behavior, not implementation

- Assert results, returned or raised errors, emitted states and data visible through the public interface.
- Verify through the interface, not a side channel: create then read back through the use case, not by querying storage directly.
- A refactor that keeps behavior must not break the test. If it would, the test is coupled to internals.
- Test your contract at its boundary (the payload you build, the query you emit, the route you register), not the library's mechanics.
- Large snapshots nobody reviews are change detectors; assert the few fields the behavior depends on.

## Doubles

Order of preference: **real** implementation, **fake** (in-memory, keeps the rules), **stub** (canned answers), **mock** (call assertions). Move down only when the real thing is slow, non-deterministic or has side effects you cannot control.

| Dependency | Use |
|---|---|
| Subject under test, its own collaborators | Real, never doubled |
| Ports owned by the workspace (repository, gateway, unit of work) | Fake that keeps the contract |
| External edges (HTTP, SDK, clock, random, file system) | Stub or mock at the edge |
| Authorization, data-scope rules, the database rules | Never mocked away: keep the rule in a fake, or leave it to integration tests |

Rules for every double:

- Learn the real method's side effects before replacing it; double the slow or external level below what the test depends on.
- Mirror the complete real data shape, not only the fields this test reads. Partial shapes pass while integration breaks.
- One fixture per branch (success, error, malformed), so the wrong branch cannot satisfy the test.
- Assert calls only when the call itself is the contract (a message sent, a payment requested), with exact arguments.
- Mock setup larger than the test logic means the design is too coupled or the test belongs at integration level.

## Determinism

Inject the clock, seed randomness, await asynchronous work, isolate state per test. A flaky test trains everyone to ignore red.

## Mutation check

Before handing off, mentally change the production code; at least one test should fail for each:

- wrong constant or argument;
- wrong branch taken;
- missing state change or side effect;
- empty or default return;
- missing validation for zero, empty, missing, unauthorized or malformed input.

A mutation nothing catches is an unprotected behavior: add the test, or record why it is out of scope.
