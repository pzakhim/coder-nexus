---
name: create-quality-environment-skill
description: "Write a workspace's own `quality-environment` skill from the skill-factory knowledge base — governing how the Quality Engineer prepares a safe, repeatable test environment across any stack: service topology, probing before starting and never stopping a stack someone else started, background startup with log capture, deterministic readiness gates (`PASS` / `FAIL`), reviewed revision alignment and local DB migrations, isolated test data and per-role accounts without leaked secrets, sandboxes or labelled stubs (`stubbed: <provider>`), post-run cleanup, `BLOCKED` handling on environment failures, and `BLOCKER` / `MAJOR` / `MINOR` review severities. Use whenever the user wants to set up, standardize, or update how test environments are started, seeded, stubbed, and cleaned for acceptance testing in a workspace, or says things like 'tạo skill môi trường test', 'dựng stack để test', 'seed dữ liệu test', 'mock provider', even if they do not say 'skill'. Writes `.agents/skills/quality-environment/`, then trial-runs it."
argument-hint: "[stack] [how services start]"
---

# Create Quality Environment Skill

Goal: produce `<workspace>/.agents/skills/quality-environment/` — how the Quality Engineer gets the workspace's services running on the reviewed revision with isolated data, per-role test accounts, and labelled stubs, without disturbing anyone else's running stack, and how it cleans up (`{{target_dir}}`).

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed pack skill of the same name). Ownership: [../../core/quality-skill-family.md](../../core/quality-skill-family.md) — `quality-planning` decides which data and environments test cases need; `quality-environment` prepares and records them; `quality-acceptance` executes the test cases.

## Step 1 — Context Card (+ Environment Facts)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project discovery ([../../core/existing-project.md](../../core/existing-project.md)). Additionally collect:

| Field | Where to Inspect |
|---|---|
| **Services & Topology** | `docker-compose.yml`, `Makefile`, `package.json`, `pyproject.toml`, `Procfile`, README local-run docs: datastores, queues, API/backend processes, background workers, client/UI dev servers |
| **Ports & Readiness Checks** | Config/env templates, HTTP health endpoints, worker readiness logs, client dev server URLs |
| **Start / Stop Rules** | Existing rules such as "probe first; never stop a stack you did not start", and which task targets kill all processes |
| **Database & Migrations** | Local/disposable DB setup, migration commands (`database-migrations`), seed commands, and forbidden commands that reset or overwrite shared data |
| **Test Accounts & Matrix** | Seeded users per role/environment, logical in-app environment selectors vs. physical DB targets, and where credentials are configured (never read or record secret values) |
| **External Providers** | Third-party APIs (ERP, LLM, payment, messaging, storage) — sandboxes or network-edge mock servers |
| **Existing Guidance** | `.agents/skills/*verification*`, `*test*`, or live-stack instructions |

## Step 2 — Enforce Base Rules (`E1`–`E14`)

Read [references/base-rules.md](references/base-rules.md), [references/stack-recipes.md](references/stack-recipes.md), and [references/stubs.md](references/stubs.md). All rules **E1–E14** are **mandatory compliance** — translate each rule into the workspace's exact service commands, ports, isolation strategy, and provider configurations.

## Step 3 — Propose

Present on one screen:
- **Stack Lifecycle & Revision Alignment (`E1`–`E4`, `E8`–`E9`)**: probe commands → reuse healthy services or start missing ones in the background with logs → readiness checks (`PASS` / `FAIL`) → checkout reviewed revision & migrate local DB → stop only what you started.
- **Test Data, Accounts & Stubs (`E5`–`E7`, `E10`, `E13`)**: isolation strategy (dedicated tenant/run IDs, resettable local fixtures), forbidden data commands, per-role test accounts (config keys only), environment matrix, and sandbox vs. `stubbed: <provider>` network-edge stubs.
- **Cleanup, `BLOCKED` Handling & Gates (`E11`, `E12`, `E14`)**: post-run data and process cleanup, `BLOCKED` reporting on environment failures, environment evidence record, CLI readiness gates (`PASS` / `FAIL`), and `BLOCKER` / `MAJOR` / `MINOR` review rubric (`shared_contracts/flags_and_statuses.md`).

