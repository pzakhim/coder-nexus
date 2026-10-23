# Checklist — requirements-specification

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule RS1–RS10 is adopted, adapted, or "not adopted" with a reason; RS5, RS9 and RS10 are adopted
- [ ] No gate, grilling law, template section or validator rule is removed or renamed
- [ ] Sources, priority on conflict and unreachable sources come from this workspace
- [ ] Question-bank examples and edge-case examples come from the workspace's own tickets or approved specs; none is carried over from the generator
- [ ] Edge-case categories the workspace does not have are listed as not applicable
- [ ] The sample BR, AC and success signal were confirmed by the user
- [ ] The vague-word list comes from the workspace's own specs or review comments, each word with what replaces it
- [ ] Terms match `domain-knowledge` verbatim (or are marked `OPEN` when it does not exist yet); the skill says a synonym is a defect
- [ ] The delta section uses ADDED / MODIFIED / REMOVED for BR in `change-impact.md` "Behavior delta" and Add / Change / Remove / Keep for AC in "AC delta"; REMOVED needs a reason and a migration note
- [ ] Gate 1 review questions exist for each job type the workspace uses; each asks about the spec text and carries `[Gap]`, `[Ambiguity]` or `[Conflict]`; the validators and the fixed `gate-review` checklist run first
- [ ] No Assumptions section and no guessed values: anything unknown becomes a `Q-NN`
