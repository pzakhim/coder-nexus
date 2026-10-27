---
name: verification
description: "Execute and verify deterministic Flutter quality gates (`G0`–`G8`: developer tools check, code generation, `flutter analyze`, `dart_code_linter` metrics, MCP architecture validators, `flutter test` unit/widget/golden suites, `{{slot:visual-quality}}` runtime visual inspection, and flavor builds) on a reviewed revision. Use when Planning defines task/phase checks, Code Writer verifies phase completion (`READY_FOR_REVIEW`), Code Reviewer re-runs checks on `REVIEW_REVISION` (`APPROVED` / `CHANGES_REQUESTED`), or Test Runner executes UI and acceptance verification (`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`)."
---

# Flutter Verification (Dart & Flutter)

This skill is `{{slot:verification}}` for the Flutter pack. Claim proof rules belong to `evidence-standard`; unified flags, severities, and handoff statuses belong to [handoff-and-status](../work-item-contract/references/handoff-and-status.md), `shared_contracts/flags_and_statuses.md`, and `shared_contracts/api_handshake_protocol.md`.

## 1. Detect Workspace Tooling First (Never Assume)

Before running any gate, inspect from the Client workspace root (`cwd`): `.fvmrc`, `pubspec.yaml`, `pubspec.lock`, `analysis_options.yaml`, `.vscode/launch.json` (or flavor scripts), and `.superpowers/setup.json`. Never guess `dev`, `lib/main_dev.dart`, Android, or FVM when the workspace specifies otherwise.

| Workspace Signal | Command Prefix | Example |
|---|---|---|
| `.fvmrc` / `.fvm/` present | `fvm flutter` / `fvm dart` | `fvm flutter analyze` |
| Standard Flutter SDK | `flutter` / `dart` | `flutter test test/modules/<feature>/` |

## 2. Deterministic Flutter Gate Matrix (`G0`–`G8`)

Run in order from the Client root holding `pubspec.yaml`. A later gate never replaces an earlier one (`evidence-standard` §2).

| Gate | Purpose | Command / Tool (standard prefix shown) | Runs When |
|---|---|---|---|
| **G0** | Developer Tools Check | `coder-nexus setup tools --pack flutter --check` | `PHASE-00` & before first phase gate (`PASS` when `TOOLS: READY`) |
| **G1** | Code Generation | `dart run build_runner build --delete-conflicting-outputs` | Phase adds or modifies generated models, routes, or DI annotations |
| **G2** | Static Analysis | `flutter analyze` | Always on every task and phase end (`0 errors, 0 warnings`) |
| **G3** | Code Metrics & Linter | `dart run dart_code_linter:metrics analyze lib` | Every phase end on touched modules (`0 violations`) |
| **G4** | Architecture Validators | MCP `validate_architecture_code` & `validate_module_architecture` | Every phase end on touched `lib/modules/<feature>/` files (`PASS`) |
| **G5** | Unit & Widget Tests | `flutter test test/modules/<feature>/` | Always when module unit/cubit/widget tests exist (`{{slot:unit-testing}}`) |
| **G6** | Golden Screenshot Tests | `flutter test <golden_test_path>` (never `--update-goldens` in verification) | Screen phases where `golden_screenshot` baseline exists and is approved |
| **G7** | Runtime Visual Check | `{{slot:visual-quality}}` on approved target & 4 states (`Loading`, `Content`, `Empty`, `Error`) | Every phase with `UI Impact: Yes` (`FE_MOCKOON` or `BE_LIVE` per `D-NN`) |
| **G8** | Target Flavor Build | `flutter build <target> --flavor <flavor> -t <entrypoint>` | Closing phase or when native/plugin/flavor config changes |

## 3. Canonical Gate Results & Role Verdicts

