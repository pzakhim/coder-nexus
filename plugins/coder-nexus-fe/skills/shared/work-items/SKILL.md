---
name: work-items
description: Routes new Frontend Client features, fixes and other development outcomes through five specialist agents and a docs writer.
---

# Frontend Client work items

New work belongs in `${workspaceFolder}/.superpowers/work-items/<slug>/vN/` in Client Git. Read [the work-item contract](references/work-item-contract.md), then only the selected row in [type sequences](references/type-sequences.md). Historical `docs/features/` versions remain readable; do not migrate or rewrite them. Plugin files are guidance, not a runtime orchestrator. The host coordinator assigns agents, asks the user, records real approvals and updates execution evidence.

Render only needed artifacts from [requirements](templates/requirements.md.tpl), [codebase-notes](templates/codebase-notes.md.tpl), [brief](templates/brief.md.tpl), [design](../../flutter/architecture-design/templates/design.md.tpl), [plan](templates/implement-plan.md.tpl) and [phase](templates/phase.md.tpl). Resolve every placeholder from real sources before asking for approval; skip optional files instead of creating empty sections.

For Flutter UI tasks, Planning classifies destinations using [the screen contract](../../flutter/clean-architecture/references/05_screen_contract.md) and records `architecture_profile.mode` with evidence in design (brief for phase-free work). Only iMESPro requires company setup, BaseScreen and company GUIDEs. External-structured follows verified Client naming/bases; external-standard uses standard Flutter. Missing an API actually required by the approved profile is `BLOCKED`. Carry the selected profile and applicable routing/lifecycle checks through each handoff.

## Route

1. **Spec Writer (Technical BA):** classify the outcome, run **1A Source Intake** (confirm PO/BA source, Figma `.md` UI/UX & design system source, and binary BE API check: `BE_API_READY` vs. `MOCKOON_MOCKED`), **1B Gap & Flow Analysis** (detect API count/schema gaps and current business flow adjustments, and immediately draft `requirements.md` (`Status: DRAFT`) + `codebase-notes.md` with `OPEN` `Q-NN` rows in `## 0. Question Queue (Q-NN)`), and **1C Interactive Open Questions** via `grill-me` + `ask_question` (**1 question at a time**, putting `(Recommended)` first, allowing user counter-questions, consulting `planning` / `code_writer` for out-of-scope technical questions without guessing, and closing each confirmed `Q-NN -> CLOSED -> D-NN` in `codebase-notes.md` while updating `requirements.md`) until `0 OPEN Q-NN` remain; features also require `design.md` (authored by Planning at Gate 2), while other types use it when needed. Feature Gate 1 approves the exact `requirements.md` and `codebase-notes.md` (or `brief.md` for small phase-free items) revision. Returns `READY_FOR_PLANNING` after Gate 1 approval.
2. **Planning (Tech Lead / Architect):** consume approved `requirements.md` and `codebase-notes.md`. Owns two distinct technical deliverables:
   - **Gate 2 (Architecture Approval):** Perform the Pre-Design Counter-Review & `grill-me` Q&A loop first (queueing any Core gap, architectural trade-off, or Mockoon trigger question as `Q-NN` in `codebase-notes.md`, asking 1 question at a time via `ask_question`, and closing into `D-NN`), then write a decisive, straight-line `design.md` citing `D-NN` across the 7 architectural pillars (architectural decision, Clean Architecture directory tree, BaseScreen/routing, state machine, API integration & Mockoon data design, Core usage + UI mapping, and UX error/storage policies) using skill `architecture-design`. Retain `codebase-notes.md` permanently throughout the entire `vN/` lifecycle.
   - **Gate 3 (Plan Approval):** For a feature, write `implement-plan.md`, `phases/phase-00-prepare.md`, and sequential `phases/*.md` (with ordered micro-tasks per phase) using skill `planning-and-task-breakdown`. For non-feature types, return `SKIPPED` when brief/requirements tasks/checks are executable.
3. **Code Writer or Docs Writer:** implement a bounded task or first ready behavior phase using `requirements.md`, `codebase-notes.md`, `design.md`, and `phases/phase-NN-*.md`. Docs Writer owns reader-facing docs and documentation-only items. Do not treat planned code or docs as built.
4. **Code Reviewer:** inspect the same diff and relevant callers, tests and docs; run architecture/analyzer and runtime visual review where applicable. Return actionable findings or an approval tied to revision.
5. **Test Runner:** independently run type-specific checks on the reviewed tree using `requirements.md`, `codebase-notes.md`, and `design.md`. Docs Writer records phase evidence in `as-built.md` from the actual review and test reports; the coordinator checks provenance, records approval references, and owns item status. For findings-only work, use `verification.md` as needed. `NOT_RUN`, `BLOCKED` and `UNVERIFIED` cannot become `PASS`. Any fix invalidates affected review/check evidence.

Use [tool usage](references/tool-usage.md) for the exact conditions, inputs and limits of Hub MCP tools. Use existing `flutter-clean-architecture`, `flutter-code-review`, `flutter-verification` and visual skills only for affected boundaries. Keep Huly read-only and credentials in the Client. No fake business data, APIs, package variants or results.

## Ownership and handoff

| Agent | Writes | Returns |
|---|---|---|
| Spec Writer | `requirements.md`, `codebase-notes.md` (and `brief.md` for phase-free items) | `READY_FOR_PLANNING`, findings-only `READY_FOR_VERIFICATION`, or `BLOCKED` |
| Planning | `codebase-notes.md` (`D-NN`), `design.md` (Gate 2), `implement-plan.md` & `phases/*.md` (Gate 3) | `READY_FOR_BUILD`, `SKIPPED`, or `BLOCKED` |
| Code Writer | Assigned Client runtime and test files | `READY_FOR_REVIEW` with full diff scope |
| Docs Writer | Assigned reader-facing docs; phase `as-built.md` after review and tests | `READY_FOR_REVIEW` for reader docs; evidence-backed phase record for coordinator |
| Code Reviewer | `.agents/reviews/` report | `APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED` |
| Test Runner | `.agents/evidence/` report | Per-AC `PASS`, `FAILED`, `BLOCKED`, or `NOT_RUN` |

Every handoff includes item/version/type, approved document revisions and user response references where required, AC IDs, task or phase, base/review revisions, staged/unstaged/untracked scope, affected files, planned checks, UI target/states, and unresolved blockers. The coordinator alone changes item status and verifies that `as-built.md` matches the underlying evidence. Docs Writer joins before final review when reader-facing docs are part of acceptance; it records the phase's as-built evidence after Test Runner reports.
