---
name: create-secure-coding-standards-skill
description: Generate or update a workspace's secure-coding-standards skill from the stack-agnostic Skill Factory knowledge base — mapping universal security rules (SC1–SC14) for boundary input validation, authentication, object-level authorization, data-scope isolation, secrets and PII protection, cryptography, injection/transport/file safety, dependency vetting, deterministic PASS/FAIL gates, and BLOCKER/MAJOR/MINOR review grading onto the workspace's real security model.
argument-hint: "[target workspace or security model notes]"
---

# Create Secure Coding Standards Skill

Goal: produce `<workspace>/.agents/skills/secure-coding-standards/` — the security contract that Code Writer follows while authoring code and Code Reviewer grades against during review.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill in `.agents/skills/secure-coding-standards/` overrides the pack skill of the same slot). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md`.

---

## Step 1 — Discover the Workspace Security Model

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and `P1`–`P2` (`~/.claude/skill-factory/core/existing-project.md`). Read [deriving-the-model.md](references/deriving-the-model.md) and collect:

| Dimension | What to Inspect in the Workspace |
|---|---|
| **Trust Boundaries (`SC1`, `SC5`)** | External entry points (endpoints/handlers, UI forms, deep links/navigation URIs, webhooks, queue consumers, file imports, external provider responses) and their validation/schema boundary |
| **Authentication & Session Lifecycle (`SC7`)** | Login/token verification helper, single-flight token refresh flow, and credential wipe on logout/expiry |
| **Authorization Model (`SC2`)** | Roles/capabilities, where object-level guards execute, and the rule that UI visibility gates are UX only |
| **Data Scopes (`SC3`)** | Active isolation dimensions (tenant, owner/user, environment, release state) and how scope filters reach queries, caches, and storage keys |
| **Secrets & Sensitive Data (`SC6`, `SC8`, `SC12`)** | Typed config/compile-time injection, encrypted/hardware-backed credential store, logger redaction, generic error envelopes, and cryptographic helpers |
| **Deterministic Security Gates** | Installed security linters, dependency advisory scanners, lockfile checks, and `rg` anti-pattern audits |

---

## Step 2 — Map Base Rules (`SC1`–`SC14`)

Read [base-rules.md](references/base-rules.md) and [deriving-the-model.md](references/deriving-the-model.md). Map all 14 mandatory rules (`SC1`–`SC14`) onto the workspace's real guards, helpers, and error types. `SC1`, `SC2`, `SC3`, `SC4`, `SC6`, and `SC13` are never omitted (in single-tenant apps, `SC3` applies to user/owner and environment scopes).

---

## Step 3 — Propose & Confirm (User Gate)

Present a concise summary for user confirmation in one round:
1. **Security Model:** Trust boundaries, authentication/session flow, object-level authorization guards, and data scopes.
2. **Secrets, PII & Runtime Risk Guards:** Secret storage, log/error redaction, and unsafe-vs-safe patterns for injection, transport/TLS, outbound calls, and files.
3. **Deterministic Gates & Review Rubric:** Exact CLI/`rg` commands (`PASS` / `FAIL`) and `BLOCKER` / `MAJOR` / `MINOR` review triggers.

---

## Step 4 — Author the Skill (`SKILL.md` + 3 Cohesive References)

Read `~/.claude/skill-factory/core/authoring-guide.md`. Generate a clean, flat 3-reference skill structure (never fragment into micro-files or `be/`/`fe/` branches):

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | Routing table (< 150 lines): Deterministic Security Gates (`PASS` / `FAIL`), Core Security Rules (`SC1`–`SC14` — Mandatory Compliance), and Reference Guides index (with `<!-- {{profile_references}} -->` when profiles apply) |
| `references/01-input-auth-and-data-scope.md` | [templates/references/01-input-auth-and-data-scope.md.tmpl](templates/references/01-input-auth-and-data-scope.md.tmpl) | Trust boundaries, input validation (`SC1`), navigation/redirect allow-lists (`SC5`), authentication (`SC7`), object-level authorization (`SC2`), data-scope isolation (`SC3`), and fail-closed handling (`SC13`) |
| `references/02-secrets-data-and-crypto.md` | [templates/references/02-secrets-data-and-crypto.md.tmpl](templates/references/02-secrets-data-and-crypto.md.tmpl) | Secrets management & encrypted storage (`SC6`), PII/log/error redaction (`SC8`), and vetted cryptography & CSPRNG (`SC12`) |
| `references/03-runtime-risks-deps-and-review.md` | [templates/references/03-runtime-risks-deps-and-review.md.tmpl](templates/references/03-runtime-risks-deps-and-review.md.tmpl) | Unsafe-vs-safe patterns for injection (`SC4`), transport/SSRF (`SC9`), file handling (`SC10`), dependency supply-chain vetting (`SC11`), deterministic `rg` gates, `SC14` handoff triggers, and `BLOCKER` / `MAJOR` / `MINOR` review rubric |

Authoring rules:
- Use only the unified gate statuses (`PASS` / `FAIL`) and 3-tier review severities (`BLOCKER` / `MAJOR` / `MINOR`); never invent `P1` / `P2` / `P3` severities.
- Keep base files 100% stack-generic when authoring a multi-profile pack skill, placing company/profile-specific contracts in `profiles/{imespro,external-structured,external-standard}/security-contracts.md`.
- Replace every `{{…}}` placeholder, strip `<!-- GEN: … -->` comments, and never include real secrets or PII in examples.

---

## Step 5 — Wire, Trial-Run & Verify

1. **Wire:** Add a pointer in `AGENTS.md` / `CLAUDE.md` if not already present.
2. **Trial-run:** Walk a real security-sensitive change (e.g., a mutating action, deep link/outbound URL, or credential storage path) against the generated skill (`~/.claude/skill-factory/core/trial-run.md`).
3. **Verify & Record:** Run [checklist.md](checklist.md) and `~/.claude/skill-factory/core/checklist-common.md`, then record provenance (`~/.claude/skill-factory/core/provenance.md`).

---

## Resources

- [references/base-rules.md](references/base-rules.md) — Universal security rules `SC1`–`SC14`, `PASS` / `FAIL` gate contract, and `BLOCKER` / `MAJOR` / `MINOR` review scale
- [references/deriving-the-model.md](references/deriving-the-model.md) — Stack-agnostic security model discovery, risk taxonomy, and `rg` audit design
- [checklist.md](checklist.md) — Verification checklist for the generated skill
