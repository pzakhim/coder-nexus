---
name: code-review
description: Review approved Flutter behavior phases across correctness, simplicity, architecture, security, performance and runtime UI evidence.
---

# Flutter Code Review and Architecture Validation

Reviewer stays read-only toward implementation and tests; write review artifacts only. Return necessary edits to Code Writer and require affected checks on the new revision. Read `{{slot:core-package-usage}}` for the approved foundation policy; external Client conventions require source inspection, never inferred company bases.


For new Client work, review `.superpowers/work-items/<slug>/vN/brief.md`, optional design/plan/phase and Docs Writer output against the same code revision. Use `work-item-contract` for type-specific evidence; a phase-free work item is valid. Run Flutter analyzer and visual checks when affected, not for a docs-only change. The `docs/features/` contract below applies to historical features.

## Historical feature workflow

Review a fixed code revision independently. Read only; do not change production code or tests during review. Use the approved `docs/features/<module>/<feature>/vN/` requirements, design, implementation plan and linked phase as the AC contract. For v2+, read `change-impact.md` and the prior as-built baseline. Huly may provide additional real source evidence.

## Inputs and revision

Record `BASE_REVISION`, `REVIEW_REVISION`, the phase ID and all in-scope uncommitted changes, including untracked files. Inspect the whole affected diff with `git diff <BASE_REVISION>..<REVIEW_REVISION>`, `git diff` and `git diff --cached` as applicable. Inspect existing test evidence when available; Test Runner's final report follows review approval. Do not infer success from the latest commit alone.

## Bug hunt first

Run core `bug-hunt` on the fixed scope before the gates below; its dimension 6 uses [the Flutter bug patterns](references/05_bug_patterns.md). Findings go into the report's bug-hunt table. A `CONFIRMED` `BLOCKER`/`MAJOR` blocks approval even when every gate passes.

## Two-Gate Protocol

These are code-review checks after the three user approval gates for specifications. Read Huly and source context from `codebase-notes.md` (`## 0A. Source Inventory`, Huly table, `## 4`) and the API contract from `design.md`; `phases/phase-00-prepare.md` (`PHASE-00`) only records readiness and links to them.

0. **For `PHASE-00` (`[EXECUTE]` — Mockoon preparation phase)**:
   - When reviewing `PHASE-00` that only prepares `mocks/<feature>_mockoon.json`, Dart file lexical checks are `N/A`; audit `mocks/<feature>_mockoon.json` against the **`Mockoon Trigger & Test Data Table`** in `design.md` (endpoints, Pass/Default `200/201`, Empty `[]`, and Fail `400/401/403/500` conditional `rules`), verify via `mockoon-cli` / `curl`, and confirm `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`** before approving `PHASE-00` to unlock `PHASE-01, 02, 03...`.
1. **File-level Hub check (`PHASE-01+` Dart phases):** Confirm `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`**. Call `validate_architecture_code` on each changed Dart file with its correct layer and explicit `architecture_profile` from the approved design/brief. `status: error`, `valid: false`, or any violation of severity `ERROR` (e.g. `PRE-006` BaseScreen Contract) **strictly blocks approval (`CHANGES_REQUESTED`)**.
   - **No reviewer waivers**: the Reviewer cannot excuse a violation with a technical argument. A real foundation/Client incompatibility is a Core gap routed to Planning for Gate 2, never an approved deviation in the review.
   - `gate_status: UNVERIFIED` means the lexical validator cannot prove syntax or integration; run the approved Client analyzer on the same tree. Investigate warnings in context and include `unsupported_checks` in the report. Supported lexical rules are listed in [the rule source matrix](references/02_rule_source_matrix.md).
2. **Integrated behavior check:** Apply [the cross-branch checklist](references/03_cross_branch_checklist.md). Pass the same explicit `architecture_profile` to `validate_module_architecture` only when a complete module is affected. `FAILED` blocks; `UNVERIFIED` or warnings require explicit Client inspection and evidence before approval. For a scoped UI-only phase, record the full-module check `N/A` with reason and inspect affected boundaries directly.
   - **Reuse & Mockoon isolation audit**: every need in the approved `Core usage` / `Client Core Mapping` table uses its mapped component, shared widgets from earlier phases are reused, `lib/` contains zero `MockDataSource` classes, and Unit Tests cover both Pass/Default and Fail scenarios from `design.md`.
   - For UI impact, use `{{slot:visual-quality}}` on the approved target and inspect real screenshots/video and logs against Visual AC before approval. Code that compiles but materially deviates from the approved design requires changes.

Do not demand empty Domain, Data or DI classes for a scoped UI-only phase. When a phase introduces a screen-scoped Cubit, review its factory lifetime and disposal. Do not treat a lexical pass as analyzer, test or runtime evidence. Reviewer owns analyzer, developer Unit Test grading, and applicable UI evidence needed for its decision; Test Runner runs UI/Widget/Visual acceptance checks and build after `APPROVED` on the same tree. This ordering avoids a review/verification dependency cycle.

For screen changes, apply [the screen contract](../clean-architecture/references/05_screen_contract.md): identify actual destinations, review names, verified base inheritance (`BaseScreen` in `imespro`), metadata and layout hook, route/DI and lifecycle. Review dialogs and child widgets by their own contract. A missing active Client base API blocks approval. Source declarations alone do not prove analytics or orientation behavior.

## Five-Axis Review

Use [the five-axis rubric](references/01_five_axis_rubric.md):

1. **Correctness:** Every mapped AC and relevant error path is implemented and evidenced, and the bug-hunt pass left no `CONFIRMED` `BLOCKER`/`MAJOR`. Audit test changes for weakened assertions.
2. **Readability and simplicity:** Names, control flow and abstractions are clear and proportional to approved behavior.
3. **Clean Architecture and DI:** Layer imports, module ownership, DI order and state patterns match the actual Client scope.
4. **Security and data safety:** No credentials, fake data, hidden parse fallback or unauthorized Huly writes.
5. **Performance and lifecycle:** Controllers, subscriptions and screen-scoped state are managed correctly.

## Report and handoff

Write a revision-bound report using [the report template](templates/code_review_report.md.tpl) under `.superpowers/work-items/<slug>/vN/reviews/review_<phase-id>_<revision>.md`.

Record approved document revisions and Gate 1–3 user response references, every AC's code/test/visual evidence or gap, planned checks, analyzer command/result, module gate resolution, full uncommitted scope and image inspection. `APPROVED` requires all applicable ACs traced and no unresolved required check; final phase `PASS` still depends on Test Runner evidence.

- `APPROVED`: pass the same feature/version/phase and revision to `{{slot:verification}}`; the coordinator records the verdict in `as-built.md`.
- `CHANGES_REQUESTED`: provide specific findings to `incremental-implementation`. A fix creates a new revision and invalidates affected earlier evidence.
- `BLOCKED`: report the missing source, environment or target. Never claim PASS from `NOT_RUN` or stale evidence.

## Hub validators

Which Hub validators apply to a Flutter Client and the required `architecture_profile` argument: [04_hub_validator_usage.md](references/04_hub_validator_usage.md).
