---
name: review-process
description: The Code Reviewer's process for one approved phase (or small item) on a fixed revision — read-only, hand-off treated as claims and checks re-run, bug-hunt, plan conformance, Review focus, verification gaps, then the stack rubric — ending in findings with severity and an APPROVED / CHANGES_REQUESTED / BLOCKED verdict under vN/reviews/. Use whenever a Code Writer hands off READY_FOR_REVIEW, when re-reviewing a fix revision, or when deciding whether a review must escalate. The stack's rubric stays in {{slot:code-review}}.
---

# Review Process

One reviewer, one fixed revision, one fixed order of passes. The order matters: checking the code before reading the writer's story stops the story from steering the review. Formats (hand-off, evidence row, report shape, statuses) live in [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md) and task fields in [plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md); this skill does not restate them.

## Inputs (all required)

| Input | Where it comes from |
|---|---|
| `BASE_REVISION..REVIEW_REVISION` and the item's uncommitted scope | Code Writer hand-off; verify both resolve (`git-preflight`) |
| Approved `requirements.md`, `design.md`, `implementation-plan.md` and Gate 1–3 approval references. The approved plan is the Gate 3 revision plus the `## Plan change log` rows of class `TASK_DETAIL` | `vN/` folder (`work-item-contract`) |
| Phase file `phases/phase-NN-*.md`, its AC IDs, `## Global constraints`, `## Review focus` | Planning, frozen at Gate 3 |
| Code Writer hand-off (`READY_FOR_REVIEW`, evidence rows, optional Concerns, bug-hunt `PLAUSIBLE` list) | Code Writer |

A missing approval, an unresolvable revision or a tree that moved during the review is `BLOCKED` — name what is missing. Never review "roughly that commit".

## Read-only

Never edit application code, tests, generated files, dependencies or the plan. Write only the review report. Reason: a reviewer who fixes code becomes an author nobody reviews, and any edit is a new revision whose evidence no longer matches.

## Order of passes

1. **Hand-off is claims, not evidence.** Run the commands the hand-off cites and the phase's Acceptance Criteria commands from their stated cwd, on `REVIEW_REVISION` (`evidence-before-claims`). Read only the commands from the hand-off; leave its Concerns and rationale unread until pass 2 is done. Record each as an evidence row. A check you could not run is `NOT_RUN` or `BLOCKED`, never `PASS`. A writer's rationale ("kept it simple on purpose") never lowers a finding's severity.
2. **Bug-hunt** at `standard` effort (`deep` for the closing phase, auth/payment/data-migration code, or a phase already returned twice), cold, before reading the documents (`bug-hunt`). Copy its table into the report with `RV-NN` IDs.
3. **Plan conformance claims check** — every ticked task, its Scope / Files, Consumes / Produces, and Expected vs AC. See [claims-check.md](references/claims-check.md).
4. **Review focus** — check each `## Review focus` line deliberately and record one row per line: what you checked, where, result. An unchecked line keeps the verdict from `APPROVED`.
5. **Verification gaps** — regressions no test would catch, and tests that cannot fail. See [verification-gap.md](references/verification-gap.md).
6. **Stack rubric and craft** — `{{slot:code-review}}` (validators, blocking rules), then `clean-code` / `{{slot:clean-code}}`, `code-simplification`, `secure-coding` / `{{slot:secure-coding}}` and `test-first` compliance, on changed code and the callers it breaks only. Legacy debt outside the diff is a note, never a blocker.

Do the passes yourself, in this order. Do not split them across helper reviewers: one review seat per phase is what the process pays for.

## Findings

One row per finding, most severe first, `CONFIRMED` before `PLAUSIBLE`:

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `RV-01` | 3 plan | `MAJOR` | `CONFIRMED` | `path/file:42` | One sentence | given … → when … → then …, or the command and its output | What must change, not the code |

- IDs are `RV-NN`, kept across rounds. Severity is the `bug-hunt` scale: `BLOCKER` / `MAJOR` / `MINOR`. Confidence is `CONFIRMED` (traced end to end or shown by a command) or `PLAUSIBLE` (name the evidence that would decide it).
- Not findings: style preferences without a concrete readability cost, cleanups without a defect (list as `NOTE` for `code-simplification`), "might be fragile".
- A rubric violation the plan itself mandates is still a finding; label it `plan-mandated` (in Problem) and route it as below. The plan's author does not grade its own work.
- A finding the writer answers `DISPUTED` is re-judged on the evidence given: keep it with the same ID, or withdraw it with the reason in the report. Never drop it silently or renumber it.

## When a finding conflicts with the plan

If the right fix would touch a frozen item (goals, AC → phase mapping, phase outcomes, Global constraints, Review focus, any `D-NN`) or the plan is simply wrong, do **not** ask the Code Writer to fix it anyway. Mark the finding `PLAN_CONFLICT` and record its row in your report (plan line, finding, evidence, options); you stay read-only, and the coordinator writes `plan-changes/PCR-NN.md` from that row for Planning (`plan-change-request`). Planning answers `AMENDED` (`TASK_DETAIL`) or `ESCALATED` (`DESIGN_CHANGE` → Gate 2, `SCOPE_CHANGE` → Gate 1). The reviewer never grants a waiver or an approved deviation.

## Verdict

| Verdict | When |
|---|---|
| `APPROVED` | Every re-run check `PASS`; every phase AC traced to code and a passing check; no `CONFIRMED` `BLOCKER`/`MAJOR`; every Review focus line checked; validators of `{{slot:code-review}}` clean; visual evidence present when the phase has UI (`{{slot:visual-verification}}`) |
| `CHANGES_REQUESTED` | Any `CONFIRMED` `BLOCKER` or `MAJOR`, any failing check, a Missing / Extra / Misunderstood task, or an open `PLAN_CONFLICT` routed to Planning |
| `BLOCKED` | Missing approvals, unverifiable or moving revision, a required check that cannot run, or a `PLAUSIBLE` `BLOCKER` whose deciding evidence is absent — name it |

`MINOR` and other `PLAUSIBLE` findings alone do not block; list them for the writer, who answers through `receiving-review`.

## Rounds and escalation

- Each fix is a new revision. Re-review it as a delta: previous `REVIEW_REVISION`..new `REVIEW_REVISION` (the header keeps the phase's `BASE_REVISION`), the findings the writer's `## Review reply (round N)` claims to close, every check the fix affects re-run. Evidence from the old revision does not carry over.
- Cap: 3 review rounds on the same phase. If round 3 is still not `APPROVED`, stop and escalate — a plan cause via `plan-change-request` to Planning, anything else to the user via the coordinator, with both positions stated. Nobody waives the finding to end the loop.

## Report

Write `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md` in the shared report shape from [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md). Review-specific content, in this order: inputs and revisions; evidence rows from pass 1; bug-hunt table; claims-check result (Missing / Extra / Misunderstood / Contract); Review focus rows; verification gaps; rubric findings; declined-to-judge list (behaviour you set aside as outside the plan, one line each with the reason); verdict with a one-line reason and round number. Hand the verdict to the coordinator; the reviewer never starts the next phase. After `APPROVED` the Docs Writer records the phase; the Test Runner runs later (order in [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md) §2).

Sources and ideas not adopted: [references/sources.md](references/sources.md).
