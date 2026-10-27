# Changelog — create-quality-environment-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

- Consolidated `templates/` from 5 fragmented files into `templates/SKILL.md.tmpl` and 3 cohesive templates under `templates/references/` (`01-stack-lifecycle-and-revision.md.tmpl`, `02-test-data-accounts-and-stubs.md.tmpl`, `03-cleanup-blocked-handling-and-gates.md.tmpl`) with binary `PASS` / `FAIL` CLI readiness gates, unified `BLOCKER` / `MAJOR` / `MINOR` review grading, and `<!-- {{profile_references}} -->`.
- Enforced mandatory compliance for all `E1`–`E14` rules (removing `"not adopted"` carve-outs).
- Made `SKILL.md` and `references/stack-recipes.md` 100% stack-agnostic by organizing recipes into generic service categories (Containerized Services, API/Backend Process, Background Worker Process, Client/UI Dev Server).

**Affects:** `SKILL.md`, `references/01..03.md`.
**Migration:** merge `01`+`04` into `references/01-stack-lifecycle-and-revision.md`, `02`+`03` into `references/02-test-data-accounts-and-stubs.md`, and `05` into `references/03-cleanup-blocked-handling-and-gates.md`; update `SKILL.md` to use `PASS`/`FAIL` readiness gates and `BLOCKER`/`MAJOR`/`MINOR` review severities.

## 1.0.0 — 2026-10-22

First version.

- Base rules E1–E14 with reasons (from the erp-knowledge-platform live-stack practice and the Coder Nexus preparation phase, generalised): know the stack, probe before starting, start in the background and stop only what you started, readiness, isolated data, per-role accounts, sandboxes or labelled stubs, migrations at the reviewed revision, revision alignment, environment matrix, cleanup, BLOCKED on failure, secrets, environment record.
- Stack recipes (probe/start/ready/stop) and stub options with labelling.
- Mandatory: `SKILL.md`, stack & lifecycle, test data & accounts, external dependencies, revision & migrations, cleanup & failures.
- Output path: `<workspace>/.agents/skills/quality-environment/`.

**Affects:** all generated files.
**Migration:** existing live-stack guidance → run the generator to **adopt** (keeps probe rules, make targets and forbidden commands).
