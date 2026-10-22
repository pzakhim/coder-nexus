---
name: feature-planner
description: Routes a Client feature through versioned requirements, codebase-notes, design and phase planning with three user approval gates.
---

# Feature Planner

Resolve foundation evidence via `{{slot:core-usage}}`. Planning records the profile at Gate 2. Kit-matching rules below apply to the company-foundation profile or a verified Client design system; the minimal profile uses the framework's standard components (see `{{slot:core-usage}}`). Preserve the approved profile in downstream work.

This skill is a legacy reader for existing `docs/features/` history. Route all new Client work through `work-item-contract` at `.superpowers/work-items/<slug>/vN/`; use the router below only to read or extend a historical `docs/features/` version.

When updating an existing feature's UI design, classify screen destinations with the screen contract in `{{slot:clean-architecture}}` and record verified base, metadata and layout ownership; do not migrate unrelated historical files.

Coordinate one feature under `docs/features/<module>/<feature>/vN/` (or `.superpowers/work-items/<slug>/vN/`) in Client Git. One version represents one approved change batch and may cite several real Huly tickets. The feature README indexes versions. Coordinator commits approved documents and later actual as-built evidence to Client Git. Keep plugin/runtime artifacts in `.agents`; old `.agents/brainstorm` and `.agents/plan` specifications are LEGACY read-only context.

## Workflow router

1. **Intake:** Read user input, Huly via `huly_get_task_detail` when present (read-only; a parent issue with `sub_issues` is one feature: one spec, children as requirement sources and planning input; a child issue is scoped to itself with the parent as context — see `huly-task-runner` `references/parent-and-sub-issues.md`), current Client code, existing feature docs and supplied visuals. Classify `INIT`, `EXTEND`, `CORE IMPACT` with [context scan](references/01_context_scan_and_module_routing.md) and the stack scan in `{{slot:architecture-design}}`. For v2+, compare prior approved docs, `as-built.md` and actual code revision in `change-impact.md`.
2. **Gate 1 — requirements & codebase-notes (`spec_writer`):** First run `goal-framing`: build the source inventory, then confirm 1–3 outcome goals with the user as the first question and write `## 0. Goals`. Every later question, BR, AC, design element and phase serves a confirmed goal (goal lock in `work-item-contract`). Interview with `grilling` (mode spec). Follow the canonical order in the `spec_writer` agent §3 (1A sources → 1A-0 job type → 1A-G goal + sufficiency → 1B draft → 1A-UX designer → 1C remaining questions → Gate 1). The goal question carries the sufficiency summary; in the turn the goals are confirmed, draft `requirements.md` (`Status: DRAFT`) and `codebase-notes.md` (with ordered `OPEN` `Q-NN` rows in `## 0. Question Queue (Q-NN)`). For UI impact, Designer then obtains approval of the `design-uiux/` revision, which Gate 1 covers together with the requirements. Interview the user **one question at a time** via `ask_question`, closing each `Q-NN -> CLOSED -> D-NN` in `codebase-notes.md` and updating `requirements.md` until `0 OPEN Q-NN` remain. Write final `requirements.md` (`Status: PENDING_REVIEW`) + `codebase-notes.md` (plus `change-impact.md` for v2+). Call `validate_proposal_spec` on each. Present exact revision through `ask_question`. Continue only after actual user approval; `valid: true` is not approval.
3. **Gate 2 — design (`planning`):** Inspect module and `get_project_structure(scope="module")`; resolve any Core risks, Core gaps, or overlapping business logic with `spec_writer` and the user via `grilling` + `ask_question` (1 question at a time, recording `D-NN` in `codebase-notes.md`) before writing a decisive, straight-line `design.md` (citing `D-NN`, zero `Option A/B`). For UI, the approved `design-uiux/` revision is the Visual AC (Designer owns the **Visual Intake Gate**); only when Designer returned `SKIPPED` for a UI item, inspect the supplied image/design-export `.md` directly, derive Visual AC/states, read the selected profile’s UI guidance via `{{slot:core-usage}}` and call `get_ux_error_patterns`. Missing visual means `VISUAL_INPUT_MISSING`, minimal layout spec and user confirmation. Lean mode may reduce depth, never skip a supplied visual. Select one viable Kit component automatically even if its styling differs from the visual; record the Kit choice in Visual AC. Multiple viable components require a user choice. With no viable Kit component, check shared widgets and composition before planning private code. Only a company-foundation setup failure blocks on company packages; other profiles require no company setup or GUIDE. Write `design.md`, call validator, ask approval for exact revision. Retain `codebase-notes.md` permanently across the entire `vN/` lifecycle. Code that differs from the Kit choice or approved Visual AC is `FAILED`.
4. **Gate 3 — plan (`planning`):** After design approval, use `planning-and-task-breakdown`. Write `implementation-plan.md`, `phases/phase-00-prepare.md`, and sequential `phases/phase-XX-<behavior>.md`. Map every AC to phases with owners, files, dependencies, code direction, verified UI/framework source, verification target/commands and done criteria. Call `validate_plan_slices(plan_path="...")`. Present the plan **and all linked phase files** for actual approval before marking the first phase `READY`.
5. **Implement, review, verify:** Hand feature/version path, approved document revisions (`requirements.md`, `codebase-notes.md`, `design.md`), Gate 1–3 approval references, phase ID, AC IDs, planned checks and required UI states to Code Writer. Pass its base/review revisions and complete staged/unstaged/untracked scope to Reviewer. Reviewer runs analyzer and applicable runtime visual review before `APPROVED`; only then does Test Runner run required tests, regressions and build on the same tree. Coordinator alone writes actual progress, code revision, review and test evidence into `as-built.md`; approved plan remains stable. A changed tree invalidates affected evidence.

## Shared evidence rules

- Huly is optional. Missing ticket requires real `USER_CONFIRMED` / `D-NN` source or a `BLOCKED` AC, never an invented ID.
- Core GUIDE entries are confirmed against package source before use; source wins over the guide.
- For multi-screen work, resolve applicable state, back/navigation, errors, input dependencies, security and post-flow effects; mark inapplicable axes N/A with reason.
- Avoid horizontal Vertical Slices such as widgets → screens → router. Add Domain/Data/Presentation/DI only where behavior needs them.
- `NOT_RUN` and `BLOCKED` are not `PASS`. Reuse approval only for the same scope and revision. Material changes return to the affected gate.
- Never invent endpoints, package APIs, tokens, task data, test results or fallback data.

## Ownership

| Stage | Owner | Artifact |
|---|---|---|
| Requirements & Context (Gate 1) | `spec_writer`, `goal-framing`, `grilling` | `vN/requirements.md`, `vN/codebase-notes.md`, `vN/change-impact.md` for v2+ |
| Design & Plan (Gate 2 & Gate 3) | `planning`, `grilling`, `{{slot:architecture-design}}`, `planning-and-task-breakdown` | `vN/codebase-notes.md` (`D-NN`), `vN/design.md`, `vN/implementation-plan.md`, `vN/phases/*.md` |
| Code | `code_writer`, `incremental-implementation` | Approved phase and code diff |
| Tests/review | `test_runner`, `code_reviewer`, verification skills | Revision-bound reports under `vN/evidence/` or `vN/reviews/` |
| Status | Coordinator | `vN/as-built.md`, feature `README.md` |

Resolve Client paths from `${workspaceFolder}`; do not include Hub author's absolute paths.
