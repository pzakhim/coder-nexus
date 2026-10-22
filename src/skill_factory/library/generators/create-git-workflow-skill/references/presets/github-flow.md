# Preset: github-flow

One long-lived branch. Fits teams that deploy from `main` often and have no frozen release candidate stage.

| Item | Rule |
|---|---|
| Lines | `main` only (protected); every change on a short-lived branch |
| Base for every job type | `origin/main` |
| Merge | PR into `main`; squash by default |
| Environments | `main` deploys to DEV/STG automatically; production from a tag or a manual approval step (run by the user) |
| Hotfix | Same as any fix: branch from `main`, PR, tag a PATCH |
| Versioning | V1–V7 apply; tags directly on `main`; no `-rc.N` unless a pre-release deploy exists |
| R1–R2 | Not applicable (no release branch); promote the artifact built from the tagged commit |

`git-preflight`'s bug question still matters when production runs an older tag than `main`: a production-only bug may need a branch from that tag and a `support/*` line; ask the user.
