# Preset: gitflow-dev-stg-prod

Git Flow with three environments. Fits teams that test a frozen release candidate on STG while development continues, and promote the tested artifact to PROD.

Core idea: **branches show the code's lifecycle; environments show where it runs; build once, configure at runtime, promote the same artifact.** `develop` = in development, `release/*` = being verified, `main` + tag = released.

## Lines and environments

| Environment | Git ref | Role |
|---|---|---|
| DEV | `develop` | Continuous integration of features and fixes; CI may auto-deploy |
| STG / UAT | `release/<x.y.z>` | Frozen release candidate for QA/UAT; no permanent staging branch |
| PROD | `main` + tag `v<x.y.z>` | Released history; deploy from the version tag after approval |

No `dev`, `staging` or `production` branches that mirror environments one to one.

## Branch types

| Branch | From | Merges into | Purpose |
|---|---|---|---|
| `feature/*` | `develop` | `develop` | New functionality |
| `fix/*` | the line where the bug was found | that `release/*` and/or `develop` | DEV/STG bugs; fix the line under test |
| `hotfix/*` | `main` | `main` + active `release/*` + `develop` | Urgent PROD bug |
| `release/*` | `develop` | `main` | Frozen candidate for STG/UAT |
| `refactor/*`, `perf/*`, `chore/*` | `develop` | `develop` | No business behavior change / performance / tooling |
| `spike/*` | `develop` | usually not merged | Short research |
| `support/*` | a release tag | — | Only when several versions are maintained long term |

## Merge strategy

| Source → target | Strategy |
|---|---|
| `feature/*` → `develop` | Squash: one ticket, one logical commit |
| `fix/*` → `release/*` | Squash |
| `release/*` → `main` | Merge commit (keep release ancestry) |
| `hotfix/*` → `main` | Merge commit (audit trail) |
| hotfix → active `release/*`, `develop` | PR from the hotfix branch or a controlled backport; never merge all of `main` into a release to get one fix |
| Personal branch update | Rebase on its base before the PR, if unshared |
| DEV → STG → PROD | Promote the release/artifact; no cherry-pick |

## Release flow

Features merge into `develop` continuously. To prepare a version, cut `release/x.y.z` from `develop` and deploy it to STG; `develop` keeps moving. STG bugs: `fix/*` from the release, merged back into the release for QA and into `develop`. When QA/UAT passes the **user** merges the release into `main`, tags `vx.y.z` and promotes the tested artifact (R1–R2 first).

## Hotfix while a release is under test

`main` @ `v1.7.3` runs PROD, `release/1.8.0` is on STG, `develop` has moved on. `hotfix/<TICKET>-…` from `main`, fixed, merged into `main` by the user as `v1.7.4`, then the same change goes to `release/1.8.0` and `develop`.

## Checklist per moment

| Moment | Required |
|---|---|
| Feature PR | Right ticket, branch name, tests and review pass, squash into `develop` |
| Cut release | Scope agreed, `release/x.y.z` from `develop`, build artifact, deploy STG |
| STG fix | Branch from the release, QA again, fix merged back into `develop` |
| PROD release (user) | STG passed, R1–R2, merge release → `main`, tag, approval, promote the tested artifact |
| PROD hotfix (user merges) | From `main`, tested, merged into `main`, patch tag, propagated to the active release and `develop` |
| After release | Delete the release branch when done; check `develop` has every fix |

## Anti-patterns

- `dev`/`staging`/`prod` branches with features cherry-picked between them.
- Building one image for STG and another for PROD from the same source.
- Squashing a whole release into `main`.
- A hotfix merged into `main` only.
- Person names in branch names.
- Several long-lived release branches without a support/backport policy.
