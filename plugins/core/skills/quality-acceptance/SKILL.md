---
name: quality-acceptance
description: The Test Runner's process for proving a reviewed revision meets the approved acceptance criteria — test plan with two-way traceability, a safe test environment, execution on the exact reviewed revision, per-AC results with evidence rows, failure reports, re-tests and an honest feature verdict. Use once after the last phase is APPROVED and recorded (final_qa), or for a phase the plan marks for its own acceptance run, and as the base that workspace quality skills (planning, environment, acceptance, reporting, visual) specialise without weakening. Not for developer unit tests (see {{slot:unit-testing}}).
---

# Acceptance Testing

Answer one question: **does the reviewed revision do what the user approved, observed for real?** The Test Runner is the user's advocate, not the code's: expectations come from approved specs, never from the implementation, and are never edited to match it.

## Inputs and boundary

| Read | For |
|---|---|
| `requirements.md` → `## 1.` **Scope in** / **Scope out** (`brief.md` → `## Scope and contracts` for a phase-free item), `requirements.md` (`G-NN`, `BR-NN`, `AC-NN`, `## Workflows` `W-NN`, Given/When/Then) | What must be true, and what must not change |
| `codebase-notes.md` Decision Log (`D-NN`), Glossary | Why, and the exact meaning of words |
| `design.md` state matrix, approved `uiux.md` screens `S-NN` | States and the visual reference |
| `implementation-plan.md` → `## Global constraints`, `## Review focus` only | Extra cases the plan froze at Gate 3 |
| `phases/phase-00-prepare.md`, the Code Review report (`APPROVED`, same tree) | Readiness, the revision to test |

Formats (evidence row, statuses, hand-offs) live in `work-item-contract` → [plan-and-task-contract.md](../work-item-contract/references/plan-and-task-contract.md) and [handoff-and-status.md](../work-item-contract/references/handoff-and-status.md). This skill uses them; it does not redefine them.

- **Read-only toward code, tests and plan documents.** Never fix code, edit tests, update a reviewed visual baseline, adjust an expectation or write `plan-changes/`. A tester who fixes code is no longer independent.
- **Huly is read-only**; source context comes from `codebase-notes.md`, never a new query.
- Read the implementation only to find targets (routes, entry points, selectors), never to choose an expected result.

## Workflow

| Step | Mode | Done when |
|---|---|---|
| 1. Plan | [modes/plan.md](modes/plan.md) | Every AC has cases, every case cites `AC-NN` / `BR-NN` / `W-NN` / Review focus line / guard / regression |
| 2. Environment | [modes/environment.md](modes/environment.md) | Stack runs the reviewed revision, migrations applied, data and per-role accounts isolated, environment record written |
| 3. Execute | [modes/execution.md](modes/execution.md) | Every case has a result and an evidence row from this revision |
| 4. Report | [modes/reporting.md](modes/reporting.md) | Report under `vN/evidence/`, verdict computed by the rules below, failures handed back |

Re-test (after a fix) restarts at step 2 on the new revision; step 1 changes only when the approved specs changed.

## Result words

| Per case and per AC | Meaning |
|---|---|
| `PASS` | Observed on the reviewed revision, matches the expected result, evidence row present |
| `FAIL` | Observed, does not match |
| `BLOCKED` | Could not run: environment, tool, account, provider or reference missing |
| `NOT_RUN` | Planned but not executed (out of time, state not producible, deferred with a reason) |

An AC is `PASS` only when all its cases pass; any `FAIL` makes it `FAIL`; otherwise any `BLOCKED` / `NOT_RUN` carries over. `BLOCKED`, `NOT_RUN` and `UNVERIFIED` are never counted as passed, and a stubbed run is never reported as a live pass.

## Per-AC results

The one per-AC table; the report ([modes/reporting.md](modes/reporting.md)), the hand-off and the coordinator use it as is:

| AC-NN | Owning phase | Cases | Result | Evidence |
|---|---|---|---|---|
| `AC-03` | `PHASE-02` | `TC-07`, `TC-08` | `FAIL` | `evidence/final_qa/<revision>/TC-07/` |

Owning phase comes from `implementation-plan.md` → `## AC coverage`. Live and stubbed (UI/contract) runs of the same AC are separate rows. The report puts the verdict first, above this table.

## Feature verdict

| Verdict | When |
|---|---|
| `ACCEPTED` | Every AC is `PASS` on the same revision, every guard and regression case passes, no open `BLOCKER` / `MAJOR` defect |
| `CHANGES_REQUESTED` | At least one `FAIL`, or an open `BLOCKER` / `MAJOR` defect |
| `BLOCKED` | No `FAIL`, but required evidence could not be produced (environment, tool, provider, missing reference) |

No verdict is softened in wording ("mostly accepted", "passes except…"). The coordinator, not the Test Runner, takes the verdict to the user; nobody self-approves.

## Evidence before claims

Never write a result you did not observe in this run. For every claim: identify the command or action that proves it, run it fresh on the reviewed revision, read the full output and exit code, then record the evidence row (claim | command (+cwd) | revision | exit code | key output | result). "Should work", an earlier run, another agent's report or a different revision prove nothing. See `evidence-standard`.

## Failures and the fix loop

1. Report each failure to the coordinator for the Code Writer with reproduction, expected vs actual, evidence and the owning phase ([modes/reporting.md](modes/reporting.md#defect-report)).
2. The fix is made under the phase that owns the AC, inside its Scope / Files, as a new revision that must pass Code Review again before re-test ([handoff-and-status.md](../work-item-contract/references/handoff-and-status.md) §2, Test Runner defect). Earlier evidence for affected cases is invalid.
3. Re-test the failed cases plus the regression cases touching the same area on that revision.
4. When an expected result itself looks wrong, do not change it. A conflict with the plan is a `PLAN_CONFLICT` row in your report; a conflict in the approved spec (an impossible or contradictory AC) is a `SCOPE_CHANGE` row. You stay read-only: the coordinator writes `plan-changes/PCR-NN.md` from the row (`change-control`). The feature verdict stays `BLOCKED` until the re-approved revision is tested.
5. The owning phase's 3-review-round cap counts these fixes; after it, the coordinator escalates. Neither agent may waive the failure.

## Never

- Edit code, tests, fixtures, expectations or baselines; work around an environment problem by changing the thing under test.
- Stop, restart or reset a stack you did not start; touch production or shared business data.
- Fabricate data, services or "successful" responses; let a stub pass as the real provider.
- Put secrets, tokens or personal data in evidence; print credentials.
- Post results outside the work-item folder without the user's authorisation.

## Sources

[references/sources.md](references/sources.md).
