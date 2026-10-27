# Checklist — quality-planning

Run this and [../../core/checklist-common.md](../../core/checklist-common.md).

- [ ] Every rule `Q1`–`Q14` is enforced as **mandatory compliance** (zero optional rule carve-outs)
- [ ] Spec sources are the workspace's real files; the implementation plan and source code are never used as sources of expected behavior (`Q1`, `Q14`)
- [ ] Canonical ID schemes for AC (`AC-NN`) and test cases (`TC-NN`) match the workspace, with a two-way traceability matrix (`Q3`, `Q12`)
- [ ] Coverage includes `Role × Environment × Action × Object` permission matrix cases (including direct API/service `401`/`403`/`404` denials) and runtime-dependent `PLAUSIBLE` items handed over from `security-review` (`SR14`, `Q4`)
- [ ] Risk tiers and plan-review findings use strictly `BLOCKER` / `MAJOR` / `MINOR` and automated CLI checks use strictly `PASS` / `FAIL` (`shared_contracts/flags_and_statuses.md`)
- [ ] Stack-neutral test levels (API/Service Acceptance, UI/Client End-to-End, Visual Fidelity, Integration, Unit) and the Integration-test owner are explicitly confirmed (`Q5`)
- [ ] Test data sources are safe and repeatable (zero production data, zero fabricated fallback data for missing sources) and external provider stubs are explicitly labelled (`Q6`, `Q7`)
- [ ] Plan location, approver, and deterministic CLI verification gates are named (`Q13`)
