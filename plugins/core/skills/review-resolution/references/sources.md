# Sources

External ideas adapted into [review-resolution](../SKILL.md), rewritten in this repo's vocabulary. Internal base inputs: `src/skill_factory/library/generators/create-code-review-skill/` (findings, verdicts and rounds from the reviewer side) and [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) (severity scale and the third-return escalation).

| Source (link pinned to sha) | Stars | Idea taken | Where used |
|---|---|---|---|
| [obra/superpowers `skills/receiving-code-review/SKILL.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/receiving-code-review/SKILL.md) | 303k | Read all, restate, verify against the code, evaluate, then respond and implement | SKILL steps 1, 2, 4 |
| same | 303k | Any unclear item stops all implementation until clarified; ask about all unclear items at once | SKILL step 3 |
| same | 303k | No performative agreement or gratitude; state the fix or push back with technical reasoning | SKILL steps 4, 6 |
| same | 303k | A finding that conflicts with the owner's prior decisions goes back to the owner | SKILL step 4 (`D-NN` -> `change-control`) |
| same | 303k | One item at a time, blocking first, test each | SKILL step 5 |
| same | 303k | Correct a wrong pushback in one factual line | SKILL step 4 |
| [obra/superpowers `skills/subagent-driven-development/references/fix-loop.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/references/fix-loop.md) | 303k | Each fix round returns the covering tests, the command and its output before re-review | SKILL steps 5, 6 |
| same | 303k | Findings that conflict with the plan text need an explicit ruling, never a silent fix or dismissal | SKILL step 4 |
| same | 303k | A capped loop; no silent discard of an open finding at the cap | SKILL step 7 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Five fix rounds, rounds 4-5 by a fresh implementer on a stronger model | superpowers fix-loop | The fixed process caps at 3 review rounds per phase, then escalates |
| The controller adjudicates open findings at the cap and parks them | superpowers fix-loop | No self-approval: open findings go to Planning or the user, never ruled away by an agent |
| Minor findings deferred to a ledger and never enter the loop | superpowers fix-loop | Repo rule (bug-hunt): cheap `MINOR`s are fixed in the same revision; others are listed in the reply, not silently deferred |
| Re-review scoped to the fix diff only | superpowers fix-loop | A new revision invalidates affected evidence; the reviewer re-checks the affected phase scope |
| YAGNI pushback ("nothing calls this, remove it?") as a reviewer-facing question | superpowers receiving-code-review | Scope is set by the approved plan; removing or adding features is a plan change request (`change-control`), not a review negotiation |
| Trust levels by source (human partner vs external reviewer) | superpowers receiving-code-review | Every finding is verified the same way; the user's own instructions arrive through gates and `D-NN`, not review |
| Replying in GitHub review threads | superpowers receiving-code-review | Replies go into the work-item hand-off; platform choice belongs to `git-preflight` / workspace skills |
