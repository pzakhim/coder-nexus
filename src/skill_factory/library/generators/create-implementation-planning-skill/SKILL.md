---
name: create-implementation-planning-skill
description: "Generate a workspace's `implementation-planning` skill from the skill-factory knowledge base — defining vertical behavior layer order, single-writer task shape, repository-derived XS–XL sizing, targeted PASS/FAIL check commands with cwd, PHASE-00 readiness items, Definition of Done, parent-ticket branch and sub-ticket/phase commit checkpoints (IP1–IP17), and BLOCKER/MAJOR/MINOR plan review rules. Writes .agents/skills/implementation-planning/ and trial-runs it on real approved designs."
argument-hint: "[target_dir] [check_runner]"
---

# Create Implementation Planning Skill

Goal: produce `<workspace>/.agents/skills/implementation-planning/` — how Planning turns an approved design into vertical behavior phases and ordered tasks tailored to this repository: layer order inside one behavior, task shape and targeted checks, `PHASE-00` readiness items, parent-ticket branch and verified commit checkpoints, and the Definition of Done. It operates inside the fixed `implementation-planning` process (vertical behavior phases, `PHASE-00`, `AC-NN` coverage, single `code_writer` executing tasks sequentially, `validate_plan_slices`).

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership: [../../core/planning-skill-family.md](../../core/planning-skill-family.md) — file paths come from `clean-architecture`, test patterns from `unit-testing`, branch and commit checkpoints from `git-workflow` / `git-preflight`, and schema migrations from `database-migrations`.

## Step 1 — Context Card (+ Delivery Facts)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project scan ([../../core/existing-project.md](../../core/existing-project.md)). Collect read-only workspace facts ([references/detection.md](references/detection.md)):

| Field | Where to Look |
|---|---|
| **Layout** | `.agents/stack.json`, top-level module/package directories, workspace manifests |
| **Past Plans** | `.superpowers/work-items/*/v*/implementation-plan.md`, `phases/*.md`, `docs/features/**`, review reports |
| **Checks** | Analyzer, linter, type-checker, and targeted test commands with `cwd`; CI workflow jobs |
| **Readiness Tooling** | Migration runner, seed scripts, mock servers, feature flags, test accounts per role |
| **Change Size & Commits** | `git log --shortstat -50`, files per reviewed commit (for `XS`–`XL`), parent-ticket branch names, and sub-ticket / `PHASE-NN` commit checkpoints |
| **Spec Values & Gaps** | Item-wide constants in approved specs (for `Global constraints`) and uncovered inputs from past reviews/bugs (for `Review focus`) |
| **Sibling Skills** | `clean-architecture`, `unit-testing`, `database-migrations`, `git-workflow`, `api-contract-design`, `change-impact-analysis` |

## Step 2 — Enforce Base Rules (`IP1`–`IP17`)

Read [references/base-rules.md](references/base-rules.md). All rules **`IP1`–`IP17`** are **mandatory compliance** across every generated `implementation-planning` skill and must be instantiated with the workspace's real module paths, check commands, `PHASE-00` items, and `git-workflow` branch/commit checkpoint conventions (`G2`, `G3`, `M3`, `M10`).

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Present a concise proposal (recommendation first, `AskUserQuestion`, ≤ 4 questions per round):

| # | Question | Default Proposal |
|---|---|---|
| Q1 | **Layer order inside one vertical behavior (`IP1`, `IP13`)** | Layer sequence observed in delivered plans and clean PRs, with one past feature re-sliced as an example |
| Q2 | **Task sizing (`XS`–`XL`) & targeted check commands (`IP4`, `IP12`)** | Repository-derived `XS`–`XL` table, split triggers, and exact check commands with `cwd` per task kind |
| Q3 | **`PHASE-00` readiness items & external handoffs (`IP5`, `IP8`)** | Readiness items (`[EXECUTE]` / `[INFO_NOTE]`) and external handoffs needed by this workspace |
| Q4 | **Definition of Done & phase commit checkpoints (`IP6`, `IP7`, `IP17`)** | All task/analyzer checks `PASS`, in-phase tests & docs, parent-ticket branch naming, and sub-ticket / `PHASE-NN` commit format |

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03-*.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md) and [../../core/layouts.md](../../core/layouts.md). Generate the cohesive 3-reference skill structure:

| Output File | Template | Kind | Purpose |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | Concise routing table (< 105 lines), `IP1`–`IP17` rules summary, sibling contracts, and `PASS`/`FAIL` + `BLOCKER`/`MAJOR`/`MINOR` gates |
| `references/01-phase-order-and-slicing-strategy.md` | [templates/references/01-phase-order-and-slicing-strategy.md.tmpl](templates/references/01-phase-order-and-slicing-strategy.md.tmpl) | **Mandatory** | `IP1`, `IP7`, `IP9`–`IP11`, `IP13`–`IP15`, `IP17` — Layer order inside a vertical slice, `Global constraints` & `Review focus`, high-risk first, prefactor, expand → migrate → contract, tests/docs in-phase, parent-ticket branch & sub-ticket/phase commit checkpoints |
| `references/02-task-shape-sizing-and-checks.md` | [templates/references/02-task-shape-sizing-and-checks.md.tmpl](templates/references/02-task-shape-sizing-and-checks.md.tmpl) | **Mandatory** | `IP2`–`IP4`, `IP12`, `IP16` — Single-`code_writer` ordered task shape, architecture-aligned paths, targeted check commands with `cwd`, `XS`–`XL` sizing & split triggers, signatures-not-bodies |
| `references/03-phase-00-readiness-and-dod.md` | [templates/references/03-phase-00-readiness-and-dod.md.tmpl](templates/references/03-phase-00-readiness-and-dod.md.tmpl) | **Mandatory** | `IP5`, `IP6`, `IP8` — `PHASE-00` `[EXECUTE]` / `[INFO_NOTE]` items, out-of-workspace handoffs/`BLOCKED`, Definition of Done per phase, `BLOCKER`/`MAJOR`/`MINOR` review rubric, `PASS`/`FAIL` CLI gates |

Writing rules: real workspace paths, exact commands with `cwd`, replace every `{{…}}`, remove every `<!-- GEN … -->`, preserve `<!-- {{profile_references}} -->` and `<!-- custom:start/end -->`.

## Step 6 — Wire, Step 7 — Trial Run & Steps 8–9 — Verify & Record

1. **Wire**: Add a pointer in `AGENTS.md` / `CLAUDE.md` to `.agents/skills/implementation-planning/SKILL.md` and link sibling skills (`incremental-implementation`, `code-review`, `git-workflow`).
2. **Trial Run**: Follow [../../core/trial-run.md](../../core/trial-run.md) — re-plan an approved design and compare phase ordering, task sizing, runnable check commands, `PHASE-00` completeness, commit checkpoint mapping, and `Review focus` coverage.
3. **Verify & Record**: Run [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), record provenance ([../../core/provenance.md](../../core/provenance.md)), and follow [../../core/sync-protocol.md](../../core/sync-protocol.md) for updates or [../../core/versioning.md](../../core/versioning.md) when evolving this generator.
