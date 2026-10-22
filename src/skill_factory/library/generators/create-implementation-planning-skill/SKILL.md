---
name: create-implementation-planning-skill
description: Write a workspace's own implementation-planning skill from the skill-factory knowledge base - how Planning orders work inside one vertical behavior for this repository (for example contract, migration, backend, frontend, wiring), what one task looks like, the real check command for each kind of task, the workspace's PHASE-00 readiness items (environments, test accounts per role, seed data, mocks, migrations, feature flags), the Definition of Done per phase, branch and hotfix tasks from git-preflight, and what is a handoff rather than a task - inside the fixed planning-and-task-breakdown process, for any stack and for fullstack repos. Use whenever the user wants to set up, standardize or update how implementation plans and phases are written in a workspace, or says things like "tạo skill lập kế hoạch", "chia phase thế nào", "task nhỏ cỡ nào", "plan cho coder", even if they do not say "skill". Writes .agents/skills/implementation-planning/, then trial-runs it on real approved designs.
argument-hint: "[be_dir] [fe_dir]"
---

# Create Implementation Planning Skill

Goal: produce `<workspace>/.agents/skills/implementation-planning/` — how Planning turns an approved design into phases and tasks that fit this repository: the order inside a behavior, task shape and real checks, PHASE-00 items and the Definition of Done. It works inside the fixed `planning-and-task-breakdown` skill (vertical behavior phases, PHASE-00, AC coverage, one Code Writer running tasks in order, `validate_plan_slices`); it never changes those.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0**. Ownership: `~/.claude/skill-factory/core/planning-skill-family.md`; where files go comes from `clean-architecture`, how tests are written from `unit-testing`, branches from `git-workflow` / `git-preflight`, schema changes from `database-migrations`.

## Step 1 — Context Card (+ delivery facts)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then collect, read-only (`references/detection.md`):

| Field | Where to look |
|---|---|
| Layout | `.agents/stack.json`, top-level folders: BE, FE, mobile, shared packages |
| Past plans | `.superpowers/work-items/*/v*/implementation-plan.md` and `phases/`, `docs/features/**` — which ones were delivered without rework |
| Checks | Analyzer, linter, type checker, test commands per branch with cwd; CI jobs |
| Readiness tools | Migration runner, seed scripts, mock servers, feature flags, test accounts |
| Change size | Typical PR size (`git log --shortstat`), files per commit |
| Sibling skills | `clean-architecture`, `unit-testing`, `database-migrations`, `git-workflow`, `api-contract-design`, `change-impact-analysis` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule IP1–IP9: adopted, adapted, or "not adopted" with a reason. IP3 (paths from clean-architecture), IP4 (a real check per task) and IP8 (out-of-workspace work is a handoff) are never "not adopted".

## Step 3 — Propose

- Order inside one behavior for this repository, with one past feature re-cut as an example.
- Task shape and the check command for each kind of task (per branch).
- PHASE-00 items this workspace needs, each `[EXECUTE]` or `[INFO_NOTE]`.
- Definition of Done per phase (per branch).
- Task-size guidance taken from the repository's history, not a number from the generator.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Order inside one behavior | The order seen in delivered plans and PRs |
| Q2 | Check command per kind of task | The commands found in CI and scripts |
| Q3 | PHASE-00 items | Those the past plans needed |
| Q4 | Definition of Done per phase | Checks green, tests for the agreed pass/fail data, migration verified, docs updated where required |

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Layout per `~/.claude/skill-factory/core/layouts.md`.

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` (router) | `templates/SKILL.md.tmpl` | **Mandatory** | What this skill adds to planning, on one screen |
| `references/01-phase-order.md` | `shared/01-phase-order.md` | `templates/01-phase-order.md.tmpl` | **Mandatory** | Order inside a behavior across branches |
| `references/02-task-shape-and-checks.md` | `be/02-…`, `fe/02-…` | `templates/02-task-shape-and-checks.md.tmpl` | **Mandatory** | Each task has a scope and a check that proves it |
| `references/03-phase-00-readiness.md` | `shared/03-phase-00-readiness.md` | `templates/03-phase-00-readiness.md.tmpl` | **Mandatory** | The Code Writer never stalls mid-phase |
| `references/04-definition-of-done.md` | `be/04-…`, `fe/04-…` | `templates/04-definition-of-done.md.tmpl` | **Mandatory** | Writer and Reviewer share one finish line |

Writing rules: real paths, commands with cwd and tool names; every rule with its reason; replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Implementation planning
   Plans and phases follow `.agents/skills/implementation-planning/SKILL.md` inside the Coder Nexus planning process.
   ```
2. Offer to link it from `incremental-implementation` and `code-review` (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Re-plan one or two features whose design was approved and delivered. Compare with and without the skill: phase order, task size, checks that actually run, PHASE-00 completeness, how many tasks the real delivery had to add.

## Step 8 — Description

Per the authoring guide: workspace name; situations (Gate 3, writing `implementation-plan.md` or phase files, splitting work, choosing checks, hotfix plans); the team's trigger words. Should not trigger while executing a phase.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report rules adapted or not adopted, trial results.

## Update mode

Existing `.agents/skills/implementation-planning/` or a workspace planning guide: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — IP1–IP9 with reasons
- `references/detection.md` — where layout, checks, readiness tools and past plans are found
- `templates/` — `SKILL.md.tmpl`, `01–04` (suggested shapes)
- `checklist.md` — topic checks