| Gate Flag | Meaning | Rule |
|---|---|---|
| **`PASS`** | Command/check ran on `REVIEW_REVISION`, exited `0`, and observable output confirms non-empty scope | Record command, `cwd`, revision, exit code, and key output/artifact path. |
| **`FAIL`** | Command/check ran and found an actionable defect (`exit != 0`, analyzer warning, test failure, visual regression) | Blocks `READY_FOR_REVIEW`, `APPROVED`, and `ACCEPTED`. Return to implementation (`{{slot:root-cause-debugging}}`). |
| **`BLOCKED`** | External/environment blocker (missing tool, device/emulator unavailable, unreachable live endpoint, Mockoon failure) | Never counts as `PASS`. Name the exact blocker and owner. |
| **`NOT_RUN`** | Required check was not executed, or `0` tests ran / tests were skipped | Never counts as `PASS`. |
| **`UNVERIFIED`** | Claim made without an executed command or verifiable evidence row (e.g., lexical check alone for a runtime screen contract) | Treated as a failure to verify; never counts as `PASS`. |
| **`N/A`** | **Visual check (`G7`) only**: approved task/phase has `UI Impact: No` and records why | Never used to skip required analyzer or test gates. |

- **Role Verdicts (`shared_contracts/flags_and_statuses.md` §4–§5)**:
  - **Code Writer**: `READY_FOR_REVIEW` (all applicable `G0`–`G8` `PASS` on committed revision) or `BLOCKED`.
  - **Code Reviewer**: Re-runs `G1`–`G6` and inspects `G7` visual/golden artifacts on `REVIEW_REVISION` → `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED`.
  - **Test Runner**: Executes independent UI & Acceptance matrix (`G2`, `G5`–`G8`) on `REVIEW_REVISION` → `ACCEPTED`, `CHANGES_REQUESTED`, or `BLOCKED`.

## 4. Mandatory Rules (`V1`–`V8`)

| ID | Mandatory Rule |
|---|---|
| **V1** | **Detect, never assume** — Confirm `.fvmrc`, flavor, entrypoint, device target, and `architecture_profile` before running commands. |
| **V2** | **Verify the exact `REVIEW_REVISION`** — `git status --short` must be clean (or explicitly scoped). Any code, test, asset, or pubspec edit invalidates prior evidence. |
| **V3** | **Never bend a gate or update goldens in verification** — `--update-goldens` is baseline authoring for Code Writer + Reviewer visual sign-off, never a verification `PASS` command. |
| **V4** | **Preserve API & data provenance** — Label `FE_MOCKOON` fixture checks separately from `BE_LIVE` integration; Mockoon success never closes live endpoint ACs (`api_handshake_protocol.md`). |
| **V5** | **Inspect real images** — A saved file path alone is `UNVERIFIED`; open and inspect screenshots across all 4 states (`Loading`, `Content`, `Empty`, `Error`). |
| **V6** | **Never fabricate data or touch Huly** — Never invent business records, mock classes in `lib/`, or write to Huly. |
| **V7** | **Read-only verification pass** — Never edit production code, tests, or dependencies during review or `test_runner` verification; return `FAIL` → `CHANGES_REQUESTED`. |
| **V8** | **Strict status vocabulary** — Use only `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `UNVERIFIED` (`N/A` for non-UI visual only) and `APPROVED` / `ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`. |

## 5. Reference Guides

| Topic | Reference File |
|---|---|
| Execution order, exit/output rules for `G0`–`G8`, data provenance (`FE_MOCKOON` vs `BE_LIVE`), and revision invalidation | [01-gates-and-check-contract.md](references/01-gates-and-check-contract.md) |
| Planning `PHASE-00` readiness scan, vertical phase slicing, task/phase check conventions, and Review Definition of Done | [02-planning-readiness-and-phase-dod.md](references/02-planning-readiness-and-phase-dod.md) |
| Test Runner UI/Acceptance matrix, 4-state runtime & golden verification rules, and copy-ready `verification_report.md` template | [03-visual-acceptance-and-report-template.md](references/03-visual-acceptance-and-report-template.md) |
<!-- {{profile_references}} -->
