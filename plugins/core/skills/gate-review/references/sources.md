# Sources - gate-review

Ideas were rewritten in this repo's vocabulary (`G-NN`, `BR-NN`, `AC-NN`, `W-NN`, `Q-NN`, `D-NN`, `PHASE-NN`, gates). No text was copied. Stars as of the review date.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [github/spec-kit `templates/commands/analyze.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/analyze.md) | 142k | Strictly read-only cross-document analysis; detection passes (ambiguity with vague adjectives, duplication, underspecification, coverage gaps, terminology drift, conflicts); CRITICAL/HIGH/MEDIUM/LOW heuristic; stable finding IDs; deterministic re-runs; capped findings table with overflow summary; coverage metrics | SKILL.md §2, §5, §7; modes/spec.md S1-S3; modes/design.md D1 |
| [github/spec-kit `templates/commands/checklist.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/checklist.md) | 142k | Checklist items test the writing of requirements, not the product; banned item openings (Verify/Test/Confirm/Click); question shapes; `[Gap]` `[Ambiguity]` `[Conflict]` markers with references; scenario classes primary/alternate/exception/recovery; recovery asked when data changes; soft item cap and merging | modes/spec.md S5, S6 |
| [github/spec-kit `templates/checklist-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/checklist-template.md) | 142k | Item numbering and the rule that a checked item means the criterion is met by the text, not that the work is done | SKILL.md §7 (ID scheme); modes/spec.md S5 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-prd/assets/prd-validation-checklist.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-prd/assets/prd-validation-checklist.md) | 54k | "Done-ness": each requirement has a testable consequence and bounds instead of adjectives ("gracefully", "user-friendly"); boilerplate quality claims flagged; severity ranks impact, not fix size; glossary drift and ID continuity as mechanical checks | SKILL.md §5; modes/spec.md S1, S2 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-architecture/references/reviewer-gate.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-architecture/references/reviewer-gate.md) | 54k | Cheap deterministic lint first so judgment goes to semantics; an independent reviewer context finds what the author talks past; architecture must fix every divergence point with an enforceable rule; nothing deferred may let two units diverge; it ratifies rather than contradicts existing code; tiered output | SKILL.md §2, §3, §7; modes/design.md D2, D4, D5 |
| [obra/superpowers `skills/subagent-driven-development/references/preflight.md`](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/references/preflight.md) | 303k | Pre-flight scan output is a table: one row per task pair sharing a file or interface (produces vs consumes) and one row per task for self-consistency; "clean" without rows is not a scan; plan items that the review rubric would reject; the spec binds, the plan argues | modes/plan.md P1, P3, preamble |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| Project constitution as the non-negotiable authority | spec-kit analyze | No constitution file here. The confirmed `D-NN` and the work-item contract play that role: text contradicting a `D-NN` is `CRITICAL`. |
| Extension hooks before and after analysis | spec-kit analyze, checklist | No hook system in this plugin; adds nothing to the review. |
| Writing checklists as files under `checklists/` with `CHK` IDs and checkbox lifecycle | spec-kit checklist, template | Would add an artifact outside the work-item contract. Findings live as `Q-NN` in `codebase-notes.md` and the summary line in its Change Log. |
| Up to five clarifying questions before generating the checklist | spec-kit checklist | Conflicts with one question at a time through the `Q-NN` queue; the mode is fixed by the gate, so there is nothing to ask. |
| `[Assumption]` marker and "Dependencies & Assumptions" category | spec-kit checklist | Conflicts with "confirm every inference" and the no-Assumptions rule. An inference becomes a `Q-NN`. |
| 80% traceability threshold | spec-kit checklist | Replaced by a stricter rule: every item carries a tag and an ID or the section where text is missing. |
| Offering remediation edits for the top N issues | spec-kit analyze | Replaced by the resolution table: meaning-preserving fixes by the owner, everything else through `Q-NN`. |
| Persona, innovation and vision "theater", strategic thesis, counter-metrics, shape fit | BMAD PRD rubric | `requirements.md` is a short work-item spec, not a PRD; goals and their success signals are owned by `goal-framing`. |
| `[ASSUMPTION]` index, `[NOTE FOR PM]` callouts, open-items density | BMAD PRD rubric | Conflicts with 0 `OPEN` `Q-NN` before a gate and no assumptions. |
| Parallel multi-lens reviewer subagents writing to a `reviews/` folder and an HTML report | BMAD reviewer gate | `vN/reviews/` belongs to the Code Reviewer; one fresh read-only reviewer is enough for a document gate. |
| Reviewer applies the clear fixes itself | BMAD reviewer gate | The reviewer stays read-only; the owning role fixes only meaning-preserving issues after the report. |
| Ledger for pre-flight rulings | superpowers preflight | No ledger artifact here; rulings become `Q-NN` / `D-NN` in `codebase-notes.md`. |
