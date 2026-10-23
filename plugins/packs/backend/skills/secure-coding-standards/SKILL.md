---
name: secure-coding-standards
description: Secure coding standards for a Backend (Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2 async, PostgreSQL) service - validate input at trust boundaries with Pydantic schemas, authorize every operation per object in the service and filter every query by data scope (tenant, owner, environment) in the repository, no f-string SQL, shell or path injection, mass assignment blocked with extra="forbid", secrets as SecretStr from settings and never in source or logs, JWT and password hashing through the workspace's auth, SSRF-safe outbound httpx calls, bounded uploads, fail closed, pip-audit for dependencies, and which changes to flag for review - each unsafe pattern next to its safe counterpart, graded on the shared severity scale. Use while the Code Writer adds or changes an endpoint, dependency, schema, repository query, background job, outbound call, file upload, auth code, settings or a new package, during the self-check before READY_FOR_REVIEW, and when the Code Reviewer checks the security axis of a backend diff, even if nobody says "security".
---

# Secure Coding Standards — Backend (FastAPI)

Goal: code that is safe the first time it is written, so review finds confirmations, not rewrites. The workspace's real auth dependency, roles, scopes and secret store come from the approved `design.md` and `codebase-notes.md`; a workspace `.agents/skills/secure-coding-standards/` overrides this skill on specifics. Neither may relax a non-negotiable. Paths such as `app/`, `tests/unit/` and `alembic/versions/` are conventions the workspace may override.

## Non-negotiables

1. Validate untrusted input at the boundary with a Pydantic schema; reject, never repair or guess (SC1). Reason: every injection and logic abuse starts with unchecked input.
2. Authorize every operation on the server, per object, deny by default; client checks only shape the UI (SC2). Reason: a direct API call skips the client.
3. Every query, cache key, file path, job and event carries its data scope explicitly; no default scope (SC3). Reason: one missing filter leaks another customer's data.
4. No SQL, shell command, template or path built from input by string joining (SC4). Reason: injection turns data into code.
5. No secret or personal data in code, commits, fixtures, URLs, logs or error bodies (SC6, SC8). Reason: a leaked secret cannot be un-leaked.
6. Fail closed: an error in validation, authorization or a dependency denies; never default or fake data (SC13). Reason: attackers aim for the error path.

Anything the design does not settle (who may see what, which scope applies) goes to Planning through `change-control`, never a guess in code.

## Rules

| # | Rule | Where |
|---|---|---|
| SC1 | Validate untrusted input at the trust boundary | [01](references/01-trust-boundaries-and-input.md) |
| SC2 | Authorize every operation on the server, per object | [02](references/02-authorization-and-data-scope.md) |
| SC3 | Isolate data scopes (single-tenant: owner/user scope still applies) | [02](references/02-authorization-and-data-scope.md) |
| SC4 | No injection (SQL, shell, path, deserialization, eval) | [04](references/04-stack-risks.md) |
| SC5 | Encode output; validate redirect targets | [04](references/04-stack-risks.md) |
| SC6 | Keep secrets secret | [03](references/03-secrets-and-sensitive-data.md) |
| SC7 | Use the workspace's authentication, never homemade | [02](references/02-authorization-and-data-scope.md) |
| SC8 | No sensitive data in logs, caches or user errors | [03](references/03-secrets-and-sensitive-data.md) |
| SC9 | Control outbound calls (allow-list, timeout, no redirects) | [04](references/04-stack-risks.md) |
| SC10 | Handle files defensively | [04](references/04-stack-risks.md) |
| SC11 | Dependencies with care | [05](references/05-dependencies.md) |
| SC12 | Vetted cryptography and secure random | [03](references/03-secrets-and-sensitive-data.md) |
| SC13 | Fail closed | [02](references/02-authorization-and-data-scope.md) |
| SC14 | Flag security-relevant changes in the handoff | [06](references/06-review-triggers.md) |

SC1, SC2, SC3, SC4, SC6 and SC13 have no exceptions.

