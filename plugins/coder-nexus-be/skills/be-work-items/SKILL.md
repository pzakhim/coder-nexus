---
name: be-work-items
description: Standard routing and lifecycle workflow for Backend work items with grill-me Socratic interviewing and permanent codebase-notes.md.
---

# Backend Work Items

Work items reside at `.superpowers/work-items/<slug>/vN/`.
Outcome types: `feature`, `bugfix`, `refactor`, `migration`, `maintenance`.

Every item contains:
- `requirements.md`: Unified human-facing specification (Scope & Alignment, Actors & Permissions, `BR-NN` Business Rules citing `D-NN`, Behavioral BDD Scenarios, Acceptance criteria `AC-NN`, Gate 1 approval; `brief.md` remains supported for small phase-free items).
- `codebase-notes.md`: Permanent agent-facing Single Source of Truth retained throughout the entire `vN/` lifecycle (`## 0. Question Queue (Q-NN)`, `## 1. Decision Log (D-NN)`, `## 2. Glossary`, `## 3. Verified Baseline Facts & Cross-Agent Notes`, `## 4. Constraints & External Integrations`, `## 5. Extended Rule Details`, `## 6. Change Log`).
- `design.md`: Straight-line technical architecture specification citing `D-NN` in `codebase-notes.md`.
- `implement-plan.md`: Sequential task slices across Clean Architecture layers (`phases/phase-NN-*.md`).
