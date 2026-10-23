---
name: gate-review
description: Reviews one gate document read-only before the user is asked to approve it - pass 1 runs the existing validators, pass 2 walks the mode checklist (spec for Gate 1, design for Gate 2, plan for Gate 3), and every finding gets a stable ID, a severity CRITICAL/HIGH/MEDIUM/LOW and a coverage report. Use as the last self-check of Spec Writer before Gate 1 and of Planning before Gate 2 and Gate 3. Findings that need a user choice become Q-NN in codebase-notes.md; a clean review is never approval.
---

# Gate Review

Answer one question: **would a builder reading this document, with only the approved inputs beside it, build the same thing the user expects?** Gate review checks the document's text, not running code (`{{slot:bug-hunt}}` and `{{slot:code-review}}` do that) and not whether a fresh reader would need to ask questions (`cold-reader-check` does that).

## 1. Modes and owners

| Mode | Before | Reviewed document | Inputs read beside it | Owning role (receives findings) |
|---|---|---|---|---|
| [spec](modes/spec.md) | Gate 1 | `requirements.md` (or `brief.md`), `codebase-notes.md` | `design-uiux/uiux.md` when it exists, source inventory | Spec Writer (Designer for `uiux.md` findings) |
| [design](modes/design.md) | Gate 2 | `design.md` | approved `requirements.md`, `codebase-notes.md`, `uiux.md` | Planning |
| [plan](modes/plan.md) | Gate 3 | `implementation-plan.md` and every linked `phases/*.md` | approved `requirements.md`, `design.md`, `codebase-notes.md` | Planning |

Load only the mode file for the gate at hand. Run gate review on the finished draft, before `cold-reader-check`, so the cold reader's time is not spent on what a validator or checklist catches.

## 2. Ground rules

- **Read-only.** The review never edits the reviewed documents. Reason: a reviewer who fixes while reviewing stops seeing the next defect and hides what changed. Prefer a fresh read-only subagent; if none is available, the owning role finishes the whole report before touching any file.
- **Cite, never guess.** Every finding names its location (`file` + section or ID) and the `G-NN` / `BR-NN` / `AC-NN` / `W-NN` / `D-NN` / `PHASE-NN` it concerns. A missing section is reported as missing, never reconstructed.
- **Deterministic.** Re-running on unchanged documents yields the same finding IDs and counts. A finding keeps its ID across rounds; resolved IDs are not reused.
- **A clean review is not approval.** Only the user approves a gate.

## 3. Pass 1 - lint (validators)

Run the validators for the mode and read every violation. Never re-check by hand what they already check.

| Mode | Validator | Already checked there - do not duplicate |
|---|---|---|
| spec | `validate_proposal_spec` on `requirements.md` and on `codebase-notes.md` (and `change-impact.md` when present) | metadata fields, required sections, placeholders, `Option A/B` / `Open Questions` / `TBD`, `OPEN` `Q-NN`, self-approval markers, AC IDs unique and sourced, goals and their BR/AC links (`REQ-005`), `W-NN` present in `## Workflows` (`REQ-006`), notes sections and `D-NN` links (`NOTES-000`...`NOTES-005`) |
| spec (UI) | `validate_ux_design` on the `vN` folder | `UX-001`...`UX-012`: workflows to goals to screens, step states, kit classes, new components, mock paths, content hash |
| design | `validate_proposal_spec` on `design.md` | `DESIGN-001`...`DESIGN-008`, including goal alignment (`DESIGN-007`) and the `S-NN` / `C-NN` mapping (`DESIGN-008`) |
| plan | `validate_plan_slices` on the saved `implementation-plan.md` | `PLAN-V-001`...`PLAN-V-010`: sections, gate references, phase files and metadata, AC to phase mapping, forward dependencies, goal coverage |

- Every validator `ERROR` is one `CRITICAL` finding (category `lint`, the rule ID in the summary). Stop pass 2 until the owner fixes them and the validator is re-run clean. Reason: checklist findings on a structurally broken document are noise.
- A validator that cannot run (tool unavailable, phase-free item, no `design-uiux/`) is recorded as `NOT_RUN` with the reason, never as `PASSED`. A phase-free item uses the work-item contract checklist instead of `validate_plan_slices`.
- `WARNING`s become `MEDIUM` findings. A reason recorded by the owner in `codebase-notes.md` closes the finding.

## 4. Pass 2 - mode checklist

Walk the mode file top to bottom. Each check produces findings and fills one part of the coverage report. When the workspace has a generated skill for the same content (`.agents/skills/requirements-specification/`, `.agents/skills/domain-knowledge/`), its items are added to the checklist; they never replace the mode's checks or the validators.

## 5. Severity

| Severity | Means | Examples |
|---|---|---|
| `CRITICAL` | The document cannot go to the gate | validator `ERROR`; an `AC-NN` or `G-NN` nothing delivers; text that contradicts a confirmed `D-NN`; two rules that cannot both hold |
| `HIGH` | Two competent builders would build different things | unmeasurable or vague AC/BR; missing exception or recovery scenario on a flow that changes data; producer/consumer mismatch between tasks; a decision point left open between two units |
| `MEDIUM` | A real gap that will cost a later round | terminology drift; a grill dimension only `Partial`; a risk without mitigation; plan out of proportion |
| `LOW` | Wording or redundancy that changes nothing | duplicated sentence, inconsistent capitalization |

Severity ranks the effect on the build, not the size of the fix.

## 6. Resolving findings

| Finding needs | Owner does | Reason |
|---|---|---|
| A user choice (scope, behavior, a value, a trade-off, any inference) | Adds a `Q-NN` (`OPEN`, owner = owning role) in `codebase-notes.md` and asks it through `grilling`, one question at a time | Every inference is confirmed; the gate needs 0 `OPEN` `Q-NN` |
| Only a meaning-preserving edit (wording, a missing link to an existing `D-NN`, a term aligned to the Glossary) | Fixes it and notes it in `codebase-notes.md` `## 6. Change Log` | No decision is created, so no question is needed |
| A change in another role's document (spec gap found at Gate 2 or 3) | Hands it to that role, who queues the `Q-NN` | Only `spec_writer` and `planning` write `codebase-notes.md`, each for its own questions |

Before the gate: 0 `CRITICAL`, 0 `HIGH` and 0 `MEDIUM` unresolved; `LOW` never blocks. Re-run pass 1 after fixes, and pass 2 for the sections that changed.

## 7. Report

Return the report in the handoff (it is not a new work-item file). Most severe first; at most 40 rows, the rest summarized by category.

| ID | Severity | Category | Location | Finding | Refs | Resolution |
|---|---|---|---|---|---|---|
| `GR-S-03` | `HIGH` | ambiguity | `requirements.md` §3 `BR-04` | "loads fast" has no threshold | `G-01`, `BR-04`, `AC-05` | `Q-09` |

- ID prefix per mode: `GR-S-NN` (spec), `GR-D-NN` (design), `GR-P-NN` (plan).
- Then the coverage report the mode file defines.
- End with `gate-review <mode>: lint <PASSED|FAILED|NOT_RUN>; <c> CRITICAL, <h> HIGH, <m> MEDIUM, <l> LOW; coverage <n>/<total>` and record that line in `codebase-notes.md` `## 6. Change Log`.

Sources and ideas not adopted: [references/sources.md](references/sources.md).
