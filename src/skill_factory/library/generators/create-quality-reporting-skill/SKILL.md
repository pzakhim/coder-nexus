---
name: create-quality-reporting-skill
description: Write a workspace's own quality-reporting skill from the skill-factory knowledge base - how the Quality Engineer reports a test run - revision-bound reports with the environment record, per-case results with evidence, acceptance-criteria coverage, an honest feature verdict (ACCEPTED / CHANGES_REQUESTED / BLOCKED) where NOT_RUN and BLOCKED never count as passed, defect lists with severity and re-test history, limitations such as stubbed providers, evidence hygiene without secrets, and where the report goes - in the workspace's own vocabulary and locations. Use whenever the user wants to set up, standardize or update how test results, QA reports or acceptance verdicts are written in a workspace, or says things like "tạo skill báo cáo test", "QA report", "kết quả nghiệm thu", even if they do not say "skill". Writes .agents/skills/quality-reporting/, then trial-runs it.
argument-hint: "[where results are recorded]"
---

# Create Quality Reporting Skill

Goal: produce `<workspace>/.agents/skills/quality-reporting/` — how the Quality Engineer turns a test run into a report the team can trust: what it contains, how coverage and the verdict are computed, how defects are tracked, what evidence is allowed and where the report goes.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — quality-acceptance produces per-case results and defects; this skill aggregates them into the report and the verdict.

## Step 1 — Context Card (+ reporting conventions)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Where results go | `as-built.md`, review/evidence folders (e.g. `reviews/e2e-round-NN/`), PR comments, tracker — and who writes each |
| Vocabulary | Case result words, feature verdict words, defect IDs and severity scale |
| Evidence rules | Allowed locations (e.g. inside the workspace), naming, redaction |
| Audience | Coordinator, user, docs writer — and what each needs first |
| Distribution rules | Whether reports may be posted outside the workspace and who authorises it |
| Base inputs (read-only) | Coder Nexus `plugins/core/agents/test_runner.md` (result reporting) |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/report-template.md`. For each rule RP1–RP12: adopted, adapted, or "not adopted" with a reason. RP1, RP3, RP4, RP7, RP8 are never "not adopted".

## Step 3 — Propose

- **Report structure** with the workspace's sections and locations.
- **Coverage and verdict rules:** how an AC result is derived from its cases, and the feature verdict criteria.
- **Defects:** ID, severity, status lifecycle, re-test rounds.
- **Evidence and distribution:** paths, redaction, who receives the report.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) report location and structure, (2) verdict criteria and words, (3) defect format and severity scale, (4) evidence rules and distribution.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout: **flat** (`references/01–04`) — reporting is the same for both branches; fullstack reports keep FE and BE results in separate tables.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The verdict rule and the honesty rules on one screen |
| `references/01-report-structure.md` | `templates/01-report-structure.md.tmpl` | **Mandatory** | Readers find the verdict first and the evidence behind it |
| `references/02-coverage-and-verdict.md` | `templates/02-coverage-and-verdict.md.tmpl` | **Mandatory** | A reproducible verdict from per-case results |
| `references/03-defects.md` | `templates/03-defects.md.tmpl` | **Mandatory** | Defects tracked until re-tested, not forgotten |
| `references/04-evidence-and-distribution.md` | `templates/04-evidence-and-distribution.md.tmpl` | **Mandatory** | Evidence that proves without leaking |

Writing rules: keep each template's purpose, give every rule its reason, the workspace's real locations and words, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Test reports
   Test runs are reported per `.agents/skills/quality-reporting/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file and from whoever records results (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Write the report for a run where 2 cases are BLOCKED by an unavailable provider and 1 failed — is the verdict not ACCEPTED, and are the limitations stated?
- Every case passed but one provider was stubbed — is the stub listed as a limitation?
- A re-test round after a fix — is the history shown with both revisions?

Compare: revision and environment present, AC coverage computed correctly, honest counts, verdict per criteria, no secrets in evidence, right destination.

## Step 8 — Description

Per the authoring guide: workspace name; situations (write the test report, summarise results, acceptance verdict, report defects, re-test summary); team trigger words. Should not trigger for executing tests.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing reporting conventions (e.g. evidence folders and `as-built.md` rules): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep locations, words and IDs verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — RP1–RP12 with reasons
- `references/report-template.md` — full report template
- `templates/` — `SKILL.md.tmpl`, `01–04` (suggested shapes)
- `checklist.md` — topic checks
