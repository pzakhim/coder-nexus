# Base rules (generic, every workspace)

Generalised from a team Git Flow policy for DEV / STG / PROD and from Semantic Versioning 2.0.0. Each rule goes into the generated skill with the workspace's real branch names, prefixes and tools **and its reason**, or is marked "not adopted" with a reason.

## M — safety (from the fixed `git-preflight` skill; never "not adopted")

| # | Rule | Why | Goes into |
|---|---|---|---|
| M1 | Before the item branch exists, only work-item documents are written, uncommitted; the branch is created right after Gate 1. | Code written on the wrong base must be moved by hand. | 02 |
| M2 | No direct work on long-lived or protected branches. | Shared lines bypass review otherwise. | 01, SKILL |
| M3 | One branch per ticket or logical change. | Clean review, revert and release scope. | 03 |
| M4 | Never discard the user's uncommitted changes; stash or commit only on the user's choice. | Local work cannot be recovered. | 02 |
| M5 | No force-push on shared branches; rebase only personal, unshared branches. | Rewritten shared history breaks every clone. | 04, SKILL |
| M6 | **Agents never merge into the production branch, tag, or deploy production**, even when asked; they prepare commands and a checklist for the user. Merges into integration/release lines and remote branch deletion need explicit approval. | Production releases stay a human decision. | SKILL, 05 |
| M7 | No secrets in commits. | History is copied everywhere. | 03 |
| M8 | The branch decision is a `D-NN` (branch, base + SHA, merge targets, scanned ref). | Every later role works from the same base and targets. | 02 |
| M9 | Re-check baseline facts when the base differs from the scanned ref. | Release and production lines can differ from the integration line. | 02 |

## G — branch model (preset `gitflow-dev-stg-prod`; other presets adapt or replace)

| # | Rule | Why | Goes into |
|---|---|---|---|
| G1 | Base and merge targets per job type; environments map to lines (`develop` = DEV, `release/x.y.z` = STG, `main` + tag = PROD); no branch per environment. | Branches show code lifecycle, environments show where it runs. | 01, 02 |
| G2 | Branch name `<type>/<TICKET>-<short-description>`, lowercase, hyphens, no person names; `release/x.y.z`; the user confirms the name; without a ticket ID the user names it freely. | Names must tell the work, not the owner. | 03 |
| G3 | Commit subject `type(TICKET): summary` (Conventional Commits; ticket as scope); `!` or `BREAKING CHANGE:` for a contract break. | Commits feed review, changelog and the version bump. | 03 |
| G4 | Squash feature/fix work into its target; merge commits for release → main and hotfix → main. | "Squash the developer's work; preserve the release's history." | 04 |
| G5 | A PROD hotfix reaches `main`, the active `release/*` (when it contains the affected code) and `develop`. | Otherwise the next release brings the bug back. | 04 |
| G6 | No cherry-pick as promotion between environments; cherry-pick only as a deliberate backport with a reason. | Promotion by cherry-pick loses ancestry and duplicates commits. | 04 |

## V — versioning (SemVer 2.0.0 for applications)

| # | Rule | Why | Goes into |
|---|---|---|---|
| V1 | The workspace names its **contracts**: APIs used by mobile, a separate FE or third parties; events; import/export and webhook formats; required environment variables and config; a database other systems read; mobile app versions still installed. | SemVer needs a public API; an application must say what that is. | 05 |
| V2 | PATCH = fixes, security patches, behavior-neutral performance; MINOR = at least one backward-compatible feature (PATCH resets); MAJOR = any contract break. The highest impact in the release wins. A business-driven MAJOR is allowed as a recorded, approved decision. | Consumers read the number to judge upgrade risk. | 05 |
| V3 | `0.y.z` before the first production release (breaks bump MINOR); `1.0.0` is the first production release with a stable contract. | SemVer's initial development phase. | 05 |
| V4 | The bump is computed from commits (`feat` → MINOR, `fix`/`perf` → PATCH, `!`/`BREAKING CHANGE` → MAJOR, others alone → none or PATCH if released); the agent proposes it with evidence, a human approves. The reviewer flags breaking changes without `!`. | Commits are the evidence; the decision stays human. | 05 |
| V5 | The release branch name is fixed at cut; STG takes fixes only; `-rc.N` tags per STG build (optional); hotfixes bump PATCH on `main` and never break a contract; DEV builds use the SHA, no tag. | Version and tested artifact must stay traceable. | 05 |
| V6 | The tag is the single source of truth; version files are synced from it by script; mobile build numbers are monotonic CI numbers after `+`; the changelog is grouped Added / Changed / Fixed / Security and edited for humans. | Hand-edited versions in many files drift. | 05 |
| V7 | Monorepo: one version for the repo (default) or per-component tags (`be-v…`, `fe-v…`). | Release trains differ per team. | 05 |

## R — release integrity (Git Flow with artifact promotion)

| # | Rule | Why | Goes into |
|---|---|---|---|
| R1 | Before release → main, the release line contains every hotfix already on `main`. | Otherwise the merge result differs from what STG tested. | 05 |
| R2 | After the merge, `git diff <release-tip> <merge-commit>` is empty; then promote the exact tested artifact and record the release SHA in the tag message. Not empty → test again on STG. | "Build once, promote many" only holds if the code is identical. | 05 |

## Recommended (reviewer flags, does not block)

- Build once and promote the same artifact; runtime configuration, no secrets in images; flag build-time API URLs in front-end bundles.
- At most one active `release/*`; long-term versions use `support/*` with a backport policy.
- Rebase a personal branch on its base before opening the PR.
- Delete the release branch after release; check `develop` has every fix.
