# Changelog — create-change-impact-analysis-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules CX1–CX7 with reasons: trace with evidence, fixed impact categories, classify hits, regression list, flag contract breaks, unknown is not "no impact", AC delta for v2+.
- Detection of module structure, UI, API consumers, data, jobs, permissions and tests per stack.
- Mandatory: `SKILL.md`, impact map, tracing recipes, regression selection, writing change-impact.md.
- Layout: flat.
- Output path: `<workspace>/.agents/skills/change-impact-analysis/`.

**Affects:** all generated files.
**Migration:** existing impact checklists → run the generator to **adopt**.
