# Changelog — create-quality-environment-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules E1–E14 with reasons (from the erp-knowledge-platform live-stack practice and the Coder Nexus preparation phase, generalised): know the stack, probe before starting, start in the background and stop only what you started, readiness, isolated data, per-role accounts, sandboxes or labelled stubs, migrations at the reviewed revision, revision alignment, environment matrix, cleanup, BLOCKED on failure, secrets, environment record.
- Stack recipes (probe/start/ready/stop) and stub options with labelling.
- Mandatory: `SKILL.md`, stack & lifecycle, test data & accounts, external dependencies, revision & migrations, cleanup & failures.
- Layout: always flat (BE/FE sections inside files for fullstack).
- Output path: `<workspace>/.agents/skills/quality-environment/`.

**Affects:** all generated files.
**Migration:** existing live-stack guidance → run the generator to **adopt** (keeps probe rules, make targets and forbidden commands).
