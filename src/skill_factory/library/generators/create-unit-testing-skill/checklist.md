# Checklist — unit-testing

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule `U1`–`U14` is included as Mandatory Compliance (no `P1`/`P2`/`P3` per-rule severity column); `U2`, `U4`, `U5`, `U6`, and `U12` are adopted
- [ ] CLI test gates are strictly binary (`PASS` / `FAIL`, with `NOT_RUN` / `BLOCKED` / `UNVERIFIED` for non-executed checks)
- [ ] Review grading uses the unified `BLOCKER` / `MAJOR` / `MINOR` scale (`shared_contracts/flags_and_statuses.md` §2)
- [ ] `references/01-test-matrix-and-structure.md` includes the `EXTEND` vs `INIT` workspace rule, test-first matrix, per-layer Pass/Fail/Empty matrix, `├──`/`└──` directory tree, and naming rules
- [ ] `references/02-doubles-fixtures-and-quality.md` includes the `Real > Fake > Stub > Mock` table, concrete copy-pasteable test patterns, AAA, independent literal expectations, right-reason red failure table, determinism rules, and mutation check
- [ ] `references/03-execution-boundaries-and-review.md` includes focused and full CLI commands, "confirm the new test ran" checks, red-to-green evidence rows, unit test boundaries, and `BLOCKER`/`MAJOR`/`MINOR` review grading
- [ ] No hardcoded company-specific classes in base pack files (profile-specific rules live in `profiles/<profile>/testing-contracts.md`)
