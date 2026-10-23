# Sources

External ideas adapted into this skill, rewritten in Coder Nexus vocabulary (SM1–SM8, `clean-code` CC rules, P1/P2/P3, `D-NN`, READY_FOR_REVIEW). Nothing is copied. Stars as of 2026-10.

Internal base input (read-only): `src/skill_factory/library/generators/create-code-simplification-skill/references/base-rules.md` (S1–S13) and `smell-catalog.md`. SM1–SM8 condense S1–S12; the report line follows S13.

| Source (link pinned to SHA) | Stars | Idea taken | Where used |
|---|---|---|---|
| [addyosmani/agent-skills `skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md) | 109k | A refactor that leaves the reader holding the same number of concepts only relocated complexity; prefer the change that makes branches or layers disappear | [SKILL](../SKILL.md) goal; [catalog](smell-catalog.md) "Reduce or relocate?" |
| same | 109k | Do not generalize until the third use case | Catalog row "Premature extraction" |
| same | 109k | Nested ternaries and "clever" tricks are readability defects | Catalog row "Clever code" |
| same | 109k | Separate refactoring from feature work | "When": only after checks pass; smells outside the diff become a separate item |
| [mattpocock/skills `skills/engineering/code-review/SKILL.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/code-review/SKILL.md) | 300k | Speculative Generality: delete abstraction added for needs the spec does not have | Catalog row "Speculative abstraction" |
| same | 300k | Middle Man and Message Chains: cut delegation, call the target | Catalog row "Needless indirection" |
| same | 300k | Data Clumps: values that always travel together want one type | Catalog row "Long parameter list" |
| same | 300k | Duplicated Code: one shared shape | Catalog row "Duplicated definitions" (definitions only; logic follows the rule of three) |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| "Could this be done in fewer lines?" as the target | addyosmani code-review-and-quality | The goal is first-read understanding; fewer lines often means clever code. Net lines are reported, not targeted |
| Extract shared shape on the first duplication | mattpocock code-review | Early extraction couples code that later diverges; rule of three for logic, definitions never duplicated |
| Replace repeated switches with polymorphism | mattpocock code-review | Introduces class hierarchies in small tasks; a lookup or a single dispatcher is decided by `{{slot:clean-architecture}}` |
| Split a large file before adding to it | addyosmani code-review-and-quality | File splitting and placement are planned work (`{{slot:clean-architecture}}`, the plan's file list), not an in-task simplification |
| Ask before deleting dead code | addyosmani code-review-and-quality | Dead code inside the diff is deleted (behavior identical by definition); outside the diff it is reported, not touched |
