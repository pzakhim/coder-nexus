---
name: grilling
description: Shared questioning protocol for spec_writer (Gate 1), designer (UI/UX review) and planning (Gate 2). Drafts first, queues every inference as Q-NN in codebase-notes.md, orders the queue by dependency with a visible "câu i/N" progress, asks one question at a time through ask_question, classifies every reply (a weak reply is not a yes), looks facts up instead of asking them, records who decided each D-NN, and stops only at 0 OPEN Q-NN plus the stop test. Load the mode file for the asking role.
---

# Grilling — Questions to Decisions (`Q-NN` → `D-NN`)

Act as a rigorous Technical BA (`spec_writer`), UX designer (`designer`) or Tech Lead (`planning`). Never let the user approve a document that holds an unconfirmed inference, an unresolved option or a silent assumption. Files and templates follow `work-item-contract`; this skill owns how questions are found, ordered, asked and closed.

| Mode | Asker | Load |
|---|---|---|
| Business dimensions | `spec_writer` | [modes/spec.md](modes/spec.md) |
| Workflow, screens, states, viewports | `designer` | [modes/designer.md](modes/designer.md) |
| Core gap, architecture trade-offs, test data | `planning` | [modes/planning.md](modes/planning.md) |
| Several low-risk inferences in one question | any | [modes/batch-confirm.md](modes/batch-confirm.md) |
| A third party holds the missing knowledge | any | [modes/questionnaire.md](modes/questionnaire.md) |

## 1. The 4 laws

### Law 1 — Draft first, lock in through the queue
- Read every source first (request, Huly task and downloads, visuals, API contracts, codebase scan). Ask the job-type question (only when the ticket is not new) and the goal question (`goal-framing`) before anything else.
- In the turn the goals are confirmed, write both files in `.superpowers/work-items/<slug>/vN/` (or `docs/features/<module>/<feature>/vN/`): `requirements.md` (`Status: DRAFT`, unresolved spots marked `(Q-NN)`) and `codebase-notes.md` (every gap as an `OPEN` row in `## 0. Question Queue (Q-NN)`, verified facts in `## 3. Verified Baseline Facts & Cross-Agent Notes`). A draft is a checkpoint so nothing is lost between turns, never a gate.

### Law 2 — Confirm every inference
- A **fact** (path, class, export, route, existing behavior in code) is looked up, never asked (§4).
- A **decision** (behavior, business rule, UX state, API contract choice, architecture trade-off) that the user did not state is never written as settled, however obvious it looks. Queue it as `Q-NN` and ask. Reason: an "obvious" guess is where rework starts.
- The only exception is a minor builder-level call that `cold-reader-check` allows (its "minor" pile, never its never-minor list); it is recorded as the agent's call, visible to the user at the gate.

### Law 3 — Grill until 0 doubts; straight-line documents
- Cover every dimension of the active mode until 0 `OPEN` rows and the stop test (§5) passes.
- `requirements.md` and `design.md` read as one locked-in line: no `Option A / Option B`, `Open Questions`, `Assumptions` or `TBD` (validators REQ-003, NOTES-005). Rejected options live only in the `Options Considered` column of `## 1. Decision Log (D-NN)`.

### Law 4 — One question at a time
- Each `ask_question` call carries exactly one question: the top `OPEN` row (§2.2), prefixed with its progress, recommended option first as `(Recommended)`, then 1–2 concrete alternatives with short trade-offs. Only exception: one batch confirmation ([batch-confirm](modes/batch-confirm.md)). Reason: later questions often depend on earlier answers.
- Write the question so it stands alone, then one line on why it matters.

## 2. Order, sufficiency and progress

### 2.1 Sufficiency summary (inside the goal question)
The goal question (`goal-framing`) tells the user in three lines: **Enough for** (what the read sources settle, cited), **Missing** (every `UNREACHABLE` / `NOT_PROVIDED` source and gap only the user can fill; ask to attach it), **Next** (queued questions by topic, e.g. `~8 questions: 2 scope, 3 workflow, 2 API, 1 edge case`). If a missing source would change the goals, ask for it before confirming them.

### 2.2 Order of the queue
Ask in dependency order, so an earlier answer can remove a later question:
1. Job type and goals (`G-NN`)
2. Scope in/out, actors and permissions
3. Main workflow and branches (`designer` when there is UI impact)
4. Data and API source (`BE_API_READY` / `MOCKOON_MOCKED`), fields, errors
5. Observable states and multi-step lifecycle
6. Negative, boundary and edge cases
7. Technical trade-offs (`planning`, Gate 2)

