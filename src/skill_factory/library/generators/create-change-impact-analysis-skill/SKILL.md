---
name: create-change-impact-analysis-skill
description: Write a workspace's own change-impact-analysis skill from the skill-factory knowledge base - when a change touches existing behavior (change requests, bug fixes, work items v2+), how to trace what it affects with evidence (screens, APIs and their consumers, data and reports, jobs and integrations, permissions, docs), how to choose regression tests, and how to fill the fixed change-impact.md - using the workspace's real dependency structure and search tools, for any domain and any stack. Use whenever the user wants to set up, standardize or update how impact and regression scope are analysed before changing existing code, or says things like "tạo skill change impact", "sửa cái này ảnh hưởng gì", "phạm vi hồi quy", "test lại những gì", even if they do not say "skill". Writes .agents/skills/change-impact-analysis/, then trial-runs it on a real past change.
argument-hint: "[module or area]"
---

# Create Change Impact Analysis Skill

Goal: produce `<workspace>/.agents/skills/change-impact-analysis/` — how to find, with evidence, everything a change to existing behavior touches in this workspace, and which regression tests follow. The result is written into the fixed `change-impact.md` template (Coder Nexus `work-item-contract` skill, `templates/change-impact.md.tpl`: baseline, behavior delta as ADDED / MODIFIED / REMOVED, AC delta, code impact, regression and migration); this skill supplies where to look and how.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0**. Ownership and the generic-vs-specific rule: `~/.claude/skill-factory/core/planning-skill-family.md`. Entities and rules come from `.agents/skills/domain-knowledge/` when it exists; test cases are owned by `quality-planning`, which receives the regression list.

## Step 1 — Context Card (+ dependency structure)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then collect, read-only (`references/detection.md`): module and import structure, routes to screens, shared components, which code reads and writes each table, jobs/workers/events, external consumers of the API, test suites per module, the tools available for tracing, and past `change-impact.md` files.

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule CX1–CX7 (CX7 uses the ADDED / MODIFIED / REMOVED vocabulary of `requirements-specification` RS10): adopted, adapted, or "not adopted" with a reason. CX1 (evidence) and CX6 (no "no impact" without evidence) are never "not adopted".

## Step 3 — Propose

- Impact map: for each impact category the workspace has, where to look and the exact command.
- Tracing recipes for the common starting points (an entity field, an API endpoint, a business rule, a shared component, a permission).
- Regression selection: which suites or cases cover which module, and the commands to run them.
- One past change re-analysed with the proposed recipes, to show the result, including its behavior delta (ADDED / MODIFIED / REMOVED) and AC delta.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Impact categories that exist in this workspace | Those found in Step 1 |
| Q2 | Tracing tools and commands | `rg` plus the language's own tools found in Step 1 |
| Q3 | Regression suites per module | As mapped from test folders and CI |
| Q4 | When the analysis is mandatory | Every work item `v2+` (a change: a feature or refactor delivered as a new `vN`), and bugfixes on built code |

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Layout: **flat** (fullstack repositories keep BE and FE rows in the same tables, labelled).

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | When to run it and the evidence rule on one screen |
| `references/01-impact-map.md` | `templates/01-impact-map.md.tmpl` | **Mandatory** | Where to look for each kind of impact |
| `references/02-tracing-recipes.md` | `templates/02-tracing-recipes.md.tmpl` | **Mandatory** | Repeatable steps from a starting point to every affected place |
| `references/03-regression-selection.md` | `templates/03-regression-selection.md.tmpl` | **Mandatory** | The tests that prove nothing else broke |
| `references/04-writing-change-impact.md` | `templates/04-writing-change-impact.md.tmpl` | **Mandatory** | How the findings fill `change-impact.md` |

Writing rules: real paths, commands and module names; every rule with its reason; replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Change impact
   Changes to existing behavior are analysed with `.agents/skills/change-impact-analysis/SKILL.md`.
   ```
2. Offer to link it from `requirements-specification`, `implementation-planning` and `quality-planning` (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Re-analyse one or two changes this workspace already delivered: does the skill find the callers, consumers, data and tests that the real change needed (compare with its diff and any regressions found later)?

## Step 8 — Description

Per the authoring guide: workspace name; situations (change request, bug fix, v2 of a feature, renaming a field, changing a rule or permission, "what does this affect"); the team's trigger words. Should not trigger for brand-new features with no existing behavior.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report categories dropped, rules adapted or not adopted, trial results.

## Update mode

Existing `.agents/skills/change-impact-analysis/` or a workspace impact checklist: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — CX1–CX7 with reasons
- `references/detection.md` — where dependencies, consumers and tests are found, per stack
- `templates/` — `SKILL.md.tmpl`, `01–04` (suggested shapes)
- `references/sources.md` — external sources and ideas not adopted
- `checklist.md` — topic checks
