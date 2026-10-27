# 01 — Scope, Two-Gate Protocol, and Hub Validators

> Topic: Fixed revision scope, read-only discipline, PHASE-00 vs PHASE-01+ Two-Gate Protocol, Hub MCP validators, and cross-branch boundary checks (`R1`–`R3`, `R6`, `R9`)

## 1. Fixed Revision & Read-Only Discipline (`R1`, `R2`, `R9`)

- **Fixed Revision (`R1`):** Record `BASE_REVISION` and `REVIEW_REVISION` from the hand-off header, plus staged, unstaged, and untracked files (`git status --short`, `git diff --stat <BASE_REVISION>..<REVIEW_REVISION>`). Review exactly that tree. A moving tree or unresolvable revision is `BLOCKED`.
- **Strictly Read-Only (`R2`):** Never edit production code (`lib/`), generated files (`.g.dart`, `.freezed.dart`), tests (`test/`), or `pubspec.yaml`. Write only the review report under `vN/reviews/`.
- **Diff & Caller Scope (`R9`):** Inspect changed files and any callers, routes, state holders, or module boundaries broken by the diff (`rg -n -w "<symbol>" lib test`). Pre-existing legacy debt outside the diff is recorded only as a non-blocking note.
- **Reviewer vs Test Runner Boundary:** Reviewer owns static analysis (`flutter analyze`), Hub architecture validators, developer Unit/Cubit Test grading, and applicable runtime UI evidence needed for the review decision; Test Runner runs full acceptance/widget/build verification after `APPROVED` on the same revision (`{{slot:verification}}`).

---

## 2. Two-Gate Protocol (`PHASE-00` vs `PHASE-01+`)

### 2.1 `PHASE-00` Gate (`[EXECUTE]` — Mockoon Preparation Phase)
When reviewing a `PHASE-00` that only prepares `mocks/<feature>_mockoon.json`:
1. Dart file lexical checks are `N/A`.
2. Audit `mocks/<feature>_mockoon.json` against the **Mockoon Trigger & Test Data Table** in `design.md` (endpoints, Pass/Default `200/201`, Empty `[]`, and Fail `400/401/403/500` conditional `rules`).
3. Verify responses via `mockoon-cli` / `curl` where applicable, and confirm `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`** before approving `PHASE-00` to unlock `PHASE-01+`.

### 2.2 Gate 1 — File-Level Hub & Analyzer Check (`PHASE-01+` Dart Phases)
1. Confirm `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`** when Mockoon is used.
2. Read `architecture_profile.mode` (`imespro`, `external-structured`, or `external-standard`) from the approved `design.md` (or `brief.md` for phase-free items) and call `validate_architecture_code` on each changed Dart file with its layer and explicit `architecture_profile`.
   - Any `status: error`, `valid: false`, or violation of severity `ERROR` **strictly blocks approval (`CHANGES_REQUESTED`)**.
   - `gate_status: UNVERIFIED` means the lexical validator cannot prove syntax or cross-file inheritance; run the Client analyzer (`flutter analyze` and `dart run dart_code_linter:metrics analyze lib` when configured) on the same revision, inspect `unsupported_checks` in context, and record the resolution in the report.

### 2.3 Gate 2 — Integrated Module & Cross-Branch Check
1. Pass the same explicit `architecture_profile` to `validate_module_architecture` when a complete module is affected (`FAILED` blocks; for a scoped UI-only phase, record `N/A` with reason and do not demand empty Domain/Data/DI boilerplate).
2. Verify the **Cross-Branch Boundary Checklist (`CRX-001..004`)**:

| Rule | Boundary Requirement | Verification Evidence |
|---|---|---|
| `CRX-001` | No imports of another module's private `presentation/` widgets or cubits | Inspect changed imports under `lib/modules/`; use shared widgets or public contracts |
| `CRX-002` | No direct imports of another module's `data/` (DataSource, DTO/Model, RepositoryImpl) | Inspect cross-module imports; consume only public Domain contracts |
| `CRX-003` | Inter-module behavior uses published Domain UseCases or shared contracts | Trace DI registrations and constructor injections across modules |
| `CRX-004` | Module DI is registered once in the composition root in verified boot order | Inspect `di.dart` / module DI wiring when DI changes |

---

## 3. Universal Clean Architecture Lexical Rule Matrix

The rules below apply across Flutter Clean Architecture scopes (profile-specific rules such as `DAT-001`, `DAT-002`, `PRE-002`, `PRE-004`, `PRE-006`, `STY-001` are detailed in the active workspace profile guide):

| Rule | Layer | Hub Severity | Reviewer Action (`BLOCKER` / `MAJOR`) |
|---|---|---|---|
| `DOM-001` Domain No Flutter | Domain | `ERROR` | Reject any `package:flutter/*` or UI import in Domain (`BLOCKER`) |
| `DOM-002` Domain Independence | Domain | `ERROR` | Reject Data or Presentation imports in Domain (`BLOCKER`) |
| `DOM-003` Entity Immutability | Domain | `WARNING` | Flag mutable entity fields (`MAJOR`) |
| `DAT-003` Safe DTO Parsing | Data | `WARNING` | Flag unsafe raw `as int`/`as double` casts or `!` on nullable JSON fields (`MAJOR` / `BLOCKER`) |
| `PRE-001` No Throw in UI | Presentation | `ERROR` | Reject direct `throw` statements inside widget/screen code (`BLOCKER`) |
| `PRE-003` Resource Disposal | Presentation | `WARNING` | Flag undisposed `Controller`, `FocusNode`, `StreamSubscription`, or `Timer` (`MAJOR`) |
| `PRE-005` Screen Naming | Presentation | `ERROR` | Flag `*Page` screen classes where `*Screen` is required (`BLOCKER`) |
| `MOD-006` Screen Paths | Module | `ERROR`/`WARNING` | Verify screen files reside under `presentation/screens/*_screen.dart` (`BLOCKER` on new screens) |
| `DIR-001` Cubit Lifetime | DI / Module | `UNVERIFIED` | Verify screen-scoped Cubit/Notifier is registered as a factory, not a leaking singleton (`MAJOR`) |
| `RTE-001` Route Ownership | Presentation | `INFO` | Verify route registration and typed route argument handling |
