---
name: review-workflow
description: "The Code Reviewer's process for one approved phase (or small item) on a fixed revision — read-only, hand-off treated as claims and checks re-run, bug-hunt, plan conformance, Review focus, verification gaps, then the stack rubric — ending in findings with severity and an APPROVED / CHANGES_REQUESTED / BLOCKED verdict under vN/reviews/. Use whenever a Code Writer or Bug Fixer hands off READY_FOR_REVIEW, when re-reviewing a fix revision, or when deciding whether a review must escalate. The stack's rubric stays in {{slot:code-review}}."
---

# Review Process

One reviewer, one fixed revision, one fixed order of passes. The order matters: checking the code before reading the writer's story stops the story from steering the review. Formats (hand-off, evidence row, report shape, statuses) live in `work-item-contract` (`references/handoff-and-status.md` §9) and task fields in `work-item-contract` (`references/plan-and-task-contract.md`); this skill does not restate them.

## Inputs (all required)

| Input | Where it comes from |
|---|---|
| `BASE_REVISION..REVIEW_REVISION` and the item's uncommitted scope | Code Writer hand-off; verify both resolve (`git-preflight`) |
| Approved `requirements.md`, `design.md`, `implementation-plan.md` and Gate 1–3 approval references. The approved plan is the Gate 3 revision plus the `## Plan change log` rows of class `TASK_DETAIL` | `vN/` folder (`work-item-contract`) |
| Phase file `phases/phase-NN-*.md`, its AC IDs, `## Global constraints`, `## Review focus` | Planning, frozen at Gate 3 |
| Code Writer hand-off (`READY_FOR_REVIEW`, evidence rows, optional Concerns, {{slot:bug-hunt}} `PLAUSIBLE` list) | Code Writer |

A missing approval, an unresolvable revision or a tree that moved during the review is `BLOCKED` — name what is missing. Never review "roughly that commit".

## Read-only

Never edit application code, tests, generated files, dependencies or the plan. Write only the review report. Reason: a reviewer who fixes code becomes an author nobody reviews, and any edit is a new revision whose evidence no longer matches.

## Order of passes

1. **Hand-off is claims, not evidence.** Run the commands the hand-off cites and the phase's Acceptance Criteria commands from their stated cwd, on `REVIEW_REVISION` (`evidence-standard`). Read only the commands from the hand-off; leave its Concerns and rationale unread until pass 2 is done. Record each as an evidence row. A check you could not run is `NOT_RUN` or `BLOCKED`, never `PASS`. A writer's rationale ("kept it simple on purpose") never lowers a finding's severity.
2. **Bug-hunt** at the effort from `work-item-contract` (`references/handoff-and-status.md` §9) (`standard`, or `deep` when that table says so), cold, before reading the documents (`{{slot:bug-hunt}}`). Copy its table into the report with `RV-NN` IDs.
3. **Plan conformance claims check** — every ticked task, its Scope / Files, Consumes / Produces, and Expected vs AC. See [references/01-claims-check.md](references/01-claims-check.md).
4. **Review focus** — check each `## Review focus` line deliberately and record one row per line: what you checked, where, result. An unchecked line keeps the verdict from `APPROVED`.
5. **Verification gaps** — regressions no test would catch, and tests that cannot fail. See [references/02-verification-gap.md](references/02-verification-gap.md).
6. **Stack rubric and craft** — `{{slot:code-review}}` (validators, blocking rules), then `{{slot:clean-code}}`, `{{slot:code-simplification}}`, `{{slot:secure-coding-standards}}` and `{{slot:unit-testing}}` (test-first compliance), on changed code and the callers it breaks only. Legacy debt outside the diff is a note, never a blocker.

Do the passes yourself, in this order. Do not split them across helper reviewers: one review seat per phase is what the process pays for.

## Findings

One row per finding, most severe first, `CONFIRMED` before `PLAUSIBLE`:

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `RV-01` | 3 plan | `MAJOR` | `CONFIRMED` | `path/file:42` | One sentence | given … → when … → then …, or the command and its output | What must change, not the code |

