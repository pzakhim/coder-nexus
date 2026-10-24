---
name: fix-planning
description: How bug_fixer writes the debug documents of defect-resolution - brief.md for every bug (symptom, expected vs actual, reproduction, root cause, impact, level proposal, scope, tasks, regression test) and fixing-plan.md for an L2 fix, including the Review focus the Code Reviewer checks, plus diagnosis.md for an investigation - from the work-item-contract templates, with checks taken from the stack's verification and unit-testing skills. Use whenever bug_fixer triages a reported bug, plans its fix or writes up an investigation.
---

# Fix planning

Fill [bug-brief.md.tpl](../work-item-contract/templates/bug-brief.md.tpl) and, for L2, [fixing-plan.md.tpl](../work-item-contract/templates/fixing-plan.md.tpl) in `.superpowers/debug/<bug-slug>/`. The levels, routing rules and status words are in [debug-item-contract](../work-item-contract/references/debug-item-contract.md); the task fields and their **Expected** rules are in [plan-and-task-contract](../work-item-contract/references/plan-and-task-contract.md) §2. This skill says how to fill each part well; it does not redefine them. Keep every template heading.

## 1. When each part is written

| Moment | Parts | Ends with |
|---|---|---|
| Triage | `brief.md` → `## 1`–`## 6` | `NOT_REPRODUCED` or `TRIAGED` |
| After the user confirms L1 or L2 | `brief.md` → `## 7`–`## 9`; `fixing-plan.md` for L2 | the first task starts |
| After the fix | `brief.md` → `## 10` | `READY_FOR_TEST` (L1) or `READY_FOR_REVIEW` (L2) |
| After `CHANGES_REQUESTED` (L2) | the fix on a new revision, `## Plan change log` when a task changes, `## 10` | `READY_FOR_REVIEW` again (contract §3 rule 9) |

## 2. Triage parts

| Part | Write it so that | Reason |
|---|---|---|
| `## 2` Expected | It cites its source: an `AC-NN` or `BR-NN` of an approved spec, a `D-NN`, or the user's own statement. No source, or sources that disagree → the spec does not say what is correct, which is L3. | The fix restores a known behavior; it never invents one. |
| `## 3` Reproduction | Prefer an automated check that fails for the reported reason (`{{slot:unit-testing}}`); otherwise exact manual steps with captured evidence. Run it before any code change and record the red result; keep the test uncommitted until the level is confirmed (contract §3 rule 8). When it does not reproduce, list every attempt (steps, data, environment) and return `NOT_REPRODUCED`. | A fix without a red run proves nothing. |
| `## 4` Root cause | Name the file and line and the mechanism that turns the input into the actual behavior, with the evidence that confirms it (`{{slot:root-cause-debugging}}`). If it is still a hypothesis, write "not confirmed" and the hypotheses tested. | An unconfirmed cause is L3 (contract §3). |
| `## 5` Impact | Search the callers and consumers of every symbol the fix would touch; one row per affected screen, flow, API, data store or shared code, each with a path and line. An empty table records the search commands that found nothing. | Impact decides the level; a guess here becomes a wrong level. |
| `## 6` Level decision | Quote the matched contract conditions and floors word for word; take the higher level when in doubt. Leave **User confirmation** as `PENDING`. | The user confirms against the same words the rules use. |

## 3. Fix parts (after confirmation)

- **`## 7` Scope / Files**: the exact files the fix creates or modifies, including the regression test. Nothing outside this list is edited; needing another file is contract §3 rule 7.
- **`## 9` Regression test**: written first, in the test location `{{slot:unit-testing}}` names. State the red run and why it fails, then the green run.
- **Tasks** (`brief.md` → `## 8` for L1, `fixing-plan.md` → `## Tasks` for L2), in the task format of `plan-and-task-contract` §2:
  - The first task adds the failing regression test; the last task re-runs the reproduction check.
  - One deliverable with its own check per task. L1 usually needs two or three tasks; an L2 that needs more than about six tasks is likely L3.
  - **Acceptance Criteria** and **Expected** use the commands of `{{slot:verification}}` and `{{slot:unit-testing}}` on the touched paths; Expected comes from `## 2`, never from what the current code prints.
- **`fixing-plan.md`** (L2): `## Global constraints` lists the files in scope, the neighbour code that must not change and the floors near the fix, taken from `## 5`. `## Final checks` repeats the reproduction check, the regression test and the stack's verification. A change after confirmation goes in `## Plan change log`; one that crosses a level returns `TRIAGED`.
- **`## Review focus`** (L2): what the Code Reviewer must check on purpose because tests may not show it, one line each with its reason, taken from `## 5` Impact and `## Global constraints`: every layer the fix crosses, shared or nearby code it calls but must not change, floors next to the fix, paths with no test, and any input, permission or data-scope handling touched. Reason: the reviewer reads one revision cold; this list keeps it on the risks of this fix instead of a generic pass.

## 4. Self-check before returning

- `TRIAGED`: `## 1`–`## 6` filled; the red reproduction run has an evidence row; every impact row has a path; the proposal quotes the contract.
- `READY_FOR_TEST`: every task ticked on `MATCH`; the regression test is red before and green after; the reproduction check passes; the self `{{slot:bug-hunt}}` at `quick` is recorded in `## 10`; only files listed in `## 7` changed.
- `READY_FOR_REVIEW` (L2): everything required for `READY_FOR_TEST`, plus every `fixing-plan.md` task ticked and `## Review focus` filled; from round 2, each review finding answered with `review-resolution` (`FIXED` with evidence, `DISPUTED` with technical evidence, or `RAISED`) in `evidence/<FIX_REVISION>/review-reply.md`.

## 5. Diagnosis (investigation items)

Fill [diagnosis.md.tpl](../work-item-contract/templates/diagnosis.md.tpl); the rules are in [debug-item-contract](../work-item-contract/references/debug-item-contract.md) §8.

| Part | Write it so that | Reason |
|---|---|---|
| `## 1` Question | A bug states expected and actual with the source of the expected; a trace states exactly what the user wants to understand. | The report answers the question asked, not a nearby one. |
| `## 2` Scenario | Steps or a check someone else can re-run on the same revision. | A finding that cannot be re-run cannot be trusted. |
| `## 3` Temporary instrumentation | Every inserted statement with file and line, the state before, and the same state after removal. | Proves nothing was left behind. |
| `## 4` Captured output | Only the lines that support a finding, masked, each with its evidence path. | Raw dumps hide the signal and may leak data. |
| `## 5` Findings | Bug: root cause with file, line and mechanism, or "not confirmed" with the hypotheses tested (`{{slot:root-cause-debugging}}`). Trace: the observed flow step by step, each step backed by a captured line. | Observation, not reading of the code, is what this item adds. |
| `## 6` Impact | For a bug, the same search as `brief.md` → `## 5`; for a trace, `none` unless the flow touches shared code. | A later fix reuses it without a second search. |
| `## 7` Next step | Fix through `defect-resolution`, no action, or the open questions. No fix level. | The level belongs to the fix flow and the user. |
