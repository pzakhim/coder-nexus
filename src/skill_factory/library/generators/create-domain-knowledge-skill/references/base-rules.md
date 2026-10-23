# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real facts **and its reason**, or is marked "not adopted" with a reason. Examples here use neutral names; the generated skill uses the workspace's own.

| # | Rule | Why | Goes into |
|---|---|---|---|
| DK1 | **One term, one meaning.** Each glossary row: the term in the team's language, its code name(s), a one-line meaning, synonyms to avoid. "Avoid saying" is data: `gate-review` spec mode reports any of those words found in goals, BR, AC or scenarios. | Specs and code must name the same thing the same way; a listed synonym can be checked, an unlisted one cannot. | 01 |
| DK2 | **Entity cards.** Each business entity: owning module, key fields, status values, allowed transitions, who or what triggers each transition, where it is enforced. | Lifecycle questions are where specs miss most. | 02 |
| DK3 | **Roles × scopes × actions.** Which role may do which action on which data, and the condition that limits the data (the "data scope"), read from permission checks and confirmed. A workspace without roles or scopes says so. | Wrong permissions are the costliest defects. | 03 |
| DK4 | **Business-rule catalog.** Each rule: ID, statement, where it is enforced (`file:symbol`), source (document, ticket, user). | Planning changes the rule in the right place, once. | 04 |
| DK5 | **Labelled facts, no invention.** `VERIFIED` (path), `CONFIRMED` (user or approved document), `OPEN` (unknown). An inference is never written as a fact. | A wrong domain skill is worse than none. | all |
| DK6 | **Link volatile facts.** Counts, customer lists, configuration values and current versions are linked to their source, not copied. | Copies go stale silently. | 05 |
| DK7 | **Keep it current.** When a work item changes an entity, role or rule, the skill is updated in the same work item; the change log names the item. | The skill must age with the code. | 05 |
| DK8 | **No personal data or secrets** in examples, terms or rules. | The skill is committed and shared. | all |
| DK9 | **Challenge new and fuzzy words.** When the user or a ticket uses a word that is not in the glossary, is overloaded, or is listed under "Avoid saying", name the glossary term(s) it could mean and ask which one (one question, recommendation first: "Customer or User?"); the answer is a `D-NN`. When the user states how something works, compare it with the code; a contradiction becomes a `Q-NN` that quotes both. A resolved term is added to the glossary in the same work item (DK7), labelled `CONFIRMED` or `VERIFIED`. | Fuzzy words are where two people agree on different things; checking against code catches a rule that is remembered wrong. | SKILL, 01 |

**Never "not adopted":** DK5, DK8, DK9.
