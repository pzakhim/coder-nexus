---
name: create-quality-environment-skill
description: Write a workspace's own quality-environment skill from the skill-factory knowledge base - how the Quality Engineer prepares a safe, repeatable test environment - the services, ports and start/stop commands, probing before starting and never stopping a stack someone else started, readiness checks, the reviewed revision and its migrations, isolated test data and per-role test accounts, sandboxes or labelled stubs for external providers, cleanup, and BLOCKED when the environment fails - for fullstack and backend/frontend workspaces. Use whenever the user wants to set up, standardize or update how test environments are started, seeded and cleaned for acceptance testing in a workspace, or says things like "tạo skill môi trường test", "dựng stack để test", "seed dữ liệu test", "mock provider", even if they do not say "skill". Writes .agents/skills/quality-environment/, then trial-runs it.
argument-hint: "[stack] [how the stack starts]"
---

# Create Quality Environment Skill

Goal: produce `<workspace>/.agents/skills/quality-environment/` — how the Quality Engineer gets the workspace's stack running on the reviewed revision with safe data, test accounts and labelled stubs, without disturbing anyone else, and how it cleans up.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — quality-planning decides which data and environments cases need; this skill provides them; quality-acceptance runs the cases.

## Step 1 — Context Card (+ environment facts)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Services | `docker-compose.yml`, `Makefile`, `package.json` scripts, `Procfile`, README "run locally": API, workers, frontend, databases, queues |
| Ports and health checks | Config/env, health endpoints, first-page URLs |
| Start/stop rules | Existing rules such as "probe first; never stop a stack you did not start" |
| Database setup | Local DB, migrations command, seed/sync commands and which ones touch shared data |
| Test accounts | Seeded users per role/environment, how credentials are configured (never values) |
| External providers | ERP, LLM, payment, mail… — sandboxes, mock servers (Mockoon, WireMock, MSW, Prism) |
| Existing skill | `.agents/skills/*verification*`, `*test*` sections on live stacks |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/stack-recipes.md`, `references/stubs.md`. For each rule E1–E14: adopted, adapted, or "not adopted" with a reason. E2, E5, E7, E9, E12, E13 are never "not adopted".

## Step 3 — Propose

- **Lifecycle:** probe → reuse or start (background, logs captured) → readiness → record → stop only what you started.
- **Data and accounts:** isolation strategy (dedicated tenant/run IDs, resettable fixtures), per-role accounts, forbidden data commands.
- **External providers:** sandbox or stub per provider, stub scenarios, labelling.
- **Revision:** how the stack is brought to the reviewed revision and migrated.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) services, commands and the own-vs-shared rule, (2) data isolation and accounts, (3) provider sandboxes/stubs, (4) failure handling and cleanup.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout: **flat** (`references/01–05`) — the environment is the whole stack, with BE/FE sections inside the files when the workspace is fullstack.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The lifecycle and the never-list on one screen |
| `references/01-stack-and-lifecycle.md` | `templates/01-stack-and-lifecycle.md.tmpl` | **Mandatory** | Starting or killing the wrong processes breaks other people's work |
| `references/02-test-data-and-accounts.md` | `templates/02-test-data-and-accounts.md.tmpl` | **Mandatory** | Shared or real data makes results lie or causes damage |
| `references/03-external-dependencies.md` | `templates/03-external-dependencies.md.tmpl` | **Mandatory** | A PASS against an unlabelled stub is a false PASS |
| `references/04-revision-and-migrations.md` | `templates/04-revision-and-migrations.md.tmpl` | **Mandatory** | Testing a different revision proves nothing about the reviewed one |
| `references/05-cleanup-and-failures.md` | `templates/05-cleanup-and-failures.md.tmpl` | **Mandatory** | Leftovers and silent environment failures poison later runs |

Writing rules: keep each template's purpose, give every rule its reason, real commands with cwd and real ports, never credential values (reference the config), replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Test environment
   Acceptance test environments are prepared per `.agents/skills/quality-environment/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md` (plans only — no services are started during the trial). Task ideas:

- Prepare the environment for a real feature's test plan.
- The API port is already in use by someone else's stack — does the plan reuse it instead of restarting it?
- A provider has no sandbox — is a stub planned and labelled?
- The reviewed revision adds a migration — is the local DB migrated before testing?

Compare: probe first, own-vs-shared respected, data isolated, accounts per role, stubs labelled, revision aligned, BLOCKED on failure.

## Step 8 — Description

Per the authoring guide: workspace name; situations (start/prepare the stack for testing, seed test data, test accounts, mock a provider, environment broken); team trigger words. Should not trigger for writing application code.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing environment guidance (e.g. a "live local stack" section in a verification skill): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep probe rules, make targets and forbidden commands verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — E1–E14 with reasons
- `references/stack-recipes.md` — probing, starting, readiness and stopping by stack
- `references/stubs.md` — sandboxes, mock servers and labelling
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `checklist.md` — topic checks
