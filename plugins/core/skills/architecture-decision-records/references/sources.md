# Sources - architecture-decision-records

Ideas were rewritten in this repo's vocabulary (`D-NN`, `Q-NN`, gates, `codebase-notes.md`). No text was copied. Stars as of the review date.

| Source (pinned) | Stars | Idea taken | Where used |
|---|---|---|---|
| [mattpocock/skills `skills/engineering/domain-modeling/ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/domain-modeling/ADR-FORMAT.md) | 300k | The three tests (hard to reverse, surprising without context, real trade-off) and why each matters; categories that usually qualify (architectural shape, integration between contexts, lock-in, ownership boundaries, deliberate deviations, invisible constraints, non-obvious rejections); `docs/adr/NNNN-slug.md` numbering; create the folder lazily; an ADR may be one paragraph | SKILL.md §1, §3, §4 |
| [addyosmani/agent-skills `skills/documentation-and-adrs/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/documentation-and-adrs/SKILL.md) | 109k | Match the existing ADR convention first (location, extension, numbering, headings, `.adr-dir`), surface conflicting conventions instead of adding a scheme; Status/Date/Context/Decision/Alternatives/Consequences sections; lifecycle Proposed -> Accepted -> Superseded or Deprecated; never delete, supersede with a new ADR | SKILL.md §3, §4, §5 |

## Not adopted

| Idea | Source | Reason |
|---|---|---|
| ADRs for every significant decision, checked as a verification item | addyosmani | Conflicts with the optional nature and with user confirmation; the three tests keep ADRs rare, and `codebase-notes.md` already records every decision. |
| Default folder `docs/decisions/` | addyosmani | `docs/adr/` chosen as the default when no convention exists; `docs/decisions/` is still detected and followed when present. |
| Mandatory pros/cons per alternative | addyosmani | Alternatives keep only the reason each lost; a small ADR may be one paragraph. |
| Status as optional frontmatter | mattpocock | Status and Date are always present because supersede-never-delete depends on them. |
| Offering ADRs spontaneously during a modeling conversation | mattpocock | Candidates are offered once, as a `Q-NN` after the gate, so the one-question-at-a-time flow is not interrupted. |
| Inline comments, README, API docs, changelog and prose-review guidance | addyosmani | Outside this skill; reader-facing docs belong to Docs Writer and code comments to `{{slot:clean-code}}`. |
