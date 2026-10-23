---
name: architecture-design
description: Guides the Frontend Tech Lead / Solution Architect in researching codebase conventions, resolving architectural trade-offs via grilling and solution-options in codebase-notes.md, and producing a straight-line 7-section technical architecture specification (design.md).
---

# Frontend Technical Architecture Design Skill

Apply the approved profile through [core-package-usage](../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

This skill guides the **Frontend Tech Lead / Solution Architect (Planning Agent)** in researching the target workspace and drafting a straight-line **Technical Architecture Specification (`design.md`)** backed by **`codebase-notes.md`** for an approved work item at `.superpowers/work-items/<slug>/vN/`.

## 1. Input Contract (Prerequisites)

Before drafting `design.md`, verify:
1. `requirements.md` and `codebase-notes.md` (or `brief.md` for phase-free items) are approved at **Gate 1**.
2. Acceptance Criteria (ACs), `BR-NN` business rules, and `D-NN` decisions in `codebase-notes.md` are locked in.
3. If Backend API is pending (`MOCKOON_MOCKED`), the business Input/Output contract is recorded in `requirements.md` and `codebase-notes.md`.

## 2. Six Codebase Intelligence Anchors & Pre-Design Counter-Review (`grilling`)

Execute targeted read-only scans across the Client workspace before specifying technical solutions:

```text
Workspace Client Root
├── pubspec.yaml / package.json      ──> 1. Framework, State management (Bloc/Cubit), Router, DI, Network
├── Approved profile / core-package-usage    ──> 2. Company guides, Client foundations, or standard Flutter
├── Client router                    ──> 3. Router table, Route Arguments, Pop return value conventions
├── Client DI entry                  ──> 4. Service Locator (get_it), scope lifecycles (factory vs singleton)
├── lib/modules/<feature>/ + shared  ──> 5. Existing module code and Client shared folders to reuse first
└── MCP Tool: get_ux_error_patterns  ──> 6. Standard UX error handling patterns (401, 400, timeouts)
```

Read, then decide:
- **Strict Boundary with `spec_writer`**: `spec_writer` owns business API Input/Output and screen UX requirements (from Figma `.md`). `planning` owns the **Data Pipeline architecture** (`DataSource`/`Model`/`Repo`/`Cubit`/DI), **API Verification / Mockoon Trigger & Test Data Table**, and **exact Codebase & UI Kit class mapping** (`app_core`, `app_util`, `app_ui_kit`).
- **Pre-Design Counter-Review & Socratic `grilling` Loop (`ask_question` before writing `design.md`)**:
  - Reuse a core API when its GUIDE "Use when" matches; otherwise take the simplest Client solution under `lib/modules/<feature>/` and record a Core gap. Do not plan `lib/core/` layers unless two or more modules need them.
  - Whenever codebase scanning exposes a **Core Risk / Core Gap**, overlapping/conflicting logic with `requirements.md`, or a choice between viable architectural approaches/components, queue it as `Q-NN` (`OPEN`) in `codebase-notes.md` (`## 0. Question Queue (Q-NN)`) and ask the user **1 question at a time** via `ask_question` with `(Recommended)` first.
  - **When `MOCKOON_MOCKED`**: Propose and agree with the user via `ask_question` on which input data represents **Pass/Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)** so the **`Mockoon Trigger & Test Data Table`** in `design.md` serves as the single contract for both `mocks/<feature>_mockoon.json` (in `PHASE-00`) and developer Unit Tests.
  - When a `Q-NN` is a real choice between viable approaches, present 2-3 technical options with trade-offs via `solution-options`, recommended first.
  - Record a decision only when two independently built parts (two phases, screen and data layer, client and BE) could otherwise choose incompatibly. Reason: decisions the code itself makes obvious bloat `design.md` and still need review.
  - Close each confirmed technical choice into `D-NN` (`Owner: planning`) in `codebase-notes.md` (`## 1. Decision Log (D-NN)`).
  - `design.md` MUST be written in **one straight locked-in line** citing `D-NN` (never containing `Option A / Option B` headings, `Open Questions`, or `TBD`).

