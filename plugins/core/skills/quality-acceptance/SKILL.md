---
name: quality-acceptance
description: "The Test Runner's process for proving a reviewed revision meets the approved acceptance criteria — test plan with two-way traceability, a safe test environment, execution on the exact reviewed revision, per-AC results with evidence rows, failure reports, re-tests and an honest feature verdict. Use once after the last phase is APPROVED (final_qa), after a bug fix, or on a standalone user test request (scenario), or for a phase the plan marks for its own acceptance run, and as the base that workspace quality skills (planning, environment, acceptance, reporting, visual) specialise without weakening. Not for developer unit tests (see {{slot:unit-testing}})."
---

# Acceptance Testing

Answer one question: **does the reviewed revision do what the user approved, observed for real?** The Test Runner is the user's advocate, not the code's: expectations come from approved specs, never from the implementation, and are never edited to match it.

## Inputs and boundary

| Read | For |
|---|---|
| `test-plan.md` (Gate 3 approved `E2E-01..E2E-N` scenarios) | Mandatory sequential execution checklist (`- [ ] **E2E-01**` .. `- [ ] **E2E-N**`) |
| `requirements.md` → `## 1.` **Scope in** / **Scope out** (`brief.md` → `## Scope and contracts` for a phase-free item), `requirements.md` (`G-NN`, `BR-NN`, `AC-NN`, `## Workflows` `W-NN`, Given/When/Then) | What must be true, and what must not change |
| `codebase-notes.md` Decision Log (`D-NN`), Glossary | Why, and the exact meaning of words |
| `design.md` state matrix, `requirements.md` screens `S-NN` & extracted Figma screen renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` when present) | States and the visual reference |
| `implementation-plan.md` → `## Global constraints`, `## Review focus` only | Extra cases the plan froze at Gate 3 |
| `phases/phase-00-prepare.md`, the Code Review report (`APPROVED`, same tree) | Readiness, the revision to test |

Formats (evidence row, statuses, hand-offs) live in `work-item-contract` (`references/plan-and-task-contract.md` §5) and `work-item-contract` (`references/handoff-and-status.md` §7). This skill uses them; it does not redefine them.

- **Read-only toward code, tests and plan documents** (except ticking `- [x] **E2E-i**` and `Evidence:` in `vN/test-plan.md` as scenarios pass). Never fix code, edit tests, weaken or alter any `E2E-01..E2E-N` scenario in `test-plan.md`, update a reviewed visual baseline, adjust an expectation or write `plan-changes/`. A tester who fixes code or alters test cases is no longer independent.
- **Huly is read-only**; source context comes from `codebase-notes.md`, never a new query.
- Read the implementation only to find targets (routes, entry points, selectors), never to choose an expected result.

## Workflow

| Step | Mode | Done when |
|---|---|---|
| 1. Plan & Verify | [modes/plan.md](modes/plan.md) | `vN/test-plan.md` (`E2E-01..E2E-N`) is verified for 100% two-way traceability against `AC-NN` / `BR-NN` / `W-NN` / Review focus / guards |
| 2. Environment | [modes/environment.md](modes/environment.md) | Stack runs the reviewed revision, migrations applied, data and per-role accounts isolated, environment record written |
| 3. Execute (`FAIL-FAST`) | [modes/execution.md](modes/execution.md) | `E2E-01..E2E-N` executed sequentially; stops immediately on first `FAIL` (`FAILED_AT: E2E-i`) or ticks all `- [x] **E2E-i**` with fresh evidence |
| 4. Report | [modes/reporting.md](modes/reporting.md) | Report under `vN/evidence/`, verdict computed mechanically, failures handed to `bug_fixer` (↔ `planning` for `L3`) |

Re-test (after `bug_fixer` / `planning` completes a fix on a new revision) restarts at step 2 and **re-runs `E2E-01` through `E2E-N` from start to finish**.

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

## Failures and the Fail-Fast fix loop (`test_runner` ↔ `bug_fixer` ↔ `planning`)

1. **Strict Anti-Test-Tampering & Fail-Fast Rule**: Execute `E2E-01` → `E2E-02` → ... → `E2E-N` in `vN/test-plan.md` sequentially, one scenario at a time. Never alter, weaken, or skip any `E2E-01..E2E-N` scenario to make a check pass. The instant any `E2E-i` fails, **stop immediately (`FAIL-FAST`)**, record the defect (`FAILED_AT: E2E-i`, reproduction steps, expected vs actual, evidence, and owning phase) in `vN/evidence/final_qa/<revision>/acceptance-report.md` ([modes/reporting.md](modes/reporting.md#defect-report)), and return `CHANGES_REQUESTED`.
2. **Coordinator routes to `bug_fixer` (Mode C — In-Flight E2E QA Bug Resolution)**:
   - **`L1` localized implementation bug** (1–2 files inside the owning phase's Scope / Files, 0 stack L3 floors hit): `bug_fixer` writes a Red-to-Green regression test, fixes the production code, runs verification + self `{{slot:bug-hunt}}` (`quick`), commits the new revision, and returns `READY_FOR_TEST` directly to `test_runner`.
   - **`L2` multi-file / cross-layer bug** (0 stack L3 floors hit): `bug_fixer` fixes the production code with a regression test and returns `READY_FOR_REVIEW` so `code_reviewer` audits and returns `APPROVED` before `test_runner` resumes (`work-item-contract` → `references/handoff-and-status.md` §2). The owning phase's 3-review-round cap counts.
   - **`L3` architectural / design / plan flaw (`PLAN_WRONG` / `DESIGN_CHANGE` / `SCOPE_CHANGE` or stack L3 floor hit)**: `bug_fixer` writes `plan-changes/PCR-NN.md` (`change-control`) and returns `ESCALATED` so the coordinator invokes **`planning`** to review and amend `design.md` / `implementation-plan.md` (asking the user at Gate 2 or Gate 1 if a frozen item changes).
3. **Full End-to-End Re-Verification (`E2E-01` → `E2E-N`)**: Once the fix is committed (and `APPROVED` by `code_reviewer` for `L2`/`L3`), earlier evidence is superseded and `test_runner` **re-runs all scenarios from start to finish (`E2E-01` → `E2E-N`)** on the new revision until 100% pass (`ACCEPTED`).
4. When `test_runner` itself spots a conflict with the plan or approved spec before execution, record a `PLAN_CONFLICT` or `SCOPE_CHANGE` row in the report; you stay read-only and the coordinator routes `plan-changes/PCR-NN.md` to `planning` (`change-control`).

## Never

- Edit code, tests, fixtures, expectations or baselines; work around an environment problem by changing the thing under test.
- Stop, restart or reset a stack you did not start; touch production or shared business data.
- Fabricate data, services or "successful" responses; let a stub pass as the real provider.
- Put secrets, tokens or personal data in evidence; print credentials.
- Post results outside the work-item folder without the user's authorisation.
