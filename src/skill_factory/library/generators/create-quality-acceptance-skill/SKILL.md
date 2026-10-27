---
name: create-quality-acceptance-skill
description: "Generate a workspace's `quality-acceptance` skill from the skill-factory knowledge base — governing how the Quality Engineer executes the approved test plan on the reviewed revision across UI/Client Surface (`A5`: real runtime states, role visibility, persistence reload, console/network health) and API/Service Surface (`A6`: real auth per role, status codes, persistence read-back, side effects, live `Role × Environment × Action × Object` `401`/`403`/`404` anti-IDOR verification, and `security-review` `SR14` runtime hand-offs), with `PASS`/`FAIL`/`BLOCKED`/`NOT_RUN` case grading, `BLOCKER`/`MAJOR`/`MINOR` defect reports, and binary `PASS`/`FAIL` CLI gates."
argument-hint: "[target_dir] [ui_tool | auto] [api_tool | auto]"
---

# Create Quality Acceptance Skill

Goal: produce `<workspace>/.agents/skills/quality-acceptance/` — governing how acceptance and end-to-end verification are executed on the reviewed revision in this workspace (`{{target_dir}}`), aligned with `shared_contracts/flags_and_statuses.md`.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: [../../core/quality-skill-family.md](../../core/quality-skill-family.md) — `quality-planning` defines the approved cases, `quality-environment` prepares the target stack and seed data, `quality-acceptance` executes the cases against the live runtime, and `quality-reporting` writes the final sign-off report.

## Step 1 — Context Card (+ Runtime Tools & Surfaces)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project adoption rules ([../../core/existing-project.md](../../core/existing-project.md)). Detect available verification tools using [references/tool-detection.md](references/tool-detection.md) and record each as available, configured-but-unreachable, or absent:

| Verification Surface | Candidate Tools & Facts to Collect |
|---|---|
| **UI / Client Surface (`A5`)** | Chrome DevTools MCP (`chrome-devtools`), scripted E2E runners (Playwright, Cypress, Maestro, integration test runners), host browser tools; viewports, console/network baseline noise |
| **API / Service Surface (`A6`)** | In-repo HTTP/RPC test clients, Postman/Newman/Bruno collections, `.http` files, `curl`/`grpcurl`; auth token acquisition per role |
| **Security Hand-Off (`A6`, `SR14`)** | `.agents/skills/security-review/` authorization matrix (`Role × Environment × Action × Object`), tenant/owner scope columns, and runtime-dependent `PLAUSIBLE` checks |
| **Evidence & Safety Rules (`A8`, `A13`)** | Revision-bound evidence directory (inside workspace), screenshot/payload naming conventions, test accounts, mutable vs. forbidden environments |

## Step 2 — Enforce Base Rules (`A1`–`A14`)

Read [references/base-rules.md](references/base-rules.md) and [references/tool-detection.md](references/tool-detection.md). All rules **`A1`–`A14`** are **mandatory compliance** (never dropped or skipped). Case outcomes use strictly **`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`**, defect severities use strictly **`BLOCKER` / `MAJOR` / `MINOR`**, and automated CLI gates use strictly **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`).

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Runtime Tools & Fallbacks**: Confirmed primary and fallback tools for **UI/Client Surface (`A5`)** and **API/Service Surface (`A6`)**, plus the concrete operations map.
2. **Permission Matrix & Security Hand-Off (`A6`, `SR14`)**: Roles, scopes, and direct forbidden calls (`401`/`403`/`404` anti-IDOR) plus runtime verification of `PLAUSIBLE` findings handed over by `security-review`.
3. **Evidence Path, Defect Channel & Re-Test Scope (`A8`–`A12`)**: Workspace evidence directory, `BLOCKER` / `MAJOR` / `MINOR` defect reporting channel, and re-test rules on fixed revisions.
4. **Safety Boundaries (`A13`)**: Allowed test accounts, mutable local/disposable environments, and redaction rules.

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate the flat, cohesive 3-reference skill structure:

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | Concise routing table (< 115 lines), confirmed tools, `A1`–`A14` rule index, `PASS`/`FAIL`/`BLOCKED`/`NOT_RUN` case status rules, and binary `PASS`/`FAIL` CLI gates |
| `references/01-preconditions-safety-and-case-loop.md` | [templates/references/01-preconditions-safety-and-case-loop.md.tmpl](templates/references/01-preconditions-safety-and-case-loop.md.tmpl) | `A1`–`A4`, `A7`–`A9`, `A13` — reviewed revision & environment preconditions, read-only boundary, safe test-account boundary, per-case execution loop, persistence read-back, and `PASS`/`FAIL`/`BLOCKED`/`NOT_RUN` rules |
| `references/02-ui-and-api-execution-checks.md` | [templates/references/02-ui-and-api-execution-checks.md.tmpl](templates/references/02-ui-and-api-execution-checks.md.tmpl) | `A5`, `A6`, `A11` — real UI/client state & console/network checks, real API/service status/persistence/side-effect checks, `Role × Environment × Action × Object` forbidden call verification (`401`/`403`/`404` anti-IDOR) + `security-review` (`SR14`) runtime checks, and guard/regression execution |
| `references/03-failures-retest-and-gates.md` | [templates/references/03-failures-retest-and-gates.md.tmpl](templates/references/03-failures-retest-and-gates.md.tmpl) | `A10`, `A12`, `A14` — actionable defect reproduction with unified `BLOCKER`/`MAJOR`/`MINOR` severities, flakiness classification, re-test protocol on fixed revision, and deterministic CLI `PASS`/`FAIL` execution gates |

## Step 6 — Wire, Step 7 — Trial Run & Step 8–9 — Verify

1. Add a pointer in `AGENTS.md` / `CLAUDE.md` to `.agents/skills/quality-acceptance/SKILL.md`.
2. Run a read-only trial ([../../core/trial-run.md](../../core/trial-run.md)) planning the exact tool operations, `401`/`403`/`404` permission matrix checks, persistence read-back, and evidence capture for a real feature spec.
3. Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), and record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Update Mode & Changing This Generator

- Existing `.agents/skills/quality-acceptance/`: registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); unregistered → adopt existing tool flows, baseline noise, and evidence paths into the 3-reference layout.
- Generator updates follow [../../core/versioning.md](../../core/versioning.md).
