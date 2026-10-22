# Changelog — create-quality-planning-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules Q1–Q14 with reasons (from Coder Nexus `plugins/core/agents/test_runner.md` and the erp-knowledge-platform verification practice, generalised): specs as source of truth, early testability review, two-way traceability, coverage categories, cheapest proving level, safe test data, environments, risk priority, out-of-scope guards, regression set, concrete expected results, case IDs, plan approval, independence from the implementation.
- Case-design techniques and test-level selection with owners (integration-test owner chosen per workspace).
- Mandatory: `SKILL.md`, sources & testability, traceability, case design, test levels, data & environments. Suggested: plan template.
- Layouts: flat `references/01–06`; branched `shared/01, 02, 03, 05, 06`, `be/04`, `fe/04`.
- First generator of the Quality Assurance Pack (`core/quality-skill-family.md`).
- Output path: `<workspace>/.agents/skills/quality-planning/`.

**Affects:** all generated files.
**Migration:** existing test-planning guidance → run the generator to **adopt** (keeps case IDs, check numbering and plan location).
