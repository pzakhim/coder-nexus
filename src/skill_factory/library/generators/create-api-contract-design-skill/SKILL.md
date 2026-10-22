---
name: create-api-contract-design-skill
description: Write a workspace's own api-contract-design skill from the skill-factory knowledge base - where the API contract lives and is designed first, naming of resources, fields and methods, the response and error shape, pagination, filtering and sorting, authentication and data scopes per endpoint, backward compatibility, deprecation and what counts as a breaking change, idempotency, how clients consume and mock the API, and contract evidence - read from the workspace's real routes, schemas, error handlers and clients, for REST and RPC style APIs on any stack and for fullstack repos. Use whenever the user wants to set up, standardize or update API design conventions for Planning, Code Writer and Reviewer in a workspace, or says things like "tạo skill API", "chuẩn thiết kế API", "format response lỗi", "đổi API có phá app không", even if they do not say "skill". Writes .agents/skills/api-contract-design/, then trial-runs it on real endpoints.
argument-hint: "[be_dir] [fe_dir]"
---

# Create API Contract Design Skill

Goal: produce `<workspace>/.agents/skills/api-contract-design/` — how this workspace designs, changes and consumes its APIs: the source of truth, naming, response and error shape, pagination, auth and scopes, compatibility and versioning, client consumption and mocks. It extends the fixed backend `api-contracts` skill and the API section of `{{slot:architecture-design}}`; the handshake evidence policy (`shared_contracts/api_handshake_protocol.md`) stays as it is.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0**. Ownership: `~/.claude/skill-factory/core/planning-skill-family.md` — this skill wins on API shape; `secure-coding-standards` owns how authorization is enforced; `git-workflow` owns the contract list and the version bump; `domain-knowledge` owns roles and data scopes.

## Step 1 — Context Card (+ API facts)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then collect, read-only (`references/detection.md`): API style (REST, RPC, GraphQL), contract files (OpenAPI, schemas), route declarations, serializers/DTOs, error handlers and codes, pagination helpers, auth middleware, version paths, idempotency keys and their store, API clients in front ends and mobile apps, mock configs, and external consumers.

GraphQL or event-only workspaces: keep the same topics, adapted to their vocabulary (schema, resolvers, events); say so in the report.

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule AP1–AP9: adopted, adapted, or "not adopted" with a reason. AP1 (one source of truth), AP6 (compatibility) and AP9 (fixture is not live) are never "not adopted". Where each idea came from: `references/sources.md`.

## Step 3 — Propose

- **Established API:** document the conventions as they are (with real endpoints as examples), list inconsistencies as drift, and propose which convention new endpoints follow.
- **New API:** propose conventions with reasons, matched to the framework's defaults.
- Show one existing endpoint and one new endpoint written in the proposed conventions.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Source of truth for the contract | The OpenAPI file if one exists; otherwise the API section of `design.md` |
| Q2 | Response and error shape | The shape most endpoints already return |
| Q3 | Pagination, filtering, sorting | The helper the code already uses |
| Q4 | Compatibility policy (additive only, version path, deprecation window) | Additive changes only; breaking changes need a new version and a deprecation note |

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Layout per `~/.claude/skill-factory/core/layouts.md`.

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` (router) | `templates/SKILL.md.tmpl` | **Mandatory** | Contract-first and the compatibility rule on one screen |
| `references/01-conventions.md` | `shared/01-conventions.md` | `templates/01-conventions.md.tmpl` | **Mandatory** | One naming, response and error shape |
| `references/02-pagination-and-filtering.md` | `shared/02-…` | `templates/02-pagination-and-filtering.md.tmpl` | **Mandatory** (one line when no lists) | Every list works the same way |
| `references/03-auth-and-scopes.md` | `be/03-auth-and-scopes.md` | `templates/03-auth-and-scopes.md.tmpl` | **Mandatory** | No endpoint returns data outside the caller's scope |
| `references/04-compatibility-and-versioning.md` | `shared/04-…` | `templates/04-compatibility-and-versioning.md.tmpl` | **Mandatory** | Clients already in use keep working |
| `references/05-consuming-and-mocking.md` | `fe/05-consuming-and-mocking.md` | `templates/05-consuming-and-mocking.md.tmpl` | Suggested (Mandatory when the repo has a client) | Clients and mocks match the contract |

Writing rules: real endpoints, files and commands; every rule with its reason; no secrets or real tokens in examples; replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## API contracts
   API design and changes follow `.agents/skills/api-contract-design/SKILL.md`.
   ```
2. Offer to link it from `implementation-planning`, `code-review` and `secure-coding-standards` (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas from this workspace:

- Design the endpoint(s) for a new list screen: naming, pagination, errors, scopes.
- Rename or remove a field that a client already uses: is it flagged as breaking, with a compatible path and a deprecation note?
- A mutation that may be retried by a mobile client: key from the intent, atomic claim, changed payload rejected, in-flight duplicate answer, timeout treated as unknown?

## Step 8 — Description

Per the authoring guide: workspace name; situations (new endpoint, changing a payload, error handling, pagination, API in `design.md`, client integration, mocks); the team's trigger words. Should not trigger for internal function signatures.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report drift found, rules adapted or not adopted, trial results.

## Update mode

Existing `.agents/skills/api-contract-design/` or a workspace API guide: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep the team's error codes, envelope and versioning verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — AP1–AP9 with reasons
- `references/sources.md` — external sources, ideas taken, ideas not adopted
- `references/detection.md` — where routes, schemas, errors, auth and clients are found, per stack
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `checklist.md` — topic checks
