# Checklist — git-workflow

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule M1–M9, G1–G6, V1–V7, R1–R2 is adopted, adapted, or "not adopted" with a reason; M1–M9 are adopted and M6 is not weakened
- [ ] Branch names, protected branches, tag format and ticket prefixes come from the repository or the user's answers, not from the preset alone
- [ ] The preflight table covers feature/refactor/perf/chore, bug on DEV, bug on STG (several or no active release), bug on PROD, spike, verification/docs
- [ ] Every row that touches the production branch says the user merges, tags and deploys; the agent only prepares commands
- [ ] The merge table matches the repository's real history or a confirmed change to it
- [ ] Hotfix propagation names every active line
- [ ] Contracts (V1) are listed for this workspace; examples for PATCH, MINOR and MAJOR are real
- [ ] Existing commit/release tools are named and used as checks instead of restated rules
- [ ] `.superpowers/work-items/` commit decision (Q9) is recorded; `.gitignore` changed only with the user's confirmation
- [ ] No secret, credential or internal host value; artifact references use placeholders
- [ ] Skill is flat; `SKILL.md` keeps the never-list and the base table on one screen
