# Base Rules — Git Workflow (`M1`–`M10`, `G1`–`G6`, `V1`–`V7`, `R1`–`R2`)

All rules below are **mandatory compliance** across every generated `git-workflow` skill (adapted to the confirmed preset `gitflow-dev-stg-prod`, `github-flow`, or `trunk-based`; never dropped as `"not adopted"`).

## 1. `M` — Mandatory Safety & Checkpoint Rules (Shared with `git-preflight`)

| ID | Rule | Why | Target Reference |
|---|---|---|---|
| `M1` | **Pre-Gate 1 Spec-Only Rule**: Before the work-item branch exists, write only uncommitted work-item documents under `.superpowers/work-items/`; create the branch only after Gate 1 approval. | Code written on the wrong base branch must be transplanted manually and risks contaminating shared lines. | `01` |
| `M2` | **No Direct Commits on Protected Lines**: Never commit directly on `main`, `develop`, `release/*`, or `support/*`. | Long-lived lines are shared integration/release targets and require PR review. | `SKILL.md`, `01` |
| `M3` | **One Branch per Parent Feature / Work Item Ticket**: Cut one branch per parent ticket (or confirmed user work item); do not spawn arbitrary sub-branches per sub-task unless explicitly requested by the user. | Keeps PR review, CI history, and revert scope cohesive for the feature. | `02` |
| `M4` | **Preserve User Uncommitted Work**: Never discard, reset, or overwrite pre-existing uncommitted user changes; stash or commit only after the user explicitly chooses. | Local uncommitted work cannot be recovered once wiped. | `01` |
| `M5` | **No Force-Push on Shared Branches**: Never force-push `main`, `develop`, `release/*`, or any branch another person/agent pulls; rebase only personal, unshared work branches. | Rewriting shared history breaks downstream clones and open PRs. | `SKILL.md`, `02` |
| `M6` | **Human-Only Production Merge, Tag & Deploy**: **Agents never merge into `main`/production, never create production release tags, and never trigger production deployments**, even if asked; agents prepare the exact commands and `R1`–`R2` checklist for the user. Merging into `develop` or `release/*` and deleting remote branches each require explicit user approval. | Production releases and shared branch integrations are human accountability gates. | `SKILL.md`, `03` |
| `M7` | **Zero Secrets in Git History**: Never stage or commit `.env` files, tokens, private keys, or credentials. | Git history is replicated to every clone and CI runner. | `02` |
| `M8` | **Branch Decision Record (`D-NN`)**: Record the confirmed branch name, base ref + SHA, scanned ref + SHA, and merge targets as a `D-NN` in `codebase-notes.md`. | Ensures Planner, Code Writer, and Reviewer operate on the exact same base and target branches. | `01` |
| `M9` | **Re-Verify Baseline Facts on Base Switch**: When the chosen base branch (`origin/release/x.y.z` or `origin/main`) differs from the ref where the spec was scanned, diff cited paths and re-verify baseline facts. | Code on `release/*` or `main` may differ from `develop`. | `01` |
| `M10` | **Verified Phase / Sub-Ticket Commit Checkpoints Only (No Arbitrary WIP Commits)**: Agents **never commit arbitrarily mid-phase** (`wip`, `update`, `temp`). A commit is created **only** after a Huly sub-ticket or an approved `PHASE-NN` slice has passed its verification gates (`PASS`) and phase review/acceptance (or on explicit user instruction for that verified checkpoint). | Guarantees every commit on the feature branch is a self-contained, verified, auditable unit of delivery. | `SKILL.md`, `02` |

---

## 2. `G` — Branching, Parent/Sub-Ticket Naming & Merge Strategy

