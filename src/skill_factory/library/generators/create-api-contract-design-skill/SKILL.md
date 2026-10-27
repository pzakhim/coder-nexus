---
name: create-api-contract-design-skill
description: "Generate a workspace's `api-contract-design` skill from the skill-factory knowledge base — covering contract-first OpenAPI/schema governance, route and input/output schema conventions (`extra=\"forbid\"`), single error envelope, bounded pagination/filtering, per-endpoint authentication & data-scope isolation (anti-IDOR), atomic idempotency keys, additive-vs-breaking compatibility (One-Version Rule), FE–BE handshake (`api_contract.json`), binary `PASS` / `FAIL` CLI gates, and `BLOCKER` / `MAJOR` / `MINOR` review grading."
argument-hint: "[target_dir]"
---

# Create API Contract Design Skill

Goal: produce `<workspace>/.agents/skills/api-contract-design/` — governing how this workspace designs, generates, changes, and verifies its API contracts (`{{target_dir}}`), aligned with `shared_contracts/api_handshake_protocol.md` and `shared_contracts/flags_and_statuses.md`.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership: [../../core/planning-skill-family.md](../../core/planning-skill-family.md) — this skill governs API contract shape, compatibility, and snapshot verification; `secure-coding-standards` governs security enforcement; `domain-knowledge` governs business roles and data scopes.

## Step 1 — Context Card (+ API Facts)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and P1–P2 ([../../core/existing-project.md](../../core/existing-project.md)). Collect read-only API facts ([references/detection.md](references/detection.md)):
- API style (REST, RPC, GraphQL) and contract artifacts (`openapi.json`, `*.proto`, `schema.graphql`, `design.md` API section).
- Route declarations, input/output DTOs/schemas, centralized error handlers and error-code enums.
- Pagination/filtering/sorting helpers, authentication security schemes, RBAC & tenant/owner scope dependencies, and `Idempotency-Key` storage.
- Consuming clients, Mockoon / mock server configurations, and `api_contract.json` handshake files.

## Step 2 — Enforce Base Rules (`AP1`–`AP9`)

Read [references/base-rules.md](references/base-rules.md). All rules **AP1–AP9** are **mandatory compliance** — map each rule to the workspace's exact framework, schema library, auth dependencies, and OpenAPI/contract tools.

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Contract Source of Truth**: Generated `openapi.json` snapshot + approved `design.md` API section.
2. **Response, Error Envelope & Pagination**: The workspace's canonical success/error envelope and bounded list pagination (`limit` / `offset` or `cursor`).
3. **Authentication, Scopes & Safe Mutations**: Security scheme declarations, `401` / `403` / `404` anti-IDOR rules, and atomic `Idempotency-Key` handling.
4. **Compatibility & Versioning Policy**: Additive-first, Hyrum's Law, One-Version Rule, and breaking-change `D-NN` protocol.

## Step 5 — Author (Cohesive 3-File `references/` Layout)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate a concise `SKILL.md` (< 120 lines) and 3 cohesive reference files under `references/`:

| Output File | Template | Kind | Purpose |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | Contract-first artifacts, mandatory rules `AP1`–`AP9`, role duties, `PASS` / `FAIL` CLI gates, and `<!-- {{profile_references}} -->` |
| `references/01-conventions-schemas-and-idempotency.md` | [templates/references/01-conventions-schemas-and-idempotency.md.tmpl](templates/references/01-conventions-schemas-and-idempotency.md.tmpl) | **Mandatory** | Route naming, separate input/output schemas (`extra="forbid"`), single error envelope, HTTP status codes, bounded pagination, and atomic `Idempotency-Key` rules (`AP1`–`AP4`, `AP8`) |
| `references/02-auth-scopes-and-compatibility.md` | [templates/references/02-auth-scopes-and-compatibility.md.tmpl](templates/references/02-auth-scopes-and-compatibility.md.tmpl) | **Mandatory** | Per-endpoint authentication & data-scope isolation (anti-IDOR `404`), additive vs. breaking classification, Hyrum's Law, and One-Version Rule (`AP5`, `AP6`) |
| `references/03-snapshot-handshake-and-review.md` | [templates/references/03-snapshot-handshake-and-review.md.tmpl](templates/references/03-snapshot-handshake-and-review.md.tmpl) | **Mandatory** | Generating & diffing `openapi.json` against `openapi.base.json`, FE–BE handshake (`api_contract.json`), `PASS` / `FAIL` CLI gates, and `BLOCKER` / `MAJOR` / `MINOR` review rubric (`AP7`, `AP9`) |

## Step 6 — Wire & Step 7 — Trial Run

1. Add a pointer in `CLAUDE.md` / `AGENTS.md`:
   ```markdown
   ## API contracts
   API design and changes follow `.agents/skills/api-contract-design/SKILL.md`.
   ```
2. Trial-run ([../../core/trial-run.md](../../core/trial-run.md)) on: (a) designing a paginated, tenant-scoped list endpoint, (b) classifying a field rename as breaking (`D-NN` + compatible path), and (c) securing a retried mutation with an atomic `Idempotency-Key`.

## Step 8 — Description & Step 9 — Verify, Record & Report

Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), then record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Resources

- [references/base-rules.md](references/base-rules.md) — Mandatory rules `AP1`–`AP9`
- [references/detection.md](references/detection.md) — Read-only API discovery commands
- [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) & `templates/references/01..03.md.tmpl`
- [checklist.md](checklist.md) — Topic verification checklist
