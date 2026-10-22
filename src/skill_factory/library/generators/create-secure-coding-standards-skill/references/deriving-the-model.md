# Deriving the workspace's security model

Write the model from what the workspace already decided; never invent a new authorization scheme.

## 1. Trust boundaries

List every place untrusted data enters, with its path:

| Boundary | Examples |
|---|---|
| HTTP API | Routers/route handlers/server actions; webhooks |
| Browser | Forms, URL params, local storage, postMessage |
| Background | Queue messages, scheduled jobs, workers |
| Files | Uploads, imports, parsed documents (PDF, DOCX, CSV) |
| External providers | ERP, LLM, payment, identity provider responses |

## 2. Authorization model

- Roles and their capabilities (copy the workspace's RBAC contract verbatim if it exists).
- Where guards live (e.g. capability guards called in use cases) and the forbidden pattern (e.g. role-string checks in routers or UI).
- Environment rules (e.g. production mutations admin-only).

## 3. Data scopes

For each scope (tenant, environment, owner, release/draft state):

| Scope | Carried by | Enforced in | Leak looks like |
|---|---|---|---|
| e.g. tenant | request context → use case → repository filter | repository queries, cache keys | query without `tenant_id` filter |

## 4. Secrets and sensitive data

Settings object and secret store; what is encrypted at rest and with which helper; which env files are git-ignored; what counts as personal data here.

## 5. Existing protections

Validation layer, guards, network allow-list/SSRF helper, sanitiser, crypto helpers, security linters and dependency audit — cite them so new code reuses them.

## Sources

`CLAUDE.md`, `AGENTS.md`, RBAC/architecture docs, the clean-architecture skill, auth/guard modules, past security fixes in git log. When the model is unclear, ask; do not guess.
