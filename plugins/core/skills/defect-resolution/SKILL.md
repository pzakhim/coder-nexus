---
name: defect-resolution
description: Entry point for a user-reported bug in built behavior - the coordinator has bug_fixer reproduce it and find the root cause, proposes a severity (S1-S4) and a fix level (L1 quick patch, L2 local fix, L3 escalate), gets the user's confirmation, then routes L1 to bug_fixer and test_runner without code review, L2 to bug_fixer, code_reviewer and test_runner, and L3 to dev-team with an escalation report. Use when the user reports something broken and wants it fixed, or says things like "fix bug", "sửa lỗi", "bị bug", "lỗi này", "app bị crash", even if they do not say "defect". Not for a failing check inside a planned phase (that is the Code Writer's root-cause debugging) and not for new or changed behavior (that is dev-team).
---

# Defect resolution

Act as the **coordinator** for one reported bug, the way `dev-team` coordinates a work item. The folder, scales, routing rules, status words and hand-offs are defined once in `work-item-contract` → [debug-item-contract](../work-item-contract/references/debug-item-contract.md); this skill decides **who runs when** and never restates them.

Coordinate three agent profiles and one skill:

- **`bug_fixer`**: reproduces, finds the root cause, proposes the levels, writes the debug documents, fixes L1/L2.
- **`code_reviewer`**: reviews an L2 fix before it is tested.
- **`test_runner`**: verifies an L1/L2 fix independently.
- **`dev-team`**: takes over an L3 bug as a work item.

The coordinator never edits code, never decides a level for the user and never starts a fix before the level is confirmed.

## 1. Intake

1. Create `.superpowers/debug/<bug-slug>/` (contract §1). If a folder for the same bug exists and is closed, open a new one that links it.
2. Run `git-preflight` Step A (read-only). Note where the bug was found (DEV / STG / PROD); when the report does not say, ask it as the first question.
3. Start `bug_fixer` with the user's report, the ticket if any, and the environment, plus `diagnosis.md` when `debug-investigation` already diagnosed this bug (contract §8, "From diagnosis to fix"). It writes `brief.md` → `## 1`–`## 6` with `fix-planning` and returns one status.

## 2. Routing (coordinator only)

| `bug_fixer` / `code_reviewer` / `test_runner` returns | Coordinator does |
|---|---|
| `NOT_REPRODUCED` | Show the attempts from `brief.md` → `## 3`; ask the user for the missing information (steps, data, environment, a recording) or to close the bug. A new answer restarts §1 step 3. |
| `TRIAGED` | Ask **one** question (`ask_question`): the proposed S and L first as "(Recommended)", with the matched conditions and floors; the other levels as alternatives. Record the answer in `brief.md` → `## 6. Level decision`. Then go to §3 (L1/L2) or §4 (L3). |
| `READY_FOR_TEST` | Check that `brief.md` records a confirmed **L1** and that the evidence rows exist; assign `test_runner` on the fix revision with the bug folder as its input. |
| `READY_FOR_REVIEW` | Check that `brief.md` records a confirmed **L2**, that every `fixing-plan.md` task is ticked and the evidence rows exist; assign `code_reviewer` on `BASE_REVISION..FIX_REVISION` with the bug folder as its input. |
| `APPROVED` (review) | Record it in `brief.md` → `## 10` → **Code review (L2)**; assign `test_runner` on the same `FIX_REVISION`. |
| `CHANGES_REQUESTED` (review) | Record the round in `brief.md` → `## 10` → **Code review (L2)**. Rounds 1–2: return the report to `bug_fixer`, which answers with `review-resolution` on a new revision. Round 3: apply contract §3 rule 9 - `bug_fixer` re-triages and returns `TRIAGED`; ask the user to confirm. |
| `VERIFIED_FIXED` | Report to the user: root cause, fix revision, evidence path. Offer the commit / PR step of `git-preflight`; never merge to a protected branch, tag or deploy. Close the bug. |
| `STILL_BROKEN` | Count the round in `brief.md` → `## 10`. Rounds 1–2: return the test report to `bug_fixer`; for L2 its new revision goes through review again (contract §3 rule 9). Round 3: apply contract §3 rule 4 - `bug_fixer` re-triages as L3 and returns `TRIAGED`; ask the user to confirm. |
| `ESCALATED` | Start `dev-team` with `escalation-report.md` as a supplied source (see `dev-team` Phase 1). This bug's flow ends here. |
| `BLOCKED` | Resolve the named blocker (environment, access, an answer) before re-assigning. Re-assigning unchanged repeats the failure. |

## 3. L1 / L2 fix

1. **Branch**: follow `git-preflight` Steps C–F with the base for where the bug was found. An S1 or S2 bug found in PROD takes the hotfix base (contract §2). Record the branch in `brief.md` → **Branch**; a debug item has no `codebase-notes.md`, so no `D-NN` is written.
2. **Plan**: `bug_fixer` completes `brief.md` → `## 7`–`## 9` with `fix-planning`; for L2 it also writes `fixing-plan.md`. Show the plan to the user only when the fix grew beyond the confirmed level (contract §3 rule 7).
3. **Fix**: `bug_fixer` runs the tasks in order and returns `READY_FOR_TEST` (L1), `READY_FOR_REVIEW` (L2), `TRIAGED` (level grew) or `BLOCKED`.
4. **Review (L2 only)**: `code_reviewer` returns `APPROVED`, `CHANGES_REQUESTED` or `BLOCKED` (§2).
5. **Verify**: `test_runner` returns `VERIFIED_FIXED` or `STILL_BROKEN` (§2).

**No code review for L1.** An L1 fix skips the Code Reviewer by design: the change is trivial, the user confirmed its size, and four checks stay mandatory (contract §6). Reason: a review round on a one-line fix costs more than the risk it removes. **L2 is reviewed**: it crosses layers and runs several tasks, and the test run sees behavior, not code in the wrong layer, a security gap or an untested path.

## 4. L3 escalation

1. `bug_fixer` writes `escalation-report.md` from its template and returns `ESCALATED`. No code is changed and no branch is created; `dev-team` decides the branch after its Gate 1.
2. Start `dev-team` with the report. Spec Writer reads it as a source and settles the job type: `bugfix` when behavior must be restored, `feature` with `change-impact.md` when it must change.

## 5. Never

- Skip reproduction, or ask the user to confirm a level for a bug that was not reproduced.
- Merge, tag or deploy; that stays with the user (`git-preflight`).
- Route a behavior change through L1/L2 (contract §3 rule 1).
- Count `NOT_RUN`, `BLOCKED` or `UNVERIFIED` as `VERIFIED_FIXED`.