## Security model (baseline)

| Item | Backend baseline |
|---|---|
| Authentication | The workspace's auth dependency on the router (`Depends(get_current_actor)` or its real name); tokens validated with pinned algorithms, audience, issuer, `exp` |
| Authorization | Object- and function-level checks in the service / use case with an explicit `actor`; role strings in routers are forbidden |
| Data scopes | Tenant / owner / environment filter inside every repository `select`, `update`, `delete`; listed per scope in the design |
| Secrets | `pydantic-settings` `BaseSettings` fields typed `SecretStr`, from environment or the untracked `.env` |

Where each guard lives follows `{{slot:clean-architecture}}`; this skill only says the guard must exist and how it is written safely.

## Which file to read

| Doing | Read |
|---|---|
| Adding an endpoint, schema, webhook, consumer or provider call | [01-trust-boundaries-and-input](references/01-trust-boundaries-and-input.md) |
| Permission checks, scoped queries, auth and tokens | [02-authorization-and-data-scope](references/02-authorization-and-data-scope.md) |
| Settings, logging, error handlers, hashing, random tokens | [03-secrets-and-sensitive-data](references/03-secrets-and-sensitive-data.md) |
| SQL, shell, paths, YAML/pickle, outbound URLs, uploads, CORS | [04-stack-risks](references/04-stack-risks.md) |
| Adding or upgrading a package | [05-dependencies](references/05-dependencies.md) |
| Handing off, or reviewing, a security-relevant change | [06-review-triggers](references/06-review-triggers.md) |

## Code Writer

1. Before editing, read the task's `Consumes`, the design's auth and scope decisions, and the rows of [04](references/04-stack-risks.md) that apply to the files in scope.
2. Write the guard with the code it protects, plus a test that a forbidden actor or wrong scope is refused (`{{slot:unit-testing}}`): another tenant's id → 404 (or 403 per the contract), no token → 401, missing capability → 403.
3. Self-check: run the gates in [04 § Gates](references/04-stack-risks.md#gates), walk the checklist in [06](references/06-review-triggers.md) over the diff, fix every hit inside scope, and list SC14 items in the handoff.

## Code Reviewer

Run the [06 checklist](references/06-review-triggers.md#reviewer-checklist) on the phase diff after `bug-hunt`, as the security axis of `{{slot:code-review}}`. The reviewer never edits code. Grade on [handoff-and-status §9](../work-item-contract/references/handoff-and-status.md); do not invent another scale:

| Finding | Grade |
|---|---|
| Authorization or scope bypass, injection, authentication bypass, secret in source/bundle/log, fail-open on a normal path | `BLOCKER` defect |
| Exploitable only on a realistic edge path; personal data in logs or errors; user-influenced outbound call or upload without its guard; unvalidated input that corrupts stored data | `MAJOR` defect |
| Defense-in-depth gap with no traced path (missing timeout on an internal call, verbose error without sensitive data) | `MINOR` defect |
| A non-negotiable or SC rule broken with no traced exploit (role string in a router while the service also checks, input schema without `extra="forbid"` and no server-owned field) | `P1` rule violation, rule ID first (`SC2: role check in router`) |

Every defect carries a `given → when → then` exploit scenario and `CONFIRMED` or `PLAUSIBLE`. A secret in source or a bundle is always `BLOCKER CONFIRMED`: the exposure is the failure. Verdict impact is §9's.

## Relationship with other skills

- Where guards and validation live: `{{slot:clean-architecture}}`. API error shapes and status codes: `api-contract-design`.
- Finding what slipped through: `{{slot:bug-hunt}}` (security dimension) and `{{slot:code-review}}`. Never simplify a guard away: `{{slot:code-simplification}}`, `{{slot:clean-code}}`.
- Evidence rows and `NOT_RUN`: `evidence-standard`. Release 3.2.0 has no separate security role; the Code Reviewer runs this checklist.

Sources: [references/sources.md](references/sources.md).
