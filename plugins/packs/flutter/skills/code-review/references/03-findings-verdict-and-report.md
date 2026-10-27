# 03 — Findings, Verdict Criteria, Rounds, and Report

> Topic: Unified BLOCKER/MAJOR/MINOR finding table, no-waiver policy, verdict thresholds, 3-round cap, delta re-review, and report format (`R7`–`R8`, `R10`–`R14`)

## 1. Unified Finding Severity & Row Format (`R8`, `R12`)

Every finding uses `RV-NN` (preserved across rounds) and the single 3-tier severity scale defined in [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) (`BLOCKER` / `MAJOR` / `MINOR`):

| ID | Pass | Severity | Confidence | File:line | Problem | Failure scenario / evidence | Fix direction |
|---|---|---|---|---|---|---|---|
| `RV-01` | 2 bug-hunt | `BLOCKER` | `CONFIRMED` | `lib/modules/orders/data/models/order_model.dart:28` | `OrderModel.fromJson` casts `json['total'] as double`, crashing on integer JSON values | given `{"total": 100}` → when `fromJson` runs → then throws `_TypeError`; no unit test for integer JSON | Use safe double parsing and add a `fromJson` unit test with integer `total` |
| `RV-02` | 6 rubric | `BLOCKER` | `CONFIRMED` | `lib/modules/orders/domain/entities/order_entity.dart:3` | `DOM-001`: Domain entity imports `package:flutter/material.dart` | `validate_architecture_code` returned `ERROR: DOM-001` | Remove Flutter import from Domain; map UI colors/icons in Presentation |

- For rubric or validator violations (`Pass: 6 rubric`), put the rule ID first in `Problem` (`DOM-001`, `DAT-003`, `PRE-006`, `CRX-001`, `TEST-TAMPER-001`, `C1`, `S1`).
- Pure cleanup or refactoring notes without a defect or rule breach go below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification` and never block (`R12`).

---

## 2. No Reviewer Waivers & Plan Conflicts (`R7`)

- **No Reviewer Waivers:** The Reviewer cannot excuse a validator `ERROR`, architecture boundary breach, missing negative unit test, or broken Visual AC with a technical argument.
- **When a Finding Conflicts with the Plan (`PLAN_CONFLICT`):** If a real foundation/Client incompatibility orCore gap requires changing `design.md` (`Core usage` / `Client Core Mapping`), `requirements.md`, or locked `D-NN` decisions, mark the finding `PLAN_CONFLICT` in the report. The Reviewer stays read-only, and the coordinator routes `plan-changes/PCR-NN.md` to Planning (`change-control`).

---

## 3. Verdict Criteria (`R10`)

| Verdict | Required Conditions |
|---|---|
| `APPROVED` | Every re-run gate (`validate_architecture_code`, `validate_module_architecture` or justified `N/A`, `flutter analyze`, unit tests) is `PASS`; every applicable phase AC is traced to code and evidence; `bug-hunt` left no `CONFIRMED` `BLOCKER` or `MAJOR`; zero rubric `BLOCKER` or `MAJOR` findings; runtime visual review is `PASS` when UI is affected (`{{slot:visual-quality}}`) |
| `CHANGES_REQUESTED` | Any `CONFIRMED` `BLOCKER` or `MAJOR` finding, any validator `ERROR` / `FAILED` gate, `flutter analyze` failure, happy-path-only tests, `TEST-TAMPER-001`, material visual mismatch, or an open `PLAN_CONFLICT` |
| `BLOCKED` | Missing Gate 1–3 approvals, unresolvable/moving revision, missing active Client base API, an analyzer/test/visual environment that cannot run, or a `PLAUSIBLE` `BLOCKER` awaiting external evidence |

---

## 4. Rounds, Delta Re-Review & Revision-Bound Report (`R11`, `R13`, `R14`)

- **Delta Re-Review (`R14`):** Each fix creates a new `REVIEW_REVISION` and invalidates affected earlier evidence. Inspect `previous_REVIEW_REVISION..new_REVIEW_REVISION`, verify every finding claimed `FIXED` or `DISPUTED` (`review-resolution`), and rerun all affected validators, analyzer, unit tests, and visual checks on the new tree.
- **3-Round Cap (`R11`):** Maximum 3 review rounds per phase. If round 3 is still not `APPROVED`, stop and escalate (`change-control` for plan conflicts, user/coordinator otherwise) with both positions stated.
- **Revision-Bound Report (`R13`):** Write `.superpowers/work-items/<slug>/vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md` containing:
  1. **Header:** Feature/version, phase ID, `BASE_REVISION`, `REVIEW_REVISION`, uncommitted scope, Gate 1–3 approval references, `architecture_profile`, round number, and overall verdict (`APPROVED` / `CHANGES_REQUESTED` / `BLOCKED`).
  2. **Gate & Validator Evidence Rows:** `validate_architecture_code` per changed file, `validate_module_architecture` + `unsupported_checks` resolution, `flutter analyze` / `dart_code_linter` exit code, and `flutter test` exit code (`PASS` / `FAIL`).
  3. **Acceptance Criteria Traceability Table:** `AC ID` → `Implementation (path:line)` → `Unit/Widget Test or Visual Check` → `Evidence` → `Status`.
  4. **Pass 2 Bug-Hunt Summary & Findings:** `bug-hunt:` summary line and `RV-NN` defect rows.
  5. **Five-Axis Assessment & Rubric Findings:** Status per axis (`PASS` / `FAIL`), `Review focus` verification rows, and `RV-NN` compliance findings table.
  6. **Runtime Visual Review Gate:** Visual verdict (`PASS` / `FAIL` / `BLOCKED` / `N/A`), target device/viewport, screenshot/recording path, Visual AC comparison, and runtime log summary.
  7. **Hand-Off Action:** Pass exact revision to `{{slot:verification}}` on `APPROVED`, or return `RV-NN` findings to `incremental-implementation` on `CHANGES_REQUESTED`.
