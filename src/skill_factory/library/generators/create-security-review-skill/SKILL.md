---
name: create-security-review-skill
description: "Generate a workspace's `security-review` skill from the skill-factory knowledge base — covering threat-focused read-only security auditing of a fixed revision, review triggers, per-change STRIDE-lite threat modeling, authorization matrix (`Role × Environment × Action × Object`) and data-scope isolation (anti-IDOR), boundary security checks, exploit-scenario findings (`CONFIRMED` / `PLAUSIBLE`) graded with unified `BLOCKER` / `MAJOR` / `MINOR` severities, binary `PASS` / `FAIL` CLI gates, and security sign-off (`APPROVED` / `CHANGES_REQUESTED` / `BLOCKED`)."
argument-hint: "[target_dir] [security role: separate | reviewer]"
---

# Create Security Review Skill

Goal: produce `<workspace>/.agents/skills/security-review/` — governing how security-relevant changes are audited in this workspace (`{{target_dir}}`), aligned with `shared_contracts/flags_and_statuses.md`.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership: [../../core/security-skill-family.md](../../core/security-skill-family.md) — `secure-coding-standards` governs how code is written safely; `security-review` governs how a fixed revision is audited for exploitability; `bug-hunt` dimension 5 is handed over here when a separate Security role exists.

## Step 1 — Context Card (+ Security Context)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and P1–P2 ([../../core/existing-project.md](../../core/existing-project.md)). Collect read-only security facts:

| Field | Where to Look |
|---|---|
| **Security & Auth Model** | `.agents/skills/secure-coding-standards/` or `.agents/skills/domain-knowledge/` if present; otherwise inspect authentication dependencies, RBAC guards, data-scope columns (`tenant_id`, `org_id`, `owner_id`), and secret configuration |
| **Security Review Mode** | Separate Security role/agent (parallel to Code Reviewer) or executed by Code Reviewer on triggered changes |
| **High-Risk Trigger Paths** | Authentication/session flows, RBAC/scope guards, multi-tenant queries/exports, payments/financial mutations, file uploads, external webhooks/outbound calls, dependency lockfiles |
| **Installed Read-Only Scanners** | Static security analyzers, dependency vulnerability auditors, secret scanners (list only tools actually installed in the workspace) |
| **Authorization Test Suite** | Existing integration/contract tests proving `401`/`403`/`404` across roles and tenant scopes |

## Step 2 — Enforce Base Rules (`SR1`–`SR14`)

Read [references/base-rules.md](references/base-rules.md), [references/threat-model.md](references/threat-model.md), and [references/checks-by-stack.md](references/checks-by-stack.md). All rules **`SR1`–`SR14`** are **mandatory compliance** (never dropped as `"not adopted"`). Finding severities use strictly **`BLOCKER` / `MAJOR` / `MINOR`** and automated tool checks use strictly **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`).

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Execution Mode & Triggers**: Separate Security role vs. Code Reviewer mode, plus high-risk paths requiring deep review.
2. **Authorization Matrix & Data Scopes**: Confirmed `Role × Environment × Action × Object` rules and tenant/owner scope columns.
3. **Boundary Security Checks & Installed CLI Scanners**: Exact `rg` patterns and read-only scanner commands.
4. **Sign-Off Verdict & Safe Disclosure Channel**: `BLOCKER` / `MAJOR` / `MINOR` mapping to `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED` and where security reports are written.

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate the flat, cohesive 3-reference skill structure:

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | Concise routing table (< 115 lines), execution mode, `SR1`–`SR14` rule index, `BLOCKER`/`MAJOR`/`MINOR` sign-off table, and binary `PASS`/`FAIL` CLI gates |
| `references/01-triggers-threat-model-and-auth-matrix.md` | [templates/references/01-triggers-threat-model-and-auth-matrix.md.tmpl](templates/references/01-triggers-threat-model-and-auth-matrix.md.tmpl) | `SR1`–`SR4`, `SR13` — review triggers, read-only revision boundary, STRIDE-lite per-change threat model, and `Role × Environment × Action × Object` authorization & data-scope matrix |
| `references/02-security-checks-and-cli-gates.md` | [templates/references/02-security-checks-and-cli-gates.md.tmpl](templates/references/02-security-checks-and-cli-gates.md.tmpl) | `SR5`–`SR10` — boundary security checks (entrypoint, persistence/query, client/UI, outbound/file, supply-chain/crypto) and deterministic read-only CLI `PASS`/`FAIL` gates |
| `references/03-findings-verdict-and-report.md` | [templates/references/03-findings-verdict-and-report.md.tmpl](templates/references/03-findings-verdict-and-report.md.tmpl) | `SR11`–`SR14` — exploit-scenario contract (`given → when → then`), `CONFIRMED` vs `PLAUSIBLE`, `BLOCKER`/`MAJOR`/`MINOR` severity rubric, sign-off rules, safe report template, and feedback loop to `secure-coding-standards` |

## Step 6 — Wire, Step 7 — Trial Run & Step 8–9 — Verify

1. Add a pointer in `AGENTS.md` / `CLAUDE.md` to `.agents/skills/security-review/SKILL.md`.
2. Run a read-only trial ([../../core/trial-run.md](../../core/trial-run.md)) on a real diff touching an endpoint or permission check.
3. Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), and record provenance ([../../core/provenance.md](../../core/provenance.md)).
