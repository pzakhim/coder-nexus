---
name: grilling
description: "Unified Socratic questioning and solution-options protocol (Q-NN -> D-NN) for spec_writer (Gate 1) and planning (Gate 2). Drafts first, queues every inference or multi-option trade-off as Q-NN in codebase-notes.md, builds 2-3 materially different options with (Recommended) first when real alternatives exist, asks one question at a time ('câu i/N') via ask_question, enforces zero-re-ask continuity from Gate 1 to Gate 2, and stops only at 0 OPEN Q-NN."
---

# Grilling & Solution Options — Questions to Decisions (`Q-NN` → `D-NN`)

Act as a rigorous Technical BA (`spec_writer`) or Solution Architect / Tech Lead (`planning`). Never let the user approve a document that holds an unconfirmed inference, an unresolved option, or a silent assumption. Files and templates follow [`work-item-contract`](../work-item-contract/SKILL.md); this skill owns how questions and 2–3 solution options are discovered, ordered, asked, and closed into `D-NN`.

## Modes & Reference Guides

| Guide / Mode | Role / When to Load |
|---|---|
| [01 — Solution Options & Divergent Pass](references/01-solution-options-and-divergent-pass.md) | Building 2–3 real, materially different options (`(Recommended)` first) when a `Q-NN` has multiple viable approaches, divergent lenses, and logging `Options Considered` in `D-NN` |
| [modes/spec.md](modes/spec.md) | `spec_writer` (Gate 1 in `dev-team`): business dimensions `A`–`E` + workflows `W-NN` / screens `S-NN` + behavior/scope options |
| [modes/planning.md](modes/planning.md) | `planning` (Gate 2 in `dev-team`): Core gaps, architecture trade-offs, parallel option exploration, and test data |
| [modes/batch-confirm.md](modes/batch-confirm.md) | Confirming several low-risk defaults in a single question (at most once per round) |
| [modes/questionnaire.md](modes/questionnaire.md) | Generating `questionnaire-<topic>.md` when a third party holds missing knowledge |

## 1. The 4 Laws

### Law 1 — Draft First, Lock In Through the Queue
- Read every source first (`huly-task-intake`, downloads, visuals, API contracts, codebase scan). Ask the job-type question (only when the ticket is not new) and the Goal Question ([`requirements-elicitation`](../requirements-elicitation/SKILL.md)) before anything else.
- In the turn the goals (`G-NN`) are confirmed, write both files in `.superpowers/work-items/<slug>/vN/`: `requirements.md` (`Status: DRAFT`, unresolved spots marked `(Q-NN)`) and `codebase-notes.md` (every gap queued as an `OPEN` row in `## 0. Question Queue (Q-NN)`, verified facts in `## 3. Verified Baseline Facts & Cross-Agent Notes`).

### Law 2 — Separate Facts, Inferences, and Multi-Way Options
- **Verified Fact** (path, class, export, route, existing behavior in code, or locked `D-NN`): look it up via `rg` and record in `## 3`. **Never ask the user a codebase fact.**
- **Single-Way Inference** (one sensible behavior/rule not explicitly stated by the user): queue as `Q-NN` and ask for confirmation (or batch low-risk defaults via [batch-confirm](modes/batch-confirm.md)).
- **Multi-Way Trade-Off** (2–3 materially different ways meet the confirmed `G-NN`): follow [01 — Solution Options & Divergent Pass](references/01-solution-options-and-divergent-pass.md) to present 2–3 real options with `(Recommended)` first and 1-line trade-offs.
- The only exception is a minor builder-level call allowed by [`gate-review`](../gate-review/SKILL.md) Pass 3 (Cold-Reader Check — never from its never-minor list), recorded visibly for the gate.

### Law 3 — Grill Until 0 Doubts; Straight-Line Documents
- Cover every dimension of the active mode until `0 OPEN` rows remain in `## 0. Question Queue` and the stop test (§5) passes.
- `requirements.md` and `design.md` must read as **one straight locked-in line**: zero `Option A / Option B`, `Open Questions`, `Assumptions`, or `TBD` (`REQ-003`, `NOTES-005`). Rejected options live **only** in the `Options Considered` column of `## 1. Decision Log (D-NN)`.

### Law 4 — One Question at a Time (`câu i/N`) with Visual Flow Explanation & Per-Question Lock
- Before calling `ask_question` for the active `OPEN` row `Q-i`, **always output a structured explanation in the chat message (`content`) dedicated solely to `Q-i`**:
  1. **Why `Q-i` exists**: the current baseline in sources/code vs. the gap, conflict, or trade-off.
  2. **Visual Flow (Mermaid / ASCII diagram)**: illustrate the flow and how the candidate options branch so the user can see the impact immediately.
  3. **Options & Trade-Off Analysis**: walk through `(Recommended)` and the alternatives.
