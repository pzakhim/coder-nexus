# 01 — Checking the Author's Hand-off Claims

> Topic: Verifying Code Writer or Bug Fixer hand-off claims, git diff scope, and command evidence against the reviewed revision.

Run after `{{slot:bug-hunt}}`, so the cold read is already done and the plan cannot steer it. The phase file and the hand-off are the change's own account of itself: testimony, not evidence. A claim repeated in a code comment or a commit message is the same claim, not confirmation. Try to falsify each one against the code.

## What to compare

Read the phase file task by task (field names in `work-item-contract` (`references/plan-and-task-contract.md`) and hand-off rules in `work-item-contract` (`references/handoff-and-status.md` §2 and §9)) against the diff `BASE_REVISION..REVIEW_REVISION`.

| Check | Question | Finding when |
|---|---|---|
| **Ticked = built** | Does every ticked task have its code in the diff? | A ticked task with no matching hunk, or a listed file the diff never touches → `Missing` |
| **Nothing Missing** | Is every behaviour the task and its AC promise present? | A promised behaviour, error path or state absent or stubbed → `Missing` |
| **Nothing Extra** | Is every changed file inside some task's Scope / Files? Does every change serve an approved `G-NN`? | Out-of-scope file, unrequested feature, speculative hook or option → `Extra` |
| **Nothing Misunderstood** | Does the code produce the task's Expected result and satisfy the AC, not just something nearby? | Right feature built the wrong way, or Expected only met by a weakened check → `Misunderstood` |
| **Consumes / Produces** | Does each produced signature, type, route or key match what the plan says, and does each consumer use exactly what an earlier task produced? | Renamed, reshaped or nullable-where-not-promised contract → `Contract` |
| **Reused Components** | Is each mapped component used instead of a private re-implementation? | Raw substitute for a mapped component → `Contract` |
| **Global constraints** | Does every changed file honour each `## Global constraints` line? | Any violation → `Misunderstood` |
| **Decisions** | Does the code contradict any `D-NN`? | Contradiction → `Misunderstood` |
| **Order** | Were tasks done in order, and did the writer's Expected triage hold (`MATCH` / `CODE_WRONG` / `PLAN_WRONG`)? | A `PLAN_WRONG` worked around in code instead of a plan-change request → `Extra` or `Misunderstood` |

## Rules

- Check file by file when a task lists several files: each listed file needs its own hunk.
- A requirement that cannot be decided from the diff alone (it lives in unchanged code or spans phases) gets one focused read of the code that decides it. If it still cannot be decided, list it as `UNVERIFIED` in the report; it is never counted as met.
- Every `Missing`, `Extra`, `Misunderstood` or `Contract` result is a finding with file:line. Default severity `MAJOR`; `BLOCKER` when an AC of this phase is not delivered; `MINOR` only for a cosmetic Extra with no behaviour.
- When the code is right and the plan is wrong (a file list that cannot work, an Expected that contradicts the AC), the finding is `PLAN_CONFLICT`, routed through `change-control`. Do not ask the writer to match a broken plan or to leave the plan.
- Verified claims produce nothing; do not pad the report with them.
