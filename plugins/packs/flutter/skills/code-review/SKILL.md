---
name: code-review
description: Flutter code review rubric and architecture validation gates for Flutter / Dart applications - strictly read-only, runs bug-hunt first, executes Hub MCP architecture validators and Client CLI gates independently, grades five review axes across correctness, simplicity, Clean Architecture, security, lifecycle, and runtime visual quality, and issues an APPROVED / CHANGES_REQUESTED / BLOCKED verdict with RV-NN findings.
---

# Code Review — Flutter / Dart

Reviewer is strictly read-only toward implementation, generated files, and tests; write review reports only (`vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`). Follow `review-workflow` for pass ordering and [handoff-and-status](../work-item-contract/references/handoff-and-status.md) for unified finding rows and status flags.

## 1. CLI & MCP Verification Gates (`PASS` / `FAIL`)

Rerun applicable checks independently on `REVIEW_REVISION` (`R6`). `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`:

| Gate | Command / MCP Tool | Pass Criteria |
|---|---|---|
| **File Architecture Validator** | `validate_architecture_code` (per changed Dart file + `architecture_profile`) | `PASS` (zero `ERROR` violations; `UNVERIFIED` resolved via analyzer + inspection) |
| **Module Boundary Validator** | `validate_module_architecture` (when full module is affected + `architecture_profile`) | `PASS` (`N/A` with reason for scoped UI-only phases) |
| **Static Analyzer** | `flutter analyze` | `PASS` (`exit 0`, zero errors/warnings on `REVIEW_REVISION`) |
| **Code Metrics / Lint** | `dart run dart_code_linter:metrics analyze lib` *(when configured)* | `PASS` (`exit 0`) |
| **Developer Unit & Cubit Tests** | `flutter test test/unit/` (or affected test files) | `PASS` (happy + negative/error paths green) |
| **Runtime Visual Gate** | `{{slot:visual-quality}}` (when phase has UI impact) | `PASS` (real target screenshot/logs match Visual AC) |

## 2. Order of Passes

1. **Fix the revision & rerun gates (`R1`, `R2`, `R6`):** Verify `BASE_REVISION..REVIEW_REVISION` and uncommitted scope; check `PHASE-00` (Mockoon preparation) or `PHASE-01+` Two-Gate Protocol and rerun CLI/MCP checks ([01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md)).
2. **Cold bug-hunt pass (`R3`):** Run `{{slot:bug-hunt}}` cold at `standard` (or `deep` for auth, secure storage, payment/order state machines, local DB migrations, or routing guards) before reading design documents.
3. **Grade the 5 Flutter review axes (`R4`, `R5`):** Audit Correctness & AC Traceability (`TEST-TAMPER-001` & Mockoon isolation), Readability & Simplicity, Clean Architecture & DI, Security & Data Safety, and Performance, Lifecycle & Visual Quality ([02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md)).
4. **Write findings & decide verdict (`R7`–`R14`):** Grade findings with unified `BLOCKER` / `MAJOR` / `MINOR` severities, enforce no-waiver rules (`PLAN_CONFLICT` → `change-control`), and write the revision-bound report ([03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md)).

## 3. Mandatory Rules (`R1`–`R14`)

| ID | Rule Summary | Reference |
|---|---|---|
| **R1–R3, R6, R9** | Fixed revision, strictly read-only, bug-hunt first, rerun MCP/CLI gates independently, diff + broken callers scope | [01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md) |
| **R4–R5** | Grade axes with Flutter rubric skills, trace every AC, reject happy-path-only or tampered tests (`TEST-TAMPER-001`) | [02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md) |
| **R7–R8, R10–R14** | No reviewer waivers (`PLAN_CONFLICT`), actionable `RV-NN` rows, verdict criteria, 3-round cap, delta re-review, report | [03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md) |

## 4. Reference Guides

| Guide | Topic |
|---|---|
| [01 — Scope, Gates & Validators](references/01-scope-gates-and-validators.md) | Fixed revision, read-only rule, `PHASE-00` vs `PHASE-01+` Two-Gate Protocol, Hub MCP validators, and `CRX-001..004` |
| [02 — Review Axes & Rubric](references/02-review-axes-and-rubric.md) | The 5 Flutter review axes, rubric skill links, AC traceability, Mockoon isolation, and visual review |
| [03 — Findings, Verdict & Report](references/03-findings-verdict-and-report.md) | Unified `BLOCKER`/`MAJOR`/`MINOR` findings, no-waiver rules, verdict thresholds, rounds, and report structure |
<!-- {{profile_references}} -->
