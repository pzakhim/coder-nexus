# Where Requirement Facts Are Found & CLI Audits

Read-only discovery commands. Skip paths the workspace does not have.

| Fact | Typical Places |
|---|---|
| Approved specs (style samples) | `.superpowers/work-items/*/v*/requirements.md` with an approval record, `docs/features/**/requirements.md`, other spec folders |
| Ticket style | Tracker's recent tickets (with the user's agreement), ticket templates, parent/child patterns |
| AC format | Past `AC-NN` tables, `.feature` files (Gherkin), test plans that cite `AC-NN` IDs |
| Design sources | Linked Figma files (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`), exported PDFs |
| Glossary and roles | `.agents/skills/domain-knowledge/`, `codebase-notes.md` → Glossary |
| Bug reports | Recent bug tickets: environment (`DEV` / `STG` / `PROD`), reproduction steps, expected vs actual |
| Review findings | Gate 1 feedback in `codebase-notes.md` (`Q-NN` raised at review), review comments, QA defects traced to unclear `AC-NN` |
| Past deltas | `change-impact.md` → Behavior delta and AC delta of delivered `v2+` items |

## Discovery & Deterministic `PASS` / `FAIL` CLI Checks

```sh
# Discover existing specs, AC tables, feature files, and change-impact deltas
rg --files -g "requirements.md" .superpowers docs
rg -n "^\| *AC-" -g "requirements.md"
rg --files -g "*.feature"
rg --files -g "change-impact.md" .superpowers

# Deterministic CLI gates (PASS = 0 invalid matches / exit 0; FAIL = non-zero matches)
rg -n -i "\b(fast|easy|user-friendly|gracefully|as appropriate|etc\.|tbd|todo)\b" <spec_dir>/requirements.md
rg -n "OPEN" <spec_dir>/codebase-notes.md
rg -n "^\| *(G|BR|AC)-[0-9]{2,}" <spec_dir>/requirements.md
```
