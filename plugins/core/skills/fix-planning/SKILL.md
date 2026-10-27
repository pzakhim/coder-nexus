---
name: fix-planning
description: "How bug_fixer writes the debug documents of bug-squad and debug-investigation — brief.md for every bug (symptom, expected vs actual, reproduction, root cause, impact, level proposal, scope, tasks, regression test, result), fixing-plan.md for an L2 fix (including Global constraints and the Review focus the Code Reviewer checks), escalation-report.md for an L3 escalation to dev-team, and diagnosis.md for a debug-investigation item — from the work-item-contract templates, with checks taken from the stack's verification and unit-testing skills. Use whenever bug_fixer triages a reported bug, plans or applies its fix, escalates an L3 bug, or writes up an investigation."
---

# Fix planning

Fill the templates of `work-item-contract` in `.superpowers/debug/<bug-slug>/`: `templates/bug-brief.md.tpl` (`brief.md`) for every bug, `templates/fixing-plan.md.tpl` (`fixing-plan.md`) for L2, `templates/escalation-report.md.tpl` (`escalation-report.md`) for L3, and `templates/diagnosis.md.tpl` (`diagnosis.md`) for `debug-investigation`. Levels, routing rules, L3 floors, and status words are defined in `work-item-contract` (`references/debug-item-contract.md`); task fields and **Expected** rules are in `work-item-contract` (`references/plan-and-task-contract.md` §2). This skill governs how to fill each section with evidence and when to stop for user confirmation; keep every template heading intact.

## 1. Two-Stage Writing Gate (Never Plan or Apply a Fix Before User Confirmation)

Never write `## 7`–`## 10` of `brief.md`, create `fixing-plan.md`, create a fix branch, or modify production code while `User confirmation` is `PENDING`.

| Moment | Parts written | Ends with |
|---|---|---|
| **Triage (Stage A — before user confirmation)** | `brief.md` → `## 1`–`## 6` only (zero production code edits, no fix branch). If entered via **Zero-Re-Ask Handoff** from `diagnosis.md` (`debug-investigation`) or `test-run-report.md` (`feature-testing`), populate `## 1`–`## 5` directly from the handed-off evidence without re-asking the user or re-investigating from scratch, then write `## 6`. | `NOT_REPRODUCED` or `TRIAGED` (`User confirmation: PENDING`) |
| **After the user confirms L1 or L2 (Stage B)** | `brief.md` → `## 7`–`## 9`; plus `fixing-plan.md` for L2 | Task 1 starts (writing and running the failing regression test) |
| **After the user confirms L3 (Stage B)** | `escalation-report.md` (`templates/escalation-report.md.tpl`), quoting and removing any uncommitted triage test from the working tree (`Code changed: none`) | `ESCALATED` |
| **After the fix (L1 or L2)** | `brief.md` → `## 10` | `READY_FOR_TEST` (L1) or `READY_FOR_REVIEW` (L2) |
| **After `CHANGES_REQUESTED` (L2) or `STILL_BROKEN` (L1/L2)** | Fix on a new revision, update `## Plan change log` when a task changes, update `## 10`, and write per-finding replies (`review-resolution`) in `evidence/<FIX_REVISION>/review-reply.md` | `READY_FOR_REVIEW` (L2) or `READY_FOR_TEST` (L1), or `TRIAGED` on round 3 / scope growth (`debug-item-contract` §3 rules 4, 7, 9) |

## 2. Stage A — Triage parts (`brief.md` `## 1`–`## 6`)

