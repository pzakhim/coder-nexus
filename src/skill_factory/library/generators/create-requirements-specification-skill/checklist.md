# Checklist — requirements-specification

Run this and [../../core/checklist-common.md](../../core/checklist-common.md).

- [ ] Every rule `RS1`–`RS10` is enforced as mandatory compliance and adapted to this workspace's real sources, terms, and examples with its reason
- [ ] No gate, `grilling` law, template section, or validator rule is removed or renamed (`RS9`)
- [ ] Requirement sources, conflict priority, and unreachable-source rules in `references/01-sources-and-grilling-questions.md` come from this workspace (`RS1`, `RS8`)
- [ ] Question-bank rows per `grilling` dimension in `references/01-sources-and-grilling-questions.md` use workspace terms and real ticket examples, and link every asked question to a confirmed `G-NN` (`RS2`)
- [ ] Mandatory edge-case categories in `references/02-edge-cases-and-writing-rules.md` include one real workspace example each, and categories the workspace does not have are listed as `not applicable` with a reason (`RS3`)
- [ ] Sample `BR-NN`, `AC-NN`, and measurable `G-NN` success signal in `references/02-edge-cases-and-writing-rules.md` were confirmed by the user (`RS4`)
- [ ] Banned vague-word replacement table comes from the workspace's own specs or review comments, with concrete replacements; unresolved vague words become `Q-NN` (`RS4`)
- [ ] Terms match `domain-knowledge` verbatim (or are marked `OPEN` when `domain-knowledge` does not exist yet); any synonym is flagged as a defect (`RS5`)
- [ ] Bug specification fields (`DEV` / `STG` / `PROD`, reproduction steps, expected vs actual, affected users/data, regression scope) and `v2+` delta rules (`ADDED` / `MODIFIED` / `REMOVED` in `change-impact.md` `"Behavior delta"`, `Add` / `Change` / `Remove` / `Keep` in `"AC delta"`, migration note on `REMOVED`) are present in `references/02-edge-cases-and-writing-rules.md` (`RS7`, `RS10`)
- [ ] Gate 1 spec review in `references/03-gate-review-and-verification.md` defines deterministic `PASS` / `FAIL` CLI gates (`validate_proposal_spec` and `rg` checks for vague words, banned synonyms, open `Q-NN`, and AC traceability) and job-type review questions tagged `[Gap]`, `[Ambiguity]`, or `[Conflict]` with unified `BLOCKER` / `MAJOR` / `MINOR` severities (`RS6`)
- [ ] `SKILL.md` links `references/01-sources-and-grilling-questions.md`, `references/02-edge-cases-and-writing-rules.md`, and `references/03-gate-review-and-verification.md`, includes `<!-- {{profile_references}} -->`, and has no `Assumptions` section or guessed values (anything unknown becomes a `Q-NN`)
