# Changelog — create-change-impact-analysis-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see [../../core/sync-protocol.md](../../core/sync-protocol.md)). Bump rules: [../../core/versioning.md](../../core/versioning.md).

## 1.1.0 — 2026-10-25

- Changed: Consolidated the 4 reference templates into 3 cohesive files under `templates/references/` (`01-impact-map-and-tracing-recipes.md.tmpl`, `02-classification-and-regression-selection.md.tmpl`, `03-writing-change-impact-and-gates.md.tmpl`) and added `<!-- {{profile_references}} -->` to `templates/SKILL.md.tmpl`.
- Changed: Enforced mandatory compliance for all rules `CX1`–`CX7` (`CX7` standardizes `ADDED` / `MODIFIED` / `REMOVED` behavior deltas against baseline built code with migration notes for `REMOVED` and `Add` / `Change` / `Remove` / `Keep` AC deltas), unified review severities (`BLOCKER` / `MAJOR` / `MINOR`), and deterministic CLI verification gates (`PASS` / `FAIL`).
- Changed: Replaced stack-biased terms in `SKILL.md` and `references/detection.md` with stack-neutral guidance across application layers, and removed `references/sources.md`.

**Affects:** `SKILL.md`, `references/01-impact-map-and-tracing-recipes.md`, `references/02-classification-and-regression-selection.md`, `references/03-writing-change-impact-and-gates.md`.
**Migration:**
1. Merge `01-impact-map.md` and `02-tracing-recipes.md` into `references/01-impact-map-and-tracing-recipes.md`.
2. Merge classification rules and `03-regression-selection.md` into `references/02-classification-and-regression-selection.md`.
3. Update `04-writing-change-impact.md` to `references/03-writing-change-impact-and-gates.md` with `ADDED` / `MODIFIED` / `REMOVED` behavior deltas, `BLOCKER` / `MAJOR` / `MINOR` review severities, and `PASS` / `FAIL` CLI gates.

## 1.0.0 — 2026-10-22

First version.

- Base rules CX1–CX7 with reasons: trace with evidence, fixed impact categories, classify hits, regression list, flag contract breaks, unknown is not "no impact", AC delta for v2+.
- Detection of module structure, UI, API consumers, data, jobs, permissions and tests per stack.
- Mandatory: `SKILL.md`, impact map, tracing recipes, regression selection, writing change-impact.md.
- Layout: flat.
- Output path: `<workspace>/.agents/skills/change-impact-analysis/`.

**Affects:** all generated files.
**Migration:** existing impact checklists → run the generator to **adopt**.
