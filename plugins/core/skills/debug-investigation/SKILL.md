---
name: debug-investigation
description: Entry point for investigating without fixing - the coordinator has bug_fixer reproduce a reported bug, or run a scenario to trace how a feature behaves at runtime (data flow, state changes, calls made), add temporary logs or traces when needed, capture the output, remove every temporary change, and write diagnosis.md. No code change is kept. Use when the user wants to debug, investigate, see logs or understand a flow, or says things like "debug chức năng", "điều tra lỗi", "xem log", "trace luồng", "vì sao màn này", even if they do not say "investigation". Not when the user wants the bug fixed now (that is defect-resolution) or wants a test run against a scenario (that is feature-testing).
---

# Debug investigation

Act as the **coordinator** for one investigation. The folder, the `DIAGNOSED` status and the temporary-instrumentation rules are defined once in `work-item-contract` → [debug-item-contract](../work-item-contract/references/debug-item-contract.md) §8; this skill decides **who runs when** and never restates them.

The work is done by **`bug_fixer`** in investigation mode: it observes and reports, it never keeps a change. The coordinator never edits code.

## 1. Intake

1. Settle the kind with the user when the request does not make it clear (one question): **Bug** (something behaves wrongly) or **Trace** (how something works).
2. For a trace, make sure the scenario is concrete enough to run: the screen or entry point, the action, and the data or account. Ask for what is missing, one question at a time.
3. Create `.superpowers/debug/<slug>/` (contract §1) and run `git-preflight` Step A (read-only) to record the current branch and revision.
4. Start `bug_fixer` in investigation mode with the question, the scenario and the environment. It writes `diagnosis.md` with `fix-planning` and returns one status.

## 2. Routing (coordinator only)

| `bug_fixer` returns | Coordinator does |
|---|---|
| `DIAGNOSED` | Check `diagnosis.md` → `## 3` shows the instrumentation removed (same status and diff as before). Report the findings and the evidence path. For a bug, ask whether to fix it now: yes starts `defect-resolution` with `diagnosis.md` (contract §8, "From diagnosis to fix"). For a trace, close. |
| `NOT_REPRODUCED` | Show the attempts; ask the user for the missing information or to close. |
| `BLOCKED` | Resolve the named blocker (device, environment, access, leftover instrumentation) before re-assigning. |

## 3. Never

- Keep or commit any code change, or start a fix from this skill.
- Propose a fix level or open a branch; both belong to `defect-resolution` once the user asks for a fix.
- Report a finding without captured evidence, or count `NOT_RUN` as observed.
