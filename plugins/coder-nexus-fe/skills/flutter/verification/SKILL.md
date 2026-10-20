---
name: verification
description: Verifies a reviewed Flutter revision with the approved analyzer, tests, build, and affected runtime visual checks, then records revision-bound evidence. Use after code review approval; return failures to implementation instead of fixing code in the verification pass.
---

# Flutter Verification

Read plugin-root `shared_contracts/api_handshake_protocol.md`. Read consolidated Huly and API context from `phases/phase-00-prepare.md` (`PHASE-00`), `requirements.md`, and `design.md` — never re-query Huly or fabricate business records, services, or production fallbacks.


For new Client work, use `.superpowers/work-items/<slug>/vN/brief.md` and optional design/plan/phase, then choose decisive checks from `flutter-work-items` by Type. A small item can have no phase. Run only checks relevant to affected Flutter boundaries, and record exact revision and provenance. The `docs/features/` contract below applies to historical features.

## Historical feature workflow

Verify the reviewed revision; do not modify production code during this pass. Read the same version's `requirements.md`, `design.md`, `phases/phase-00-prepare.md`, approved `implementation-plan.md`, linked `phases/phase-XX-<behavior>.md`, review report and [Client check contract](references/01_client_check_contract.md) before running commands.

For screen changes, verify the selected profile’s screen/base, routing and applicable tracking/responsive contract using actual Client source and target results. BaseScreen is mandatory only for iMESPro.

## Preconditions

- `BASE_REVISION` and `REVIEW_REVISION` are explicit, and the review report covers that range.
- Feature/version path, phase ID, AC IDs, approved document revisions and actual Gate 1–3 approval references are explicit; approvals cover their current revisions.
- `phases/phase-00-prepare.md` is ticked **`[x] PREPARED / COMPLETED`** (or **`[x] PREPARED (INFO_READY)`**).
- The review verdict allows verification. `CHANGES_REQUESTED` returns to `flutter-incremental-implementation`; `BLOCKED` remains blocked.
- Commands, working directory, flavor, entrypoint, target, and required UI states come from the approved plan and real workspace configuration.
- Staged, unstaged and untracked changes are absent or explicitly included in the review report. Never silently verify a different tree.

## Verification flow

1. Record Client workspace path, Hub source revision, installed plugin version, Flutter/FVM version, `BASE_REVISION`, `REVIEW_REVISION`, approved document revisions, approval references, planned checks and `git status --short`.
2. Build an independent **UI & Acceptance test-case matrix** from `requirements.md` (BDD Scenarios, 4 Visual States, AC table), `design.md` (UI State Matrix & Component Mapping), and `brief.md` (Scope In & Out-of-Scope boundaries). Isolated developer Unit Tests have already been reviewed and approved by Code Reviewer; `test_runner` does **not** use Mockoon payloads to run unit-level logic tests. Focus strictly on **UI / Widget / Golden Screenshot & Runtime Visual Verification** (layout, `app_ui_kit` widgets, screen interactions, and the 4 visual states: `Loading`, `Content`, `Empty`, `Error`). Never fabricate business data to fill a case.
3. Inspect the Reviewer's analyzer and visual evidence for the same tree. Run the approved checks in dependency order: required generation first, rerun analyzer when stale evidence requires it, then targeted widget/UI tests, affected regression tests and the required flavor build. Skip only checks the approved plan marks out of scope and record why. Run an approved `golden_screenshot` comparison with ordinary `flutter test` only when its dev dependency, test file and human-reviewed baseline are already present. `--update-goldens` is baseline creation, never a pre-release PASS command.
4. For UI impact, invoke `flutter-visual-verification` (ensuring `mockoon-cli` from `PHASE-00` is running in the background when `MOCKOON_MOCKED` is used). Reuse visual evidence only when revision, platform, target, flavor, route, data source, and required states all match. Open and inspect screenshots, then make the images and findings available to the coordinator for pre-release review. A saved path alone is not evidence.
5. Map each acceptance criterion and UI test case to an observable check and evidence. Use `PASS`, `FAILED`, `BLOCKED`, or `NOT_RUN`; only non-UI visual checks may use `N/A`, with a reason.
6. Create `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<review-revision>/verification_report.md` from [the report template](templates/verification_report.md.tpl). Send actual results to the coordinator for `as-built.md`.

## Verdict and handoff

- `PASS`: every required AC/check has current-revision evidence.
- `FAILED`: an executed check found a defect. Hand the failure to `flutter-incremental-implementation`.
- `BLOCKED`: environment, source, service, credential, permission, or target prevented a required check.
- `NOT_RUN`: a required check has not been attempted and the slice is not complete.

Any code fix creates a new revision and invalidates affected review, test, build, and visual evidence. Review the affected scope again before rerunning verification. Do not change tests merely to make an implementation pass, fabricate logs or business data, install dependencies, change flavors, or write to Huly.