## Step 4 — Gate (User Confirms)

Confirm in one round where possible: (1) services, commands, and own-vs-shared stack rules, (2) data isolation, forbidden commands, and role accounts, (3) external provider sandboxes/stubs, and (4) readiness gates (`PASS` / `FAIL`), cleanup, and `BLOCKED` failure handling.

## Step 5 — Author (Cohesive 3-File `references/` Layout)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate a concise `SKILL.md` (< 115 lines) and 3 cohesive reference files under `references/`:

| Output File | Template | Kind | Purpose |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | Deterministic CLI readiness gates (`PASS` / `FAIL`), 6-step lifecycle, Never-list, mandatory `E1`–`E14` rule index, and `<!-- {{profile_references}} -->` |
| `references/01-stack-lifecycle-and-revision.md` | [templates/references/01-stack-lifecycle-and-revision.md.tmpl](templates/references/01-stack-lifecycle-and-revision.md.tmpl) | **Mandatory** | Service topology, probe-before-start, never stop unowned stacks, readiness checks, reviewed revision checkout, and local DB migration (`E1`–`E4`, `E8`–`E9`) |
| `references/02-test-data-accounts-and-stubs.md` | [templates/references/02-test-data-accounts-and-stubs.md.tmpl](templates/references/02-test-data-accounts-and-stubs.md.tmpl) | **Mandatory** | Isolated test data, per-role test accounts without leaked credentials, sandbox vs. labelled stubs (`stubbed: <provider>`), and environment matrix (`E5`–`E7`, `E10`, `E13`) |
| `references/03-cleanup-blocked-handling-and-gates.md` | [templates/references/03-cleanup-blocked-handling-and-gates.md.tmpl](templates/references/03-cleanup-blocked-handling-and-gates.md.tmpl) | **Mandatory** | Post-run cleanup, `BLOCKED` on environment failure, environment evidence record, deterministic CLI `PASS` / `FAIL` readiness gates, and `BLOCKER` / `MAJOR` / `MINOR` review rubric (`E11`, `E12`, `E14`) |

Writing rules: keep each template's purpose, give every rule its reason, use real commands with `cwd` and real ports, never include credential values (reference config keys only), replace every `{{…}}`, delete every `<!-- GEN … -->`, write in English, keep each file under ~200 lines, and preserve `<!-- custom:start -->` / `<!-- custom:end -->`.

## Step 6 — Wire

1. Add a pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Test environment
   Acceptance test environments are prepared per `.agents/skills/quality-environment/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file.

## Step 7 — Trial Run

Follow [../../core/trial-run.md](../../core/trial-run.md) (plan-only — do not start live services during the trial):
- Prepare the environment for a real feature's acceptance test plan.
- An application port is already in use by someone else's stack — verify the plan reuses it if healthy or reports `BLOCKED` if unhealthy, instead of killing/restarting it.
- An external provider has no sandbox — verify a network-edge stub is planned and labelled `stubbed: <provider>`.
- The reviewed revision adds a schema migration — verify the local/disposable DB is migrated before testing.

## Step 8 — Description & Step 9 — Verify, Record & Report

Craft the frontmatter description per [../../core/authoring-guide.md](../../core/authoring-guide.md). Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), then record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Update Mode & Changing This Generator

- **Update mode:** registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); unregistered → adopt ([../../core/existing-project.md](../../core/existing-project.md): preserve probe rules, task targets, and forbidden commands verbatim).
- **Changing this generator:** follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- [references/base-rules.md](references/base-rules.md) — Mandatory rules `E1`–`E14` with rationale
- [references/stack-recipes.md](references/stack-recipes.md) — Probing, starting, readiness, and stopping by generic service category
- [references/stubs.md](references/stubs.md) — Provider sandboxes, network-edge stubs, and `stubbed: <provider>` labelling
- [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) & `templates/references/01..03.md.tmpl`
- [checklist.md](checklist.md) — Topic verification checks
