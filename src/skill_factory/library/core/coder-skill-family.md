# The Code Writer skill family

Factory skills live in `.agents/skills/` and are owned by the workspace. In a workspace also synced by Coder Nexus, a factory skill overrides the fixed skill of the same name or slot (see [workflow.md](workflow.md) Step 0).

Rules shared by every coder-skill generator. Each generated skill states its own row of this table and links to the siblings that exist in the workspace.

## Ownership

| Skill (`.agents/skills/<name>/`) | Answers | When the Code Writer uses it | Wins on conflict over |
|---|---|---|---|
| `incremental-implementation` | How to execute an approved phase: order, scope, checkpoints, handoff | Start and end of every phase, between tasks | — (process; it calls the others) |
| `clean-architecture` | Where code goes, who may import whom | Before creating files/folders | clean-code, unit-testing, simplification |
| `clean-code` | How to write each line/function | While coding | simplification |
| `unit-testing` | How to prove behavior | While coding (TDD when the plan asks) | simplification |
| `code-simplification` | How to reduce the diff without changing behavior | After checks pass, on the diff only | — |
| `bug-hunt` | How to find real defects in a diff | Self-check at phase end; review | — |
| `root-cause-debugging` | How to fix a known failure (red check, confirmed finding) at its root | When a check is red or a defect must be fixed | — (fix scope follows incremental-implementation) |
| `secure-coding-standards` | How to write it safe: input, authorization, data scopes, secrets, injection | While coding anything that touches input, permissions, scoped data, secrets, files or URLs | clean-code, code-simplification (never simplify a guard away) |
| `database-migrations` | How schema/data changes are designed, verified and delivered (backend) | Any table, column, index, constraint or backfill change | — (sensitive data follows secure-coding-standards) |

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
