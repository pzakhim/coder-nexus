# Symptom → approach

Starting points for `02-isolate-and-hypothesize.md`; the generated skill keeps the rows that matter in the workspace, with its real examples.

| Symptom | First moves | Typical root causes |
|---|---|---|
| **Exception / stack trace** | Read the first frame in your code; reproduce with the smallest input; check the value that is null/wrong at that frame | Missing null/empty handling, wrong assumption about a caller, contract change |
| **Wrong value, no error** | Assert the expected value at the boundary closest to the output; walk backwards one layer at a time | Wrong condition/operator, unit/timezone/rounding, mapping dropped a field, stale cache |
| **Regression ("it worked before")** | `git diff <last-green>..HEAD`, `git log -p -- <path>`; `git bisect run <failing command>` | A change elsewhere in the diff, a caller now passing different data |
| **Flaky / intermittent** | Rerun N times; isolate the test; fix seeds/clock; look for shared state and un-awaited async | Order dependence, shared fixtures, race, real time/random, network |
| **Async / ordering** | Log (temporarily) the order of events with timestamps; check every await; check work after commit/dispose | Missing await, stale response overwriting newer, double submit |
| **Works locally, fails in CI** | Diff environments: versions, env vars, timezone/locale, file paths/case, parallelism | Environment drift, hidden dependency on local state |
| **Type / analyzer / build error** | Read the first error; fix types at the source, not with casts | Contract change, wrong import, generated code out of date |
| **Performance / timeout** | Measure first (timing around the suspect), then change one thing | N+1 queries, missing index, unbounded loop, sync call in async path |
| **Only with real data** | Capture the failing input (anonymised); write it as a test case | Unexpected data shape, encoding, large values |

## Hypothesis log (keep while debugging)

```
H1: <what you think is wrong> → check: <command or read> → result: <confirmed | ruled out>
H2: …
```

Ruled-out hypotheses go into the report; they save the reviewer the same detour.
