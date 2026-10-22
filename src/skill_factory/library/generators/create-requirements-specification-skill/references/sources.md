# Sources

External material read when shaping this generator. Ideas are rewritten in this repository's vocabulary (`G-NN`, `BR-NN`, `AC-NN`, `Q-NN`, `D-NN`, gates); nothing is copied.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [github/spec-kit `templates/spec-template.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/spec-template.md) | 142k | Success criteria must be measurable and technology-neutral; Given/When/Then acceptance scenarios; edge cases as an explicit section | RS4 (success signals), `04` "Goals and success signals" |
| [github/spec-kit `templates/commands/checklist.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/checklist.md) | 142k | A review checklist tests the requirement text, not the implementation; items phrased as questions with `[Gap]` / `[Ambiguity]` / `[Conflict]` markers and a reference to the section checked; vague terms must be quantified | RS6, `05-gate-review-questions`, RS4 vague-word list |
| [Fission-AI/OpenSpec `schemas/spec-driven/templates/spec.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/schemas/spec-driven/templates/spec.md) | 73k | A change is written as a delta grouped by ADDED requirements, with scenarios | RS10 |
| [Fission-AI/OpenSpec `docs/writing-specs.md`](https://github.com/Fission-AI/OpenSpec/blob/c04f30e57817422c1a107ea00a682c1d29a423ca/docs/writing-specs.md) | 73k | ADDED / MODIFIED / REMOVED chosen against the current behavior; MODIFIED gives the full new version; REMOVED says why; one observable behavior per requirement; "handle gracefully" is not testable | RS10, RS4, `04` "Change jobs: delta" |
| [bmad-code-org/BMAD-METHOD `skills/bmad-prd/SKILL.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-prd/SKILL.md) | 54k | Capabilities, not implementation; reviewer findings are tiered by severity before the document is final | RS4 (no implementation words), RS6 (severity on findings) |
| [bmad-code-org/BMAD-METHOD `skills/bmad-prd/assets/prd-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-prd/assets/prd-template.md) | 54k | Glossary terms used verbatim everywhere; a synonym is a discipline violation; each requirement carries testable consequences | RS5, `04` "Terms" |
| [mattpocock/skills `skills/engineering/to-spec/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/to-spec/SKILL.md) | 300k | Use the project's glossary vocabulary throughout the spec; problem and solution stated from the user's view | RS5 |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| `Assumptions` section and `[ASSUMPTION]` tags filled with reasonable defaults | spec-kit spec template, BMAD PRD | Conflicts with the `grilling` law "confirm every inference": anything unknown becomes a `Q-NN` and is asked. |
| `[NEEDS CLARIFICATION]` markers left inside requirements; an "Open Questions" section | spec-kit, BMAD PRD | `requirements.md` must hold no open marker (`validate_proposal_spec` REQ-002/REQ-003); open items live as `Q-NN` in `codebase-notes.md`. |
| `[Assumption]` checklist marker | spec-kit checklist | Same reason as the Assumptions section; only `[Gap]`, `[Ambiguity]`, `[Conflict]` are kept. |
| Fast path that drafts the whole document with inferred values for later review | BMAD PRD | The draft-first law already exists, but inferences must be confirmed one at a time before Gate 1. |
| A separate checklist file per domain (`checklists/ux.md`, …) owned by the reviewer | spec-kit checklist | One review path: `gate-review` spec mode; the workspace adds questions, not a second artifact. |
| Delta merged into a living main spec on archive; capability retirement | OpenSpec | Coder Nexus keeps each version in its own `vN/` folder; the full current set is in `requirements.md` of `vN` and the delta in `change-impact.md`. |
| Delta words ADDED / MODIFIED / REMOVED written in the AC delta column | OpenSpec | That column is checked by `validate_proposal_spec` (IMPACT-002: Keep / Add / Change / Remove); the words are used in "Behavior delta" and AC rows trace to them. |
| User stories, priorities P1–P3, success metrics with counter-metrics | spec-kit, BMAD PRD, to-spec | The fixed `requirements.md` template has goals, BR, scenarios and AC; adding sections would change the validated template. |
| Implementation and testing decisions inside the spec | to-spec | Belong to Planning (`design.md`, `implementation-plan.md`) and `quality-planning`. |
| Publishing the spec to the tracker without an interview | to-spec | The tracker is read-only for the Spec Writer and Gate 1 needs the user's approval. |
