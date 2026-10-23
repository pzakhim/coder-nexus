---
name: incremental-implementation
description: The Code Writer's process for executing one approved phase of a work item task by task - preconditions, a pre-flight check of what tasks consume and produce, a per-task loop that compares each check with its Expected result, phase-end verification and the hand-off. Use after Gate 3 (or for an approved brief task) whenever code is written for .superpowers/work-items/<slug>/vN/; never for brainstorming or unapproved scope.
---

# Incremental Implementation

One Code Writer executes one approved phase, tasks strictly in order, and proves each task before the next. Reason: a defect found right after the change that caused it is cheap; found at phase end it is tangled with every other task. Legacy `docs/features/<module>/<feature>/vN/` work keeps the same loop.

Formats live in one place: task fields and amendment classes in [plan-and-task contract](../work-item-contract/references/plan-and-task-contract.md), statuses and evidence rows in [hand-off and status](../work-item-contract/references/handoff-and-status.md). Detail for this skill: [pre-flight and hand-off](references/preflight-and-handoff.md), [sources](references/sources.md).

## 1. Preconditions

Stop with `BLOCKED` if any is missing. Reason: code built on an unapproved or unverified base is work the user may reject.

| Check | Where |
|---|---|
| Gate 1, 2, 3 approvals cover this `vN` (a phase-free item: approved `brief.md`) | `implementation-plan.md` approval references, `work-item-contract` |
| `PHASE-00` carries an accepted tick (`[x] PREPARED / COMPLETED`, `[x] PREPARED (INFO_READY)` or `[x] PREPARED (NO_EXTERNAL_API)`; [plan-and-task contract](../work-item-contract/references/plan-and-task-contract.md) → `PHASE-00` readiness tick); every phase in `Depends on` passed | `phases/phase-00-prepare.md`, `implementation-plan.md` |
| `git branch --show-current` equals the branch in the `git-preflight` `D-NN` | `codebase-notes.md` |
| Every task has concrete Scope / Files, Acceptance Criteria (command + cwd) and Expected | phase file; a gap is a plan change request (`change-control`), never a guess |

Context comes from the approved files only: Huly and source facts from `codebase-notes.md`, the API contract from `design.md` (handshake rules in plugin-root `shared_contracts/api_handshake_protocol.md`). Never re-query Huly or invent a record a source lacks.

Assigned `PHASE-00 [EXECUTE]` itself: run its tasks with this same loop and tick `[x] PREPARED / COMPLETED` in `phases/phase-00-prepare.md` and `implementation-plan.md` before the hand-off; the reviewer only confirms that tick. Preparation specifics (fixture or stub servers, test-data files, smoke commands) come from the stack part of the Code Writer profile and `{{slot:verification}}`.

**Resuming** (new session or lost context): ticks in the phase file and `git log` are the record, not memory. Resume at the first unticked task; re-run its predecessor's check once if the tree changed since its tick.

## 2. Pre-flight before Task 1