| Part | Write it so that | Reason |
|---|---|---|
| `## 1` Symptom & `## 2` Expected vs actual | `## 1` records what the user sees and where in their words (or pulled from Huly via `huly-task-intake`). `## 2` **Expected** cites its authoritative source: an `AC-NN` or `BR-NN` of an approved spec, a `D-NN`, a Huly ticket acceptance criterion (`huly-task-intake`), or the user's explicit statement. Missing or conflicting sources → the spec does not define what is correct, which forces **L3**. | A fix restores a known behavior; it never invents one. |
| `## 3` Reproduction | Prefer an automated check that fails for the reported reason (`{{slot:unit-testing}}`), kept uncommitted until the level is confirmed (`debug-item-contract` §3 rule 8); otherwise exact runtime reproduction (`chrome-devtools` MCP console/network capture, emulator/device, or ASGI/API request) with red evidence saved under `evidence/`. Must run **before** any code change. If not reproduced, list every attempt (steps, command, data, environment) and return `NOT_REPRODUCED`. | A fix without a red run proves nothing. |
| `## 4` Root cause | Pinpoint the exact `file:line`, trigger condition, and mechanism that turns the input into the actual failure (`{{slot:root-cause-debugging}}`), backed by **Git Forensics** (`git log -S`, `git log -L`, `git blame -L`, `git diff`, or disposable-worktree `git bisect`) and/or tagged temporary `[DBG-<slug>]` instrumentation (removed before returning). If it remains a hypothesis, write `"not confirmed"` with the hypotheses tested and their results, which forces **L3**. | An unconfirmed cause is L3 (`debug-item-contract` §3). |
| `## 5` Impact | Combine **`gitnexus` MCP (`impact`, `context`, `query`, `detect_changes`)** (when available) and `rg -n "<symbol>"` to trace direct callers and indirect consumers of every symbol the fix would touch; write one row per affected screen, flow, controller/cubit/bloc, use case, API endpoint, data store, or shared module (`file:line` per row, or record the exact search commands that returned nothing when empty). | Blast radius decides the level; guessing here produces a wrong level. |
| `## 6` Level decision | Propose **Severity** (`S1`–`S4`) and **Fix level** (`L1`, `L2`, or `L3`), quoting the matched `debug-item-contract` §3 conditions and stack L3 floors word for word; take the higher level when in doubt. Leave **User confirmation** as `PENDING`. | The user confirms against the exact contract rules before any fix starts. |

## 3. Stage B — Post-confirmation parts (L1 / L2 fix & L3 escalation)

- **`## 7` Scope / Files**: Record **Architecture profile** (where the stack defines one) and the exact files the fix creates or modifies, including the regression test. Nothing outside this list may be edited; needing another file triggers `debug-item-contract` §3 rule 7 (stop and return `TRIAGED`).
- **`## 9` Regression test**: Written first, in the test location `{{slot:unit-testing}}` names. State the **Red run (before the fix)** and why it fails, then the **Green run (after the fix)**.
- **Tasks** (`brief.md` → `## 8. Tasks and verification` for L1, `fixing-plan.md` → `## Tasks` for L2), using the task format of `plan-and-task-contract` §2:
  - **Task 1** writes and runs the failing regression test (recording red run and failure reason); the **last task** re-runs the reproduction check plus `{{slot:verification}}`.
  - One deliverable with its own check per task. L1 usually needs 2–3 tasks; an L2 requiring more than ~6 tasks is likely L3.
  - **Acceptance Criteria** and **Expected** use the commands of `{{slot:verification}}` and `{{slot:unit-testing}}` on the touched paths; **Expected** comes from `## 2`, never from what the current buggy code outputs.
- **`fixing-plan.md`** (L2, `templates/fixing-plan.md.tpl`):
  - **`## Global constraints`**: Lists **In scope** files (from `brief.md` → `## 7`), **Out of scope** neighbour code that must not change, and **Floors not to cross** near the fix (from `brief.md` → `## 5` & `## 6`).
  - **`## Review focus`**: What `code_reviewer` must check on purpose because automated tests may not catch it — one line per item with its reason, derived from `## 5` Impact and `## Global constraints`: every layer the fix crosses, shared or nearby code called without modification, L3 floors adjacent to the fix, paths lacking automated coverage, and any input, permission, or data-scope handling touched.
  - **`## Final checks` & `## Plan change log`**: `## Final checks` repeats the reproduction check, regression test, and stack verification (`{{slot:verification}}`). Any task adjustment after confirmation is logged in `## Plan change log`; a change that crosses a level returns `TRIAGED`.