| ID | Rule | Why | Target Reference |
|---|---|---|---|
| `G1` | **Lifecycle Branches vs. Runtime Environments**: Map environments to lifecycle refs (`develop` = DEV, `release/x.y.z` = STG/UAT candidate, `main` + tag `vx.y.z` = PROD in `gitflow-dev-stg-prod`; adapted per preset). Never maintain long-lived `dev` / `staging` / `prod` environment branches with cherry-picked features. | Branches represent code maturity; CI/CD pipelines deploy artifacts to environments. | `01` |
| `G2` | **Parent-Ticket Branch Naming**: Name the branch after the **Parent / Feature Ticket**: `<type>/<PARENT-TICKET>-<short-description>` (lowercase, hyphen-separated, no developer names, e.g., `feature/IMES-1200-order-workflow`, `fix/IMES-1240-tax-rounding`, `hotfix/IMES-1299-auth-timeout`). When no ticket exists, use `<type>/<short-description>` confirmed by the user. | Links the branch directly to the feature epic/ticket in Huly/tracker without personal/vague names. | `02` |
| `G3` | **Sub-Ticket & Accepted-Phase Commit Traceability**: Every commit subject follows Conventional Commits and **must** carry explicit ticket and/or accepted phase traceability:<br>• **Parent Ticket + Huly Sub-Tickets**: `<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]` (or `Refs: <PARENT-TICKET>, PHASE-NN` in footer).<br>• **Parent Ticket + Multi-Phase (no separate sub-ticket ID)**: `<type>(<PARENT-TICKET>): [PHASE-NN] <summary>`.<br>• **No Ticket ID (user-supplied requirement)**: Allowed only after completing a clearly accepted phase: `<type>(phase-NN): <summary>`.<br>• Append `!` or `BREAKING CHANGE:` footer whenever a public contract breaks (`V1`). | Prevents ad-hoc untraceable commits inside a multi-phase feature branch and feeds automated changelogs and SemVer bumps. | `02` |
| `G4` | **Squash Work Branches; Merge-Commit Releases & Hotfixes**: Squash-merge `feature/*` / `fix/*` / `refactor/*` into `develop` (or `fix/*` into `release/*`); use `--no-ff` merge commits for `release/*` → `main` and `hotfix/*` → `main`. | Compresses granular sub-ticket/phase commits into one clean feature commit on `develop` while preserving exact release ancestry on `main`. | `02` |
| `G5` | **Complete Hotfix Propagation**: Every `hotfix/*` merged into `main` must be propagated to the active `release/*` (when affected) and to `develop`. | Prevents the next release from re-introducing a fixed production regression. | `02` |
| `G6` | **No Cherry-Pick Promotion**: Never use `git cherry-pick` to promote features between environments; cherry-pick is allowed only as a documented backport with an explicit justification in the PR. | Cherry-picking duplicates commit SHAs and corrupts merge-base ancestry. | `02` |

---

## 3. `V` — Semantic Versioning (`MAJOR.MINOR.PATCH`) & `R` — Release Integrity

| ID | Rule | Why | Target Reference |
|---|---|---|---|
| `V1` | **Explicit Public Contracts**: Enumerate what constitutes a versioned contract in this workspace (HTTP/RPC/realtime APIs, event/webhook schemas, CLI flags, required environment variables, shared database schemas). | SemVer requires a well-defined public contract boundary. | `03` |
| `V2` | **Deterministic Bump Classification**: `PATCH` = bug fixes, security patches, behavior-neutral perf; `MINOR` = backward-compatible features/additive contracts; `MAJOR` = any breaking contract change (or approved business-driven major release). Highest impact wins. | Communicates upgrade risk to downstream consumers and DevOps. | `03` |
| `V3` | **`0.y.z` vs `1.0.0+` Lifecycle**: `0.y.z` for pre-production development; `1.0.0` marks the first production release with a stable contract. | Aligns with SemVer 2.0.0 initial development semantics. | `03` |
| `V4` | **Evidence-Based Version Proposal & Human Approval**: Compute the proposed bump from commits since the last tag (`feat` → MINOR, `fix`/`perf` → PATCH, `!`/`BREAKING CHANGE` → MAJOR) and present the commit list to the user; **the user decides the version**. | Keeps version numbering deterministic and human-approved. | `03` |
| `V5` | **Frozen Release Candidate & Pre-Release Tags**: `release/X.Y.Z` accepts fixes only (`fix/*`); optional `-rc.N` tags mark STG builds; DEV builds use commit SHAs without version tags. | Guarantees every tag maps to an immutable, traceable build. | `03` |
| `V6` | **Single Source of Truth (SSOT) Version Sync**: Synchronize all manifest files (`package.json`, `pyproject.toml`, `pubspec.yaml`, `bundle_manifest.json`) via the workspace's version sync script before tagging. | Eliminates version drift across package manifests. | `03` |
| `V7` | **Monorepo Versioning Policy**: Use one unified repo version (`vX.Y.Z`) by default, or explicit component-prefixed tags (`<component>-vX.Y.Z`, e.g., `api-v1.2.0`, `worker-v1.2.0`) when components release independently. | Prevents tag collisions in multi-component repositories. | `03` |
| `R1` | **Hotfix Inclusion Check Before Release**: Verify `git log release/X.Y.Z..main` is empty before merging `release/X.Y.Z` into `main` so every production hotfix is included. | Prevents a release merge from overwriting a recent production hotfix. | `03` |
| `R2` | **Tree-Identity Verification After Release Merge**: Verify `git diff release/X.Y.Z <merge-commit>` is empty on `main` so the exact STG-verified tree is what ships to production. | Proves "build/verify once, promote the exact same tree to production". | `03` |
