# 01 — Codebase Readiness and Gap Analysis Protocol

Read plugin-root `shared_contracts/api_handshake_protocol.md`. Only explicitly approved contract-derived development fixtures may support UI/contract checks. Record fixture provenance and contract revision separately from live integration evidence. Required live ACs remain `BLOCKED` or `NOT_RUN` until exercised against the real endpoint; fixture success cannot close the handshake or imply overall feature acceptance. Never fabricate business records, Huly data, services or production success fallbacks.


This reference guides the Planning Agent (Tech Lead) in executing the mandatory 3-input verification before formulating any implementation plan or task breakdown.

## 1. Three Input Verification Requirements

Planning must confirm three complete inputs before writing tasks:
1. **Feature Requirements & Scope**: Approved `brief.md` or `requirements.md` covering the 5 Frontend Pillars and Gate 1 approval.
2. **UI/UX & Design System**: Approved visual source/layout, token definitions, and UI Kit candidate matching (Gate 2 approval).
3. **Current Codebase Scan (Readiness & Gap Analysis)**: An active scan of the target repository to verify what exists and what is missing.

## 2. Framework-Specific Codebase Scan Checklist

Every stack scans the same four areas; the stack-specific checklist (file names, packages, commands) lives in the installed stack skills — read the codebase-scan reference of `{{slot:verification}}` (or of `{{slot:clean-architecture}}` when the stack keeps it there):
1. **Foundation & UI kit**: Read the approved foundation profile via `{{slot:core-usage}}`. Only a failed setup that the selected profile requires blocks on company dependencies. Do not invent required missing APIs.
2. **Routing & Screen Registry**:
   - Check the Client's router configuration.
   - If route definition is missing for the new screen, plan a task to register it before screen assembly.
3. **State Management & DI**:
   - Verify the active state management and DI conventions of the Client.
4. **Reuse before build**:
   - For each need, decide with `{{slot:core-usage}}`: reuse a fitting core API, else the target module, else a Client shared folder when two or more modules need it. Record every gap in the `Core usage` table.

## 3. Backend API Dependency & Mockoon Strategy Protocol

1. **Case 1 — BE API Exists (`BE_API_READY`)**:
   - Request the user to provide the BE API specification (Huly BE task, Swagger/OpenAPI, or `.md` file) and plan integration tasks directly against the documented endpoints.
2. **Case 2 — BE API Does Not Exist or Missing Endpoints (`MOCKOON_MOCKED`)**:
   - Request the user to use **Mockoon** and design the Mockoon data (`mocks/<feature>_mockoon.json` with realistic 200/400/500 response rules) in `design.md` based on the business Input/Output in `requirements.md`.
   - Allocate **`PHASE-01` (`phase-01-prepare-mockoon-api.md`)** as the initial phase to prepare and verify the Mockoon API mock before subsequent feature phases (`PHASE-02`+) integrate the FE layers.
   - In the Client source, always implement the real remote data source calling the Client's API service (domain from configuration) — never create fake mock data source classes in Client source. Switching to live BE only updates the `.env` domain; if the delivered BE contract changes, return to the affected approval gate.
   - **Zero Cross-Repo Mutation**: Never generate tasks that modify Backend repositories, server code, or database schemas.

## 4. Gate 3 User Negotiation & Plan Freeze Protocol

When presenting the plan to the User via `ask_question`, provide 3 clear choices:
1. **[Approve Plan & Proceed to Build]**:
   - User approves plan and phase breakdown.
   - Freeze all specs and plans (`APPROVED_FOR_BUILD`).
   - Trigger `code_writer`.
2. **[Refine Technical Decisions]**:
   - User requests technical adjustments (mock approach, scaffold choice, task order).
   - Planning directly adjusts `implement-plan.md` and re-presents without involving Spec Writer.
3. **[Modify Business Requirements / Scope]**:
   - User requests changes to feature behavior, visual scope, or acceptance criteria.
   - Planning halts and transfers the request back to `spec_writer` to revise `brief.md` / `requirements.md` (Gate 1/2) first.
   - Prevents plan and specs from drifting apart.

## 5. Consultation during requirements (on demand)

Agents run only when the coordinator invokes them; Planning does not listen to the Spec Writer conversation in the background.

1. **Consult call**: when Spec Writer needs a codebase fact ("does module X exist?", "does the UI kit have a date picker?", "is setup READY?"), the coordinator invokes Planning with that one question.
2. **Answer and stop**: Planning reads the Client and core guides, answers with file/GUIDE evidence, and returns. It does not draft `design.md` or a plan before Gate 1 is approved.
3. **Use and clean up the temporary scratchpad**: Planning appends each answer to `.superpowers/work-items/<slug>/vN/codebase-notes.md` (question, answer, evidence path). At Gate 2 it starts from these notes instead of rescanning, consolidates all confirmed decisions into `design.md`, and deletes `codebase-notes.md` immediately upon Gate 2 approval.