1. Read `## Global constraints` and `## Review focus` in `implementation-plan.md`. Constraints bind every task; Review focus names inputs the reviewer will try deliberately, so plan tests or guards for them now.
2. Build the Consumes / Produces table for the phase: one row per edge between tasks, or between a task and existing code (format in [pre-flight](references/preflight-and-handoff.md#pre-flight-table)). Open the existing symbol and compare the real signature, not the plan's description of it.
3. Any mismatch, missing producer, task that contradicts a Global constraint, or check command that cannot work → raise a `PCR-NN` (`change-control`) before writing code and return `BLOCKED` naming it. Planning answers `AMENDED` (class `TASK_DETAIL`) or `ESCALATED`.

A clean table is still written down. Reason: "no conflicts" without rows is a scan nobody ran.

## 3. Task loop

For each task, top to bottom. Never code two tasks in one pass.

| Step | Do | Reason |
|---|---|---|
| A. Read | Re-open the phase file; take the first unticked task; confirm every earlier task is ticked; note Scope / Files, Reused Components, Consumes, Produces, Acceptance Criteria, Expected | What you remember is a summary; the file has the exact values |
| B. Code | Edit only Scope / Files. Use the Reused Components and the conventions of `{{slot:clean-architecture}}`, `{{slot:core-package-usage}}`, `{{slot:clean-code}}`, `{{slot:secure-coding-standards}}`. Write the failing test first where `{{slot:unit-testing}}` requires it | Files outside scope are unreviewed design changes |
| C. Check | Run the Acceptance Criteria command in its cwd; read the whole output | Only a run you read is evidence (`evidence-standard`) |
| D. Triage | Compare the output with Expected (table below) | Silent deviation is a decision made without the people who approved the plan |
| E. Tick | `- [x]` the task with the revision and command (format in [hand-off](references/preflight-and-handoff.md#tick-line)); then re-read the plan before the next task | The tick is the ledger that survives lost context |

| Outcome | Meaning | Action |
|---|---|---|
| `MATCH` | Output equals Expected | Tick, continue |
| `CODE_WRONG` | The plan is right, the code is not | `{{slot:root-cause-debugging}}`; fix inside Scope / Files; re-run C. Never patch the output to look like Expected |
| `PLAN_WRONG` | Expected, a signature, a file list or the command itself is wrong or impossible | Task stays unticked; raise a `PCR-NN` (`change-control`) and return `BLOCKED` naming it; resume only after `AMENDED` |

Hard rules for every task:

- **No bulk coding, no context drift**: one task, one check, one tick, then re-read.
- **No bypassing the mapping**: a mapped component that does not fit is `PLAN_WRONG`, never a local substitute.
- **No construction in entry points**: screens, handlers and other entry points receive dependencies through the approved wiring convention.
- **Never weaken tests**: no deleted assertion, loosened expectation, added skip or edited expected value to turn a check green (see `{{slot:unit-testing}}`).
- **No fake success**: no invented data, stub fallbacks or placeholder results to make a missing dependency look available; fail explicitly.
- **Keep it buildable**: after each tick the project builds and earlier checks still pass.
- **Noticed but not touching**: an unrelated problem goes on the hand-off list, not into the diff.

## 4. Phase end

When every task is ticked:

1. Full phase checks with `{{slot:verification}}` (analyzer, tests, build). Task checks are narrow; only the full run shows interactions.
2. UI impact: `{{slot:visual-quality}}` on the approved target and states.
3. `{{slot:bug-hunt}}` at `quick` effort on the phase diff; grade with [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md) §9 and put its `bug-hunt:` line in the hand-off. Fix each `CONFIRMED` finding with a reproducing test first (`{{slot:unit-testing}}`), re-run affected checks; carry `PLAUSIBLE` ones as Concerns.
4. `{{slot:code-simplification}}` only when a concrete smell from `{{slot:clean-code}}` exists in changed code; re-run affected checks after; put its `simplify:` line (§9) in the hand-off.
5. `evidence-standard`: every claim in the hand-off has an evidence row; `NOT_RUN`, `BLOCKED` and `UNVERIFIED` are never `PASS`.

## 5. Hand-off

Commit the phase, then write `evidence/<phase-id>/<REVIEW_REVISION>/writer-handoff.md` (the folder is named after the committed `REVIEW_REVISION`) and return exactly one status (fields in [hand-off](references/preflight-and-handoff.md#hand-off)):

| Status | When |
|---|---|
| `READY_FOR_REVIEW` | All tasks `MATCH`, phase checks run on a committed `REVIEW_REVISION` (never `+dirty`); optional **Concerns** list |
| `BLOCKED` | A precondition, environment, approval or open `PCR-NN` stops the work and nothing in scope can fix it |
| `NEEDS_CONTEXT` | A fact is missing; state what was tried and what is needed |

Every status carries the **Noticed but not touching** list and any `TASK_DETAIL` amendments made during the phase, so the coordinator can tell the user at the phase checkpoint.

After review: findings come back through `review-resolution`; the round-N reply goes into the new `writer-handoff.md` under `## Review reply (round N)`. Every fix is a new revision that invalidates the affected review, test and visual evidence. Three review rounds on the same phase without `APPROVED` → escalate through `change-control` or the coordinator. The approved plan stays stable; actual results go to `as-built.md`, written by Docs Writer from the evidence.
