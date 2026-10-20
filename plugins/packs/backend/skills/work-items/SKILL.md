---
name: work-items
description: Backend specifics for work items — service/endpoint/table scope, backend templates (brief, requirements, codebase-notes) and the backend work-item contract. Complements the core work-items lifecycle.
---

# Backend Work Items

The core `work-items` skill defines the lifecycle, gates and agent handoffs. For a backend service item, use the backend templates in `templates/` (`brief.md.tpl`, `requirements.md.tpl`, `codebase-notes.md.tpl`) and the [backend work-item contract](references/work-item-contract.md) instead of the generic Client templates.

Work items reside at `.superpowers/work-items/<slug>/vN/`.
Outcome types: `feature`, `bugfix`, `refactor`, `migration`, `maintenance`.

Every item contains:
- `requirements.md`: Unified human-facing specification (Scope & Alignment, Actors & Permissions, `BR-NN` Business Rules citing `D-NN`, Behavioral BDD Scenarios, Acceptance criteria `AC-NN`, Gate 1 approval; `brief.md` remains supported for small phase-free items).
- `codebase-notes.md`: Permanent agent-facing Single Source of Truth retained throughout the entire `vN/` lifecycle (`## 0. Question Queue (Q-NN)`, `## 1. Decision Log (D-NN)`, `## 2. Glossary`, `## 3. Verified Baseline Facts & Cross-Agent Notes`, `## 4. Constraints & External Integrations`, `## 5. Extended Rule Details`, `## 6. Change Log`).
- `design.md`: Straight-line technical architecture specification citing `D-NN` in `codebase-notes.md`.
- `implement-plan.md`: Sequential task slices across Clean Architecture layers (`phases/phase-NN-*.md`).
