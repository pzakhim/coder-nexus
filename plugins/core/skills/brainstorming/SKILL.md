---
name: brainstorming
description: Discovers and confirms functional requirements, UI expectations, and acceptance criteria via Socratic grill-me rounds (goal question with sufficiency summary first, then drafting requirements.md + codebase-notes.md and locking in Q-NN -> D-NN one question at a time) before handoff to Planning.
---

# Brainstorming (Requirements Discovery & Grill-Me)

This skill guides the **Spec Writer Agent (Technical BA)** in discovering and confirming requirements, acceptance criteria, and initial technical boundaries for new Client work in `.superpowers/work-items/<slug>/vN/` or `docs/features/<module>/<feature>/vN/`.

## Gate 1 — Requirements Discovery & Socratic `grill-me` Loop (`1A` $\to$ `1B Draft` $\to$ `1C Grill 1-by-1` $\to$ `1D Lock In`)

**Order**: the canonical order in the `spec_writer` agent §3 (1A sources → 1A-0 job type → 1A-G goal + sufficiency → 1B draft → 1A-UX designer → 1C remaining questions → Gate 1).

**Iron Law**: Draft `requirements.md` (`Status: DRAFT`) + `codebase-notes.md` in the turn the goals are confirmed, queue every ambiguity or inference as `Q-NN` (`OPEN`) in `codebase-notes.md`, and interview the user **one question at a time** via `ask_question` until `0 OPEN Q-NN` remain before presenting Gate 1 for approval.

1. **Stage 1A — Three-Pillar Source Intake (`ask_question` when missing)**:
   - Confirm the exact sources for:
     1. **PO/BA Requirements**: Huly task (read once via `huly_get_task_detail`), external PO/BA specification file, or direct user prompt.
     2. **UI Screens, UX & Design System**: Screen definitions, UX flows, and design system specs (typically exported from the design tool into `.md` files or attached visuals). Record them in the Source Inventory. The **Visual Intake Gate** belongs to Designer at Step 1A-UX (approved `design-uiux/` revision); only when Designer returns `SKIPPED` for a UI-affecting item (an existing visual approved as `D-NN`) inspect that visual directly, and with no visual record `VISUAL_INPUT_MISSING` and confirm layout expectations (`planning` owns `{{slot:core-usage}}` profile resolution and UI Kit component mapping at Gate 2).
     3. **API Integration Source (Binary Check: Does BE API Exist?)**:
        - **If BE API exists (`BE_API_READY`)**: Record the API specification (Huly BE task, Swagger/OpenAPI, or `.md` file) in `codebase-notes.md`.
        - **If BE API does not exist or has missing endpoints (`MOCKOON_MOCKED`)**: Request the user to use **Mockoon**; `spec_writer` defines the required business Input/Output in `requirements.md` and `codebase-notes.md`, and `planning` designs the Mockoon data (`mocks/<feature>_mockoon.json`) and allocates `PHASE-00` (`phase-00-prepare.md`) to prepare the Mockoon API mock so FE integrates via the real `RemoteDataSource` (`ApiService`).
1G. **Stage 1A-0 / 1A-G — Job type and goal question**: ask the job type only when the ticket is no longer new, then one goal question with the source inventory, goal candidates, non-goals, conflicts and the sufficiency summary (`grill-me` §2.1).
2. **Stage 1B — Input Analysis, API Gaps & Draft (`DRAFT`, the turn the goals are confirmed)**:
   - Read the confirmed sources and run the codebase scan (`docs/features/<module>/<feature>/vN/` or `.superpowers/work-items/<slug>/vN/`; for v2+, compare previous approved requirements/design and actual code in `change-impact.md`).
   - Cross-check UI/UX flows against available APIs to detect **API count or schema gaps** (e.g., user estimates 3 APIs, but the screen flow requires 4 APIs) and identify necessary adjustments against the existing business flow in code.
   - Write **`requirements.md`** (`Status: DRAFT`, marking unresolved points with `(Q-NN)`) and **`codebase-notes.md`** (populating `## 0. Question Queue (Q-NN)` with `OPEN` rows and `## 3. Verified Baseline Facts & Cross-Agent Notes`).
2U. **Stage 1A-UX — Designer (UI impact only)**: call Designer with the goals and the draft; it asks the `Owner: designer` rows and returns the approved `uiux.md` revision (`READY_FOR_SPEC`), `SKIPPED` or `BLOCKED`.
3. **Stage 1C — Interactive Open Questions & Cross-Agent Consultation (`grill-me` + `ask_question` 1-by-1)**:
   - Ask **strictly 1 question per `ask_question` call** (`questions` length = 1) for the top `OPEN` `Q-NN` you own in `codebase-notes.md` (order `grill-me` §2.2, with `câu i/N`), with 2–3 viable choices and `(Recommended)` first.
   - Classify each user reply:
     - If the user asks a counter-question or requests clarification $\implies$ explain clearly (and if outside `spec_writer` expertise, **never fabricate an answer** — ask the coordinator to consult `planning` or `code_writer`, record the verified finding in `codebase-notes.md`, and relay it to the user) and re-ask `Q-NN`.
     - If the user confirms a choice $\implies$ mark `Q-NN` as `CLOSED -> D-NN` in `codebase-notes.md`, append `D-NN` to `## 1. Decision Log (D-NN)`, update `requirements.md` (`(Q-NN)` $\to$ `(D-NN)`), and ask the next `OPEN` `Q-NN`.
4. **Stage 1D — Artifact Finalization & Validation**:
   - Once `0 OPEN Q-NN` remain in `codebase-notes.md`, set `requirements.md` `Status: PENDING_REVIEW` (using [requirements.md.tpl](../work-items/templates/requirements.md.tpl) and [codebase-notes.md.tpl](../work-items/templates/codebase-notes.md.tpl)).
   - Validate both files with `validate_proposal_spec(proposal_path=".../codebase-notes.md")` and `validate_proposal_spec(proposal_path=".../requirements.md")`.
5. **Gate 1 Approval**:
   - Present exact revision to user via `ask_question` for actual user approval.
   - Never self-approve or mark `APPROVED_BY_SPEC`.
6. **Handoff to Planning Agent (Tech Lead)**:
   - Upon Gate 1 user approval, hand off `requirements.md` and permanent `codebase-notes.md` to `planning` with `READY_FOR_PLANNING`.
   - `planning` assumes technical ownership for **Gate 2 (Architecture Design via `{{slot:architecture-design}}`)** and **Gate 3 (Execution Planning via `planning-and-task-breakdown`)**.
