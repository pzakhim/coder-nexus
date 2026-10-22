---
name: create-quality-planning-skill
description: Write a workspace's own quality-planning skill from the skill-factory knowledge base - how the Quality Engineer turns approved specs into a test plan - testability review right after requirements, acceptance criteria to test cases with two-way traceability, coverage of happy paths, validation, permissions per role and environment, empty/loading/error states and boundaries, the cheapest test level that proves each case (API acceptance, UI end-to-end, visual, manual), test data and environments, risk priority, out-of-scope guards and regression - independent from the implementation, for fullstack repos with backend and frontend branches. Use whenever the user wants to set up, standardize or update how test cases are designed from specs in a workspace, or says things like "tạo skill test plan", "viết test case từ spec", "QA lập kế hoạch test", even if they do not say "skill". Writes .agents/skills/quality-planning/, then trial-runs it on a real spec.
argument-hint: "[stack/framework] [where specs live]"
---

# Create Quality Planning Skill

Goal: produce `<workspace>/.agents/skills/quality-planning/` — how the Quality Engineer designs test cases from the workspace's approved specs: testability review, traceability, coverage, test levels, data, environments and the plan format.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — quality-planning is the QA side (what to test); execution, environment and reporting are the other Quality skills; unit tests belong to the Code Writer.

## Step 1 — Context Card (+ spec and test landscape)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Spec artifacts | Brief (scope in/out), requirements with AC and BDD scenarios, design state matrix, decisions (`D-NN`), glossary — e.g. `.superpowers/work-items/<slug>/vN/`, `docs/features/…` |
| AC and case IDs | `AC-NN`, `FLOW-NN`, `E2E-NN`, `TC-NN` or the workspace's own |
| Existing test skills | `.agents/skills/*test*`, `*verification*`, tester role files |
| Test levels present | Unit, integration (real DB), API collections (Postman/Newman, HTTP tests), browser E2E (MCP browser tool, Playwright), visual checks |
| Roles and data scopes | RBAC roles, environments, tenants — for the permission matrix |
| Test data sources | Seeds, fixtures, local DB sync, mock servers for external providers |
| Base inputs (read-only) | Coder Nexus `plugins/core/agents/test_runner.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/case-design.md`, `references/test-levels.md`. For each rule Q1–Q14: adopted, adapted, or "not adopted" with a reason. Q1, Q2, Q3, Q4, Q11, Q14 are never "not adopted".

## Step 3 — Propose

- **Sources and testability checklist** with the workspace's spec files.
- **Plan format:** case ID scheme, traceability table, where the plan lives and who approves it.
- **Levels per branch:** which cases are API acceptance, UI end-to-end, visual or manual; **who owns integration tests** in this workspace (default: Code Writer).
- **Data and environments:** sources, seeding, stubs for external providers, which environments are allowed.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) sources, IDs and plan location/approval, (2) coverage categories and priority scheme, (3) test levels per branch and the integration-test owner, (4) data and environment rules.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06`; branched: `shared/01, 02, 03, 05, 06`, `be/04`, `fe/04`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The planning steps and the non-negotiables on one screen |
| `references/01-sources-and-testability.md` | `shared/01-…` | `templates/shared/01-sources-and-testability.md.tmpl` | **Mandatory** | Untestable AC found early cost a question; found late they cost a release |
| `references/02-traceability.md` | `shared/02-…` | `templates/shared/02-traceability.md.tmpl` | **Mandatory** | Every AC proven, every case justified |
| `references/03-case-design.md` | `shared/03-…` | `templates/shared/03-case-design.md.tmpl` | **Mandatory** | Coverage categories and concrete expected results |
| `references/04-test-levels.md` | `be/04-…`, `fe/04-…` | `templates/branch/04-test-levels.md.tmpl` | **Mandatory** | The cheapest level that proves the behavior, per branch |
| `references/05-data-and-environments.md` | `shared/05-…` | `templates/shared/05-data-and-environments.md.tmpl` | **Mandatory** | Safe, repeatable data and the right target |
| `references/06-plan-template.md` | `shared/06-…` | `templates/shared/06-plan-template.md.tmpl` | Suggested | The plan document; may merge into 02 |

Writing rules: keep each template's purpose, give every rule its reason, the workspace's real spec paths, IDs and roles, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Quality planning
   Test plans are derived from approved specs per `.agents/skills/quality-planning/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file and from the spec writer role (testability review) (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Plan the tests for a real approved spec (or a recent feature's requirements).
- A spec with one vague AC ("works quickly", "user-friendly") — is it flagged as untestable with a question back?
- A feature with role and environment rules — is the permission matrix covered at API level, not only in the UI?

Compare: every AC traced, categories covered, levels sensible, expected results concrete, data safe, independence kept.

## Step 8 — Description

Per the authoring guide: workspace name; situations (plan tests for a feature, review a spec for testability, write test cases, traceability); team trigger words. Should not trigger for running tests (quality-acceptance) or unit tests (unit-testing).

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/quality-planning/` or test-planning sections (e.g. in `fe-testing-and-verification`): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep case IDs, checks numbering, plan location).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — Q1–Q14 with reasons
- `references/case-design.md` — coverage categories and design techniques
- `references/test-levels.md` — choosing the level and its owner
- `templates/` — `SKILL.md.tmpl`, `shared/01, 02, 03, 05, 06`, `branch/04` (suggested shapes)
- `checklist.md` — topic checks
