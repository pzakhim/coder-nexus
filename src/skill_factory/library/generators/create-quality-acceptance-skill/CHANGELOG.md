# Changelog — create-quality-acceptance-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules A1–A14 with reasons (from the Coder Nexus test runner role and the erp-knowledge-platform interactive E2E practice, generalised): approved plan on the reviewed revision, read-only, cases as written, real data paths and persistence read-back, real browser states/permissions/environment switch/console-network for the frontend, real API with auth per role/status/persistence/side effects/403 for the backend, BLOCKED when a tool is unreachable, evidence per case, result vocabulary, failure details, out-of-scope and regression cases, re-test scope, safety, flakiness.
- Browser and API tools are **not fixed**: detected in the workspace (chrome-devtools MCP, Playwright, Claude in Chrome, built-in browser; HTTP clients, Postman/Newman, `.http`, curl) and chosen at the gate, with an operations map per tool.
- Mandatory: `SKILL.md`, preconditions & safety, executing cases, execution (be/fe), failures & re-test.
- Layouts: flat `references/01–04`; branched `shared/01, 02, 04`, `be/03`, `fe/03`.
- Output path: `<workspace>/.agents/skills/quality-acceptance/`.

**Affects:** all generated files.
**Migration:** existing E2E guidance → run the generator to **adopt** (keeps checks numbering, tool flows, baseline noise and evidence paths).
