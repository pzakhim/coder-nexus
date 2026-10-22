# Base rules (generic, every workspace)

Each rule goes into the generated skill with the workspace's real facts **and its reason**, or is marked "not adopted" with a reason. Examples here use neutral names; the generated skill uses the workspace's own.

| # | Rule | Why | Goes into |
|---|---|---|---|
| DK1 | **One term, one meaning.** Each glossary row: the term in the team's language, its code name(s), a one-line meaning, synonyms to avoid. | Specs and code must name the same thing the same way. | 01 |
| DK2 | **Entity cards.** Each business entity: owning module, key fields, status values, allowed transitions, who or what triggers each transition, where it is enforced. | Lifecycle questions are where specs miss most. | 02 |
| DK3 | **Roles × scopes × actions.** Which role may do which action on which data, and the condition that limits the data (the "data scope"), read from permission checks and confirmed. A workspace without roles or scopes says so. | Wrong permissions are the costliest defects. | 03 |
| DK4 | **Business-rule catalog.** Each rule: ID, statement, where it is enforced (`file:symbol`), source (document, ticket, user). | Planning changes the rule in the right place, once. | 04 |
| DK5 | **Labelled facts, no invention.** `VERIFIED` (path), `CONFIRMED` (user or approved document), `OPEN` (unknown). An inference is never written as a fact. | A wrong domain skill is worse than none. | all |
| DK6 | **Link volatile facts.** Counts, customer lists, configuration values and current versions are linked to their source, not copied. | Copies go stale silently. | 05 |
| DK7 | **Keep it current.** When a work item changes an entity, role or rule, the skill is updated in the same work item; the change log names the item. | The skill must age with the code. | 05 |
| DK8 | **No personal data or secrets** in examples, terms or rules. | The skill is committed and shared. | all |

**Never "not adopted":** DK5, DK8.
