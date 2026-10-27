# As-Built Record: <Feature / Work Item Name>

> **Work Item**: `<slug>` | **Version**: `vN` | **Type**: `<feature|bugfix|refactor|optimization|migration|maintenance|documentation>`
> **Ticket**: `<ISSUE-ID or N/A>` | **Branch**: `<branch-name>` | **Final Accepted Revision**: `<FINAL_REVISION>`
> **Status**: `RECORDED` (written once after Test Runner `ACCEPTED` or for a completed `documentation` item)

---

## 1. Executive Summary (What Shipped)

- **Goals Delivered (`G-NN`)**: <Concise 1-2 sentence summary of the business/user outcome delivered and which `G-NN` goals from `requirements.md` are fulfilled>
- **User-Facing / System Outcome**: <What the end user or caller can now do, which screens/endpoints/commands changed, and the verified target environment>

---

## 2. Visual Flow & Architecture Overview

> A single concise Mermaid diagram (`flowchart LR` or `sequenceDiagram`) showing the actual as-built user/system flow across screens, state/domain controllers, and data/API boundaries so any reader grasps the built feature at a glance.

```mermaid
flowchart LR
    User(["Actor / Trigger"]) --> UI["Presentation / Entry Point"]
    UI --> State["State / Use Case"]
    State --> Repo["Repository / Service"]
    Repo --> API[("API / Local Storage")]
```

---

## 3. Delivered Code & Component Map

| Layer / Area | File Path | Role & Reused Foundation / Kit Components |
|---|---|---|
| Presentation | `<path/to/screen_or_handler>` | <Responsibility; reused Kit widgets / foundation classes> |
| Domain / State | `<path/to/controller_or_usecase>` | <State transitions / business rules (`BR-NN`) enforced> |
| Data / Integration | `<path/to/repository_or_datasource>` | <Endpoint / storage contract, error mapping> |
| Tests | `<path/to/test_files>` | <Unit / widget / integration test coverage> |

---

## 4. Phase, Review & QA Evidence Ledger

| Stage / Phase | Scope & `AC-NN` Covered | Approved Revision | Report / Evidence Path | Verdict |
|---|---|---|---|---|
| Gate 1 (Spec & Screens/Workflows) | `G-NN`, `AC-NN`, `S-NN`, `W-NN` | `<SPEC_REVISION>` | `requirements.md`, `codebase-notes.md` | `APPROVED` |
| Gate 2 & 3 (Design & Plan) | Architecture & Phase plan | `<PLAN_REVISION>` | `design.md`, `implementation-plan.md` | `APPROVED_FOR_BUILD` |
| `PHASE-01` | `<phase summary / AC-NN>` | `<REVIEW_REVISION>` | `reviews/review_PHASE-01_<REVIEW_REVISION>.md` | `APPROVED` |
| `final_qa` | All `Scope in` `AC-NN` | `<FINAL_REVISION>` | `evidence/final_qa/<FINAL_REVISION>/` | `ACCEPTED` |

---

## 5. Deviations, Plan Changes & Known Limitations

- **Approved Plan Changes (`PCR-NN`)**: `None` (or list each `PCR-NN` with 1-line summary and link to `plan-changes/PCR-NN.md`)
- **Runtime / Fixture Limitations**: `None` (or list stubbed providers, mocked endpoints, or environment limits recorded in `final_qa`)
- **Reader Docs / Catalog Updated**: <List updated `docs/`, `README.md`, or `.superpowers/ux/screen-catalog.md` entries, or `None required`>
