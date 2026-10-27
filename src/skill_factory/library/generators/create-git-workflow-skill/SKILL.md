---
name: create-git-workflow-skill
description: "Generate a workspace's `git-workflow` skill from the skill-factory knowledge base — covering the branch model (`gitflow-dev-stg-prod`, `github-flow`, or `trunk-based`), base branch per job type, parent-ticket branch naming (`G2`), sub-ticket and accepted-phase commit checkpoint discipline (`M10`, `G3`), merge strategy (`squash` vs `--no-ff`), hotfix propagation across active lines, SemVer (`MAJOR.MINOR.PATCH`) contract versioning, release integrity checks (`R1`–`R2`), binary `PASS` / `FAIL` CLI gates, and `BLOCKER` / `MAJOR` / `MINOR` review grading."
argument-hint: "[preset] [target_dir]"
---

# Create Git Workflow Skill

Goal: produce `<workspace>/.agents/skills/git-workflow/` — the workspace's branch model, base branch per job type, parent-ticket branch naming, sub-ticket / accepted-phase commit traceability (`M10`, `G3`), merge strategy, hotfix propagation, and SemVer release rules, aligned with `shared_contracts/flags_and_statuses.md`. This workspace skill overrides the defaults of the fixed `git-preflight` skill.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership: [../../core/coder-skill-family.md](../../core/coder-skill-family.md) — `git-workflow` owns branches, commits, merges, and versions; `incremental-implementation` owns task order inside a phase; `database-migrations` and `api-contract-design` decide whether a schema or API change breaks a contract.

## Step 1 — Context Card (+ Git Setup)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and P1–P2 ([../../core/existing-project.md](../../core/existing-project.md)). Collect read-only Git facts ([references/tooling-detection.md](references/tooling-detection.md)):

| Field | Where to Look |
|---|---|
| **Branches** | `git branch -a`: `main`/`master`, `develop`, `release/*`, `hotfix/*`, `support/*` |
| **Tags** | `git tag --sort=-creatordate`: format (`v1.2.3`, `1.2.3`, `<component>-v1.2.3`), pre-release tags (`-rc.N`), `0.x` vs `1.0.0+` |
| **Merge History** | `git log --merges --first-parent <integration-branch>`: squash vs `--no-ff` merge commits per target |
| **Ticket & Commit Conventions** | Last 50 branch names and commit subjects: parent ticket prefixes (e.g. `IMES-`, `ABC-`), sub-ticket & `PHASE-NN` commit scopes, Conventional Commits |
| **CI/CD & Protection** | `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`: branch/tag deployment filters, protected branches, approval gates |
| **Tools & Version SSOT** | `commitlint`, `commitizen`, `husky`/`lefthook`/`pre-commit`, `semantic-release`, `release-please`, `changesets`, version files (`package.json`, `pubspec.yaml`, `pyproject.toml`), sync scripts |
| **Work-Item Tracking** | Whether `.superpowers/` or `.superpowers/work-items/` is ignored (`git check-ignore -v`) |

## Step 2 — Enforce Base Rules (`M1`–`M10`, `G1`–`G6`, `V1`–`V7`, `R1`–`R2`)

Read [references/base-rules.md](references/base-rules.md) and the presets under `references/presets/` ([gitflow-dev-stg-prod.md](references/presets/gitflow-dev-stg-prod.md), [github-flow.md](references/presets/github-flow.md), [trunk-based.md](references/presets/trunk-based.md)). All rules **`M1`–`M10`, `G1`–`G6`, `V1`–`V7`, `R1`–`R2`** are **mandatory compliance** (adapted to the chosen preset; never dropped as `"not adopted"`). `M6` (agents never merge into `main`/production, tag, or deploy production) and `M10`/`G3` (no arbitrary commits; every commit must bind to a verified sub-ticket or accepted `PHASE-NN`) are never weakened.

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Branch Model & Protected Lines**: `gitflow-dev-stg-prod` (when `develop` + `release/*` exist), `github-flow`, or `trunk-based`; confirm `develop`, `release/*`, `main`.
2. **Parent-Ticket Branch Naming & Sub-Ticket / Phase Commit Rule (`G2`, `G3`, `M10`)**: Confirm ticket prefix (e.g., `IMES-`), parent-ticket branch pattern (`<type>/<PARENT-TICKET>-<short-description>`), and sub-ticket / `PHASE-NN` commit format.
3. **Merge Strategy & Hotfix Propagation (`G4`–`G6`)**: Squash for work branches into `develop` / `release/*`; `--no-ff` merge commit for `release/*` → `main` and `hotfix/*` → `main`.
4. **Contracts, Versioning & `.superpowers/work-items/` Tracking (`V1`–`V7`)**: Public contracts, `0.x` vs `1.0.0+`, `-rc.N` tags, single version vs `<component>-v…`, and whether `.superpowers/work-items/` is committed with the branch.

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate the flat, cohesive 3-reference skill structure:

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | Concise routing table (< 115 lines), `M1`–`M10` never-list, base table, and binary `PASS`/`FAIL` CLI gates |
| `references/01-branch-model-and-preflight.md` | [templates/references/01-branch-model-and-preflight.md.tmpl](templates/references/01-branch-model-and-preflight.md.tmpl) | `M1`, `M2`, `M4`, `M8`, `M9`, `G1` — environment-to-branch mapping, protected lines, base & merge targets per job type, `D-NN` branch record |
| `references/02-naming-commits-and-merge-strategy.md` | [templates/references/02-naming-commits-and-merge-strategy.md.tmpl](templates/references/02-naming-commits-and-merge-strategy.md.tmpl) | `M3`, `M5`, `M7`, `M10`, `G2`–`G6` — parent-ticket branch naming, sub-ticket / accepted-phase commit traceability (`G3`, `M10`), squash vs `--no-ff` merge table, hotfix propagation, no cherry-pick promotion |
| `references/03-versioning-release-and-gates.md` | [templates/references/03-versioning-release-and-gates.md.tmpl](templates/references/03-versioning-release-and-gates.md.tmpl) | `M6`, `V1`–`V7`, `R1`–`R2` — SemVer contracts, version SSOT, user-executed release runbook, CLI `PASS`/`FAIL` gates, and `BLOCKER`/`MAJOR`/`MINOR` review rubric |

## Step 6 — Wire, Step 7 — Trial Run & Step 8–9 — Verify

1. Add a pointer in `AGENTS.md` / `CLAUDE.md` to `.agents/skills/git-workflow/SKILL.md`.
2. Run a plan-only trial ([../../core/trial-run.md](../../core/trial-run.md)): test a multi-phase feature with Huly sub-tickets, a STG bug while `develop` moved on, a PROD hotfix propagation, and a release readiness check (`R1`–`R2`).
3. Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), and record provenance ([../../core/provenance.md](../../core/provenance.md)).