- **`escalation-report.md`** (L3, `templates/escalation-report.md.tpl`):
  - Fill `## 1`–`## 5` from `brief.md` (`Code changed: none`), quoting any triage reproduction test in `## 2` (`Triage test (removed from the tree)`) and removing it from the working tree so `git status --short` is clean.
  - Fill `## 6. Suggested work item` (**Type**: `bugfix` when approved specs already state the right behavior, or `feature` when specs are missing or changing; **Needs `change-impact.md`**: `YES` or `NO` with reason) and `## 7. Open questions for Spec Writer`.

## 4. Self-check before returning

- `TRIAGED`: `brief.md` → `## 1`–`## 6` filled; red reproduction run has an `evidence/` path; every impact row has `file:line` (or exact search commands when empty); `## 6` quotes `debug-item-contract` §3 conditions and L3 floors with `User confirmation: PENDING`; zero production files modified.
- `READY_FOR_TEST` (L1): every task in `brief.md` → `## 8` ticked `[x]` on `MATCH`; regression test in `## 9` is red before and green after; reproduction check passes; `{{slot:verification}}` passes; self `{{slot:bug-hunt}}` (`quick`) recorded in `## 10`; only files in `## 7` changed.
- `READY_FOR_REVIEW` (L2): everything required for `READY_FOR_TEST`, plus every `fixing-plan.md` task ticked `[x]` and `## Review focus` filled; from round 2 onward, every review finding answered via `review-resolution` (`FIXED` with `file:line` + command evidence, `DISPUTED` with technical proof, or `RAISED`) in `evidence/<FIX_REVISION>/review-reply.md`.
- `ESCALATED` (L3): `escalation-report.md` (`## 1`–`## 7`) complete; uncommitted triage tests removed from the working tree (`Code changed: none`); `brief.md` status set to `ESCALATED`.

## 5. Diagnosis (investigation items)

Fill `templates/diagnosis.md.tpl` (`diagnosis.md`); rules are in `work-item-contract` (`references/debug-item-contract.md` §8).

| Part | Write it so that | Reason |
|---|---|---|
| `## 1` Question | A bug states symptom, expected, and actual with the source of the expected; a trace states the exact behavior or flow the user wants to understand. | The report answers the question asked, not a nearby one. |
| `## 2` Scenario | Numbered steps and an exact check command (`cwd`) someone else can re-run on the same revision. | A finding that cannot be re-run cannot be trusted. |
| `## 3` Temporary instrumentation | Every inserted `[DBG-<slug>]` statement with `file:line`, what it logs, `Removed` confirmation, and `git status` / `git diff` before vs after removal. | Proves zero temporary logs or debug edits were left behind. |
| `## 4` Captured output | Only the lines, traces, or responses that support a finding, with secrets/tokens/PII masked, each linked to its `evidence/` path. | Raw dumps hide the signal and may leak sensitive data. |
| `## 5` Findings | **Bug**: root cause with `file:line` and mechanism (`{{slot:root-cause-debugging}}`), or `"not confirmed"` with the hypotheses tested. **Trace**: the observed flow step by step, each step backed by a captured line. | Runtime observation and forensics, not static guessing, are what this item adds. |
| `## 6` Impact | For a bug, the same `gitnexus` MCP + `rg -n` caller/consumer table as `brief.md` → `## 5`; for a trace, `none` unless the flow touches shared code. | A subsequent `bug-squad` handoff reuses it directly without a second search. |
| `## 7` Next step | Fix through `bug-squad` (`Zero-Re-Ask Handoff`), no action, or the open questions. No fix level. | The level decision belongs to `bug-squad` and the user confirmation gate. |
