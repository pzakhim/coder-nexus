---
name: work-item-contract
description: Backend specifics for the work-item contract - service/endpoint/table scope, backend templates (brief, requirements, codebase-notes) and the backend contract checklist. Complements the core work-item-contract skill (folders, Types, gates, goal lock, ownership, handoff).
---

# Backend work-item contract

The core `work-item-contract` skill defines folders and versions, the 8 Types, which file each gate approves, the goal-lock rule, ownership and the handoff payload. Orchestration lives in `dev-team` and the agent profiles. For a backend service item, use the backend templates in `templates/` (`brief.md.tpl`, `requirements.md.tpl`, `codebase-notes.md.tpl`) and the [backend contract checklist](references/work-item-contract.md) instead of the generic Client templates; `change-impact.md` (`v2+`) and the plan/phase templates come from core.

Work items reside at `.superpowers/work-items/<slug>/vN/`.
Types: `feature`, `bugfix`, `refactor`, `optimization`, `migration`, `maintenance`, `investigation`, `documentation`.

Every item contains:
- `requirements.md`: Unified human-facing specification (`## 0. Goals` with user-confirmed `G-NN`, Scope & Alignment, Actors & Permissions, `BR-NN` Business Rules citing `D-NN` and a goal, Behavioral BDD Scenarios, Acceptance criteria `AC-NN` with a goal, Gate 1 approval; `brief.md` remains supported for small phase-free items).
- `codebase-notes.md`: Permanent agent-facing Single Source of Truth retained throughout the entire `vN/` lifecycle (`## 0. Question Queue (Q-NN)`, `## 1. Decision Log (D-NN)`, `## 2. Glossary`, `## 3. Verified Baseline Facts & Cross-Agent Notes`, `## 4. Constraints & External Integrations`, `## 5. Extended Rule Details`, `## 6. Change Log`).
- `design.md`: Straight-line technical architecture specification citing `D-NN` in `codebase-notes.md`.
- `implement-plan.md`: Sequential task slices across Clean Architecture layers (`phases/phase-NN-*.md`).
