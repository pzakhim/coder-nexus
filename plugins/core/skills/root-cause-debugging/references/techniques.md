# Debugging techniques

Starting points for steps 1-4 of [root-cause-debugging](../SKILL.md). Commands come from the task's Acceptance Criteria and the stack's `{{slot:verification}}`; this file names techniques, not tools.

## Ways to get a red-capable reproduction

| # | Loop | Use when |
|---|---|---|
| 1 | The failing check from the task, narrowed to the failing case | A task check went red |
| 2 | A focused test at the seam that reaches the bug | Defect report on existing code |
| 3 | A request or CLI script against a local run, asserting the exact symptom | Behaviour visible only end to end |
| 4 | Replay of a captured input (redacted) through the code path | Fails only with real data |
| 5 | Loop the trigger many times, fixed seed and clock, isolated state | Flaky or timing-dependent |
| 6 | Differential run: last green revision vs current, same input | Regression with unknown cause |

Tighten the loop before hypothesising: faster (narrow scope, skip unrelated setup), sharper (assert the symptom, not "no crash"), more deterministic (pin time, seed randomness, isolate files and network).

## Symptom to first move

| Symptom | First move | Typical root cause |
|---|---|---|
| Exception or stack trace | First frame in our code; the value that is wrong there; trace it back caller by caller | Missing empty/null handling, wrong caller assumption, changed contract |
| Wrong value, no error | Assert the expected value at the boundary nearest the output; walk back one layer at a time | Wrong condition or operator, unit/timezone/rounding, mapping dropped a field, stale cache |
| Regression | Diff and log of touched paths since the last green revision; differential run | A change elsewhere in the diff, a caller now passing other data |
| Flaky | Rerun N times; run the case alone vs after others | Order dependence, shared fixtures, missing await, real time or randomness |
| Ordering or async | Tagged temporary logs with timestamps at each boundary | Missing await, stale response overwriting a newer one, double submit, work after dispose |
| Works locally, fails elsewhere | Diff versions, env vars, locale/timezone, path case, parallelism | Environment drift (often `BLOCKED`, not code) |
| Type, analyzer or build error | Read the first error; fix types at the source | Contract change, wrong import, generated code out of date |
| Slow or timeout | Measure a baseline first, then change one thing | Repeated queries in a loop, unbounded work, blocking call on an async path |

Multi-component path (entry -> service -> storage): log what enters and leaves each boundary once, find the boundary where good data turns bad, then investigate only that component.

Bisecting revisions checks out other commits: do it only in a separate disposable worktree, never in the shared working tree with uncommitted work.

## Hypothesis log

Keep while debugging; it goes into the report.

```
H1 (rank 1): <suspected cause> | predicts: <changing Y removes the failure> | probe: <command or read> | result: CONFIRMED / RULED OUT
H2 (rank 2): ...
Fix attempts: 1/3 <what changed> -> reproduction <PASS/FAIL>
```

## Defensive checks after the fix

When the root cause was bad data entering through a boundary, add validation at the boundary that owns it per `{{slot:clean-architecture}}` (usually the entry point), failing loudly. Do not add checks in every layer beyond the task scope; extra layers are a design change for Planning.

## Report block

```
Symptom:      <what failed, where; reported by>
Reproduction: <command> (cwd <dir>) @ <revision> -> exit <n>, <key output>
Root cause:   <the defect, file:line, why it happened>
Fix:          <what changed and why at this layer>
Regression:   <test> - FAIL with fix undone, PASS with fix (both runs recorded)
Evidence:     rows per evidence-before-claims
Ruled out:    H2 <why>, H3 <why>
Debug tags:   grep [DEBUG-xxxx] -> no matches
```
