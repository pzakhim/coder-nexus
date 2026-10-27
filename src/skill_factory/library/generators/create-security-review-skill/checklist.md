# Checklist — `create-security-review-skill`

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All rules `SR1`–`SR14` are enforced as mandatory compliance (zero `"not adopted"` carve-outs).
- [ ] Security finding severities use strictly the unified 3-tier scale **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`; zero `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` or `P0`–`P3` remnants).
- [ ] Deterministic CLI security/scanner gates use strictly **`PASS` / `FAIL`** (`NOT_RUN`, `BLOCKED`, `UNVERIFIED` never count as `PASS`).
- [ ] Generator and templates are 100% stack-agnostic (zero hardcoded `be/`/`fe/` branched folders or framework assumptions).
- [ ] Generated skill uses the flat 3-reference layout (`references/01-triggers-threat-model-and-auth-matrix.md`, `references/02-security-checks-and-cli-gates.md`, `references/03-findings-verdict-and-report.md`) and `SKILL.md` is < 115 lines.
- [ ] Every finding requires a concrete exploit scenario (`given → when → then`), confidence (`CONFIRMED` / `PLAUSIBLE`), and maps deterministically to `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED`.
- [ ] Safe-testing boundary (`SR13`: no live exploitation of shared/production environments, no real secrets/PII in reports) is explicitly stated.
