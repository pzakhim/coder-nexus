# Where requirement facts are found

Read-only. Skip what the workspace does not have.

| Fact | Typical places |
|---|---|
| Approved specs (style samples) | `.superpowers/work-items/*/v*/requirements.md` with an approval record, `docs/features/**/requirements.md`, other spec folders |
| Ticket style | The tracker's recent tickets (with the user's agreement), ticket templates, parent/child patterns |
| AC format | Past AC tables, `.feature` files (Gherkin), test plans that cite AC IDs |
| Design sources | Linked design files, exported PDFs, `design-uiux/` of past items |
| Glossary and roles | `.agents/skills/domain-knowledge/`, `codebase-notes.md` → Glossary |
| Bug reports | Recent bug tickets: which fields they carry (environment, steps, expected/actual) |
| Review findings | Gate 1 feedback in `codebase-notes.md` (`Q-NN` raised at review), review comments, QA defects traced to unclear AC |
| Past deltas | `change-impact.md` → Behavior delta and AC delta of delivered `v2+` items |

```sh
rg --files -g "requirements.md" .superpowers docs
rg -n "^\| *AC-" -g "requirements.md"
rg --files -g "*.feature"
rg --files -g "change-impact.md" .superpowers
```
