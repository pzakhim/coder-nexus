# Changelog — create-api-contract-design-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `~/.claude/skill-factory/core/sync-protocol.md`). Bump rules: `~/.claude/skill-factory/core/versioning.md`.

## Unreleased

- Changed: AP8 tightened — idempotency key from the client's intent, claimed atomically, changed payload under the same key rejected, defined in-flight duplicate answer, timeout treated as unknown outcome, retention ≥ longest retry path → `references/01-conventions.md` (`shared/01-…`) "Safe mutations" table, `05-consuming-and-mocking.md` retries line. (minor)
- Changed: AP6 tightened — prefer adding over modifying, Hyrum's Law (observable behavior counts), One-Version Rule → `04-compatibility-and-versioning.md`. (minor)
- Changed: AP3 tightened — one error envelope definition referenced by every endpoint → `01` "Errors". (minor)
- Changed: generated `SKILL.md` "Always" list gains the envelope, idempotency and prefer-adding bullets. (minor)
- Added: generator `references/sources.md`, idempotency detection rows, checklist items, sharper idempotency trial task. (patch)

**Affects:** `SKILL.md`, `references/01-conventions.md` (`shared/01-…`), `references/04-compatibility-and-versioning.md` (`shared/04-…`), `references/05-consuming-and-mocking.md` (`fe/05-…`).
**Migration:** look up retried mutations, the idempotency store and its unique constraint, the error schema location and how many API versions are live. Add the "Safe mutations" table and the envelope-reference line to 01, the prefer-adding / Hyrum / One-Version lines to 04, the timeout line to 05, the new "Always" bullets to `SKILL.md`. Keep the team's existing codes and envelope verbatim; non-breaking.

## 1.0.0 — 2026-10-22

First version.

- Base rules AP1–AP9 with reasons: contract first with one source of truth, naming, response and error shape, lists, auth and scopes per endpoint, compatibility, clients and mocks follow the contract, safe mutations, fixture is not live.
- Detection of contract files, routes, models, errors, pagination, auth, versioning, clients, mocks and consumers per stack.
- Mandatory: `SKILL.md`, conventions, pagination and filtering, auth and scopes, compatibility and versioning. Suggested: consuming and mocking (mandatory with a client).
- Layout: flat or branched (`shared/` + `be/` + `fe/`).
- Output path: `<workspace>/.agents/skills/api-contract-design/`.

**Affects:** all generated files.
**Migration:** existing API guides → run the generator to **adopt** (keeps error codes, envelope and versioning).
