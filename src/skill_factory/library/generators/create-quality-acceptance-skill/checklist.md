# Checklist — `create-quality-acceptance-skill`

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All rules `A1`–`A14` are enforced as mandatory compliance (zero optional carve-outs).
- [ ] Case outcomes use strictly **`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`**, defect severities use strictly **`BLOCKER` / `MAJOR` / `MINOR`**, and CLI execution gates use strictly **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`; zero legacy priority-tier severity tokens).
- [ ] Generator and templates are 100% stack-agnostic and organized by **UI/Client Surface (`A5`)** and **API/Service Surface (`A6`)** (zero branched `shared/` + `branch/` or `be/`/`fe/` folder assumptions).
- [ ] Generated skill uses the flat 3-reference layout (`references/01-preconditions-safety-and-case-loop.md`, `references/02-ui-and-api-execution-checks.md`, `references/03-failures-retest-and-gates.md`) and `SKILL.md` is < 115 lines.
- [ ] `A6` explicitly connects with `security-review` (`SR14`) to execute live runtime verification of the `Role × Environment × Action × Object` permission matrix (`401`/`403`/`404` anti-IDOR) and any runtime-dependent `PLAUSIBLE` checks handed over by Security Review.
- [ ] UI/client and API/service tools were detected in the workspace and confirmed at the gate with an explicit operations map and fallback order (`BLOCKED` when unreachable).
- [ ] Safe-testing boundary (`A13`: test accounts only, no production mutation, no secrets or real PII in evidence) and read-only code boundary (`A2`) are explicitly enforced.
