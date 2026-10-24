# Changelog

All notable changes to Coder Nexus are documented here.

## [Unreleased]

### Added
- **Bug Fixer:** new entry skill `defect-resolution`, next to `dev-team`, and an 8th agent `bug_fixer` (core profile plus frontend-layer and Flutter overlays). A reported bug is reproduced first, then given a root cause, a severity (S1–S4) and a fix level (L1 quick patch, L2 local fix, L3 escalate) that the user confirms. L1/L2 are fixed in `.superpowers/debug/<bug-slug>/`; L1 goes straight to `test_runner`, L2 is reviewed by `code_reviewer` (with the fixing plan's `## Review focus`) before `test_runner`; L3 gets an escalation report and goes to `dev-team`. Contract: `work-item-contract` → `debug-item-contract.md` with templates `bug-brief`, `fixing-plan` and `escalation-report`; writing guide: `fix-planning`. Contract- and render-tested only; not yet run on a real bug.
- **Debug investigation:** new entry skill `debug-investigation`. The Bug Fixer reproduces a bug or traces a feature's runtime flow, may add temporary logs (never committed, removed with the same `git status`/`git diff` as before), and writes `diagnosis.md`; no code change is kept. A diagnosed bug can move to `defect-resolution` without repeating the investigation. Flutter: tagged `debugPrint`/`log`, a temporary `BlocObserver`, `flutter logs`, DevTools.
- **Feature testing:** new entry skill `feature-testing`. The Test Runner runs a scenario the user gives (free text or file) on the current revision, applies default checks DC1–DC4 when no expected result is stated (`expected inferred`), and reports per-case PASS/FAIL with evidence, gaps and suggested cases (listed after the run, not executed). Read-only; contract `test-run-contract.md` with templates `test-scenario`, `test-plan`, `test-run-report`.

- **Flutter user guide:** a pack may ship a `GUIDELINE.md`, copied by the build next to the plugin's json files (`.agents/plugins/coder-nexus/GUIDELINE.md`) on every sync. The Flutter pack's guide (English) covers which skill to call, setup, `dev-team` (inputs, API source, with or without a design), `defect-resolution`, `debug-investigation`, `feature-testing` and the `.superpowers/` folders.

### Changed
- **Agents split by tier:** each agent rule now lives in one tier. Core agents are stack-neutral: no "Client", `lib/`, `Mock<Feature>` or UI-kit table names, and PHASE-00, task-field and template details point to their skills. Frontend-only rules live in `plugins/layers/frontend/`. Flutter overlays point to `core-package-usage` instead of restating Mode 1/2/3. Unmaintained `web-standard` notes were removed. Rendered agents shrink by about 10% (Flutter) and 6% (Backend).
- **Flutter UI Kit rule** follows `core-package-usage`: use a UI Kit widget when its GUIDE "Use when" fits.
- **Backend `spec_writer`** no longer loads `backend-clean-architecture`.

## [3.2.0] - 2026-10-23

See detailed release notes in [docs/releases/v3.2.0.md](docs/releases/v3.2.0.md).

### Breaking Changes
- **Core Skill Renames:** Renamed 12 core skills to formal process names (`delivery-workflow`, `requirements-elicitation`, `architecture-decision-records`, `implementation-planning`, `change-control`, `review-workflow`, `review-resolution`, `quality-acceptance`, `evidence-standard`, `huly-task-intake`, `user-documentation`, `ui-ux-design`).
- **Pack Slot Renames:** Renamed 6 pack slots (`unit-testing`, `api-contract-design`, `visual-quality`, `core-package-usage`, `ui-kit-mapping`, `secure-coding-standards`).
- **Skill Migration to Packs:** 6 skills removed from `plugins/core/skills/` and migrated to stack packs (`clean-code`, `secure-coding-standards`, `code-simplification`, `unit-testing`, `root-cause-debugging`, `bug-hunt`).

### Features & Architecture
- **Mandatory Pack Slots:** Enforced in `plugin_build.py` via `slots.json` required list.
- **Generator Traceability:** Added `generated_from` in `pack.json` with test validation.
- **Flutter & Backend Packs:** Fully generated skills conforming to Skill Factory generators.
