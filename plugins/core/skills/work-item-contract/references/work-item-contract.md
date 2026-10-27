# Work-Item Contract, Type Sequences & Hub Tool Usage

## 1. Document Roles, Versioning & Cross-Department Continuity

Classify the independently accepted **outcome**, not file count or code area. One primary `Type`: `feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`. Tests and docs supporting a feature stay in that item. Independently valuable outcomes use linked items. Record type, risk, and uncertainty separately.

New versions live at `.superpowers/work-items/<slug>/vN/`. Never overwrite a closed version. Link historical `docs/features/` or `.agents/plan` paths as read-only sources. Every `v2+` compares the previous approved contract with actual code and evidence in `change-impact.md` (`IMPACT-001..003`); never assume an old design shipped.

### Zero-Re-Ask Continuity (`spec_writer` → `planning` & `bug-squad` → `dev-team`)

1. **`requirements.md` and `codebase-notes.md`** (authored by `spec_writer` via [`grilling`](../../grilling/SKILL.md) and [`figma-intake`](../../figma-intake/SKILL.md); `brief.md` remains supported for small phase-free items) establish the **Gate 1** contract:
   - `requirements.md` is the **human-facing specification** ($\le \sim 120$ lines, pure business/UX language, zero code/class names, zero `Option A / Option B` or `Open Questions` sections): `## 0. Goals` (`G-NN`), `## 1. Scope & Alignment` (`Scope in` / `Scope out`), `## 2. Actors & Permissions`, `## 3. Business Rules` (`BR-NN` citing `D-NN`), `## Screens & Visual Sources` (`S-NN`), `## Workflows` (`W-NN`), `## 4. Behavioral Scenarios & Visual States` (`Given-When-Then`), `## 5. Acceptance Criteria` (`AC-NN`), and `## 6. Gate 1 Approval`.
   - `codebase-notes.md` is the **permanent agent-facing Single Source of Truth** retained throughout the entire `vN/` lifecycle: `## 0. Question Queue (Q-NN)` (must have `0 OPEN` rows before Gate 1 or Gate 2 approval), `## 1. Decision Log (D-NN)` (recording every confirmed user choice and options considered), `## 2. Glossary`, `## 3. Verified Baseline Facts & Cross-Agent Notes`, `## 4. Constraints & External Integrations`, `## 5. Extended Rule Details`, and `## 6. Change Log`. Only `spec_writer` and `planning` write `codebase-notes.md`; all other agents read it.
   - **Zero-Re-Ask Handoff Rule**: When `spec_writer` completes Gate 1 (`requirements.md` + `codebase-notes.md` with `0 OPEN Q-NN` + `BRANCH_READY`), it hands off `READY_FOR_PLANNING` to `planning` (Gate 2 & Gate 3). **`planning` inherits every confirmed `G-NN`, `AC-NN`, `D-NN`, `S-NN`, and `W-NN` without re-asking the user.** When `dev-team` is resumed after Gate 1 is already approved, `dev-team` skips `spec_writer` and starts directly at `planning`.
2. **`design.md`** (authored by `planning` via `{{slot:architecture-design}}` + [`grilling`](../../grilling/SKILL.md)) establishes the **Gate 2** technical architecture in one straight locked-in line across the architectural pillars (citing `D-NN` in `codebase-notes.md` without `Option A / Option B` sections).
3. **`implementation-plan.md`** (authored by `planning` via `implementation-planning`, required for a feature, optional for other types) maps `AC-NN` → task/phase → decisive check, names dependencies, file ownership, actual Client commands/targets, and recovery where relevant. Create `phases/phase-NN-<behavior>.md` only when later deliverables depend on a separately checked result. A feature's **Gate 3** covers `implementation-plan.md` **and all linked phase revisions**. Task fields, `Expected` triage, what Gate 3 freezes, and the `## Plan change log` are defined in [plan-and-task-contract](plan-and-task-contract.md); hand-offs and status words in [handoff-and-status](handoff-and-status.md).
4. **Phase Checkpoints & Final `as-built.md` Closure**:
   - During Phase 3 build, each phase runs `code_writer` (`READY_FOR_REVIEW`) → `code_reviewer` (`APPROVED`) → **Coordinator User Checkpoint** (asking the user before starting the next phase).
   - Once `test_runner` returns **`ACCEPTED`** in `final_qa` (or directly for a `documentation` item), the coordinator invokes `docs_writer` **once** to write the concise, visual [`as-built.md`](../templates/as-built.md.tpl) (including a Mermaid Flow Diagram, Delivered Code & Component Map, and Phase/Review/QA Evidence Ledger) and any required reader docs (`RECORDED`). Use `verification.md` for findings-only (`investigation`) items.

