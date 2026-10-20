---
name: grill-me
description: Relentless Socratic interviewing skill for spec_writer (Gate 1) and planning (Gate 2). Forces the agent to draft requirements.md + codebase-notes.md immediately, queue every inference or ambiguity as Q-NN in codebase-notes.md, and use ask_question one question at a time across interactive rounds until 0 open questions remain before locking in requirements.md or design.md.
---

# Grill-Me — Socratic Interviewing & Decision-Log Protocol

When this skill is active, act as a rigorous Technical Business Analyst (`spec_writer` at Gate 1) or Frontend Tech Lead (`planning` at Gate 2). Never let the user approve a document containing unverified inferences, unresolved options, or silent assumptions.

---

## 1. The 4 Iron Laws of `grill-me`

### Law 1 — Draft First, Lock In Through Question Queue (`Q-NN` $\to$ `D-NN`)
1. **Immediate Turn-1 Draft (`DRAFT`)**: On the first turn after scanning the request, Huly task (when provided), supplied visuals, and existing codebase context, immediately create or update both files in `.superpowers/work-items/<slug>/vN/` (or `docs/features/<module>/<feature>/vN/`):
   - **`requirements.md`** (`Status: DRAFT`): Capture the explicitly confirmed scope, actors, business rules, and scenarios; mark any unresolved detail inline with `(Q-NN)`.
   - **`codebase-notes.md`**: Populate `## 0. Question Queue (Q-NN)` with every ambiguity, inference, API/UX gap, or edge case as an `OPEN` row, and record verified codebase/package facts in `## 3. Verified Baseline Facts & Cross-Agent Notes`.
2. **Never Present `DRAFT` as Gate 1 Approval**: A `DRAFT` file is a working checkpoint so nothing is lost across turns. Gate 1 approval happens only when `## 0. Question Queue (Q-NN)` has **zero `OPEN` rows**, all `(Q-NN)` markers in `requirements.md` are replaced by `(D-NN)`, and `Status` transitions to `PENDING_REVIEW`.

### Law 2 — Confirm Every Inference (`Confirm Every Inference`)
- **If a fact can be verified directly from the repository or supplied spec** (file paths, class names, `core-usage` package exports, existing route names): inspect it with `view_file` / `run_command` (`rg`) and record it in `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`). Do not bother the user with questions the codebase already answers.
- **If a behavior, business rule, UX state, API contract choice, or architectural trade-off is NOT explicitly stated by the user** (even if it looks "obvious" or can be guessed from similar screens): you **MUST NOT** silently write it as a settled rule. Log it as `Q-NN` (`OPEN`) in `codebase-notes.md` and ask the user via `ask_question`.

### Law 3 — Grill Until `0 Doubts` & Straight-Line Documents
- Interview across all applicable dimensions until **`0 doubts, 0 open questions, 0 assumptions, 0 options`**:
  1. **Scope & Data/API Source**: In-scope vs out-of-scope boundaries, `BE_API_READY` vs `MOCKOON_MOCKED`, endpoint/payload mismatches.
  2. **Happy Path & UX/Visual States**: Primary actor flow, 4 mandatory visual states (`Default/Content`, `Loading`, `Empty`, `Error`), Kit widget selection when multiple viable `core-usage` candidates exist.
  3. **Clarification of Inferences**: Every point inferred from existing flows or partial prompts.
  4. **Negative, Boundary & Edge Cases**: Validation errors, network timeouts, duplicate clicks, empty lists, unauthorized states.
  5. **Multi-Screen / State Lifecycle**: Navigation/back behavior, state retention across steps, cache/list refresh after mutations.
- **Straight-Line Final Documents**:
  - `requirements.md` and `design.md` must read in **one straight locked-in line**.
  - Never leave `Option A / Option B`, `Open Questions`, `Assumptions`, or `TBD` in `requirements.md`, `codebase-notes.md`, or `design.md`.
  - Options that were considered and rejected belong exclusively in the `Options Considered` column of `## 1. Decision Log (D-NN)` inside `codebase-notes.md`.

