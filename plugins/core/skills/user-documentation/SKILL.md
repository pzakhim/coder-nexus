---
name: user-documentation
description: "Author the final visual as-built summary (vN/as-built.md) once after ACCEPTED QA, maintain .superpowers/ux/screen-catalog.md and user-confirmed ADRs, and write or verify reader-facing documentation from implemented source."
---

# As-Built Record and Reader Documentation

This skill governs the two documentation responsibilities owned by `docs_writer`: recording the single final visual as-built summary (`vN/as-built.md`) at work-item closure, and authoring or updating reader-facing documentation verified against implemented source.

---

## 1. Two Modes of Operation

| Dimension | Mode 1 — Final As-Built Record (`vN/as-built.md`) | Mode 2 — Reader-Facing Documentation |
|---|---|---|
| **When triggered** | Once after `Test Runner` returns `ACCEPTED` in `final_qa` (or at closure of a pure `documentation` work item). Never between intermediate code phases. | When a work item's approved scope requires creating or updating user guides, runbooks, `README.md`, or API docs from implemented source. |
| **Primary inputs** | Approved `requirements.md`, `design.md`, `implementation-plan.md`, `codebase-notes.md`, phase review reports (`reviews/review_PHASE-NN_<rev>.md`), and `final_qa` report (`evidence/final_qa/<rev>/`). | Approved `requirements.md` / `brief.md`, `design.md`, and the actual implemented source, configuration, and tests on the current revision. |
| **Owned outputs** | `.superpowers/work-items/<slug>/vN/as-built.md`, plus `.superpowers/ux/screen-catalog.md` (when UI screens shipped) and user-confirmed ADRs in `docs/adr/`. | Bounded reader-facing Markdown paths (`docs/`, `README.md`, runbooks) named in the work item's **Scope in**. |
| **Return status** | `RECORDED` or `BLOCKED` | `READY_FOR_REVIEW` or `BLOCKED` |

---

## 2. Mode 1 — Final As-Built Record (`vN/as-built.md`)

Write `.superpowers/work-items/<slug>/vN/as-built.md` **once** using the canonical template in `work-item-contract` (`templates/as-built.md.tpl` and `references/handoff-and-status.md` §8) — never after individual code phases:

1. **Executive Summary (What Shipped)**:
   - State the fulfilled business/user goals (`G-NN` from `requirements.md`) in 1–2 concise sentences.
   - Summarize the user-facing or system outcome, changed entry points/screens/endpoints/commands, and the verified target environment.
2. **Visual Flow & Architecture Overview**:
   - Include a single concise Mermaid diagram (`flowchart LR` or `sequenceDiagram`) depicting the actual built user/system flow across entry points/screens, state/domain controllers, and data/storage boundaries so any reader grasps the delivered work at a glance.
3. **Delivered Code & Component Map**:
   - Tabulate each delivered layer/area (`Presentation`, `Domain / State`, `Data / Integration`, `Tests`), the exact file path, and its responsibility alongside reused foundation or UI kit components mapped in `design.md`.
   - Mark `UI: N/A` when the work item has no visual user interface.
4. **Phase, Review & QA Evidence Ledger**:
   - Record one row per completed stage (`Gate 1`, `Gate 2 & 3`, each `PHASE-NN`, and `final_qa`):

| Stage / Phase | Scope & `AC-NN` Covered | Approved Revision | Report / Evidence Path | Verdict |
|---|---|---|---|---|
| Gate 1 (Spec & Screens/Workflows) | `G-NN`, `AC-NN`, `S-NN`, `W-NN` | `<SPEC_REVISION>` | `requirements.md`, `codebase-notes.md` | `APPROVED` |
| Gate 2 & 3 (Design & Plan) | Architecture & Phase plan | `<PLAN_REVISION>` | `design.md`, `implementation-plan.md` | `APPROVED_FOR_BUILD` |
| `PHASE-01` | `<phase summary / AC-NN>` | `<REVIEW_REVISION>` | `reviews/review_PHASE-01_<REVIEW_REVISION>.md` | `APPROVED` |
| `final_qa` | All `Scope in` `AC-NN` | `<FINAL_REVISION>` | `evidence/final_qa/<FINAL_REVISION>/` | `ACCEPTED` |

   - Copy every revision, path, and verdict directly from real approved reports per `evidence-standard`. Never invent rows, cite a chat status message as evidence, or round `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` into `PASS`.
5. **Deviations, Plan Changes & Known Limitations**:
   - List approved plan changes (`PCR-NN` with 1-line summary and path `plan-changes/PCR-NN.md`, or `None`), runtime/fixture limitations recorded in `final_qa`, and updated reader docs or catalog paths.

### Screen Catalog & ADR Updates

- **Screen Catalog (`.superpowers/ux/screen-catalog.md`)**: When a verified UI work item delivers new or modified screens, update each delivered screen entry (`NEW` -> `EXISTING`), record the Figma node/source reference, and link the current verified screenshot path.
- **Architecture Decision Records (`docs/adr/`)**: When delivered work carries a user-confirmed, hard-to-reverse `D-NN` in `codebase-notes.md` worth a permanent record, follow `architecture-decision-records`. Never write an ADR without explicit user confirmation.

---

## 3. Mode 2 — Reader-Facing Documentation

1. **Write from implemented source, never from speculation**:
   - Read the approved `requirements.md` (or `brief.md`), `design.md`, and the actual implemented source and tests. Write only inside the assigned documentation paths (`docs/`, `README.md`, runbooks).
   - Describe real user/system behavior, inputs/outputs, states, error handling, routing, component usage, and setup following the workspace stack conventions (`{{slot:architecture-design}}`, `{{slot:clean-architecture}}`). Never present unbuilt or planned work as shipped.
2. **Verify every claim, command, and link (`evidence-standard`)**:
   - Check every CLI command, configuration key, code snippet, file path, Mermaid diagram, and relative link against the current codebase revision.
   - If the implemented source and the approved specification/contract contradict each other, stop and return `BLOCKED` naming the exact discrepancy.
3. **Hand off for review (`READY_FOR_REVIEW`)**:
   - Return `READY_FOR_REVIEW` with the changed documentation files and the exact source/test paths backing each material claim so `Code Reviewer` can verify them before closure.
   - If `Code Reviewer` returns `CHANGES_REQUESTED`, apply `review-resolution` on a new revision.

---

## 4. Guardrails

- **Strictly read-only toward runtime and specification artifacts**: Never edit runtime application source code, test files, fixtures, baselines, or approved work-item specs/plans (`requirements.md`, `design.md`, `implementation-plan.md`, `phases/`, `codebase-notes.md`).
- **Self-contained skill references**: Reference companion skills by name (`work-item-contract`, `evidence-standard`, `architecture-decision-records`, `review-resolution`) and slot placeholders (`{{slot:architecture-design}}`, `{{slot:clean-architecture}}`) without fragile cross-skill relative directory links.
- **Honest status reporting**: Return `BLOCKED` whenever a required review report, `final_qa` acceptance report, or revision reference is missing or inconsistent.
