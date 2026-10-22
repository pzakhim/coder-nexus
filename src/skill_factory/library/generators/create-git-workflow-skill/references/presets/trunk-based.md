# Preset: trunk-based

Short-lived branches merged into the trunk within one to three days; unfinished work hides behind feature flags.

| Item | Rule |
|---|---|
| Lines | `main` (trunk, always deployable) |
| Base for every job type | `origin/main` |
| Branch life | One to three days; larger work is split or flagged |
| Merge | Squash or rebase-merge into `main` after review and green CI |
| Release branches | Only when a version must be stabilised while `main` moves on (`release/x.y`), fixes land on `main` first and are backported |
| Hotfix | Fix on `main`, then backport to the release line if one exists |
| Versioning | V1–V7 apply; tags on `main` (or the release line) |
| R1–R2 | Apply only when a release branch is used |

Feature flags are part of the contract surface when other teams or clients toggle them (V1).
