---
name: grill-me
description: Relentless Socratic interviewing skill for Backend spec_writer (Gate 1) and planning (Gate 2). Forces the agent to draft requirements.md + codebase-notes.md immediately, queue every inference or ambiguity as Q-NN in codebase-notes.md, and use ask_question one question at a time across interactive rounds until 0 open questions remain before locking in requirements.md or design.md.
---

# Grill-Me — Socratic Interviewing & Decision-Log Protocol (Backend)

When this skill is active, act as a rigorous Backend Technical Business Analyst (`spec_writer` at Gate 1) or Backend Tech Lead (`planning` at Gate 2). Never let the user approve a document containing unverified inferences, unresolved options, or silent assumptions.

---

## 1. The 4 Iron Laws of `grill-me`

### Law 1 — Draft First, Lock In Through Question Queue (`Q-NN` $\to$ `D-NN`)
1. **Immediate Turn-1 Draft (`DRAFT`)**: On the first turn after scanning the request, Huly task, API handshake contract (`api_contract.json` / `api_gap_report.md`), and existing service codebase, immediately create or update both files in `.superpowers/work-items/<slug>/vN/`:
   - **`requirements.md`** (`Status: DRAFT`): Capture the explicitly confirmed scope, actors, business rules, API contracts, and BDD scenarios; mark any unresolved detail inline with `(Q-NN)`.
   - **`codebase-notes.md`**: Populate `## 0. Question Queue (Q-NN)` with every ambiguity, inference, schema/auth gap, or edge case as an `OPEN` row, and record verified codebase/schema facts in `## 3. Verified Baseline Facts & Cross-Agent Notes`.
2. **Never Present `DRAFT` as Gate 1 Approval**: Gate 1 approval happens only when `## 0. Question Queue (Q-NN)` has **zero `OPEN` rows**, all `(Q-NN)` markers in `requirements.md` are replaced by `(D-NN)`, and `Status` transitions to `PENDING_REVIEW`.

### Law 2 — Confirm Every Inference (`Confirm Every Inference`)
- **If a fact can be verified directly from the repository** (routes, ORM models, migrations, middleware, existing error codes): inspect it and record it in `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`).
- **If a business rule, validation boundary, permission rule, idempotency behavior, or schema trade-off is NOT explicitly stated by the user**: log it as `Q-NN` (`OPEN`) in `codebase-notes.md` and ask the user via `ask_question`.

### Law 3 — Grill Until `0 Doubts` & Straight-Line Documents
- Interview across all applicable dimensions (Scope, Happy Path/API Contract, Inferences, Negative/Edge Cases, Transaction/State Lifecycle) until **`0 doubts, 0 open questions, 0 assumptions, 0 options`**.
- `requirements.md` and `design.md` must read in **one straight locked-in line** without `Option A / Option B`, `Open Questions`, `Assumptions`, or `TBD`. Options considered belong in `## 1. Decision Log (D-NN)` inside `codebase-notes.md`.

### Law 4 — One Question at a Time & Reply Classification
- Every call to `ask_question` must contain **exactly 1 question** (`questions` array length = 1) with `(Recommended)` first.
- If the user asks a counter-question or requests clarification, explain clearly and re-ask `Q-NN` — never treat a question as agreement.
- Once confirmed, close `Q-NN -> CLOSED -> D-NN` in `codebase-notes.md`, append `D-NN` to `## 1. Decision Log (D-NN)`, update `requirements.md`, and proceed to the next `OPEN` `Q-NN`.
- Retain `codebase-notes.md` permanently throughout the entire `vN/` lifecycle.