- Then call `ask_question` with **exactly one question (`len(questions) == 1`)**: the top `OPEN` row (§2.2), prefixed with its progress (`Q-07 · câu 3/9 · Workflow`), `(Recommended)` option first, followed by 1–2 concrete alternatives with concise trade-offs, plus `"Need to discuss / clarify this question further before deciding"` (`"Cần phân tích / thảo luận làm rõ thêm câu này trước khi chốt"`). Only exception: one [batch-confirm](modes/batch-confirm.md) call for low-risk assumptions after all real open questions are locked.
- **Strictly Forbidden**: Calling `ask_question` with `content: None` (a bare popup without explanation/flow), or chaining `ask_question(Q-01)` → `ask_question(Q-02)` back-to-back in a tool loop without first discussing, locking `Q-01 -> CLOSED -> D-NN` in `codebase-notes.md`, updating the draft, and pruning downstream `Q-NN` rows.

## 2. Queue Order, Sufficiency & Cross-Department Continuity

### 2.1. Sufficiency Summary (Inside the Goal Question)
The Goal Question (`requirements-elicitation`) states in three lines: **Enough for** (what read sources settle, cited), **Missing** (every `UNREACHABLE` / `NOT_PROVIDED` source only the user can supply), and **Next** (queued `Q-NN` count by topic).

### 2.2. Dependency Order of the Queue
Ask in dependency order so earlier answers eliminate downstream questions:
1. Job type and goals (`G-NN`)
2. Scope in/out, actors, and permissions
3. Main workflow (`W-NN`), screens (`S-NN`), and branches (`spec_writer` via `figma-intake` when there is UI impact)
4. Data and API source (`BE_API_READY` / `MOCKOON_MOCKED`), fields, errors
5. Observable states and multi-step lifecycle
6. Negative, boundary, and edge cases
7. Technical trade-offs (`planning`, Gate 2)

Within a group, ask the row with the highest **impact × uncertainty** first. After each answer, prune or update dependent rows; never ask what a source or `D-NN` already settles. Keep `Grill-Me Rounds` in `codebase-notes.md` current (`REQ-001` rejects `0`).

### 2.3. One Queue Across Roles (Zero-Re-Ask Continuity)
All askers share `codebase-notes.md` (`## 0. Question Queue` and `## 1. Decision Log`):
- **At Gate 1 (`spec_writer`)**: `spec_writer` (`Owner: spec_writer`) resolves every business, screen (`S-NN`), workflow (`W-NN`), and state question until `0 OPEN` `Q-NN` remain and Gate 1 is `APPROVED`.
- **Handoff from Gate 1 (`spec_writer`) to Gate 2 (`planning`)**: `planning` reads the locked `## 1. Decision Log (D-NN)` from `codebase-notes.md` and **never re-asks any business rule, scope boundary, actor permission, workflow `W-NN`, screen `S-NN`, or UI state**. `planning` queues only technical Gate 2 rows (`Owner: planning`).
- If a question outside the active agent's ownership surfaces, add it to the queue under the owning role and route via the department coordinator so the user still experiences one question at a time.

## 3. Reply Classification (Before Editing Any File)

| User Reply | Required Action |
|---|---|
| **Counter-question** (*"why option 1?"*) | Do **not** close `Q-NN`. Answer with evidence from sources/code, then re-ask the same row. |
| **Weak reply** (*"whatever you think"*, *"ok"*, *"sounds good"*) | Not a valid confirmation (unless the question was explicitly framed as yes = accept recommendation). Re-ask as two concrete options. |
| **Buzzword answer** (*"scalable"*, *"standard"*, *"like other apps"*) | Probe for the concrete outcome or threshold by offering 2 measurable readings. |
| **Free text / new constraint** | Verify against rules and codebase. If clear and conflict-free → record `D-NN`. If it introduces a new trade-off → explain impact and confirm first. |
| **Changes a locked `D-NN`** | Reopen the `D-NN`, check ripple effects on `BR-NN` / `AC-NN` / `W-NN` / `design.md`, and sync both files. A goal or scope change reopens Gate 1. |
| **Clear pick** | Mark `Q-NN` → `CLOSED -> D-NN`; append `D-NN` (with all presented options in `Options Considered` and `(user choice)` or `(default accepted)` in `User Confirmed Decision`); replace `(Q-NN)` with `(D-NN)` in the draft; ask the next `OPEN` row. |

## 4. When to Stop & Present the Gate

Present the gate only when **both** hold:
1. `0 OPEN` rows remain in `## 0. Question Queue (Q-NN)` and every `(Q-NN)` marker in the draft is replaced by `(D-NN)`.
2. **Stop test**: you can accurately predict the user's answers to any remaining edge questions. Proceed to `Status: PENDING_REVIEW` → [`gate-review`](../gate-review/SKILL.md) (Pass 1 validators → Pass 2 checklist → Pass 3 cold-reader check) → user gate approval.
