# Versioning generators

Every generator folder has `VERSION` (semver) and `CHANGELOG.md`. Workspaces are synced from the CHANGELOG, so **a change without an entry cannot reach any workspace**.

The version describes **what an existing workspace has to do**, not how big the edit to the generator was.

## Decide the bump with one question

> *Does a workspace that already has this skill need to change its content?*

| Answer | Bump | Sync behaviour |
|---|---|---|
| **No** — or only wording/links/duplication, rules mean the same | **patch** `x.y.Z` | Optional; show a one-line summary, apply on request |
| **Yes, by adding or tightening** — new rule, new mandatory content, a rule made stricter or a default changed, compatibly | **minor** `x.Y.0` | Apply per workspace, with confirmation |
| **Yes, by breaking** — output files renamed/removed/merged, layout changed, a rule reversed or dropped, the mandatory set changed | **major** `X.0.0` | Migration + inbound-link update (P3), with confirmation |

## Examples

| Change | Bump | Why |
|---|---|---|
| Fix a typo, reword a GEN note, better example in a template | patch | Workspace rules unchanged |
| Improve the generator's own process (detection, questions, trial-run steps, checklist) | patch | Only affects future generations |
| Move a shared reference into `core/` | patch | Internal reorganisation |
| Add a stack preset (`stacks/go.md`) | patch | Existing workspaces of other stacks are unaffected; new workspaces use it at generation |
| Remove duplicated thresholds from a generated file and link the owner instead | patch | Same numbers, one source |
| Add a rule (B14), a smell row, or a new mandatory section | minor | Workspaces gain content |
| Change a default threshold (300 → 250 lines) | minor | Rule tightened |
| Rename `be/08-runtime.md`, drop a file, change the mandatory set | major | Workspace files and links break |
| Reverse a rule ("repositories may commit") | major | Meaning flips |

## Batch work with `Unreleased`

Do **not** bump on every edit. While working, add bullets under `## Unreleased` at the top of the CHANGELOG. Bump once, when the batch is done (a phase finished, or the user says release):

1. Take the **highest** bump any bullet needs (one minor bullet + three patch bullets → minor).
2. Rename `## Unreleased` to `## x.y.z — <date>`, write **Affects** and **Migration** for the whole batch, update `VERSION`.
3. Commit generator change + VERSION + CHANGELOG together.

Sync only applies **released** entries; `Unreleased` never reaches a workspace.

## Entry format

```markdown
## Unreleased

- Added: B14 logging context rule → be/08-runtime.md "Logging". (minor)
- Fixed: typo in 04 smell table. (patch)
```

```markdown
## 1.3.0 — 2026-11-02

- Added: B14 logging context rule → `be/08-runtime.md` "Logging" section.
- Fixed: typo in 04 smell table.

**Affects:** be/08-runtime.md (generated sections).
**Migration:** add the "Logging" section to be/08 with the workspace's real logger. Non-breaking.
```

Rules:
- Tag each `Unreleased` bullet with the bump it needs (`patch` / `minor` / `major`).
- **Affects** names generated output files (paths inside the workspace skill), not template file names. Patch-only releases may say "Affects: none (generator only)".
- **Migration** is written for an agent: what to add, change, rename or delete in a workspace, and which workspace facts to look up first.
- Major versions also list link changes (renamed files) so the sync can apply P3 (inbound links).
- Never rewrite a released entry after it was synced to a workspace; add a new one.
