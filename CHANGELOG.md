# Changelog

All notable changes to Coder Nexus are documented here.

## [Unreleased]

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
