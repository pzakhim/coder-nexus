# Checklist — quality-environment

Run this checklist alongside [../../core/checklist-common.md](../../core/checklist-common.md):

- [ ] All mandatory rules **E1–E14** are enforced (zero optional rule carve-outs)
- [ ] Services, ports, start commands (`cwd`), health checks, and start order reflect the real workspace; task runner targets were inspected before listing
- [ ] Probe-first (`E2`) and "stop only what you started" (`E3`, `E11`) are explicit; destructive or stop-all targets are flagged
- [ ] Revision alignment (`E9`) and local/disposable DB migration (`E8`) steps are explicit before acceptance testing
- [ ] Forbidden data commands are named (`E5`); test data isolation strategy and seeds target local/disposable storage only
- [ ] Per-role test accounts (`E6`) and environment matrix rules (`E10`) list account/role names and config keys only — zero secret values (`E13`)
- [ ] Every external provider has a sandbox, a network-edge stub labelled `stubbed: <provider>` (`E7`), or reports `BLOCKED` (`E12`)
- [ ] Deterministic CLI readiness gates use binary **`PASS` / `FAIL`** flags (`BLOCKED` / `NOT_RUN` never count as `PASS`), and review findings use **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`)
- [ ] Cohesive 3-file `references/` layout (`01-stack-lifecycle-and-revision.md`, `02-test-data-accounts-and-stubs.md`, `03-cleanup-blocked-handling-and-gates.md`) with `<!-- {{profile_references}} -->` in `SKILL.md`
