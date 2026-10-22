# Sources

External material read when shaping this generator. Ideas are rewritten in this repository's vocabulary (`Q-NN`, `D-NN`, labels `VERIFIED` / `CONFIRMED` / `OPEN`); nothing is copied.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [mattpocock/skills `skills/engineering/domain-modeling/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/domain-modeling/SKILL.md) | 300k | Challenge a word that conflicts with the glossary; turn an overloaded word into a choice between precise terms; check what the user says against the code and raise contradictions; write a resolved term down at once, not in a batch; the glossary holds meanings, not implementation | DK9, `01` "New and fuzzy words", DK7 |
| [bmad-code-org/BMAD-METHOD `skills/bmad-prd/assets/prd-template.md`](https://github.com/bmad-code-org/BMAD-METHOD/blob/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b/skills/bmad-prd/assets/prd-template.md) | 54k | Every domain noun is defined once and used verbatim; a synonym anywhere is a violation; a new noun is added to the glossary in the same pass | DK1 ("Avoid saying" checked by `gate-review`), DK9 |
| [github/spec-kit `templates/commands/checklist.md`](https://github.com/github/spec-kit/blob/dc2cec4f568d0f6e2cdfb8571c69116bc55c1aaf/templates/commands/checklist.md) | 142k | Undefined or vague terms are reported as `[Ambiguity]` findings about the text | DK1 (the list is what the review checks) |

## Not adopted

| Idea | Source | Why not |
|---|---|---|
| A root `GLOSSARY.md` (or one per bounded context with a map file) | domain-modeling | The workspace glossary lives in `.agents/skills/domain-knowledge/references/01-glossary.md`; an existing `GLOSSARY.md` is adopted verbatim (P5) instead of creating a second one. |
| Offering ADRs from this skill | domain-modeling | Decision records belong to Planning (`decision-records`); this skill records meanings, not technical choices. |
| Inventing edge-case scenarios to stress concept boundaries | domain-modeling | Edge cases are owned by `requirements-specification` (RS3, mandatory edge cases); here only the term question is asked. |
| Updating the glossary silently as soon as the agent thinks a term is settled | domain-modeling | Every new term is confirmed by the user (`D-NN`) or read from code (`VERIFIED`) first; "confirm every inference" applies. |
| Glossary with cardinality and relationships inside each definition | BMAD PRD template | Relationships and lifecycles live in the entity cards (`02`); the glossary row stays one line. |
