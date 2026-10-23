---
name: receiving-review
description: How the Code Writer (and the Docs Writer for document reviews) handles a CHANGES_REQUESTED review - read every finding, restate and verify each against the code, clarify all unclear items before fixing any, fix one finding at a time with a test where it is a defect, push back with evidence, escalate findings that collide with a D-NN or the plan, and reply per finding with FIXED / DISPUTED / RAISED. Use whenever a review verdict comes back CHANGES_REQUESTED, or a Test Runner defect comes back for the owning phase, before editing anything.
---

# Receiving Review

Answer one question per finding: **is it true for this code and this approved plan, and what is the evidence?** Technical correctness beats social comfort: no performative agreement, no silent disagreement, no blind implementation. The reviewer never edits code; every change is yours and lands as a new revision.

## 1. Read everything first

Read the whole review before touching code: verdict, every finding (`RV-NN`, severity `BLOCKER` / `MAJOR` / `MINOR`, `CONFIRMED` / `PLAUSIBLE`, file:line, failure scenario, fix direction) and the round number. Findings are often related; fixing the first one before reading the rest invites a wrong fix.

## 2. Restate and verify each finding

For every finding, write one line in your own words: what is wrong, under which input or state. Then check it against the code at the reviewed revision:

| Check | How |
|---|---|
| Does the failure path exist? | Trace from the entry point to the line; run the existing test or the reviewer's scenario where a command can decide it |
| Is it a defect or a preference? | Defect = wrong result, crash, leak, security hole, AC broken. Preference without a failure = not a blocker |
| Does the fix direction break something? | Read callers of the touched symbol; check other tasks' Consumes / Produces |
| Does it contradict a decision? | Compare with every `D-NN`, Global constraints, Review focus and the task's Scope / Files |

`PLAUSIBLE` findings name the evidence that would confirm them: get that evidence, do not guess.

## 3. Clarify before implementing any

If any finding is unclear (you cannot restate it, or cannot tell which code or AC it means), **stop and implement nothing yet**. Send the questions for all unclear items at once through the coordinator, listing which items you did understand. Partial understanding produces fixes the next round rejects.

## 4. Decide per finding

| Situation | Reply | Action |
|---|---|---|
| Verified defect inside the approved scope | `FIXED` | Fix it (step 5) |
| Wrong for this code, or a preference with no failure | `DISPUTED` | Give technical evidence: traced path, command output, the guard that prevents it, the `D-NN` it would violate |
| Fix needs to change a frozen item (goal, AC mapping, phase outcomes, Global constraints, Review focus, any `D-NN`), the file list, or a dependency | `RAISED` | `plan-change-request`; do **not** fix silently |
| Cannot verify without missing access or information | `RAISED` | `NEEDS_CONTEXT` naming exactly what is needed |

Reply words are defined in [handoff-and-status](../work-item-contract/references/handoff-and-status.md) §3. `ESCALATED` is Planning's answer to a `PCR-NN`, never a reply to a finding.

Never agree in words and leave the code unchanged; never change the code while disputing in words. If you disputed and then find the reviewer was right, say so in one factual line and fix it.

## 5. Fix one finding at a time

Order: `BLOCKER`, then `MAJOR`, then cheap `MINOR`s. For each:

1. A defect gets a test that fails before the fix and passes after (`root-cause-debugging` step 5, `test-first`). For documents, the equivalent is the validator or check that would catch it.
2. Apply the smallest fix inside the task's Scope / Files; no drive-by refactors.
3. Rerun the covering checks and record evidence rows (`evidence-before-claims`).
4. Then the next finding. Batching several fixes makes a failed check ambiguous.

After all fixes, rerun the task checks of every task the change touched and your `bug-hunt` self-check at `quick`.

## 6. Reply per finding

| Finding | Restated | Reply | Revision | Evidence |
|---|---|---|---|---|
| `RV-03` | Empty page returns stale items when the filter changes | `FIXED` | `<new SHA>` | Regression test FAIL before / PASS after; task check exit 0 |
| `RV-04` | Asks to cache the lookup | `DISPUTED` | - | `D-07` forbids caching this data; trace shows one call per request |
| `RV-05` | Rename public field | `RAISED` | - | Changes the contract in `D-04`; plan-change-request PCR-02 |

No thanks, no praise, no apology: the reply states facts. Put the table in the new revision's `writer-handoff.md` under `## Review reply (round N)` and return `READY_FOR_REVIEW` with the new committed revision and an optional Concerns list. The reviewer re-judges each `DISPUTED` row on its evidence and keeps the finding with the same ID or withdraws it with the reason. Formats: [handoff-and-status](../work-item-contract/references/handoff-and-status.md).

## 7. Revisions and the round cap

- The fix is a **new revision**. Evidence recorded on the old revision for touched code (review, task checks, test results) is invalid; list which evidence must be rerun.
- The reviewer re-reviews the whole phase scope affected by the fix, not only your reply.
- **Test Runner defects** (`DEF-NN`) use the same table and steps. The fix is made under the phase that owns the failing AC, inside its Scope / Files, through `root-cause-debugging`, and counts toward that phase's cap ([handoff-and-status](../work-item-contract/references/handoff-and-status.md) §2, Test Runner defect).
- **3 review rounds on the same phase** is the cap. If round 3 still returns `CHANGES_REQUESTED`, do not start a fourth fix: report both positions per open finding to the coordinator, who escalates to Planning (`plan-change-request`) or the user. Neither you nor the reviewer may waive a finding.
