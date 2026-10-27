# Changelog — create-api-contract-design-skill

Each entry lists what changed, which generated files it affects, and how to migrate an existing workspace (see `../../core/sync-protocol.md`). Bump rules: `../../core/versioning.md`.

## 1.1.0 — 2026-10-25

- Standardized `AP1`–`AP9` as mandatory compliance (removing `"not adopted"` carve-outs and deleting `references/sources.md`).
- Made generator 100% stack-agnostic (replacing `be_dir` / `fe_dir` and branched `shared/` + `be/` + `fe/` folders with `{{target_dir}}` and flat cohesive `references/01..03.md`).
- Tightened `AP3` (single centralized error envelope referenced by every endpoint), `AP5` (authentication security schemes, RBAC, anti-IDOR `404` for out-of-scope resources, and bounded pagination `le=100` / rate limit `429`), `AP6` (additive-first, Hyrum's Law, One-Version Rule), and `AP8` (atomic `Idempotency-Key` claim, payload-mismatch rejection, in-flight duplicate policy, and timeout-as-unknown-outcome).
- Consolidated `templates/` into `templates/SKILL.md.tmpl` and 3 cohesive templates under `templates/references/` (`01-conventions-schemas-and-idempotency.md.tmpl`, `02-auth-scopes-and-compatibility.md.tmpl`, `03-snapshot-handshake-and-review.md.tmpl`) with binary `PASS` / `FAIL` CLI gates, unified `BLOCKER` / `MAJOR` / `MINOR` review grading, and `<!-- {{profile_references}} -->`.

**Affects:** `SKILL.md`, `references/01..03.md`.

## 1.0.0 — 2026-10-22

First version.

- Base rules AP1–AP9 with reasons: contract first with one source of truth, naming, response and error shape, lists, auth and scopes per endpoint, compatibility, clients and mocks follow the contract, safe mutations, fixture is not live.
- Output path: `<workspace>/.agents/skills/api-contract-design/`.
