---
name: git-preflight
description: Puts every work item on the right Git branch before code is written - a read-only check when the task starts, then after Gate 1 the branch is created from the base its job type needs (feature from develop, STG bug from the active release, PROD bug as a hotfix from main), the uncommitted spec moves with it, baseline facts are re-checked and the branch decision is recorded as a D-NN. Never merges to main, tags or deploys production. Used by Spec Writer, Planning, Code Writer and Code Reviewer.
---

# Git Preflight

Answer one question before any code is written: **is this work item on its own branch, cut from the base its job type needs?** A workspace skill `.agents/skills/git-workflow/` (from `skill-factory get git-workflow`) overrides the defaults below: its branch model, base table, naming, merge strategy and versioning win. Without it, use these defaults and ask the user where a default does not fit.

## 1. Rules (every workspace)

| # | Rule | Why |
|---|---|---|
| M1 | Before the item's branch exists, write only work-item documents under `.superpowers/work-items/` and commit nothing. Never edit code on another branch. | Code written on the wrong base has to be moved by hand. |
| M2 | Never work directly on a long-lived or protected branch (`main`, `develop`, `release/*`, `support/*`). | Those lines are shared; direct commits bypass review. |
| M3 | One branch per parent feature / work-item ticket (`<type>/<PARENT-TICKET>-<short-description>`). Do not create ad-hoc sub-branches per sub-task unless explicitly requested by the user. | Reviews, reverts and release scope stay cohesive for the feature. |
| M4 | Never discard or overwrite the user's uncommitted changes. Stash or commit only after the user chooses. | Lost local work cannot be recovered. |
| M5 | Never force-push a shared branch. Rebase only a personal branch nobody else has pulled. | Rewritten shared history breaks everyone else's clone. |
| M6 | **Never put code on production:** no merge into `main`, no tag, no production deploy, even when asked. Prepare the exact commands and checklist; the user runs them. Merging into `develop` or `release/*` and deleting remote branches need the user's explicit approval. | Production releases stay a human decision. |
| M7 | Never commit a secret. | Git history is copied everywhere and is hard to clean. |
| M8 | Record the branch decision as a `D-NN` in `codebase-notes.md` (template in §4). | Planning, Code Writer and Reviewer need the same base and merge targets. |
| M9 | After switching, re-check the "Verified Baseline Facts" when the base differs from the ref the spec was scanned on. | A bug on STG lives in `release/x.y.z`, which may differ from `develop`. |
| M10 | **Verified Phase / Sub-Ticket Commit Checkpoints Only (no arbitrary WIP commits):** Never commit mid-phase (`wip`, `update`, `temp`). Create a commit only after a Huly sub-ticket or an approved `PHASE-NN` slice passes its verification gates (`PASS`) and phase acceptance/review, with explicit sub-ticket/phase traceability in the commit subject. | Every commit on the feature branch is a verified, auditable unit of delivery. |

## 2. Step A — quick check when the task starts (read-only)

Run in the workspace root before the 1A source intake:

```sh
git fetch origin --prune
git status --short --branch
git branch -a --list "*<TICKET>*"
git branch -r --list "origin/release/*"
git describe --tags --abbrev=0 origin/main
```

- Uncommitted changes that are not this item's documents → ask the user (1 question, `(Recommended)` first): commit them on the current branch, stash them, or stop. Never decide alone (M4).
- Record the current branch and `HEAD` SHA: the spec is scanned on that ref. Put it in `codebase-notes.md` → `## 3. Verified Baseline Facts` as `Scanned on: <ref> @ <sha>`.
- An existing branch for the ticket is noted for Step C; do not switch yet.

The job type and, for a bug, **where it was found (DEV / STG / PROD)** are ordinary `Q-NN` questions in the spec loop; propose the answer from the ticket's labels or environment field.

## 3. Steps C–F — after Gate 1 is approved

