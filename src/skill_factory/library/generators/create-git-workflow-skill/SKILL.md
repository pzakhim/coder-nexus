---
name: create-git-workflow-skill
description: Write a workspace's own git-workflow skill from the skill-factory knowledge base - the branch model (Git Flow with DEV/STG/PROD, GitHub Flow or trunk-based), which base each job type branches from (feature from develop, STG bug from the active release, PROD hotfix from main), branch and commit naming, merge strategy per source and target, hotfix propagation, no cherry-pick promotion, semantic versioning for applications (what is a contract, when PATCH, MINOR or MAJOR, rc tags, one source of truth) and release integrity checks - with the agent never merging to main, tagging or deploying production. Use whenever the user wants to set up, standardize or update the Git branching, commit, release or versioning rules of a workspace, or says things like "tạo skill git flow", "quy chuẩn branch", "checkout từ đâu", "khi nào tăng version", "hotfix quy trình", even if they do not say "skill". Writes .agents/skills/git-workflow/, then trial-runs it on real tasks.
argument-hint: "[preset] [repo]"
---

# Create Git Workflow Skill

Goal: produce `<workspace>/.agents/skills/git-workflow/` — the workspace's branch model, the base each job type branches from, naming, merge strategy, hotfix propagation and versioning, with its real branch names, ticket prefixes, CI and tools. The fixed core skill `git-preflight` runs the branch steps for every workspace; this generated skill supplies the workspace facts it reads and overrides its defaults.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same topic — here `git-preflight`). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — this skill owns branches, commits, merges and versions; incremental-implementation owns task order inside a phase; database-migrations decides whether a schema change breaks a contract.

## Step 1 — Context Card (+ Git setup)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect, read-only (`references/tooling-detection.md`):

| Field | Where to look |
|---|---|
| Branches | `git branch -a`: `main`/`master`, `develop`, `release/*`, `hotfix/*`, `support/*`, environment branches (`dev`, `staging`, `prod`) |
| Tags | `git tag --sort=-creatordate`: format (`v1.2.3`, `1.2.3`, `be-v…`), pre-release tags (`-rc.N`), first `1.0.0` or still `0.x` |
| Merge history | `git log --merges --first-parent <integration branch>` and squash commit shapes: squash vs merge commits per target |
| Naming | Last 50 branch names and commit subjects: ticket prefixes (`WMS-`, `DEVOPS-`), types, Conventional Commits |
| CI/CD | `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`: which branch or tag deploys where, approvals for production |
| Tools | commitlint, commitizen, husky/lefthook, semantic-release, release-please, changesets, standard-version |
| Version files | `package.json`, `pubspec.yaml`, `pyproject.toml`, `build.gradle`, `*.csproj`, sync scripts |
| Protection | Branch protection when readable (`gh api repos/<o>/<r>/branches/<b>/protection`); otherwise ask |
| Policy docs | `CONTRIBUTING.md`, `docs/*git*`, release docs, a policy file the user provides |
| Ignore | Whether `.superpowers/` or `.superpowers/work-items/` is ignored (`git check-ignore -v`) |
| Existing skill | `.agents/skills/*git*`, `*release*`, `*commit*` |

## Step 2 — Map the base rules

Read `references/base-rules.md` and the preset files under `references/presets/`. For each rule M1–M9, G1–G6, V1–V7, R1–R2: adopted, adapted, or "not adopted" with a reason. M1–M9 come from the fixed `git-preflight` skill and are never "not adopted"; M6 (never merge to main, tag or deploy production) and V4's human approval are never weakened.

## Step 3 — Propose

- **Established repository:** document the model as it is (branches, merges, tags seen in history), then list drift from the closest preset and open decisions.
- **New or unclear repository:** propose one of `gitflow-dev-stg-prod`, `github-flow`, `trunk-based` with reasons drawn from the Context Card (environments, release cadence, team size, mobile store releases).
- Show the base table, naming, merge table and version rules as they would read in the generated skill.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first. Rounds as needed:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Branch model | `gitflow-dev-stg-prod` when `develop` + `release/*` exist; `github-flow` when only `main` |
| Q2 | Integration and protected branch names | `develop`, `main`, `release/*` as found |
| Q3 | Ticket prefixes and branch types in use | From recent branches and commits |
| Q4 | Merge strategy per source → target | The preset's merge table (G4) |
| Q5 | The workspace's contracts (V1) | V1 default list minus what does not exist |
| Q6 | Still `0.x` or already `1.0.0` | From the latest tag |
| Q7 | `-rc.N` tags on each STG deploy | Yes |
| Q8 | Monorepo: one version or per component (V7) | One version |
| Q9 | Only when `.superpowers/` is ignored: un-ignore `.superpowers/work-items/` so specs are committed with the branch? | Yes; keep `.superpowers/sources/` ignored |

Nothing is written before the user confirms.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout: always **flat** (`references/01–05`); a monorepo with per-component versions adds one table per component in `05`, not branches.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The never-list and the base table on one screen |
| `references/01-branch-model.md` | `templates/01-branch-model.md.tmpl` | **Mandatory** | Which line is DEV, STG and PROD, and what is protected |
| `references/02-preflight.md` | `templates/02-preflight.md.tmpl` | **Mandatory** | Base and merge targets per job type, read by `git-preflight` |
| `references/03-naming-and-commits.md` | `templates/03-naming-and-commits.md.tmpl` | **Mandatory** | Branch and commit names drive review, changelog and versioning |
| `references/04-merge-and-propagation.md` | `templates/04-merge-and-propagation.md.tmpl` | **Mandatory** | Merge strategy, hotfix propagation, no cherry-pick promotion |
| `references/05-versioning-and-release.md` | `templates/05-versioning-and-release.md.tmpl` | **Mandatory** | When PATCH, MINOR, MAJOR; release integrity; what the user runs |

Writing rules: real branch names, prefixes and commands from Step 1; every rule with its reason; commands are prepared for the user wherever M6 applies; no secret, registry credential or internal host value (use placeholders such as `<registry>/<app>:<sha>`); replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

If the user chose to un-ignore `.superpowers/work-items/` (Q9), propose the exact `.gitignore` change and apply it only after the user confirms it.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Git workflow
   Branches, commits, merges and versions follow `.agents/skills/git-workflow/SKILL.md`. Agents never merge into `main`, tag or deploy production.
   ```
2. If commitlint or similar runs in the repo, link its config from `03` instead of restating every rule.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Plan only; never create real branches, commits or tags. Task ideas:

- A new feature ticket: which base, which name, which merge target?
- A bug reported on STG while `develop` has moved on.
- A PROD hotfix while a release is under test: which lines receive the fix, what version is proposed?
- "Release it to production": does the agent prepare commands and the R1–R2 check instead of merging and tagging?
- A change that removes an API field: is it marked breaking and proposed as MAJOR?

## Step 8 — Description

Per the authoring guide: workspace name; situations (start a task, create a branch, bug on STG/PROD, hotfix, cut a release, choose a version, write a commit message, open a PR); team trigger words. Should not trigger for code-only questions inside an existing branch.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted or not adopted, trial results.

## Update mode

Existing `.agents/skills/git-workflow/` or a workspace Git/release skill: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep branch names, prefixes, merge rules and release steps verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — M1–M9, G1–G6, V1–V7, R1–R2 with reasons
- `references/presets/` — `gitflow-dev-stg-prod.md`, `github-flow.md`, `trunk-based.md`
- `references/tooling-detection.md` — what to read and how to use the repo's own tools as checks
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `checklist.md` — topic checks
