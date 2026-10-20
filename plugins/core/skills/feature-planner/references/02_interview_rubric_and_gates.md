# 02 — Evidence-Based Socratic Interview (`grill-me`) and Three Approval Gates

Resolve foundation evidence via `{{slot:core-usage}}`. Planning records the profile at Gate 2. Kit-matching rules below apply to the company-foundation profile or a verified Client design system; the minimal profile uses the framework's standard components (see `{{slot:core-usage}}`). Preserve the approved profile in downstream work.

## Interview rule (`1A Source Intake` $\to$ `1B Gap Analysis & Turn-1 DRAFT` $\to$ `1C Grill 1-by-1 (Q-NN -> D-NN)` $\to$ `Lock In Specs`)

Follow the 4 Iron Laws of `grill-me`:
1. **1A — Source Intake**: Confirm the 3 sources with the user via `ask_question` if not already supplied: (1) PO/BA requirements (Huly task or external prompt/file), (2) UI screens, UX descriptions & Design System (typically design-tool exports converted to `.md` files), and (3) API integration source (binary check: does BE API exist (`BE_API_READY`) or does it require **Mockoon** (`MOCKOON_MOCKED`) so live cutover only swaps domain in `.env`).
2. **1B — Gap & Flow Analysis + Turn-1 Draft (`DRAFT`)**: Read the confirmed sources and existing Client flow. Detect API count/payload mismatches (e.g., user estimates 3 APIs while UX/business flow needs 4 APIs), overlapping rules, and codebase adjustments needed. Immediately draft `requirements.md` (`Status: DRAFT`, marking unresolved spots with `(Q-NN)`) and `codebase-notes.md` (queueing every ambiguity or inference as an `OPEN` `Q-NN` row in `## 0. Question Queue (Q-NN)` and recording verified repo facts in `## 3. Verified Baseline Facts & Cross-Agent Notes`).
3. **1C — Open Questions & Clarification Loop (1 Question per Turn)**: Ask **strictly one unresolved `Q-NN` at a time** via `ask_question`, with clear context, 2–3 viable choices, and a `(Recommended)` option first. If the user asks a counter-question or requests clarification, explain clearly and re-ask `Q-NN` — never record a counter-question as agreement. When a user question or codebase check falls outside `spec_writer` scope, consult `planning` (Tech Lead) or `code_writer` (Dev) via the coordinator — never fabricate an answer. As each `Q-NN` is confirmed, mark `Q-NN -> CLOSED -> D-NN` in `codebase-notes.md`, append `D-NN` to `## 1. Decision Log (D-NN)`, and replace `(Q-NN)` with `(D-NN)` in `requirements.md` until `0 OPEN Q-NN` remain. Unknown external contracts remain `BLOCKED`.

| Group | Clarify |
|---|---|
| Data / API | Source (`BE_API_READY` vs `MOCKOON_MOCKED`), API count/field gaps vs UX flow, payload, nullability and errors; N/A with reason if no network. |
| Business / State | Actor, permission, trigger, transitions, overlapping rules, duplicate actions and unhappy paths. |
| UI / Variant | Design-export `.md` design system source, visual tokens, catalog candidates and verified APIs. |
| UX / Quality | Loading, empty, error, disabled, input retention, accessibility and Visual AC. |
| Integration | Owner module, current business flow adjustments, DI, router, affected consumers and regression risks (consult Planning/Dev when needed). |

For a multi-screen flow, resolve applicable state ownership, navigation/back, unhappy paths, inter-field dependencies and validation timing, step-up security, and post-flow effects. Mark an irrelevant axis N/A with a reason.

## Visual Intake Gate

For UI work, inspect a supplied design frame or image directly and derive layout, spacing, typography, tokens and required states. Lean mode controls inspection depth but does not skip a supplied visual. When none exists, record `VISUAL_INPUT_MISSING`, draft a minimal layout specification and ask for confirmation. Passing analyzer/tests while materially diverging from the approved design is `FAILED`. Read the selected profile’s UI guidance via `{{slot:core-usage}}` and call `get_ux_error_patterns`. Select one viable Kit match automatically even when its styling differs from the visual; Kit styling governs Visual AC. Multiple viable Kit matches require a user choice. With none, inspect shared widgets and composition before planning a private widget. Only a company-foundation setup failure blocks on company packages; other profiles require no company setup or GUIDE.

## Three gates

```text
Real intake + Client context + prior version/as-built for v2+
  → Gate 1 (spec_writer): requirements.md + codebase-notes.md (+ change-impact.md for v2+) → user approval
  → Gate 2 (planning): straight-line design.md + updated codebase-notes.md (D-NN) → user approval (retain codebase-notes.md permanently)
  → Gate 3 (planning): implementation-plan.md + all linked phases/*.md → user approval
  → code/review/test → as-built.md with actual evidence
```

The canonical location is `docs/features/<module>/<feature>/vN/` (or `.superpowers/work-items/<slug>/vN/`) in Client Git. One approved change batch uses one version and may cover several Huly tickets. The feature README indexes versions; dates belong in metadata, not version directory names. New vN never rewrites a completed older version.

At Gate 1, Spec Writer validates structural completeness (`validate_proposal_spec` on `codebase-notes.md` and `requirements.md`), presents the exact document revision (`requirements.md` with `codebase-notes.md`) and asks through `ask_question`. At Gate 2 and Gate 3, Planning Agent (Tech Lead) validates and presents the decisive straight-line technical architecture (`design.md` citing `D-NN` in `codebase-notes.md`) and the sequential implementation plan (`implementation-plan.md` and all linked phase revisions, including `PHASE-00` for context/Mockoon preparation). Initial approval status is `PENDING_REVIEW`; `valid: true` is not user approval. Never write `APPROVED_BY_SPEC` or invent a signature. Missing evidence remains `BLOCKED`.

Gate 1 covers scope in/out, actors/permissions, `BR-NN` business rules citing `D-NN`, BDD scenarios, 4 visual states, `AC-NN` table, and, for v2+, delta against both prior approved docs and actual code/as-built. Gate 2 covers straight-line architectural decision citing `D-NN`, folder/module ownership, layers actually needed, state/data/routing, Mockoon data design (when `MOCKOON_MOCKED`), UI Kit mapping and verification.

Gate 3 maps each AC to an executable behavior phase with owner, dependencies, files, code direction, source of UI Kit/framework APIs, targets, commands, and done criteria. When presenting at Gate 3, Planning handles three distinct user feedback paths:
1. **Approve & Freeze**: User approves plan and phases -> marks `APPROVED_FOR_BUILD`, freezes specs and plan, and hands off to Code Writer.
2. **Technical Refinement**: User requests technical adjustments (mock approach, scaffold vs existing base, phase order) -> Planning adjusts the plan directly without changing specs.
3. **Requirements / Scope Change**: User requests changes to business rules, UX behavior, or scope -> Planning halts and routes back to Spec Writer to update `requirements.md` and `codebase-notes.md` (Gate 1) before replanning.

The approved plan remains stable; the coordinator records execution in `as-built.md`.

Legacy `.agents/brainstorm` and `.agents/plan` files may be read for migration; they do not grant approval to a new version.