**C. Decide the branch.**
- Already on a non-protected branch named for the ticket (or the user says it is the branch): check its base and age.
  ```sh
  git merge-base --is-ancestor origin/<base> HEAD && echo based-on-base
  git rev-list --count HEAD..origin/<base>
  ```
  Wrong base → warn, explain what it would carry (for example `develop`-only commits reaching STG) and offer to recreate it. The user decides; do not block. Behind its base → offer a rebase (personal branch only) or a merge.
- A branch for the ticket already exists locally or on `origin` → offer to switch to it instead of creating a new one.
- Otherwise pick the base from the table (workspace `git-workflow` skill first):

| Job type | Base | Merges into (by the user / PR) |
|---|---|---|
| Feature, refactor, perf, chore | `origin/develop` | `develop` |
| Bug found on DEV | `origin/develop` | `develop` |
| Bug found on STG | `origin/release/<x.y.z>` (ask which when several; none active → treat as DEV) | that `release/*`, then `develop` |
| Bug found on PROD | `origin/main` (latest tag) as `hotfix/*` | `main`, the active `release/*`, `develop` |
| Spike | `origin/develop` | usually not merged |
| Verification / docs only | ask whether a branch is needed | — |

No `develop` in the repository → the default branch is the base for everything except PROD hotfixes, which the workspace skill must define.

**D. Create it.** Propose `<type>/<TICKET>-<short-description>` (lowercase, hyphens, no person names; without a ticket ID the user names it freely). The user confirms or edits the name. Then:

```sh
git switch -c <branch> origin/<base>
```

Uncommitted documents under `.superpowers/work-items/` move with the switch. If Git refuses because the target already has a file at the same path, report it to the user; never force.

**E. Re-check facts (M9).** When `<base>` differs from the scanned ref:

```sh
git diff --stat <scanned-sha> origin/<base> -- <paths cited in codebase-notes.md>
```

Update the facts that changed. If a change affects a requirement, reopen it as a `Q-NN` and present Gate 1 again.

**F. Commit the spec and record.** Add the `D-NN` (§4), then commit the work-item documents as the branch's first commit, for example `docs(<TICKET>): add requirements`. If `.superpowers/` is ignored (`git check-ignore -q .superpowers/work-items/x`), ask once whether to un-ignore only `.superpowers/work-items/` (recommended; keep `.superpowers/sources/` ignored); if the user keeps it ignored, skip this commit and say so in the `D-NN`. Do not push; the branch is pushed when the PR is opened.

Return `BRANCH_READY` with the `D-NN`, or `BLOCKED` with the decision the user still has to make.

## 4. Branch decision record

```text
D-NN Branch: fix/ABC-142-<short-description>
     Base: origin/release/1.8.0 @ <sha>
     Spec scanned on: origin/develop @ <sha> (re-checked, <n> cited paths changed)
     Merge to: release/1.8.0, then develop
     Source: bug found on STG (Q-NN → D-NN)
     Spec committed: yes | no (.superpowers ignored by user choice)
```

## 5. Later roles

- **Planning:** scan code on the item branch; copy branch, base and merge targets into `implementation-plan.md`; a PROD hotfix gets explicit tasks to bring the fix into the active `release/*` and `develop`.
- **Code Writer:** before each phase, `git branch --show-current` must match the `D-NN` branch; commit only at verified sub-ticket / `PHASE-NN` checkpoints (M10) using explicit traceability (`<type>(<SUB-TICKET>): <summary> [parent: <PARENT-TICKET>, PHASE-NN]`, `<type>(<PARENT-TICKET>): [PHASE-NN] <summary>`, or `<type>(phase-NN): <summary>` when no ticket exists).
- **Code Reviewer:** the PR targets the `D-NN` merge target; no commit on a protected branch; a hotfix reaches every line listed; a breaking contract change is marked as such for versioning.
- **Release and production:** prepare commands and a checklist (merge, tag, propagate, promote the tested artifact) for the user to run (M6).
