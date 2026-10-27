---
name: create-quality-reporting-skill
description: "Write a workspace's `quality-reporting` skill from the skill-factory knowledge base — governing how the Quality Engineer turns test execution into a revision-bound report with environment records, per-case evidence links, deterministic AC roll-ups, honest feature verdicts (`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`) where `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`, defect tracking graded with `BLOCKER` / `MAJOR` / `MINOR` severities, multi-round re-test ledgers, and redacted evidence hygiene. Use whenever the user wants to set up, standardize, or update how test results, QA reports, or acceptance verdicts are written in a workspace, or says things like 'tạo skill báo cáo test', 'QA report', 'kết quả nghiệm thu', even if they do not say 'skill'. Writes `.agents/skills/quality-reporting/`, then trial-runs it."
argument-hint: "[where results are recorded]"
---

# Create Quality Reporting Skill

Goal: produce `<workspace>/.agents/skills/quality-reporting/` — governing how the Quality Engineer turns a test run into a trustworthy, revision-bound report (`RP1`–`RP12`), aligned with `shared_contracts/flags_and_statuses.md`.

User input: `$ARGUMENTS`

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: [../../core/quality-skill-family.md](../../core/quality-skill-family.md) — `quality-acceptance` produces per-case results and defects; `quality-reporting` aggregates them into the report and feature verdict.

## Step 1 — Context Card (+ Reporting Conventions)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project discovery ([../../core/existing-project.md](../../core/existing-project.md)). Additionally collect:

| Field | Where to Look |
|---|---|
| **Report Location & Ledger** | `as-built.md`, review/evidence folders (e.g. `reviews/e2e-round-NN/`), work-item handoff docs, and who owns writing each |
| **Verdict & Status Vocabulary** | Case status words (`PASS` / `FAIL` / `BLOCKED` / `NOT_RUN`), feature verdict words (`ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`), and unified defect severities (`BLOCKER` / `MAJOR` / `MINOR`) |
| **Verification Surfaces** | Single unified results table vs. separate `API / Service Surface` and `UI / Client Surface` tables |
| **Evidence & Redaction Rules** | Allowed workspace artifact paths, naming patterns, and secret/token/PII redaction rules |
| **Distribution & Authorization** | Internal handoff target (Coordinator, Docs Writer, User) and explicit user-authorization requirement before any external post |

## Step 2 — Enforce Base Rules (`RP1`–`RP12`)

Read [references/base-rules.md](references/base-rules.md) and [references/report-template.md](references/report-template.md). All rules **`RP1`–`RP12`** are **mandatory compliance**. Defect severities use strictly **`BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`), and `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `PASS`.

## Step 3 — Propose & Step 4 — Gate (User Confirms)

Confirm in one round (recommendation first):
1. **Report Location, Naming & Surface Tables**: Where round reports and summary ledgers live, and whether results use a unified table or `API / Service Surface` + `UI / Client Surface` tables.
2. **AC Roll-Up & Feature Verdict Criteria**: Deterministic mapping from case statuses and `BLOCKER`/`MAJOR`/`MINOR` defects to `ACCEPTED` / `CHANGES_REQUESTED` / `BLOCKED`.
3. **Defect Lifecycle & Multi-Round Re-Test Ledger**: Defect ID scheme, `open → fixed-awaiting-retest → verified` lifecycle (`wont-fix` requires explicit user decision), and round-by-round history table.
4. **Evidence Hygiene, Redaction & Distribution**: Workspace evidence directory, secret/PII redaction checks, and external posting gate.

Nothing is written before the user confirms.

## Step 5 — Author (`templates/SKILL.md.tmpl` + `templates/references/01..03.md.tmpl`)

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Generate the flat, cohesive 3-reference skill structure:

| Output File | Template | Kind | Why It Exists |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | Concise (< 115 lines) routing table, `RP1`–`RP12` mandatory compliance index, feature verdict criteria, and deterministic CLI `PASS`/`FAIL` report gates |
| `references/01-report-structure-and-verdict.md` | [templates/references/01-report-structure-and-verdict.md.tmpl](templates/references/01-report-structure-and-verdict.md.tmpl) | **Mandatory** | `RP1`–`RP4`, `RP6`, `RP7`, `RP11`, `RP12` — verdict-first executive header, revision/environment context, per-case to per-AC roll-up, honest counting, and `ACCEPTED`/`CHANGES_REQUESTED`/`BLOCKED` decision table |
| `references/02-defects-and-retest-history.md` | [templates/references/02-defects-and-retest-history.md.tmpl](templates/references/02-defects-and-retest-history.md.tmpl) | **Mandatory** | `RP5`, `RP10` — defect table with `BLOCKER`/`MAJOR`/`MINOR` severities, status lifecycle, and multi-round re-test ledger |
| `references/03-evidence-hygiene-and-gates.md` | [templates/references/03-evidence-hygiene-and-gates.md.tmpl](templates/references/03-evidence-hygiene-and-gates.md.tmpl) | **Mandatory** | `RP8`, `RP9` — secret/PII redaction, workspace artifact paths, external distribution gate, deterministic CLI `PASS`/`FAIL` checks, and `BLOCKER`/`MAJOR`/`MINOR` report quality rubric |

Writing rules: keep each template's purpose, state the reason for every rule, use the workspace's real paths and IDs, replace every `{{…}}`, delete every `<!-- GEN … -->`, keep `SKILL.md` < 115 lines and each reference < 200 lines.

## Step 6 — Wire

1. Add a pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Test reports
   Test runs are reported per `.agents/skills/quality-reporting/SKILL.md`.
   ```
2. Offer to link `.agents/skills/quality-reporting/SKILL.md` from the tester / Quality Engineer role file.

## Step 7 — Trial Run

Follow [../../core/trial-run.md](../../core/trial-run.md). Trial scenarios:
- Write a report where 2 cases are `BLOCKED` by an unavailable external provider and 1 failed with a `MAJOR` defect — verify the verdict is `CHANGES_REQUESTED` (not `ACCEPTED`) and limitations are listed at the top.
- Every case passed (`PASS`), 0 `BLOCKER`/`MAJOR` defects, but one external provider was stubbed — verify the stub is explicitly declared under `Limitations`.
- Write a Round 2 re-test report after a fix — verify Round 1 remains visible in the re-test history table with both revision SHAs.

## Step 8 — Description & Step 9 — Verify, Record & Report

1. Finalize the generated `SKILL.md` frontmatter description (workspace name, reporting triggers, double-quoted YAML string).
2. Verify against [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md), and record provenance ([../../core/provenance.md](../../core/provenance.md)).

## Update Mode & Changing This Generator

- Existing workspace reporting conventions: registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); unregistered → adopt ([../../core/existing-project.md](../../core/existing-project.md): preserve workspace paths and IDs).
- Generator updates follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- [references/base-rules.md](references/base-rules.md) — `RP1`–`RP12` mandatory compliance rules and reasons
- [references/report-template.md](references/report-template.md) — stack-agnostic report template
- [checklist.md](checklist.md) — verification checklist
