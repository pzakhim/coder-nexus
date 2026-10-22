# Changelog — create-change-impact-analysis-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Changed: CX7 uses the ADDED / MODIFIED / REMOVED vocabulary shared with `requirements-specification` RS10 — classified against the built code in the template's new "Behavior delta" section, each row with reason and evidence, REMOVED with its effect on existing data and users; AC delta rows (Add / Change / Remove / Keep) trace to them → `references/04-writing-change-impact.md` "Behavior delta", "AC delta", "Regression and migration"; `SKILL.md` "Rules". (minor)
- Changed: the fixed template is named at its new home (`work-item-contract` skill, `templates/change-impact.md.tpl`); the default for when the analysis is mandatory follows the work-item Types (every `v2+`, bugfixes on built code). (patch)
- Added: `references/sources.md` with the external sources and ideas not adopted. (patch)

**Affects (when released):** `SKILL.md`, `references/04-writing-change-impact.md`.
**Migration (when released):**
1. In `references/04-writing-change-impact.md`, add the "Behavior delta" bullet (ADDED / MODIFIED / REMOVED against the built code), make the AC delta bullet trace to it, and add the migration of REMOVED behavior to "Regression and migration".
2. In `SKILL.md` "Rules", add the behavior-delta bullet.
3. If the workspace says "Change and bug-fix job types" for when the analysis runs, align it with the work-item Types (every `v2+`, bugfixes on built code) after confirming with the user.

## 1.0.0 — 2026-10-22

First version.

- Base rules CX1–CX7 with reasons: trace with evidence, fixed impact categories, classify hits, regression list, flag contract breaks, unknown is not "no impact", AC delta for v2+.
- Detection of module structure, UI, API consumers, data, jobs, permissions and tests per stack.
- Mandatory: `SKILL.md`, impact map, tracing recipes, regression selection, writing change-impact.md.
- Layout: flat.
- Output path: `<workspace>/.agents/skills/change-impact-analysis/`.

**Affects:** all generated files.
**Migration:** existing impact checklists → run the generator to **adopt**.
