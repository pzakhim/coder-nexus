---
name: create-quality-planning-skill
description: "Generate a workspace's `quality-planning` skill from the skill-factory knowledge base — covering how the Quality Engineer turns approved specs into a test plan: early testability review right after requirements, two-way `AC-NN ↔ TC-NN` traceability, coverage categories including `Role × Environment × Action × Object` permission matrices and `security-review` (`SR14`) runtime hand-offs, stack-neutral test levels (API/Service Acceptance, UI/Client End-to-End, Visual Fidelity, Integration, Unit), safe repeatable data and named environments, `BLOCKER` / `MAJOR` / `MINOR` risk tiers and plan review severities, and binary `PASS` / `FAIL` CLI verification gates."
argument-hint: "[target_dir] [where specs live]"
---

# Create Quality Planning Skill

Goal: produce `<workspace>/.agents/skills/quality-planning/` — governing how the Quality Engineer designs test cases from the workspace's approved specs (`{{target_dir}}`), aligned with `shared_contracts/flags_and_statuses.md`.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: [../../core/quality-skill-family.md](../../core/quality-skill-family.md) — `quality-planning` is the QA design side (what to test); `quality-environment`, `quality-acceptance`, and `quality-reporting` govern environment readiness, execution, and reporting; unit tests belong to the Code Writer.

## Step 1 — Context Card (+ Spec and Test Landscape)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project discovery ([../../core/existing-project.md](../../core/existing-project.md)). Collect read-only quality planning facts:

| Field | Where to Look |
|---|---|
| **Spec Artifacts** | Brief (scope in/out), requirements with AC and BDD scenarios, design state matrix, decisions (`D-NN`), glossary — e.g. `.superpowers/work-items/<slug>/vN/`, `docs/features/…` |
| **AC and Case IDs** | `AC-NN`, `FLOW-NN`, `E2E-NN`, `TC-NN` or the workspace's canonical ID scheme |
| **Existing Quality & Security Skills** | `.agents/skills/quality-*`, `.agents/skills/security-review/`, tester role files |
| **Test Levels Present** | Unit, Integration (real database/service), API/Service Acceptance, UI/Client End-to-End, Visual Fidelity |
| **Roles and Data Scopes** | RBAC roles, environments, tenant/owner scopes (`Role × Environment × Action × Object`) for the permission matrix |
| **Test Data Sources** | Seeds, fixtures, local DB reset scripts, network-edge stubs for external providers |
| **Base Inputs (Read-Only)** | Coder Nexus `plugins/core/agents/test_runner.md` |

## Step 2 — Enforce Base Rules (`Q1`–`Q14`)

Read [references/base-rules.md](references/base-rules.md), [references/case-design.md](references/case-design.md), and [references/test-levels.md](references/test-levels.md). All rules **`Q1`–`Q14`** are **mandatory compliance** (zero optional rule exclusions). Risk tiers and plan-review findings use strictly **`BLOCKER` / `MAJOR` / `MINOR`** and automated CLI verification gates use strictly **`PASS` / `FAIL`** (`shared_contracts/flags_and_statuses.md`).

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Spec Sources, IDs & Plan Location/Approval**: Real spec paths, `AC-NN ↔ TC-NN` scheme, where the test plan lives, and who approves it before execution.
2. **Coverage Categories, Security Hand-Off & Risk Tiers**: Coverage categories including `Role × Environment × Action × Object` permission matrix cases, `security-review` (`SR14`) runtime `PLAUSIBLE` items, and `BLOCKER` / `MAJOR` / `MINOR` risk tier ordering.
3. **Test Levels & Integration Ownership**: Which cases use API/Service Acceptance, UI/Client End-to-End, Visual Fidelity, or Manual (with written reason), plus who owns Integration tests (default: Code Writer).
4. **Data, Named Environments & CLI Plan Gates**: Safe seed sources, stub labelling rules, and deterministic CLI commands (`PASS` / `FAIL`) verifying traceability and plan readiness.

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md) and [../../core/layouts.md](../../core/layouts.md). Generate the flat, cohesive 3-reference skill structure:

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | Concise routing table (< 115 lines), `Q1`–`Q14` mandatory invariants, test level ownership, `BLOCKER`/`MAJOR`/`MINOR` risk & plan sign-off table, and binary `PASS`/`FAIL` CLI gates |
| `references/01-sources-testability-and-traceability.md` | [templates/references/01-sources-testability-and-traceability.md.tmpl](templates/references/01-sources-testability-and-traceability.md.tmpl) | `Q1`–`Q3`, `Q12`, `Q14` — spec sources of truth, independence from code, early testability review after requirements, canonical IDs, and two-way `AC-NN ↔ TC-NN` traceability matrix |
| `references/02-case-design-and-test-levels.md` | [templates/references/02-case-design-and-test-levels.md.tmpl](templates/references/02-case-design-and-test-levels.md.tmpl) | `Q4`, `Q5`, `Q8`–`Q11` — coverage categories, `Role × Environment × Action × Object` permission matrix & `security-review` (`SR14`) runtime hand-offs, concrete expected results, `BLOCKER`/`MAJOR`/`MINOR` risk tiers, out-of-scope guards, regression set, and stack-neutral test levels |
| `references/03-data-environments-and-plan-gates.md` | [templates/references/03-data-environments-and-plan-gates.md.tmpl](templates/references/03-data-environments-and-plan-gates.md.tmpl) | `Q6`, `Q7`, `Q13` — safe repeatable test data, named environments & labelled external stubs, test plan template, deterministic CLI `PASS`/`FAIL` gates, and `BLOCKER`/`MAJOR`/`MINOR` plan review rubric |

Writing rules: keep each template's purpose, give every rule its reason, populate the workspace's real spec paths, IDs, roles, and scopes, replace every `{{…}}`, delete every `<!-- GEN … -->`, keep `<!-- {{profile_references}} -->` in `SKILL.md`, and keep `<!-- custom:start -->` / `<!-- custom:end -->` blocks intact.

## Step 6 — Wire, Step 7 — Trial Run & Step 8–9 — Verify

1. Add a pointer in `AGENTS.md` / `CLAUDE.md` to `.agents/skills/quality-planning/SKILL.md` and link from the Quality Engineer / Tester and Spec Writer role files.
2. Run a read-only trial ([../../core/trial-run.md](../../core/trial-run.md)) on a real approved spec (verify vague AC are flagged, `AC-NN ↔ TC-NN` is two-way complete, and permission matrix cases include direct API/service `403`/`404` checks).
3. Refine the frontmatter description per [../../core/authoring-guide.md](../../core/authoring-guide.md) (workspace name, concrete planning triggers, boundary vs `quality-acceptance` and `unit-testing`).
4. Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), and record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Update Mode & Generator Changes

- Existing `.agents/skills/quality-planning/`: if registered, follow [../../core/sync-protocol.md](../../core/sync-protocol.md); if not registered, adopt existing case IDs, plan location, and role conventions ([../../core/existing-project.md](../../core/existing-project.md)).
- Generator updates follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- [references/base-rules.md](references/base-rules.md) — `Q1`–`Q14` mandatory quality planning invariants
- [references/case-design.md](references/case-design.md) — coverage categories, `security-review` (`SR14`) hand-off, case format, and `BLOCKER` / `MAJOR` / `MINOR` risk tiers
- [references/test-levels.md](references/test-levels.md) — stack-neutral test levels and ownership
- [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) and `templates/references/01..03.md.tmpl` — cohesive 3-reference skill templates
- [checklist.md](checklist.md) — topic verification checklist
