---
name: change-control
description: "Raise, classify, and resolve a Plan Change Request (PCR-NN) when an approved phase cannot be implemented or verified as written, routing TASK_DETAIL, DESIGN_CHANGE, or SCOPE_CHANGE through Planning and the affected approval gate."
---

# Plan change request

An approved plan can be wrong in a detail or in a decision. This skill keeps both cases honest: the person who finds the gap stops and asks, Planning fixes only what it may fix alone, and everything else goes back to the user through the gate that approved it. Formats live in `work-item-contract`: frozen vs amendable and the `## Plan change log` in `work-item-contract` (`references/plan-and-task-contract.md` §5), status words and paths in `work-item-contract` (`references/handoff-and-status.md`).

## 1. When to raise

| Trigger | Typical evidence | Raised by |
|---|---|---|
| A check's **Expected** cannot be met by correct code (`PLAN_WRONG`) | The command, its output, why correct code still differs | Code Writer |
| A consumed symbol does not exist or differs from its **Produces** line | Search result or the real signature | Code Writer |
| A mapped / reused component does not fit the task | The component's real contract against what the task needs | Code Writer |
| The code (existing or required) contradicts a `D-NN`, a Global constraint or the design | The `D-NN` text beside the code location | Code Writer, Code Reviewer |
| A needed file lies outside the task's **Scope / Files** | The file and why the task cannot work without it | Code Writer |
| A finding whose right fix touches the plan (`PLAN_CONFLICT`), or **a cross-boundary file split (`FILE_BLOAT_SPLIT`)** | The finding row, file line count (`build()` > 50 or file > 300), proposed decomposition crossing module boundaries, shared public APIs, or plan/phase ownership (routine same-module internal widget/helper extraction needs no `PCR-NN`) | Code Reviewer, Code Writer, Test Runner |
| The cause found by `{{slot:root-cause-debugging}}` lies in the plan, or 3 review rounds end without `APPROVED` for a plan reason | The debugging report or the round history | Code Writer, Code Reviewer |

Not a plan change: a code defect (`CODE_WRONG` → `{{slot:root-cause-debugging}}`), a missing environment or service (`BLOCKED`), information the approved documents already contain (`NEEDS_CONTEXT`). Reason: routing a code bug to Planning moves the fix to the wrong owner.

## 2. Rules for the raiser

- **Stop at the task.** Leave it unticked; keep earlier ticked tasks as they are. Reason: a half-built workaround becomes the design nobody approved.
- **No workaround**: no local alternative component, no extra cross-boundary file, no unilateral cross-module/shared-API file split (routine internal helper/widget extraction inside the same module to meet LOC limits `build()` ≤ 50 / file ≤ 300 is allowed without a `PCR-NN`), no edited check, test or **Expected**, no fallback or fake data to get past the gap.
- **Code Writer**: write `plan-changes/PCR-NN.md` from [templates/change-control.md.tpl](templates/change-control.md.tpl) and return `BLOCKED` naming `PCR-NN`.
- **Code Reviewer or Test Runner**: stay read-only. Record the conflict as a `PLAN_CONFLICT` row in your own report (plan line, finding, evidence, options / proposed file decomposition) and return your verdict; the coordinator writes `plan-changes/PCR-NN.md` from that row and gives it the next number. Reason: the roles that judge the work never write the documents they judge (`work-item-contract` (`references/handoff-and-status.md` §2)).
- Give options, at most three, with one recommendation and its cost. Reason: Planning and the user decide faster on a concrete choice, but the raiser never applies it.

## 3. Classification (Planning)

| Class | Touches | Decided by | Planning answers |
|---|---|---|---|
| `TASK_DETAIL` | A broken check command, task order inside a phase with no broken **Consumes** edge, splitting a task description (or clarifying same-module internal helper/widget files without altering shared APIs or module boundaries), a task's Acceptance Criteria or Expected brought into line with an unchanged approved source (cite it) | Planning alone | `AMENDED` |
| `DESIGN_CHANGE` | **Splitting a bloated file across module boundaries, shared public APIs, or approved phase ownership (`FILE_BLOAT_SPLIT`)**, `design.md`, a `D-NN`, Global constraints, Review focus, the phase list or a phase outcome, the AC → phase mapping | User at Gate 2 / Gate 3 (`planning` presents the proposed file structure in session chat and obtains user confirmation via Coordinator Main-Chat `ask_question` before re-planning) | `ESCALATED` |
| `SCOPE_CHANGE` | A goal, `BR-NN` or `AC-NN` | User at Gate 1, through the Spec Writer | `ESCALATED` |

In doubt, choose the higher class. Reason: an amendment that should have been a decision is self-approval.

A conflict between the approved spec and what the Test Runner observes the spec requires (an `AC-NN` that cannot all be true, a missing case the goal needs) is `SCOPE_CHANGE`; the feature verdict stays `BLOCKED` until the re-approved revision is tested.

## 4. What Planning does

1. Read every `## Plan change log` row; no answer may undo an earlier row's constraint.
2. Verify the claim against the code and the approved documents. The request is a claim, not evidence.
3. If the plan was right and the raiser misread it, make the task text unambiguous (that is a `TASK_DETAIL` clarification) and answer `AMENDED`.
4. `TASK_DETAIL`: edit only the affected task lines, append one log row (**Authority**: `TASK_DETAIL (Planning, no approval needed)`), write the answer with the exact changed lines in `PCR-NN.md`. Untick any already ticked task the change affects; its evidence is invalid.
5. Escalation: queue a `Q-NN` in `codebase-notes.md` with the options and recommendation, answer `ESCALATED` with the target gate. Change nothing frozen until the user's answer closes the `Q-NN` into a `D-NN` and the gate re-approves the revised documents; then append the log row with that approval reference.

Planning never edits code, never waives a finding and never marks a request resolved on the raiser's behalf.

## 5. Who tells the user (`ask_question` Main-Chat Ownership & 2-Channel Short Asking)

Direct `ask_question` belongs ONLY to the active user-facing conversation (Main Chat). When running subagents or in Hybrid `/swarm` mode, only the Coordinator (`@coordinator`) relays user escalations in Main Chat (never require the user to switch subagent threads):

| Answer | When the user hears | How |
|---|---|---|
| `AMENDED` | At the next phase checkpoint (the existing "continue?" prompt) | Summarize the new `## Plan change log` rows in session chat, one line each |
| `ESCALATED` | At once; the affected phase pauses | Follow **2-Channel Grilling** (`grilling` Law 4): explain the `Q-NN`, options, and trade-offs in session chat (`content`), then call 1 short 1-line `ask_question` with `(Recommended)` first; approval follows the normal gate |

## 6. Waiting and resuming

- The Code Writer waits. Later tasks are not started: tasks run strictly in order, and later tasks may consume what the blocked one should produce.
- On `AMENDED`: re-read the amended task and the new log row, redo unticked tasks from the first affected one, and re-run their checks.
- On `ESCALATED`: the phase restarts from the re-approved plan revision; earlier review and test evidence for touched code does not carry over.

## 7. Round cap

- A task that needs a third request, or an amendment contested twice by the same role, goes to the user via the coordinator whatever its class. Reason: repeated amendments mean the design premise is wrong, not the detail.
- A review that reaches its 3-round cap for a plan reason raises one request; it is never closed by lowering a finding.
