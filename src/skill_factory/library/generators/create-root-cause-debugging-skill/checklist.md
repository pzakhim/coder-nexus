# Checklist — root-cause-debugging

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule `D1`–`D14` is included as Mandatory Compliance (no `P1`/`P2`/`P3` per-rule severity column); `D1`, `D7`, `D8`, `D9`, and `D12` are adopted
- [ ] CLI diagnostic and verification gates are strictly binary (`PASS` / `FAIL`, with `NOT_RUN` / `BLOCKED` / `UNVERIFIED` for non-executed or blocked checks)
- [ ] Review grading uses the unified `BLOCKER` / `MAJOR` / `MINOR` scale (`shared_contracts/flags_and_statuses.md` §2)
- [ ] `references/01-reproduce-read-and-tools.md` includes the `EXTEND` vs `INIT` workspace rule, reproduction hierarchy, reading the first real frame, untrusted log redaction, and non-interactive CLI/tracing commands (no interactive REPL debuggers that hang agent shells)
- [ ] `references/02-isolate-and-hypothesize.md` includes diff/layer isolation, 3–5 ranked falsifiable hypotheses (`H1`..`H3`), tagged `[DEBUG-xxxx]` cleanup proof, and the Symptom → First Moves → Typical Root Cause matrix
- [ ] `references/03-fix-escalate-and-report.md` includes Red-to-Green regression testing, Never Green-Wash rules, Environment (`BLOCKED`) vs Code table, 3-attempt time-box, `change-control` escalation classes, hand-off Debug Report block, and `BLOCKER`/`MAJOR`/`MINOR` review grading
- [ ] No hardcoded company-specific classes in base pack files (profile-specific rules live in `profiles/<profile>/debugging-contracts.md`)
