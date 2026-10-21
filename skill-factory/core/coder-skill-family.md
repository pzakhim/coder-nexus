# The Code Writer skill family

Applies to **manual workspaces** only. Workspaces synced by Coder Nexus already get these skills from the extension (`.agents/plugins/coder-nexus/skills/`) and are out of scope (see [workflow.md](workflow.md) Step 0).

Rules shared by every coder-skill generator. Each generated skill states its own row of this table and links to the siblings that exist in the workspace.

## Ownership

| Skill (`.agents/skills/<name>/`) | Answers | When the Code Writer uses it | Wins on conflict over |
|---|---|---|---|
| `incremental-implementation` | How to execute an approved phase: order, scope, checkpoints, handoff | Start and end of every phase, between tasks | — (process; it calls the others) |
| `clean-architecture` | Where code goes, who may import whom | Before creating files/folders | clean-code, unit-test, simplification |
| `clean-code` | How to write each line/function | While coding | simplification |
| `unit-test` | How to prove behavior | While coding (TDD when the plan asks) | simplification |
| `code-simplification` | How to reduce the diff without changing behavior | After checks pass, on the diff only | — |
| `bug-hunt` | How to find real defects in a diff | Self-check at phase end; review | — |

Workspace decisions (`D-NN` or equivalent) and the approved plan override every skill for the phase they cover.

## Linking

- Refer to siblings by path: `.agents/skills/<name>/SKILL.md`. If a sibling does not exist yet, write "not set up in this workspace" instead of a dead link, and add a CHANGELOG-free note in the generated skill's custom block only if the user wants one.
- Fullstack: link the branch file when it exists (e.g. `.agents/skills/clean-architecture/references/be/05-dependency-rules.md`).
- Coder Nexus generic skills (`plugins/core/skills/*`) are base inputs for generators, never runtime links from a workspace skill.

## Shared vocabulary

| Term | Meaning |
|---|---|
| Phase | One approved, independently verifiable slice of a plan |
| Task | One ordered step inside a phase, with its own file scope and check |
| Gate | A user approval (requirements, design, plan…) — agents never approve for the user |
| Evidence | Exact command, revision, target and result |
| `PASS` / `FAIL` | A check ran and passed / failed |
| `NOT_RUN` / `BLOCKED` / `UNVERIFIED` | Not a pass. Must be reported as such |

Generated skills keep the workspace's own vocabulary when it already has one (P1), and map it to this table.

## Base content vs workspace content

| Lives in the generator (same for every workspace) | Lives in the generated skill (workspace facts) |
|---|---|
| Principles, loops, rule catalogs, stop criteria, anti-patterns | Real paths, file formats, commands, tool names, thresholds, vocabulary, sibling links, known debt |
