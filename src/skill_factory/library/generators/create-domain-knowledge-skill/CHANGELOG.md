# Changelog — create-domain-knowledge-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Changed: DK1 — "Avoid saying" is data that `gate-review` spec mode checks; a listed word in a goal, BR, AC or scenario is a finding → `references/01-glossary.md`. (minor)
- Added: DK9 challenge new and fuzzy words — name the candidate glossary terms and ask which one (answer → `D-NN`), compare claims about behavior with the code (contradiction → `Q-NN`), add the resolved term in the same work item → `references/01-glossary.md` "New and fuzzy words", `SKILL.md` "Use it like this". DK9 is never "not adopted". (minor)
- Changed: Step 3 drafts "Avoid saying" from words that name one thing in different places and lists overloaded words; two trial prompts added (overloaded word, behavior claim the code contradicts). (patch)
- Added: `references/sources.md` with the external sources and ideas not adopted. (patch)

**Affects (when released):** `SKILL.md`, `references/01-glossary.md`.
**Migration (when released):**
1. In `references/01-glossary.md`, add the line that `gate-review` checks "Avoid saying", and the "New and fuzzy words" section; pick a real overloaded word of the workspace for the example (look in labels vs code names vs past tickets first) and name where a behavior claim is checked (entity cards, rule locations).
2. In `SKILL.md` "Use it like this", replace the glossary bullet with the verbatim-terms bullet and add the fuzzy-word bullet.
3. Fill missing "Avoid saying" cells where the workspace has known synonyms; ask the user to confirm them.

## 1.0.0 — 2026-10-22

First version.

- Base rules DK1–DK8 with reasons: one term one meaning, entity cards with lifecycles, roles × scopes × actions, business-rule catalog with locations, labelled facts, linked volatile facts, upkeep, no personal data.
- Domain-neutral detection of entities, statuses, transitions, roles, data scopes, user-facing labels and documents; tracker history optional.
- Mandatory: `SKILL.md`, glossary, entities and lifecycles, roles and scopes, business rules, sources and upkeep.
- Layout: flat; large domains split per module.
- Output path: `<workspace>/.agents/skills/domain-knowledge/`.

**Affects:** all generated files.
**Migration:** existing glossary or domain docs → run the generator to **adopt** (keeps terms, IDs and confirmed rules).
