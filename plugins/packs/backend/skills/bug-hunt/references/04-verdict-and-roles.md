# 04 — Verdict and roles

Clear consequences stop endless review rounds, and fixed roles keep the Reviewer independent of the code it judges.

## What findings do to the verdict

The effect of each severity and confidence is the "Verdict impact" table in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md); the verdict words are in §3 of the same file. Apply it as written:

- A `CONFIRMED` `BLOCKER` or `MAJOR` keeps the phase from `APPROVED`, even when every axis of `{{slot:code-review}}` passes.
- A `PLAUSIBLE` `BLOCKER` makes the verdict `BLOCKED` until the evidence the finding names is supplied (for example a test against a real PostgreSQL instead of SQLite, or the production column's nullability).
- Other `PLAUSIBLE` findings go to the Code Writer as questions in the review report; they do not block alone.
- `MINOR` findings are listed and fixed in the same revision when cheap and inside the phase scope.

No role lowers a severity to end a round. The three-round cap and escalation are owned by `review-workflow`; a finding whose right fix touches the plan is a `PLAN_CONFLICT` row (`change-control`), not a request to the Code Writer.

## Reviewer

- Runs this skill as pass 2 of `review-workflow` at `standard`, or `deep` when §9 or the Backend triggers in [SKILL.md](../SKILL.md#effort) apply, cold, before reading the hand-off's Concerns and the documents.
- Stays read-only toward application code, tests, migrations and databases; writes findings only into `reviews/review_<phase-id>_<REVIEW_REVISION>.md` as `RV-NN` rows (03 → "Finding row"). Reason: a reviewer who edits the code is reviewing its own work.
- Re-judges a `DISPUTED` finding on the evidence given (`review-resolution`); keeps its ID or withdraws it with the reason.

## Code Writer (self-check)

- Runs this skill at `quick` on its own phase diff after the targeted checks pass and before `READY_FOR_REVIEW` (`incremental-implementation`). Reason: cheap defects are cheapest to fix before a review round is spent on them.
- For each `CONFIRMED` finding: write the reproducing test first (`{{slot:unit-testing}}`), fix inside the approved Scope / Files at the root (`{{slot:root-cause-debugging}}`), re-run the affected checks and record evidence rows.
- Lists remaining `PLAUSIBLE` findings as Concerns in `writer-handoff.md` with what would confirm them, and writes the `bug-hunt:` line there ([handoff-and-status](../../work-item-contract/references/handoff-and-status.md) §2, §9).
- A fix that changes behavior, an API contract, a migration plan or the design goes back to Planning as a `PCR-NN` (`change-control`) instead of being made in place.
