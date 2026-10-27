---
name: bug-squad
description: "Entry point for a user-reported bug in built behavior — the coordinator has bug_fixer reproduce it and find the root cause, proposes a severity (S1-S4) and a fix level (L1 quick patch, L2 local fix, L3 escalate), gets the user's confirmation, then routes L1 to bug_fixer and test_runner without code review, L2 to bug_fixer, code_reviewer and test_runner, and L3 to dev-team with an escalation report. Use when the user reports something broken and wants it fixed, supplies a bug ticket, or says things like 'fix bug', 'sửa lỗi', 'bị bug', 'lỗi này', 'app bị crash', even if they do not say 'defect'. Not for a failing check inside a planned phase (that is the Code Writer's root-cause debugging) and not for new or changed behavior (that is dev-team)."
---

# Bug Squad

Act as the **coordinator** for one reported bug, the way `dev-team` coordinates a work item. The folder layout, severity/fix scales, routing rules, status words, and hand-offs are defined once in `work-item-contract` (`references/debug-item-contract.md` and `references/handoff-and-status.md`); this skill decides **who runs when** and never restates them.

Coordinate three agent profiles and one skill:

- **`bug_fixer`**: reproduces the bug, finds the root cause and call-graph impact, proposes `S1–S4` and `L1/L2/L3`, writes the debug documents with `fix-planning`, and implements L1/L2 fixes.
- **`code_reviewer`**: reviews an L2 fix (`review-workflow`) before it goes to `test_runner`.
- **`test_runner`**: verifies an L1/L2 fix independently against the bug folder and fix revision.
- **`dev-team`**: takes over an L3 bug as a full work item (`Zero-Re-Ask Handoff` via `escalation-report.md`).

The coordinator never edits code, never chooses a level for the user, and never starts a fix before the user confirms the triage level.

## 1. Three Entry Paths & Intake (Zero Code Edits on Intake)

`bug-squad` accepts a bug through one of three entry paths:

1. **Path A — Direct User Report or Huly Bug Ticket**: The user reports broken behavior directly or supplies a `<PROJECT>-<NUMBER>` ticket (`bug_fixer` uses `huly-task-intake` `coder-nexus huly task-detail <TICKET> --download` to fetch the description, reproduction steps, and attachments).
2. **Path B — From `debug-investigation` (`diagnosis.md` Zero-Re-Ask Handoff)**: When `debug-investigation` returns `DIAGNOSED` and the user confirms fixing it now, pass `.superpowers/debug/<slug>/diagnosis.md` directly to `bug_fixer` (`debug-item-contract` §8, "From diagnosis to fix"). `bug_fixer` copies the verified scenario (`## 2`), root cause (`## 5`), and impact (`## 6`) into `brief.md` (`## 1`–`## 5`) without re-asking the user or repeating the investigation, and proceeds directly to proposing `## 6. Level decision` (`TRIAGED`).
3. **Path C — From `feature-testing` (`test-run-report.md` Zero-Re-Ask Handoff)**: When `feature-testing` returns `COMPLETED` with `FAIL` cases and the user asks to fix a `FAIL` case, pass the `FAIL` row (steps, expected vs actual, evidence path) from `.superpowers/test-runs/<slug>/test-run-report.md` directly to `bug_fixer` without re-asking.

### Intake Steps

1. Create `.superpowers/debug/<bug-slug>/` (`debug-item-contract` §1). If a closed folder for the same bug exists, open a new one that links it.
2. Run `git-preflight` Step A (read-only) to record the current branch and `BASE_REVISION`. Note where the bug was found (`DEV` / `STG` / `PROD`); when the report, ticket, or handoff does not say, ask it as the first question.
3. Assign `bug_fixer` in **Stage A — Triage Mode (`brief.md` `## 1`–`## 6` only)** with the entry-path inputs and environment. No production code is modified and no fix branch is created during Intake/Triage.

## 2. The 4-Gate Anti-Rush Sequence (Hard Gate Before Any Fix)

`bug_fixer` and the coordinator enforce four sequential gates so no agent ever jumps straight from a bug report to editing code:

| Gate | Requirement | Outcome if Unmet |
|---|---|---|
| **Gate 1: Scenario & Red Reproduction** | Reproduce the exact failure first via a failing automated test (`Red run`, kept uncommitted during triage) or a real runtime/UI/API run with saved evidence (`brief.md` → `## 3`). | Record every attempt in `brief.md` → `## 3` and return `NOT_REPRODUCED`. Stop immediately; never guess a fix. |
| **Gate 2: Evidence-Backed Root Cause & Call-Graph Impact** | Prove the exact `file:line` mechanism (`{{slot:root-cause-debugging}}`, git forensics, temporary `[DBG-<slug>]` logs removed before returning) in `## 4` and trace all direct/indirect callers (`gitnexus` MCP + `rg -n`) in `## 5`. | If the root cause cannot be proven with evidence or blast radius crosses L3 boundaries, classify as **L3**. |
| **Gate 3: `S1–S4` & `L1/L2/L3` Classification + User Confirmation** | `bug_fixer` writes `brief.md` → `## 6. Level decision` (`User confirmation: PENDING`) and returns `TRIAGED`. Coordinator asks the user via `ask_question` with the proposed `(S, L)` first as `(Recommended)`. | No fix branch is created and zero production code is modified while `User confirmation` is `PENDING`. |
| **Gate 4: Level-Routed Fix & Independent Verification** | Only after user confirmation: execute L1 (`bug_fixer` → `test_runner`), L2 (`bug_fixer` → `code_reviewer` → `test_runner`), or L3 (`escalation-report.md` → `dev-team`). | Any scope growth beyond `## 7` or hit on an L3 floor halts coding and returns `TRIAGED` for re-confirmation. |

