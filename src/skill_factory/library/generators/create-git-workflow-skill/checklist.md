# Checklist — `create-git-workflow-skill`

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All rules `M1`–`M10`, `G1`–`G6`, `V1`–`V7`, and `R1`–`R2` are enforced as mandatory compliance (zero `"not adopted"` carve-outs); `M6` (human-only production merge/tag/deploy) and `M10`/`G3` (verified sub-ticket / `PHASE-NN` commit checkpoints) are intact.
- [ ] Branch names, protected branches, tag format, and ticket prefixes come from the repository and user confirmation — zero hardcoded `be-v…` / `fe-v…` stack assumptions.
- [ ] Parent-Ticket Branch Naming (`G2`: `<type>/<PARENT-TICKET>-<short-description>`) and Sub-Ticket / Accepted-Phase Commit Traceability (`G3` & `M10`: `<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]` or `<type>(<PARENT-TICKET>): [PHASE-NN] <summary>` or `<type>(phase-NN): <summary>`) are explicitly documented with concrete workspace examples.
- [ ] The preflight base table covers `feature`/`refactor`/`perf`/`chore`, bug on DEV, bug on STG (`release/*`), bug on PROD (`hotfix/*`), spike, and docs/verification.
- [ ] Merge strategy (`squash` vs `--no-ff` merge commit) and hotfix propagation across all active lines (`main`, `release/*`, `develop`) are specified.
- [ ] Contracts (`V1`), SemVer bump rules (`V2`–`V7`), and release integrity checks (`R1`–`R2`) are documented with user-executed command blocks.
- [ ] Deterministic CLI verification gates use strictly **`PASS` / `FAIL`**, and review findings use strictly **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`).
- [ ] Generated skill uses the flat 3-reference layout (`references/01-branch-model-and-preflight.md`, `references/02-naming-commits-and-merge-strategy.md`, `references/03-versioning-release-and-gates.md`) and `SKILL.md` is < 115 lines.