---

## 2. Type-Specific Sequences & Decisive Evidence

Read only the row selected for the work item. These are dependency patterns, not compulsory phase counts.

| Type | Sequence | Decisive Evidence |
|---|---|---|
| `feature` | Confirm goals → Figma/screen & workflow intake (`figma-intake` for UI items) → requirements & Gate 1 (`READY_FOR_PLANNING`) → `planning` Gate 2 `design.md` & Gate 3 `implementation-plan.md` → phased build & review → `final_qa` (`ACCEPTED`) → final `as-built.md` (`RECORDED`) | Approved Gate 1–3 revisions, AC scenarios, the stack's analyzer/test checks, required runtime UI states, and `ACCEPTED` QA report |
| `bugfix` | Reproduce expected vs actual → identify cause → narrow correction → regression | Reproduction fails before and focused regression passes after; nearby behavior remains intact |
| `refactor` | Capture public baseline → move coherent owner → compare contracts → remove obsolete path | Imports, routes, state, API, side effects, and errors remain as approved |
| `optimization` | Measure representative baseline → change bottleneck → measure same workload | Target metric and correctness meet brief on comparable conditions |
| `migration` | Define old/new compatibility → prepare → cut over → verify/recover | Data/contract integrity and recovery check; irreversible step named |
| `maintenance` | Reproduce tool/build problem → adjust → repeat check | Affected tool or pipeline succeeds under the stated environment |
| `investigation` | Gather evidence → test hypotheses → report recommendation in `verification.md` | Findings answer the decision question with sources and limits; code plan skipped |
| `documentation` | Verify source and reader task → write → check examples/links → record `as-built.md` | Reader can follow accurate instructions; `docs_writer` owns delivery |

For UI work, the extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`) or verified existing screen baseline are the visual input; `design.md` names real visual inputs, Kit candidates, required states, and target. For non-UI work, mark UI checks `N/A` with reason. A missing device, data source, service, or baseline remains `BLOCKED` or `NOT_RUN`.

---

## 3. Hub MCP Tool Usage & Deterministic Gates

Tools read Hub or Client evidence; they never approve a user gate or prove runtime Client behavior. Deterministic CLI/MCP tool checks return `PASS` or `FAIL` (or `UNVERIFIED` when lexical/static limits require Client analyzer inspection).

| Tool | When and Input | Required Interpretation |
|---|---|---|
| `huly_get_my_tasks`, `huly_get_task_detail` | `spec_writer` reads real Huly tasks when referenced or requested (`huly-task-intake`); detail takes an ID or pasted Huly link and returns status, people, parent, sub-issues, comments, and `sources`. Use `download: true` to save attachments and linked visual assets to `.superpowers/sources/<ISSUE-ID>/` (Git-ignored, local only) | Read-only. `UNREACHABLE` sources are reported to the user, never guessed. A missing Huly task may be replaced by actual user requirements, never an invented ticket |
| `get_project_structure` | `spec_writer` / `planning` / `code_writer` compare a root or module blueprint with the actual Client | Blueprint is guidance; inspect Client routing, state, DI, and files before naming paths |
| `get_ux_error_patterns` | When loading, empty, auth, timeout, or validation states apply | Use only relevant patterns; derive Visual AC from real visual and product decisions |
| `validate_proposal_spec` | Saved feature `requirements.md`, `codebase-notes.md`, `change-impact.md`, or `design.md` | Enforces straight-line docs (zero `Option A/B`, `Open Questions`, `TBD`, or `OPEN` `Q-NN` rows) and `D-NN` traceability; `valid: true` (`PASS`) is structural only; generic `brief.md` uses the work-item contract checklist |
| `validate_plan_slices` | Versioned feature plan with sibling `requirements.md`, `design.md`, and linked phase files | Cannot validate a brief-only item or phase-free plan; Gate 3 approval still comes from the user |
| `validate_architecture_code` | `code_reviewer` checks changed source with correct layer, when `{{slot:code-review}}` lists it for this stack | Lexical `UNVERIFIED` needs Client analyzer/inspection; never treat it as a compile pass |
| `validate_module_architecture` | `code_reviewer` checks an affected complete module | For scoped UI work use `N/A` with reason and inspect changed imports/state directly |
