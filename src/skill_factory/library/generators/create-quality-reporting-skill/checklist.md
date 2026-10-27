# Checklist — `create-quality-reporting-skill`

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All rules `RP1`–`RP12` are enforced as **mandatory compliance** across the generated skill.
- [ ] Defect and report-audit severities use strictly the unified 3-tier scale **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`).
- [ ] Deterministic CLI report verification gates use strictly **`PASS` / `FAIL`**, and per-case/AC roll-ups never count `NOT_RUN`, `BLOCKED`, or `UNVERIFIED` as `PASS`.
- [ ] Feature verdict rules (`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`) require every AC `PASS` and `0` open `BLOCKER` or `MAJOR` defects for `ACCEPTED`.
- [ ] Generator and templates are 100% stack-agnostic (use `API / Service Surface` and `UI / Client Surface` or a single unified table).
- [ ] Generated skill uses the flat 3-reference layout (`references/01-report-structure-and-verdict.md`, `references/02-defects-and-retest-history.md`, `references/03-evidence-hygiene-and-gates.md`) and `SKILL.md` is < 115 lines.
- [ ] Evidence paths, secret/PII redaction rules, and external distribution authorization requirements are explicitly stated.
