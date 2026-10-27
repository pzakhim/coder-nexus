# Deriving the Root-Cause Debugging Model from a Workspace

Stack-neutral guide for discovering a workspace's non-interactive diagnostic commands, tracing tools, symptom-to-cause patterns, and environment checks before authoring `.agents/skills/root-cause-debugging/`.

---

## 1. Discovering Diagnostic Commands & Tracing Tools (`EXTEND` vs `INIT`)

Inspect the workspace before proposing debugging commands:
- **Existing project (`EXTEND`):** The workspace's configured test runner, linter, code-intelligence tools, and architectural layer conventions always win. Never introduce interactive debuggers (such as terminal REPL debuggers) that block unattended CLI execution.
- **Greenfield project (`INIT`):** Use the stack's standard non-interactive CLI test flags (single test filter, stop-on-first, verbose locals/stack, log level) and `rg -n` / GitNexus tracing.

| Discovery Target | What to Collect (For `01-reproduce-read-and-tools.md`) |
|---|---|
| **Focused Reproduction** | Command to run a single test case or in-process request (`exit != 0` on the symptom) |
| **Stop-at-First & Rerun-Failed** | Flags to stop on the first failure (`D3`) and rerun only previously failed tests |
| **Verbose Stack & Locals** | Flags to print full tracebacks, local variables, and captured debug logs without opening an interactive prompt |
| **Debug Leftover Check** | Linter rules and `rg -n` patterns that catch leftover debug prints, breakpoints, or temporary `[DEBUG-xxxx]` tags (`D11`) |
| **Disposable Bisect** | `git worktree add` + `git bisect run` workflow so regressions are bisected without touching the active working tree (`D4`) |
| **Code Intelligence** | GitNexus (`query`, `context`, `impact`, `detect_changes`) or `rg -n` caller/dependency searches (`D13`) |

---

## 2. Building the Symptom → First Moves → Typical Cause Matrix (For `02-isolate-and-hypothesize.md`)

Sample recent bug-fix commits (`git log --grep='fix' -n 15`) and map the stack's common failure modes into a table with three columns:
1. **Symptom** (the exact error class, status code, UI state failure, or warning observed)
2. **First Moves** (the immediate non-interactive check, log filter, or layer boundary inspection to run)
3. **Typical Root Cause** (the underlying defect in the stack's Domain, Application/State, Data/Repository, or Presentation/API layer)

Always cover these universal categories in the workspace's terms:
- **Unhandled exception / stack trace** → read down to the first workspace frame; inspect null/empty/contract mismatch.
- **Wrong output / state with no error** → assert at the boundary closest to the output and walk backwards one layer at a time (`D6`).
- **Validation / contract rejection** → inspect schema/serializer error details and field/alias mappings.
- **Lifecycle / async / concurrency failure** → inspect un-awaited futures/coroutines, closed sessions/controllers/streams, or shared mutable state.
- **Regression ("worked before")** → diff against `<last-green-sha>`, check lockfile/codegen drift, or bisect in a disposable worktree.
- **Flaky / order-dependent failure** → reproduce with fixed random seed/clock and inspect leaked state between tests.
- **Performance / timeout / N+1** → measure statement/rebuild counts first before changing code.

### Hypothesis Log Template
```text
H1 (rank 1): <suspected cause> | predicts: <changing Y removes the failure> | probe: <command or read> | result: CONFIRMED / RULED OUT
H2 (rank 2): ...
Fix attempts: 1/3 <what changed> -> reproduction <PASS/FAIL>
```

---

## 3. Environment (`BLOCKED`) vs. Code & Escalation Rules (For `03-fix-escalate-and-report.md`)

Define deterministic checks that separate environment failures (`BLOCKED`) from code defects:
- **Database / External Service Unreachable:** Port/readiness check fails → `BLOCKED` (never stop/restart a shared container or service you did not start).
- **Missing Environment Variable / Credential:** Startup/config validation fails on missing key → `BLOCKED` (compare variable names only; never print secret values).
- **Unapplied Migration or Stale Codegen:** Schema/head check or generated file check shows drift → `BLOCKED` (or regenerate if in task scope).
- **Dependency / Virtualenv / Lockfile Drift:** Dry-run sync check fails → `BLOCKED`.
- **Time-Box & Gate Escalation (`D12`):**
  - After **3 failed fix attempts**, stop and return `BLOCKED` with the hypothesis log.
  - Any fix requiring out-of-scope file edits (`TASK_DETAIL`), API/schema/dependency/layer changes (`DESIGN_CHANGE`), or acceptance-criteria changes (`SCOPE_CHANGE`) stops and escalates via `change-control`.
