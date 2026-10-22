# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real sources, terms and examples **and its reason**, or is marked "not adopted" with a reason. The fixed `grill-me` laws (draft first, confirm every inference, 0 open questions, one question at a time) always apply; these rules add content inside them.

| # | Rule | Why | Goes into |
|---|---|---|---|
| RS1 | **Source map.** Each kind of requirement: where it comes from, how it is read, which sources are often unreachable, which wins on conflict. | The Source Inventory is right from the first turn. | 01 |
| RS2 | **Question bank per dimension.** For each `grill-me` dimension (scope and data source, happy path and states, inferences, negative and edge cases, lifecycle), the questions this workspace usually needs, in its terms; each asked question names the `G-NN` it serves. | Fewer, better questions. | 02 |
| RS3 | **Mandatory edge cases.** The catalog categories the workspace really has, each with a real example; the Spec Writer checks each one against the item. | Defects cluster in familiar edge cases. | 03 |
| RS4 | **Observable AC.** Given/When/Then (or the team's format), one behavior per AC, no implementation words, testable by QA; examples from approved specs. | QA can test it, the user can read it. | 04 |
| RS5 | **Domain terms only.** BR and AC use the glossary terms of `domain-knowledge`; a new term is added there first. | One name per thing across spec and code. | 04, SKILL |
| RS6 | **Ready for Gate 1** per job type (feature, change, bug fix, verification, documentation): what must be true before the spec is presented. | Knowing when to stop asking. | 05 |
| RS7 | **Bug specs.** Reproduction steps, where it was found (DEV / STG / PROD), expected vs actual, affected users and data, regression scope. | A bug spec needs different facts than a feature. | 04, 05 |
| RS8 | **Language.** User-facing documents in the team's language; code names stay as in code. | The user approves what they can read. | SKILL |
| RS9 | **Fixed process unchanged.** No gate, `grill-me` law, template section or validator rule is removed or renamed. | Workspace skills add content, not a different process. | SKILL |

**Never "not adopted":** RS5, RS9.
