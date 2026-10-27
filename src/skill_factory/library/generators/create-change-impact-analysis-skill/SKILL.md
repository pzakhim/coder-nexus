---
name: create-change-impact-analysis-skill
description: "Write a workspace's own change-impact-analysis skill from the skill-factory knowledge base - when a change touches existing behavior (change requests, bug fixes, work items v2+), how to trace what it affects with evidence (screens, APIs and their consumers, data and reports, jobs and integrations, permissions, docs), how to choose regression tests, and how to fill the fixed change-impact.md - using the workspace's real dependency structure and search tools, for any domain and any stack. Use whenever the user wants to set up, standardize or update how impact and regression scope are analysed before changing existing code, or says things like 'tạo skill change impact', 'sửa cái này ảnh hưởng gì', 'phạm vi hồi quy', 'test lại những gì', even if they do not say 'skill'. Writes .agents/skills/change-impact-analysis/, then trial-runs it on a real past change."
argument-hint: "[module or area]"
---

# Create Change Impact Analysis Skill

Goal: produce `<workspace>/.agents/skills/change-impact-analysis/` — how to find, with evidence, everything a change to existing behavior touches in this workspace, and which regression tests follow. The result is written into the fixed `change-impact.md` template (Coder Nexus `work-item-contract` skill, `templates/change-impact.md.tpl`: baseline, behavior delta as `ADDED` / `MODIFIED` / `REMOVED`, AC delta as `Add` / `Change` / `Remove` / `Keep`, code impact, regression and migration); this skill supplies where to look and how.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership and the generic-vs-specific rule: [../../core/planning-skill-family.md](../../core/planning-skill-family.md). Entities and rules come from `.agents/skills/domain-knowledge/` when it exists; test cases are owned by `quality-planning`, which receives the regression list.

## Step 1 — Context Card (+ dependency structure)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project scan ([../../core/existing-project.md](../../core/existing-project.md)). Then collect, read-only (`references/detection.md`): module and import structure, routes to screens, shared components, which code reads and writes each table, jobs/workers/events, external consumers of the API, test suites per module, the tools available for tracing, and past `change-impact.md` files.

## Step 2 — Enforce the base rules

Read `references/base-rules.md`. All rules `CX1`–`CX7` (`CX7` uses the `ADDED` / `MODIFIED` / `REMOVED` vocabulary of `requirements-specification` RS10) are mandatory compliance and must be instantiated with the workspace's real search tools, dependency layout, and test runners. Review findings on impact analysis use `BLOCKER` / `MAJOR` / `MINOR`; deterministic CLI verification checks use `PASS` / `FAIL`.

## Step 3 — Propose

- Impact map and tracing recipes (`CX1`, `CX2`): for each impact category the workspace has, where to look and the exact command, plus repeatable recipes for common starting points (entity field, API endpoint, business rule, shared component, permission).
- Classification and regression selection (`CX3`–`CX6`): classifying hits (`behavior changes` vs `regression only`) with `file:symbol` evidence, contract break flags, `Q-NN` for unsettled impacts, and regression suites per module.
- Writing `change-impact.md` and gates (`CX7`): one past change re-analysed with the proposed recipes, including its behavior delta (`ADDED` / `MODIFIED` / `REMOVED`), AC delta (`Add` / `Change` / `Remove` / `Keep`), `BLOCKER` / `MAJOR` / `MINOR` review rubric, and `PASS` / `FAIL` CLI gates.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Impact categories that exist in this workspace | Those found in Step 1 |
| Q2 | Tracing tools and commands | `rg` plus the language's own tools found in Step 1 |
| Q3 | Regression suites per module | As mapped from test folders and CI |
| Q4 | When the analysis is mandatory | Every work item `v2+` (a change: a feature or refactor delivered as a new `vN`), and bugfixes on built code |

## Step 5 — Author

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Layout: **flat** (multi-surface repositories keep all application layer rows in the same tables, labelled by module/surface).

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Routing table, `CX1`–`CX7` index, and gate summary |
| `references/01-impact-map-and-tracing-recipes.md` | `templates/references/01-impact-map-and-tracing-recipes.md.tmpl` | **Mandatory** | `CX1`, `CX2`: The 6 impact categories and repeatable tracing recipes |
| `references/02-classification-and-regression-selection.md` | `templates/references/02-classification-and-regression-selection.md.tmpl` | **Mandatory** | `CX3`–`CX6`: Hit classification, contract breaks, `Q-NN` escalation, and regression selection |
| `references/03-writing-change-impact-and-gates.md` | `templates/references/03-writing-change-impact-and-gates.md.tmpl` | **Mandatory** | `CX7`: Filling `change-impact.md` deltas, `BLOCKER` / `MAJOR` / `MINOR` rubric, and `PASS` / `FAIL` CLI gates |

Writing rules: real paths, commands and module names; every rule with its reason; replace every `{{…}}`, delete every `<!-- GEN … -->`, keep `<!-- {{profile_references}} -->` in `SKILL.md`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Change impact
   Changes to existing behavior are analysed with `.agents/skills/change-impact-analysis/SKILL.md`.
   ```
2. Offer to link it from `requirements-specification`, `implementation-planning` and `quality-planning` ([../../core/existing-project.md](../../core/existing-project.md)).

## Step 7 — Trial run

Follow [../../core/trial-run.md](../../core/trial-run.md). Re-analyse one or two changes this workspace already delivered: verify that the skill finds the callers, consumers, data, and tests that the real change needed (compare with its diff and any regressions found later).

## Step 8 — Description

Per the authoring guide: workspace name; situations (change request, bug fix, v2 of a feature, renaming a field, changing a rule or permission, "what does this affect"); the team's trigger words. Should not trigger for brand-new features with no existing behavior.

## Step 9 — Verify, record & report

Run `checklist.md` + [../../core/checklist-common.md](../../core/checklist-common.md); record provenance ([../../core/provenance.md](../../core/provenance.md)); report categories mapped, rules instantiated, and trial results.

## Update mode & Versioning

Existing `.agents/skills/change-impact-analysis/` or a workspace impact checklist: registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); not registered → adopt ([../../core/existing-project.md](../../core/existing-project.md)). When changing this generator, follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- `references/base-rules.md` — `CX1`–`CX7` mandatory rules with reasons
- `references/detection.md` — where dependencies, consumers and tests are found across stacks
- `templates/` — `SKILL.md.tmpl` and `templates/references/01..03-*.md.tmpl`
- `checklist.md` — topic checks
