# 03 — Findings, Verdict Criteria, Rounds, and Report

> Topic: Unified BLOCKER/MAJOR/MINOR finding table, no-waiver policy, verdict thresholds, 3-round cap, delta re-review, and report format (`R7`–`R8`, `R10`–`R14`)

## 1. Unified Finding Severity & Row Format (`R8`, `R12`)

Every finding uses `RV-NN` (preserved across rounds) and the single 3-tier severity scale defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) (`BLOCKER` / `MAJOR` / `MINOR`):

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `RV-01` | 2 bug-hunt | `BLOCKER` | `CONFIRMED` | `app/orders/router.py:58` | `get_order` queries by `Order.id` without `owner_id` scope | given order 42 owned by A → when user B calls `GET /orders/42` → then 200 with A's order; no test covers foreign owner | Filter query by `(Order.id, Order.owner_id)` and add a foreign-owner 404 test |
| `RV-02` | 6 rubric | `BLOCKER` | `CONFIRMED` | `tests/unit/test_create_order.py:18` | `UT-02`: Unit test suite covers only 201 happy path | `pytest` file contains 1 test (`test_create_order_success`); missing 422 validation, 409 duplicate, and rollback tests | Add negative and rollback unit tests per `unit-testing` |

- For rubric violations (`Pass: 6 rubric`), put the rule ID first in `Problem` (`DOM-001`, `APP-001`, `C5`, `S3`, `UT-02`, `TEST-TAMPER-001`).
- Pure cleanup or refactoring notes without a defect or rule breach go below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification` and never block (`R12`).

---

## 2. No Reviewer Waivers & Plan Conflicts (`R7`)

- **No Reviewer Waivers:** The Reviewer cannot excuse a rule violation, missing error test, or architecture breach, however convincing the writer's explanation.
- **When a Finding Conflicts with the Plan (`PLAN_CONFLICT`):** If the right fix requires altering a locked decision (`D-NN`), changing `api_contract.json`, or modifying frozen phase outcomes, mark the finding `PLAN_CONFLICT` in the report. The Reviewer stays read-only, and the coordinator routes `plan-changes/PCR-NN.md` to Planning (`change-control`).

---

## 3. Verdict Criteria (`R10`)

| Verdict | Required Conditions |
|---|---|
| `APPROVED` | Every re-run CLI gate (`ruff`, `mypy`, `bandit`, `pytest`, `alembic`) is `PASS`; every applicable phase AC is traced to code and a passing test; `bug-hunt` left no `CONFIRMED` `BLOCKER` or `MAJOR`; zero rubric `BLOCKER` or `MAJOR` findings; all `## Review focus` lines checked |
| `CHANGES_REQUESTED` | Any `CONFIRMED` `BLOCKER` or `MAJOR` finding, any `FAIL` CLI gate, happy-path-only tests, `TEST-TAMPER-001`, an untraced/missing task, or an open `PLAN_CONFLICT` |
| `BLOCKED` | Missing Gate 1–3 approvals, unresolvable/moving revision, a required check/database/environment that cannot run, or a `PLAUSIBLE` `BLOCKER` awaiting external evidence |

---

## 4. Rounds, Delta Re-Review & Revision-Bound Report (`R11`, `R13`, `R14`)

- **Delta Re-Review (`R14`):** Each fix revision is reviewed as a delta (`previous_REVIEW_REVISION..new_REVIEW_REVISION` while keeping the phase's `BASE_REVISION`). Verify every finding the writer marked `FIXED` or `DISPUTED` (`review-resolution`), and rerun all affected CLI gates on the new revision.
- **3-Round Cap (`R11`):** Maximum 3 review rounds on the same phase. If round 3 is still not `APPROVED`, stop and escalate (`change-control` for plan conflicts, user/coordinator otherwise) with both positions stated.
- **Revision-Bound Report (`R13`):** Write `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md` containing:
  1. Revision & approval header (`BASE_REVISION`, `REVIEW_REVISION`, uncommitted scope, Gate 1–3 references, round number, overall verdict)
  2. Independent CLI gate evidence rows (`Command`, `Cwd`, `Exit`, `Result: PASS/FAIL`)
  3. Acceptance criteria traceability table (`AC ID` → `Implementation` → `Test` → `Status`)
  4. Pass 2 `bug-hunt` summary line and findings
  5. Pass 3–6 claims check, `Review focus` verification rows, verification gaps, and `RV-NN` rubric findings table
  6. Verdict decision and next-role hand-off (`{{slot:verification}}` on `APPROVED`, `incremental-implementation` on `CHANGES_REQUESTED`)
