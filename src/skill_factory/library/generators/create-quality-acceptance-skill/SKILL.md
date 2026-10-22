---
name: create-quality-acceptance-skill
description: Write a workspace's own quality-acceptance skill from the skill-factory knowledge base - how the Quality Engineer executes the approved test plan on the reviewed revision - frontend cases in a real browser (states produced for real, permissions per role, environment switch, persistence after reload, console and network health) and backend cases through the real API (real auth per role, status codes, persisted data, side effects, direct forbidden calls returning 403), with evidence per case, PASS/FAIL/BLOCKED/NOT_RUN, failure reports and re-tests - using whichever browser and API tools the workspace actually has (detected and confirmed at the gate - chrome-devtools MCP, Playwright, Claude in Chrome, HTTP clients, Postman collections). Use whenever the user wants to set up, standardize or update how acceptance or end-to-end tests are run in a workspace, or says things like "tạo skill E2E", "test thực tế trên web", "QC chạy test", "test API nghiệm thu", even if they do not say "skill". Writes .agents/skills/quality-acceptance/, then trial-runs it.
argument-hint: "[stack] [browser tool | auto]"
---

# Create Quality Acceptance Skill

Goal: produce `<workspace>/.agents/skills/quality-acceptance/` — how the Quality Engineer runs the approved test plan against the reviewed revision in this workspace: frontend in a real browser, backend through the real API, with the tools the workspace has, evidence per case and clear results.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — quality-planning provides the cases, quality-environment the stack and data, this skill executes, quality-reporting writes the final report.

## Step 1 — Context Card (+ tools)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then **detect the tools** with `references/tool-detection.md` and record each as available / configured but unreachable / absent:

| Branch | Candidates |
|---|---|
| Frontend (browser) | chrome-devtools MCP, Playwright, Claude in Chrome, the host's built-in browser tool |
| Backend (API) | HTTP client scripts/tests (httpx, requests, supertest), Postman/Newman collections, `.http` files, curl |

Also collect: existing E2E/acceptance skills or checks numbering, evidence location rules (e.g. screenshots must be inside the workspace), known console/network baseline noise, roles and environments to switch.

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/tool-detection.md`. For each rule A1–A14: adopted, adapted, or "not adopted" with a reason. A1, A2, A4, A7, A9, A13 are never "not adopted".

## Step 3 — Propose

- **Tool per branch** from what was detected (never one that is absent); fallback order if the first is unreachable at run time.
- **Tool operations map:** how navigate / read the page / fill / click / wait / screenshot / console / network / resize are done with the chosen tool.
- **Per-case loop and evidence** (paths, naming), results vocabulary, failure report format, re-test scope.
- **Safety:** which environments may be mutated, accounts used, what is never done.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) **browser tool** for the frontend (options = detected tools, recommended first) and **API tool** for the backend, (2) evidence location and naming, (3) failure report and re-test rules, (4) safety boundaries.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–04`; branched: `shared/01, 02, 04`, `be/03`, `fe/03`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Preconditions, the case loop and the never-list on one screen |
| `references/01-preconditions-and-safety.md` | `shared/01-…` | `templates/shared/01-preconditions-and-safety.md.tmpl` | **Mandatory** | Testing the wrong revision, or mutating the wrong environment, makes everything after it worthless |
| `references/02-executing-cases.md` | `shared/02-…` | `templates/shared/02-executing-cases.md.tmpl` | **Mandatory** | One loop and one evidence standard for every case |
| `references/03-execution.md` | `be/03-…` (API), `fe/03-…` (browser) | `templates/branch/03-execution.md.tmpl` | **Mandatory** | The real tool, its operations and the branch-specific checks |
| `references/04-failures-and-retest.md` | `shared/04-…` | `templates/shared/04-failures-and-retest.md.tmpl` | **Mandatory** | Reproducible defects and the right re-test scope |

Writing rules: keep each template's purpose, give every rule its reason, only tools that exist in the workspace, real URLs/endpoints/roles, never credential values, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Acceptance testing
   Acceptance and end-to-end tests are executed per `.agents/skills/quality-acceptance/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md` (plans only — no browser or API calls during the trial). Task ideas:

- Execute a real plan's P1 cases for one feature: list the tool operations per step and the evidence to save.
- The browser tool is unreachable at run time — are the FE cases `BLOCKED`, not asserted?
- A mutating endpoint — is a direct forbidden call for a lower role planned, expecting `403`?
- A case passes visually but the console shows an error — reported?

Compare: preconditions checked, real tool operations, persistence verified by reload/read-back, evidence per case, correct result words, safety respected.

## Step 8 — Description

Per the authoring guide: workspace name; situations (run E2E/acceptance tests, test on the real web app, verify API behavior, re-test after a fix); team trigger words. Should not trigger for writing unit tests or test plans.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, tools chosen, trial results.

## Update mode

Existing E2E/acceptance guidance (e.g. "Check 3" in a verification skill): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep checks numbering, tool flows, baseline noise and evidence paths verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — A1–A14 with reasons
- `references/tool-detection.md` — detecting browser/API tools and mapping their operations
- `templates/` — `SKILL.md.tmpl`, `shared/01, 02, 04`, `branch/03` (suggested shapes)
- `checklist.md` — topic checks
