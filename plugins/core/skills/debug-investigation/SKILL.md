---
name: debug-investigation
description: "Entry point for investigating without fixing - the coordinator has bug_fixer reproduce a reported bug, or run a scenario to trace how a feature behaves at runtime (data flow, state changes, calls made), add temporary logs or traces when needed, capture the output, remove every temporary change, and write diagnosis.md. No code change is kept. Use when the user wants to debug, investigate, see logs or understand a flow, or says things like 'debug chức năng', 'điều tra lỗi', 'xem log', 'trace luồng', 'vì sao màn này', even if they do not say 'investigation'. Not when the user wants the bug fixed now (that is bug-squad) or wants a test run against a scenario (that is feature-testing)."
---

# Debug investigation

Act as the **coordinator** for one investigation. The folder structure, the `DIAGNOSED` status, the temporary-instrumentation rules, and the diagnosis template are defined once in `work-item-contract` (`references/debug-item-contract.md` §8 and `templates/diagnosis.md.tpl`); this skill decides **who runs when** and never restates them.

The work is done by **`bug_fixer`** in investigation mode: it observes, proves with runtime or git evidence, and reports; it never keeps a code change. The coordinator never edits code.

## 1. Intake & Scenario Lock

1. Settle the investigation kind with the user when unclear (one question): **Bug** (something behaves wrongly and the user wants to know why) or **Trace** (how a feature works at runtime: screens, state transitions, API/DB calls).
2. When a Huly ticket (`<PROJECT>-<NUMBER>`) is supplied, `bug_fixer` uses `huly-task-intake` (`coder-nexus huly task-detail <TICKET> --download`) to pull the description, steps, and attachments once without re-asking.
3. Make sure the scenario is concrete enough to run: entry screen or endpoint, user action or request payload, test account/data, and target environment (`DEV` / `STG` / `PROD`). Ask for what is missing, one question at a time.
4. Create `.superpowers/debug/<slug>/` (`debug-item-contract` §1) and run `git-preflight` Step A (read-only) to record the current branch, `HEAD` revision, and `git status --short` baseline.
5. Start `bug_fixer` in investigation mode with the question, scenario, and environment. It writes `diagnosis.md` with `fix-planning` and returns one status.

## 2. Disciplined Investigation Workflow (Observe, Prove, Clean Up)

1. **Reproduce or Run Scenario**: Execute the scenario on a test runner or live runtime target (browser console/network/DOM inspection, mobile/desktop emulator or device, or in-process API/service runner and read-only dev/test database query plan inspection per the stack's `bug_fixer` rules and `{{slot:root-cause-debugging}}`).
2. **Git Forensics & Call-Graph Tracing**: Use `git log -S`, `git log -L`, `git blame -L`, `git diff`, and `gitnexus` MCP (`impact`, `context`, `query`, `detect_changes`) + `rg -n` to trace code history and affected callers/consumers (`diagnosis.md` -> `## 6. Impact`).
3. **Tagged Temporary Instrumentation (`[DBG-<slug>]`)**: When existing logs are insufficient, add minimal temporary logs/traces tagged with `DBG-<slug>` (masking secrets, tokens, and PII), re-run the scenario, and save captured output under `evidence/`.
4. **Mandatory Zero-Residue Cleanup Before `DIAGNOSED`**: Remove every `DBG-<slug>` line and any temporary reproduction test; prove clean state in `diagnosis.md` -> `## 3` via `rg -n "DBG-<slug>"`, the stack's print/analyzer check (`{{slot:verification}}`), and `git status --short` / `git diff` matching the starting baseline.

## 3. Routing (coordinator only)

| `bug_fixer` returns | Coordinator does |
|---|---|
| `DIAGNOSED` | Check `diagnosis.md` -> `## 3` proves instrumentation removed (same `git status --short` and `git diff` as baseline). Report the findings and evidence path. For a **Bug**, ask whether to fix it now — yes starts `bug-squad` with `diagnosis.md` via **Zero-Re-Ask Handoff** per `debug-item-contract` §8 (no re-asking or re-investigating). For a **Trace**, close. |
| `NOT_REPRODUCED` | Show the recorded attempts from `diagnosis.md`; ask the user for the missing information or to close. |
| `BLOCKED` | Resolve the named blocker (device, environment, access, or leftover `DBG-<slug>` instrumentation) before re-assigning. |

## 4. Never

- Keep or commit any code change, or start a fix from this skill.
- Propose a fix level or open a branch; both belong to `bug-squad` once the user asks for a fix.
- Leave any `DBG-<slug>` log, temporary print statement, or temporary reproduction test in the working tree when returning `DIAGNOSED`.
- Report a finding without captured evidence, or count `NOT_RUN` as observed.
