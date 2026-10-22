---
name: incremental-implementation
description: Implements an approved plan one dependency-ready slice at a time with Clean Architecture, simple code, targeted checks, and recorded evidence. Use after plan approval; do not use for brainstorming or unapproved scope.
---

# Incremental Implementation

Read plugin-root `shared_contracts/api_handshake_protocol.md`. Read Huly and source context from `codebase-notes.md` (`## 0A. Source Inventory`, Huly table, `## 4`) and the API contract from `design.md`; `phases/phase-00-prepare.md` (`PHASE-00`) only records readiness and links to them — never re-query Huly or fabricate business records, services, or production fallbacks.


For new Client work, use the approved `.superpowers/work-items/<slug>/vN/brief.md` with optional design/plan/phase. A small non-feature task can be executable from the brief alone; a feature still requires all three actual user gates. Follow the chosen type's checks in `work-item-contract`. The versioned `docs/features/` preconditions below apply only to historical feature work.

## Historical feature workflow

Implement the smallest approved behavior that can be verified end to end. Apply `{{slot:clean-architecture}}` for project conventions, `{{slot:core-usage}}` for core and UI reuse, and `clean-code` while writing the task.

## Preconditions

- Gate 1–3 approvals cover the current `docs/features/<module>/<feature>/vN/` requirements, design, plan and linked phases.
- **For `PHASE-00` (`[EXECUTE]` — Mockoon preparation)**: `design.md` contains the approved `Mockoon Trigger & Test Data Table`. Upon completing `PHASE-00` (`mocks/<feature>_mockoon.json` + `mockoon-cli` smoke test) and passing review, tick **`[x] PREPARED / COMPLETED`** in `phases/phase-00-prepare.md` and `implementation-plan.md`.
- **For `PHASE-01, 02, 03...`**: `phases/phase-00-prepare.md` must already be ticked **`[x] PREPARED / COMPLETED`** (or **`[x] PREPARED (INFO_READY)`** when `PHASE-00` is `[INFO_NOTE]`), and all earlier phase dependencies are complete.
- File scope and verification commands are concrete.

## Slice loop & Task-by-Task Grounding (Sequential Single-Agent Execution)

**Strict Non-Negotiable Rule**: Prohibit ungrounded bulk coding. NEVER attempt to code all tasks of a phase in one blind pass without checkpoints. A single `code_writer` receives one phase at a time and executes its ordered tasks through the strict Task-by-Task Grounding Loop below:

1. **Phase Initialization**:
   - Open `phases/phase-00-prepare.md` (to confirm `[x] PREPARED / COMPLETED`) and `phases/phase-XX-<behavior>.md`.
   - Confirm all earlier phase dependencies listed in `Depends on` are `PASSED`.

2. **Sequential Micro-Task Execution Cycle (Repeat for each task in the phase from top to bottom)**:
   - **A. Read & Ground Task (i)**:
     * Read the next unticked task (`- [ ] **Task X.Y**`).
     * Verify all prior tasks in the phase are already ticked `- [x]`.
     * Note exact target files (`Scope / Files`), the components the design maps for this need (`Reused Components`), `Produces` signatures, and immediate acceptance criteria.
   - **B. Implement Task Scope**:
     * Write/modify only the files specified by Task (i).
     * Use the components and conventions recorded for the approved `architecture_profile` (design `Core usage` / `Client Core Mapping` table, screen contract). A mapped component that does not fit is a Planning blocker, not a local workaround.
   - **C. Immediate Local Verification**:
     * Run the task's specific acceptance check (e.g. the stack's analyzer on the changed file, a single unit test). Fix any analyzer errors immediately.
   - **D. Tick & Re-Ground**:
     * Return to `phases/phase-XX-<behavior>.md` to tick `- [ ]` → `- [x]` for Task (i).
     * **Mandatory Plan Re-Reading**: Open and re-read the phase document to inspect the next task (i+1) (scope, reuse mapping, public signatures, acceptance criteria) to reload fresh context before touching any code for task (i+1). NEVER start coding task (i+1) in bulk or without re-reading the plan.

3. **Phase-Level Integration & Handoff**:
   - Once all tasks in the phase are `- [x]`, run the full phase verification suite (the stack's analyzer and the phase's tests; exact commands in `{{slot:verification}}`).
   - For UI impact, invoke `{{slot:visual-verification}}` on the approved target/states.
   - Run `bug-hunt` at `quick` effort on the phase diff as a self-check; fix `CONFIRMED` findings with their missing tests and rerun the affected checks before handoff.
   - Report exact commands, revision, target and results to the coordinator for `as-built.md`; `NOT_RUN` and `BLOCKED` are not `PASS`.
   - If checks fail, fix within the approved scope. If the fix changes behavior, API, architecture, dependencies, or component contract, return to the relevant planning/design gate.
   - Coordinator marks the phase complete in `as-built.md` only when its AC, review and verification evidence pass.

## Simplicity pass

After behavior passes, inspect only the changed code. Invoke `code-simplification` only when it identifies concrete complexity worth removing. Do not perform drive-by refactors, change tests to accommodate a simplification, or remove validation/error paths. Re-run affected checks after any simplification.

## Handoff

Hand off feature/version path, phase ID, approved revisions, changed files and actual code revision. Phase 2.4 review consumes that revision; Phase 2.5 verification consumes the reviewed revision. Any fix creates a new revision and restarts affected review, tests and visual states. The approved phase remains stable; coordinator writes actual results to `as-built.md`.
