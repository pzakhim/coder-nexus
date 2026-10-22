# Changelog — create-api-contract-design-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules AP1–AP9 with reasons: contract first with one source of truth, naming, response and error shape, lists, auth and scopes per endpoint, compatibility, clients and mocks follow the contract, safe mutations, fixture is not live.
- Detection of contract files, routes, models, errors, pagination, auth, versioning, clients, mocks and consumers per stack.
- Mandatory: `SKILL.md`, conventions, pagination and filtering, auth and scopes, compatibility and versioning. Suggested: consuming and mocking (mandatory with a client).
- Layout: flat or branched (`shared/` + `be/` + `fe/`).
- Output path: `<workspace>/.agents/skills/api-contract-design/`.

**Affects:** all generated files.
**Migration:** existing API guides → run the generator to **adopt** (keeps error codes, envelope and versioning).