## 3. Seven Architectural Pillars & Reference Mapping

When writing `design.md`, each section MUST adhere to its dedicated reference guideline:

| Section in `design.md` | Dedicated Reference Guide | Core Deliverable |
| :--- | :--- | :--- |
| **1. Architectural Decision** | [01_architectural_options.md](references/01_architectural_options.md) | Straight-line confirmed architectural decision citing `D-NN` in `codebase-notes.md`. |
| **2. Target Directory Tree & Layout** | [02_directory_tree_clean_arch.md](references/02_directory_tree_clean_arch.md) | Only the `lib/modules/<feature>/` folders the feature needs. |
| **3. Screen, Routing & DI Contract** | [03_basescreen_and_routing.md](references/03_basescreen_and_routing.md) | Selected profile screen/base policy, route arguments, and DI scopes. |
| **4. State Management & Data Flow** | [04_state_and_data_flow.md](references/04_state_and_data_flow.md) | Cubit states (Client convention), methods, and needed UseCases/Repositories. |
| **5. Backend API Contract & Mock Strategy** | [05_api_mocking_strategy.md](references/05_api_mocking_strategy.md) | `BE_API_READY` audit or `MOCKOON_MOCKED` (`Mockoon Trigger & Test Data Table`), data pipeline, cutover plan (omit if no external API). |
| **6. Core Usage, UI Mapping & 4 Visual States** | [core-package-usage](../core-package-usage/SKILL.md), [06_ui_kit_mapping_states.md](references/06_ui_kit_mapping_states.md) | `Core usage` table (Need · reused API · or Client location + gap) and 4 visual states. |
| **7. UX Error Handling & Storage Policy** | [07_ux_error_and_storage.md](references/07_ux_error_and_storage.md) | Error pattern codes, fallback toasts/dialogs, and cache invalidation. |

### Optional subsections

Add these only when they apply, as `###` subsections inside the existing sections (never as new `##` sections, never renaming a validated heading). Details: [10_optional_design_subsections.md](references/10_optional_design_subsections.md).

| Subsection | Inside section | When |
|---|---|---|
| Deferred decisions | `## Architectural decision` | A choice this version does not need, with the reason it can wait and its revisit trigger |
| Complexity justifications | `## Foundation reuse ...` | A deviation from the approved foundation components; the cited `D-NN` records violation / why needed / simpler alternative rejected because |
| Risk → Mitigation | `## Integration, errors, and risks` | A known risk to an AC or goal |
| Migration plan and rollback | `## Integration, errors, and risks` | Local storage keys, cache schema or persisted format change |

## 4. Verification & Gate 2 Approval

1. Render `design.md` using [design.md.tpl](templates/design.md.tpl) only after all pre-design `Q-NN` items in `codebase-notes.md` are closed into `D-NN`.
2. Validate both `codebase-notes.md` and `design.md` with `validate_proposal_spec`.
3. Run `gate-review` with `modes/design.md` (it starts from the validator result), then `cold-reader-check` on `design.md`. Fix findings you own; minor questions are Planning's call and marked as such; user's-call questions become `Q-NN` in `codebase-notes.md`, asked one at a time and closed into `D-NN`. Present Gate 2 only with 0 `OPEN` `Q-NN`.
4. Present the technical blueprint to the User via `ask_question` for **Gate 2 (Architecture Approval)**.
5. Once Gate 2 is approved, retain `codebase-notes.md` permanently in the version folder and hand off to execution planning (`implementation-planning`) starting with `PHASE-00` (`phase-00-prepare.md`).

## 5. Flutter Values for Core Planning Skills

The core `delivery-workflow`, `dev-team`, `clean-code`, `code-simplification` and `user-documentation` skills are stack-neutral. Their Flutter specifics live here:

- [08_flutter_context_scan.md](references/08_flutter_context_scan.md) — detection, workspace scan paths, state patterns, router/DI anchors and screen-contract classification.
- [09_flutter_delivery_conventions.md](references/09_flutter_delivery_conventions.md) — profile/kit matching, analyzer and test commands, golden baselines, UI provenance, clean-code and docs conventions.