## 3. Routing (coordinator only)

| `bug_fixer` / `code_reviewer` / `test_runner` returns | Coordinator does |
|---|---|
| `NOT_REPRODUCED` | Show the attempts from `brief.md` → `## 3`; ask the user for the missing information (steps, data, environment, a recording) or to close the bug. A new answer restarts §1 step 3. |
| `TRIAGED` | Ask **one** question (`ask_question`): the proposed S and L first as `(Recommended)`, with the matched conditions and floors; the other levels as alternatives. Record the answer in `brief.md` → `## 6. Level decision`. Then go to §4 (L1/L2) or §5 (L3). |
| `READY_FOR_TEST` | Check that `brief.md` records a confirmed **L1** and that the evidence rows exist; assign `test_runner` on the fix revision with the bug folder as its input. |
| `READY_FOR_REVIEW` | Check that `brief.md` records a confirmed **L2**, that every `fixing-plan.md` task is ticked, and that the evidence rows exist; assign `code_reviewer` on `BASE_REVISION..FIX_REVISION` with the bug folder as its input. |
| `APPROVED` (review) | Record it in `brief.md` → `## 10` → **Code review (L2)**; assign `test_runner` on the same `FIX_REVISION`. |
| `CHANGES_REQUESTED` (review) | Record the round in `brief.md` → `## 10` → **Code review (L2)**. Rounds 1–2: return the report to `bug_fixer`, which answers with `review-resolution` on a new revision. Round 3: apply `debug-item-contract` §3 rule 9 — `bug_fixer` re-triages and returns `TRIAGED`; ask the user to confirm. |
| `VERIFIED_FIXED` | Report to the user: root cause, fix revision, evidence path. Offer the commit / PR step of `git-preflight`; never merge to a protected branch, tag, or deploy. Close the bug. |
| `STILL_BROKEN` | Count the round in `brief.md` → `## 10`. Rounds 1–2: return the test report to `bug_fixer`; for L2 its new revision goes through review again (`debug-item-contract` §3 rule 9). Round 3: apply `debug-item-contract` §3 rule 4 — `bug_fixer` re-triages as L3 and returns `TRIAGED`; ask the user to confirm. |
| `ESCALATED` | Start `dev-team` Phase 1 with `escalation-report.md` as a supplied source (`Zero-Re-Ask Handoff`). This bug's flow ends here. |
| `BLOCKED` | Resolve the named blocker (environment, access, an answer) before re-assigning. Re-assigning unchanged repeats the failure. |

## 4. L1 / L2 fix (only after Gate 3 user confirmation)

1. **Branch**: follow `git-preflight` Steps C–F with the base for where the bug was found. An `S1` or `S2` bug found in `PROD` takes the hotfix base (`debug-item-contract` §2). Record the branch in `brief.md` → **Branch**; a debug item has no `codebase-notes.md`, so no `D-NN` is written.
2. **Plan**: `bug_fixer` completes `brief.md` → `## 7`–`## 9` with `fix-planning`; for L2 it also writes `fixing-plan.md`. Task 1 is always adding/running the failing regression test (`Red` before the fix, `Green` after). Show the plan to the user only when the fix grew beyond the confirmed level (`debug-item-contract` §3 rule 7).
3. **Fix**: `bug_fixer` executes the tasks in order within `## 7 Scope / Files`. If scope expands beyond the confirmed level or hits an L3 floor during coding, `bug_fixer` stops immediately and returns `TRIAGED` (`debug-item-contract` §3 rule 7). Otherwise it returns `READY_FOR_TEST` (L1), `READY_FOR_REVIEW` (L2), or `BLOCKED`.
4. **Review (L2 only)**: `code_reviewer` returns `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED` (§3).
5. **Verify**: `test_runner` returns `VERIFIED_FIXED` or `STILL_BROKEN` (§3).

**No code review for L1.** An L1 fix skips `code_reviewer` by design: the change is trivial, the user confirmed its size, and four checks stay mandatory (`debug-item-contract` §6: regression test Red → Green, original reproduction check, `{{slot:verification}}`, and `{{slot:bug-hunt}}` in `quick` mode). Reason: a review round on a one-line fix costs more than the risk it removes. **L2 is reviewed**: it crosses layers and runs several tasks, and the test run sees behavior, not code in the wrong layer, a security gap, or an untested path.

## 5. L3 escalation

1. `bug_fixer` writes `escalation-report.md` from its template with zero production code changes (any uncommitted triage test from `brief.md` → `## 3` is quoted in the report and removed from the working tree) and returns `ESCALATED`. No fix branch is created; `dev-team` decides the branch after its Gate 1.
2. Start `dev-team` Phase 1 with `escalation-report.md` as a supplied source (`Zero-Re-Ask Handoff`). Spec Writer reads it directly without re-asking the user and settles the job type: `bugfix` when behavior must be restored, `feature` with `change-impact.md` when it must change.

## 6. Never

- Never skip reproduction, guess a fix for an unreproduced bug, or modify production code before the user confirms the level in Gate 3.
- Never merge, tag, or deploy; that stays with the user (`git-preflight`).
- Never route a behavior change through L1/L2 (`debug-item-contract` §3 rule 1).
- Never count `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` as `VERIFIED_FIXED`.
