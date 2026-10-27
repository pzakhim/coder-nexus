---
name: gate-review
description: "Unified 3-pass read-only verification before presenting Gate 1 (spec), Gate 2 (design), or Gate 3 (plan) to the user: Pass 1 runs deterministic validators (PASS / FAIL / NOT_RUN), Pass 2 walks the mode checklist with unified BLOCKER / MAJOR / MINOR severities, and Pass 3 runs the fresh cold-reader subagent check (sorting questions into Answered already, Minor — Agent's call, or User's call — OPEN Q-NN). Use as the final self-check of Spec Writer before Gate 1 and of Planning before Gates 2 and 3."
---

# Gate Review & Cold-Reader Check (3-Pass Pre-Gate Verification)

Answer one question before asking the user to approve a gate: **would the next agent, reading only the gate documents and approved inputs (with zero chat history), build the exact same thing the user expects?**

## 1. Modes & Owners

| Mode | Gate | Reviewed Document(s) | Approved Inputs Read Beside It | Owning Role | Cold Reader Plays |
|---|---|---|---|---|---|
| [modes/spec.md](modes/spec.md) | Gate 1 | `requirements.md` (or `brief.md`), `codebase-notes.md` | `Source Inventory`, extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` when present) | `spec_writer` | `planning` |
| [modes/design.md](modes/design.md) | Gate 2 | `design.md` | Approved `requirements.md`, `codebase-notes.md`, extracted Figma outputs (when present) | `planning` | `code_writer` |
| [modes/plan.md](modes/plan.md) | Gate 3 | `implementation-plan.md` and all linked `phases/*.md` | Approved `requirements.md`, `design.md`, `codebase-notes.md` | `planning` | `code_writer` |

Load only the mode file for the current gate. Run the 3 passes in strict order: **Pass 1 (Validators) → Pass 2 (Mode Checklist) → Pass 3 (Cold-Reader Check)**.

## 2. Ground Rules

- **Strictly read-only during each pass**: Never edit the reviewed documents in the middle of a pass. Complete the pass report first, then apply fixes.
- **Cite, never guess**: Every finding names its exact location (`file` + section or ID) and the `G-NN` / `BR-NN` / `AC-NN` / `W-NN` / `D-NN` / `PHASE-NN` it concerns.
- **Deterministic IDs**: Findings use `GR-S-NN` (spec), `GR-D-NN` (design), or `GR-P-NN` (plan). Resolved IDs are never reused.
- **Clean review ≠ user approval**: Only the user approves a gate.

---

## 3. Pass 1 — Deterministic Lint (Validators: `PASS` / `FAIL` / `NOT_RUN`)

Run the deterministic validators for the active mode first. Never re-check manually what the validator already enforces:

| Mode | Validator Tool / CLI | Enforces |
|---|---|---|
| `spec` | `validate_proposal_spec` on `requirements.md`, `codebase-notes.md`, and `change-impact.md` (`v2+`) | Metadata, required sections, placeholders, zero `Option A/B` / `Open Questions` / `TBD`, `0 OPEN` `Q-NN`, self-approval markers, `REQ-001..006`, `NOTES-000..005`, `IMPACT-001..003` |
| `design` | `validate_proposal_spec` on `design.md` | `DESIGN-001`…`DESIGN-008`, including `## Goal alignment` (`DESIGN-007`) and `S-NN` / `C-NN` mapping (`DESIGN-008`) |
| `plan` | `validate_plan_slices` on `implementation-plan.md` | `PLAN-V-001`…`PLAN-V-010`: sections, gate references, phase files/metadata, AC-to-phase mapping, forward dependencies, goal coverage |

- Every validator `ERROR` (`FAIL`) is a `BLOCKER` finding (`category: lint`). **Stop Pass 2 and Pass 3 until Pass 1 returns `PASS`.**
- A validator that cannot run (e.g., phase-free `brief.md`) is recorded as `NOT_RUN` with the reason, never `PASS`.
- Validator `WARNING`s become `MAJOR` findings unless justified in `codebase-notes.md`.

---

## 4. Pass 2 — Mode Checklist (`BLOCKER` / `MAJOR` / `MINOR`)

Walk the mode file (`modes/{spec,design,plan}.md`) top to bottom. When the workspace has generated skills (`.agents/skills/requirements-specification/`, `.agents/skills/domain-knowledge/`), include their gate-review items alongside the mode checks.

### Unified Severity Scale (`shared_contracts/flags_and_statuses.md`)

| Severity | Means | Examples |
|---|---|---|
| `BLOCKER` | **Blocks the gate unconditionally.** Either the document is structurally invalid or two competent builders would build incompatible things. | Validator `FAIL`; an unserved `G-NN` or `AC-NN`; text contradicting a confirmed `D-NN`; unmeasurable/vague `BR-NN` or `AC-NN`; missing exception/recovery path on a data-mutating flow; `Produces`/`Consumes` mismatch between tasks; unfalsifiable task `Expected`. |
| `MAJOR` | **Blocks the gate unless resolved or explicitly justified in `codebase-notes.md`.** A real gap that would cause rework in a later phase. | Terminology drift against `## 2. Glossary`; a `grilling` dimension marked `Partial`; a risk without mitigation; gold-plating design element serving no input; plan >3× disproportion or transcribed function bodies. |
| `MINOR` | **Non-blocking polish.** Meaning-preserving wording or formatting cleanup fixed directly before presenting. | Near-duplicate sentence, capitalization/formatting inconsistency. |

### Resolving Pass 2 Findings

| Finding Requires | Owner Action |
|---|---|
| **A user decision** (scope, behavior, threshold, trade-off, unconfirmed inference) | Queue an `OPEN` `Q-NN` in `codebase-notes.md` and ask via [`grilling`](../grilling/SKILL.md) one question at a time. |
| **Meaning-preserving edit** (aligning a term to Glossary, linking an existing `D-NN`, removing a duplicate line) | Fix directly and log in `codebase-notes.md` → `## 6. Change Log`. |
| **Change in an upstream role's document** (e.g., spec gap discovered at Gate 2 or 3) | Route via coordinator to `spec_writer` to queue the `Q-NN`. |

**Gate Pass 2 Exit Criteria**: `0 BLOCKER` and `0 MAJOR` findings unresolved.

---

## 5. Pass 3 — Fresh Cold-Reader Subagent Check

Once Pass 1 is `PASS` and Pass 2 has `0 BLOCKER` / `0 MAJOR`:

1. **Spawn one fresh read-only subagent** using the exact prompt in the mode file (`modes/{spec,design,plan}.md`).
   - Pass **only** the gate document paths and already-approved upstream documents. Never pass chat history, working notes, or summaries.
   - The cold reader reports at most **10 ranked questions** where it would otherwise have to guess and a wrong guess would alter its work (or replies `nothing important left`).
   - *(If no subagent tool is available, read the documents from the top using the same prompt and state in the gate presentation that the cold read was self-executed.)*
2. **Sort every reported question into one of 3 piles**:

| Pile | Condition | Required Action |
|---|---|---|
| **1. Answered already** | The answer is already in a gate document, `D-NN`, or cited source | Clarify the wording at that location so the next reader cannot miss it; never alter behavior. |
| **2. Minor (`Agent's call`)** | The next role can settle it without changing user-visible behavior, scope, or approved contracts, and no `D-NN` covers it | Decide it and record in `codebase-notes.md` → `## 3. Verified Baseline Facts & Cross-Agent Notes` as `Agent's call (cold-reader-check, Gate N): <question> → <decision> — <reason>`. |
| **3. User's call (`OPEN Q-NN`)** | Only the user can decide, or the answer changes behavior, business rules, permissions, data scope, money, API contracts, observable states, AC, scope, or goals (**Never Minor**) | Queue a new `OPEN` `Q-NN` in `codebase-notes.md` and ask via [`grilling`](../grilling/SKILL.md) one at a time. The gate waits for `0 OPEN` `Q-NN`. |

---

## 6. Consolidated Report & Audit Line

Include the findings table (most severe first) and mode coverage summary in the handoff, and append the single audit line to `codebase-notes.md` → `## 6. Change Log`:

```text
gate-review <spec|design|plan>: lint <PASS|FAIL|NOT_RUN>; <b> BLOCKER, <m> MAJOR, <n> MINOR; coverage <k>/<total>; cold-reader: <a> answered, <c> agent-calls, <u_q> user-questions
```