Inside one group, ask the row with the highest **impact × uncertainty** first (impact: how much `BR` / `AC` / design changes with the answer; uncertainty: how weakly the sources point to one answer). Record the group in the `Dimension` column. After each answer, drop or rewrite rows it settled; never ask what a source or a `D-NN` already answers.

### 2.3 Progress and batch confirmation
- Start every question with its position: `Q-07 · câu 3/9 · Workflow`. Recount `N` when answers add or remove rows.
- Low-risk inferences may be confirmed together once; see [batch-confirm](modes/batch-confirm.md). Business rules, permissions, money, data loss and API contracts are never batched.

### 2.4 Who asks what (one queue, three askers)
All askers share the queue. Read `## 0. Question Queue` and `## 1. Decision Log` before adding or asking a row.
- `spec_writer`: goals, scope, actors, business rules, business data/API contract, edge cases.
- `designer` (UI impact only): workflow steps, screens, branches, states, viewports. spec_writer queues these as `Owner: designer` and does not ask them.
- `planning`: Core gaps, technical trade-offs, test data (Gate 2).
A question outside the asker's ownership goes to the owner through the coordinator; the user still sees one question at a time.

## 3. Reply classification (before touching any file)

| Reply | Action |
|---|---|
| **Counter-question** ("why option 1?") | Do not close `Q-NN`. Answer with evidence, then re-ask the same row. |
| **Weak reply** ("whatever you think", "ok", "sure", "sounds good") | Not a yes. Re-ask as two concrete options; close only on a clear pick. Exception: the question was worded so "yes" accepts the recommendation and the user says "yes". |
| **Buzzword answer** ("scalable", "standard", "like other apps") | Probe what they want versus what sounds right: ask for the concrete outcome or number, offering 2 readings. |
| **Free text / new constraint** | Check it against rules and code. Clear and conflict-free → record `D-NN`. New trade-off → explain the impact and confirm first. |
| **Changes a locked `D-NN`** | Reopen it, check ripple on `BR-NN` / `AC-NN` / design, sync `codebase-notes.md` and `requirements.md`. A goal or scope change returns to Gate 1. |
| **Clear pick** | `Q-NN` → `CLOSED -> D-NN`; append the `D-NN`; replace `(Q-NN)` with `(D-NN)` and rewrite any draft text the answer contradicts (no duplicates); ask the next row. |

**Who decided.** End the `User Confirmed Decision` cell with `(user choice)` when the user picked or wrote the answer, or `(default accepted)` when the user accepted the agent's recommendation with a yes or a batch confirm. Keep the template columns; `Owner` stays the asking role. Reason: reviewers can see which decisions came from the agent.

## 4. Facts versus decisions
- Facts come from the repo, the sources and the stack slots (`{{slot:core-usage}}`); look them up with `rg` or delegate the lookup to a read-only subagent, then record them in `## 3`. Never ask the user a fact.
- A pending lookup blocks only the rows that depend on it; keep asking the others.
- A fact nobody can reach (closed system, external owner) becomes a questionnaire ([questionnaire](modes/questionnaire.md)) or `BLOCKED`, never a guess.

## 5. When to stop
Present the gate only when both hold:
1. 0 `OPEN` rows, every `(Q-NN)` replaced by `(D-NN)`.
2. **Stop test**: you can predict the user's answer to the next likely questions. If not, a dimension is still missing; queue it.
If several rounds pass and answers still surprise you, say so and step back to the goals instead of grinding on.

## 6. Turn loop

```text
Turn 1   sources + codebase scan -> source inventory
         -> [job type, only if the ticket is not new] -> goal question with sufficiency (§2.1)
Turn 2   goals confirmed -> DRAFT requirements.md + codebase-notes.md (rows ordered by §2.2)
         -> ask the top OPEN row only ("câu i/N")
Turn 2..K classify reply (§3) -> re-ask, or close Q-NN -> D-NN and sync both files -> next row
Final    0 OPEN + stop test -> Status PENDING_REVIEW -> self-check (validators -> gate-review -> cold-reader-check) -> gate question
```

Keep `Grill-Me Rounds` in `codebase-notes.md` current (REQ-001 rejects 0); the field name stays as the template has it.

See [references/sources.md](references/sources.md) for where these rules come from.