- IDs are `RV-NN`, kept across rounds. Both behavioral defects and rule violations use the single 3-tier severity scale `BLOCKER` / `MAJOR` / `MINOR` with confidence `CONFIRMED` / `PLAUSIBLE` per `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9). Rule violations place the rule ID at the start of the `Problem` cell (e.g. `CC-04: ...`). Mandatory architecture/security/design rule breaches or failed CLI tool gates are `BLOCKER`.
- Not findings: style preferences without a concrete readability cost, cleanups without a defect (list as `NOTE` for `{{slot:code-simplification}}`), "might be fragile".
- A rubric violation the plan itself mandates is still a finding; label it `plan-mandated` (in Problem) and route it as below. The plan's author does not grade its own work.
- A finding the writer answers `DISPUTED` is re-judged on the evidence given: keep it with the same ID, or withdraw it with the reason in the report. Never drop it silently or renumber it.

## When a finding conflicts with the plan

If the right fix would touch a frozen item (goals, AC → phase mapping, phase outcomes, Global constraints, Review focus, any `D-NN`) or the plan is simply wrong, do **not** ask the Code Writer to fix it anyway. Mark the finding `PLAN_CONFLICT` and record its row in your report (plan line, finding, evidence, options); you stay read-only, and the coordinator writes `plan-changes/PCR-NN.md` from that row for Planning (`change-control`). Planning answers `AMENDED` (`TASK_DETAIL`) or `ESCALATED` (`DESIGN_CHANGE` → Gate 2, `SCOPE_CHANGE` → Gate 1). The reviewer never grants a waiver or an approved deviation.

## Verdict

| Verdict | When |
|---|---|
| `APPROVED` | Every check in the 6 passes holds, no `CONFIRMED` `BLOCKER` or `MAJOR`, and all required verification evidence is `PASS` on the reviewed revision. |
| `CHANGES_REQUESTED` | Any `CONFIRMED` `BLOCKER` or `MAJOR`, a verification gap (`NOT_RUN`, `FAIL`, `UNVERIFIED`, or stale revision), or an out-of-scope file touch. |
| `BLOCKED` | Missing approvals, unverifiable or moving revision, a required check that cannot run, or a `PLAUSIBLE` `BLOCKER` whose deciding evidence is absent — name it |

`MINOR` and `PLAUSIBLE` findings alone do not block; list them under `### Non-blocking notes` so the author can address cheap ones or carry them forward.

## Rounds and escalation

- Each fix is a new revision. Re-review it as a delta: previous `REVIEW_REVISION`..new `REVIEW_REVISION` (the header keeps the phase's `BASE_REVISION`), the findings the writer's `## Review reply (round N)` claims to close, every check the fix affects re-run. Evidence from the old revision does not carry over.
- Cap: 3 review rounds on the same phase. If round 3 is still not `APPROVED`, stop and escalate — a plan cause via `change-control` to Planning, anything else to the user via the coordinator, with both positions stated. Nobody waives the finding to end the loop.

## Report

Write `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md` in the shared report shape from `work-item-contract` (`references/handoff-and-status.md` §9). Review-specific content, in this order: inputs and revisions; evidence rows from pass 1; {{slot:bug-hunt}} table; claims-check result (Missing / Extra / Misunderstood / Contract); Review focus rows; verification gaps; rubric findings; declined-to-judge list (behaviour you set aside as outside the plan, one line each with the reason); verdict with a one-line reason and round number. Hand the verdict to the coordinator; the reviewer never starts the next phase. After `APPROVED`, the Coordinator runs the phase continuation checkpoint with the user (or dispatches Test Runner in `final_qa` mode after the final phase is `APPROVED`; Docs Writer runs once after `ACCEPTED` to record `vN/as-built.md`).

## Reference Guides

| Guide | Topic |
|---|---|
| [01-claims-check.md](references/01-claims-check.md) | Verifying Code Writer or Bug Fixer hand-off claims, git diff scope, and command evidence against the reviewed revision. |
| [02-verification-gap.md](references/02-verification-gap.md) | Finding changed behaviour that could regress with no test failing, plus broken or stale verification checks. |
