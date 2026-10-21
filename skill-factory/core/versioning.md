# Versioning generators

Every generator folder has `VERSION` (semver) and `CHANGELOG.md`. Workspaces are synced from the CHANGELOG, so **a change without an entry cannot reach any workspace**.

## When to bump

| Bump | Change | Examples |
|---|---|---|
| **patch** `x.y.Z` | Wording, typos, clearer examples; no rule meaning changes | Rephrase a GEN comment |
| **minor** `x.Y.0` | New rule, new section, new optional file, new preset | Add B14, add `stacks/go.md`, new smell row in 04 |
| **major** `X.0.0` | Layout change, renamed/removed files, a rule reversed | Rename `be/08-runtime.md`, drop the flat layout |

## Entry format

```markdown
## 1.3.0 — 2026-11-02

- Added: B14 logging context rule → `be/08-runtime.md` "Logging" section.
- Changed: 04 smell table gains "god router → <topic>_router.py".

**Affects:** be/08-runtime.md, be/04-long-files-splitting.md (generated sections).
**Migration:** add the "Logging" section to be/08 with the workspace's real logger; add the smell row to be/04 with real paths. Non-breaking.
```

Rules:
- **Affects** names generated output files (paths inside the workspace skill), not template file names.
- **Migration** is written for an agent: what to add, change, rename or delete in a workspace, and which workspace facts to look up first.
- Major versions also list link changes (renamed files) so the sync can apply P3 (inbound links).
- Date each entry. Never rewrite an entry after it was synced to a workspace; add a new one.
