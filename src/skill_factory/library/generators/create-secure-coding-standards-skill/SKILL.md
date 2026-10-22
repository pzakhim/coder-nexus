---
name: create-secure-coding-standards-skill
description: Write a workspace's own secure-coding-standards skill from the skill-factory knowledge base - how code is written safe the first time - input validation at trust boundaries, object-level authorization and data-scope isolation (tenant, environment, owner), injection and XSS prevention, secrets and sensitive data, authentication and sessions, outbound calls (SSRF), file handling, dependencies, fail-closed errors, and what to flag for security review - mapped onto the workspace's real auth model, scopes and stack, for fullstack repos with backend and frontend branches. Use whenever the user wants to set up, standardize or update secure coding rules for the coder, reviewer or security roles in a workspace, or says things like "tạo skill secure coding", "chuẩn bảo mật khi code", "phân quyền dữ liệu", "OWASP", even if they do not say "skill". Writes .agents/skills/secure-coding-standards/, then trial-runs it on real code.
argument-hint: "[stack/framework] [auth model]"
---

# Create Secure Coding Standards Skill

Goal: produce `<workspace>/.agents/skills/secure-coding-standards/` — the rules the Code Writer follows **while writing** so the code is safe by default, which the Code Reviewer grades against and the Security role reviews deeper. Built from generic secure-coding rules plus the workspace's real trust boundaries, authorization model, data scopes and stack.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — this skill is how to write it safe; clean-architecture decides *where* guards live; bug-hunt (dimension 5) and the future `security-review` find what slipped through.

## Step 1 — Context Card (+ security model)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Read `references/deriving-the-model.md` and collect:

| Field | Where to look |
|---|---|
| Authentication | Login flow, identity provider (OAuth/OIDC/MSAL…), session/token storage |
| Authorization model | Roles, capabilities/permissions, where guards live, "UI hiding is not authorization" rules (`CLAUDE.md`, `AGENTS.md`, RBAC docs) |
| Data scopes | Tenant / environment / owner / release scopes and how they reach queries and caches |
| Trust boundaries | Public endpoints, webhooks, workers, file uploads, external providers, browser → API |
| Secrets | Settings object, secret store, encryption at rest, env files and what is git-ignored |
| Existing security code | Validation layer, guards, network allow-lists (e.g. an SSRF guard), crypto helpers |
| Gates | Security linters (bandit, eslint-plugin-security, semgrep), dependency audit, AST tests |
| Past security fixes | `git log --grep='security\|auth\|permission\|xss\|inject'` |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/risks-by-stack.md`. For each rule SC1–SC14: enforced by a gate (cite it), adopted, adapted to the workspace model, or "not adopted" with a reason. SC1, SC2, SC3, SC4, SC6, SC13 are never "not adopted" (for a single-tenant app SC3 still applies to owner/user scope).

## Step 3 — Propose

- The workspace's **security model on one page**: trust boundaries, authorization model with real guard names, data scopes with how each is enforced.
- Per branch, the stack risks that apply, each with the workspace's safe pattern (real function/component names) and the unsafe pattern to avoid.
- **Review triggers:** which changes must be flagged for the reviewer/security role (auth code, guards, scopes, migrations touching sensitive data, new dependencies, file/URL handling).

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) security model (boundaries, authz, scopes), (2) safe patterns per branch, (3) secrets and logging policy, (4) review triggers and severities.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06`; branched: `shared/01–03, 05, 06`, `be/04`, `fe/04`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The non-negotiables and the security model on one screen |
| `references/01-trust-boundaries-and-input.md` | `shared/01-…` | `templates/shared/01-trust-boundaries-and-input.md.tmpl` | **Mandatory** | Everything starts with knowing where untrusted data enters |
| `references/02-authorization-and-data-scope.md` | `shared/02-…` | `templates/shared/02-authorization-and-data-scope.md.tmpl` | **Mandatory** | Broken access control and scope leaks are the costliest bugs |
| `references/03-secrets-and-sensitive-data.md` | `shared/03-…` | `templates/shared/03-secrets-and-sensitive-data.md.tmpl` | **Mandatory** | Leaked secrets and PII cannot be un-leaked |
| `references/04-stack-risks.md` | `be/04-…`, `fe/04-…` | `templates/branch/04-stack-risks.md.tmpl` | **Mandatory** | Injection, XSS, SSRF, uploads — safe vs unsafe pattern in this stack |
| `references/05-dependencies.md` | `shared/05-…` | `templates/shared/05-dependencies.md.tmpl` | Suggested | Supply-chain rules; may merge into 06 |
| `references/06-review-triggers.md` | `shared/06-…` | `templates/shared/06-review-triggers.md.tmpl` | Suggested | What must be flagged for review; may merge into `SKILL.md` |

Writing rules: keep each template's purpose, give every rule its reason, real guard/helper names and paths, safe pattern next to the unsafe one, rules enforced by a gate cite it, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end. Never paste real secrets or tokens as examples.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Secure coding
   Code that handles input, authorization, data scopes, secrets or external calls follows `.agents/skills/secure-coding-standards/SKILL.md`.
   ```
2. Offer to link it from the coder, reviewer and (when it exists) security role files (P3).
3. If `bug-hunt` exists, offer to link its dimension 5 to this skill's model.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Add a mutating endpoint / server action for a real resource — are validation, object-level authorization and scope filters planned?
- Add a feature that calls a user-supplied URL or accepts a file upload.
- Render user-provided rich text in the frontend.
- A change that logs request data — are secrets/PII kept out?

Compare: guards and scopes named correctly, safe patterns used, no secrets in examples, review triggers flagged.

## Step 8 — Description

Per the authoring guide: workspace name; situations (new endpoint, permission check, tenant/environment data, file upload, external URL, rendering user content, logging, new dependency); team trigger words.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/secure-coding-standards/` (or security sections in other skills): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep the workspace's RBAC contract and scope matrix verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — SC1–SC14 with reasons
- `references/risks-by-stack.md` — safe vs unsafe patterns per stack
- `references/deriving-the-model.md` — how to derive trust boundaries, authz model and scopes from a workspace
- `templates/` — `SKILL.md.tmpl`, `shared/01–03, 05, 06`, `branch/04` (suggested shapes)
- `checklist.md` — topic checks