### Law 4 — One Question at a Time & Reply Classification
- **Strictly 1 Question per `ask_question` Call**: Every call to `ask_question` must contain **exactly 1 question** (`questions` array length = 1) corresponding to the highest-priority `OPEN` `Q-NN` in `codebase-notes.md`. Never bundle 3–5 questions into one turn.
- Put the recommended option first, prefixed with `(Recommended)`, followed by 1–2 concrete alternatives and brief trade-offs.
- **Classify every user reply before updating files**:

| User Reply Pattern | Required Agent Action |
|---|---|
| **1. Counter-question / asks for explanation** (e.g., *"Why option 1?"*, *"How does X work?"*) | **DO NOT close `Q-NN`**. Answer the user's question clearly with codebase/business evidence, then re-ask `Q-NN` via `ask_question` so the user can make an informed choice. |
| **2. Free-text custom answer / new constraint** | Analyze the custom answer against existing rules and codebase constraints. If clear and conflict-free, confirm and record `D-NN`. If it introduces a new trade-off or ambiguity, explain the impact and confirm via `ask_question` before closing `Q-NN`. |
| **3. Modifies a previously locked `D-NN`** | Re-open or update the affected `D-NN` in `codebase-notes.md`, check ripple effects on other `BR-NN` / `AC-NN` rows, and sync both `codebase-notes.md` and `requirements.md`. |
| **4. Selects a clear option** | Mark `Q-NN` as `CLOSED -> D-NN` in `## 0. Question Queue (Q-NN)`, append `D-NN` to `## 1. Decision Log (D-NN)`, update `requirements.md` (replacing `(Q-NN)` with `(D-NN)`), and ask the next `OPEN` `Q-NN`. |

---

## 2. Iterative Turn-by-Turn Loop

```text
Turn 1: Intake & Scan -> Write DRAFT requirements.md + codebase-notes.md (with Q-01..Q-NN OPEN)
        -> Call ask_question for Q-01 ONLY (1 question, Recommended first)
Turn 2..K: Receive user reply -> Classify reply (Explain & re-ask OR lock in D-NN)
        -> Update codebase-notes.md (Q-NN -> CLOSED -> D-NN) + update requirements.md
        -> Call ask_question for next OPEN Q-NN ONLY
Final Turn (0 OPEN Q-NN):
        -> Set requirements.md Status = PENDING_REVIEW
        -> Run validate_proposal_spec on codebase-notes.md and requirements.md
        -> Present Gate 1 (or Gate 2 for design.md) approval via ask_question
```

---

## 3. Role-Specific Application

- **`spec_writer` (Gate 1)**:
  - Owns `requirements.md` (human-facing, concise $\le \sim 120$ lines, business/UX language, every `BR-NN` cites `D-NN`, zero code/class/node names) and `codebase-notes.md` (agent-facing SSOT).
  - Never invents codebase facts; when a question requires deep architectural or implementation inspection, requests consultation with `planning` or `code_writer` via the Coordinator and records the verified finding in `codebase-notes.md`.
- **`planning` (Gate 2)**:
  - Reads `requirements.md` and `codebase-notes.md` (`D-NN`, Glossary, Verified Facts) first.
  - Never writes `design.md` with `Option A / Option B` or unconfirmed architectural trade-offs. If a Core gap, architectural choice, or widget trade-off arises, logs `Q-NN` in `codebase-notes.md`, asks the user one question at a time via `ask_question`, records `D-NN` (`Owner: planning`), and then writes `design.md` in one straight line citing `D-NN`.
  - **Retains `codebase-notes.md` permanently** in the version folder throughout the entire `vN/` lifecycle for `code_writer`, `code_reviewer`, `test_runner`, and `docs_writer`.
