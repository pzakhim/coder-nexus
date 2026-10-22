---
name: create-code-review-skill
description: Write a workspace's own code-review skill from the skill-factory knowledge base - the Code Reviewer's process - review a fixed revision read-only, run bug-hunt first, then grade each axis (plan and scope, architecture, code quality, tests, security, API contract, UI, migrations) against the workspace's own skills and gates, rerun checks independently, trace acceptance criteria, write findings with severity and fix direction, decide APPROVED / CHANGES_REQUESTED / BLOCKED, handle rounds and escalation - for any stack and fullstack repos with backend and frontend branches. Use whenever the user wants to set up, standardize or update how the reviewer agent reviews code in a workspace, or says things like "tạo skill code review", "quy trình review", "reviewer chấm thế nào", even if they do not say "skill". Writes .agents/skills/code-review/, then trial-runs it on a real diff.
argument-hint: "[stack/framework] [review process]"
---

# Create Code Review Skill

Goal: produce `<workspace>/.agents/skills/code-review/` — how the Code Reviewer reviews one revision in this workspace: scope, order of passes, axes graded against the workspace's own skills and gates, findings, verdicts, rounds and the report.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/reviewer-skill-family.md` — code-review owns the process and the verdict; the Engineering skills are the rubrics; bug-hunt is the first pass.

## Step 1 — Context Card (+ review process)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing review skills / roles | `.agents/skills/*review*`, `.agents/agents/*reviewer*`, `AGENTS.md` review sections |
| Rubric skills present | clean-architecture, clean-code, unit-testing, secure-coding-standards, database-migrations, bug-hunt — and their gates |
| Inputs a review receives | Handoff format, plan/phase files, acceptance criteria IDs, decisions (`D-NN`), goals |
| Gates and validators | Architecture tests, boundary scripts, analyzers, test suites, contract checks, visual checks |
| Vocabulary | Verdict words, finding IDs and severities, report location, rounds/escalation rules |
| Base inputs (read-only) | Coder Nexus `plugins/core/agents/code_reviewer.md`, `plugins/packs/<stack>/skills/code-review/SKILL.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/axes.md`. For each rule R1–R14: adopted, adapted to the workspace vocabulary, or "not adopted" with a reason. R1, R2, R3, R6, R7, R10 are never "not adopted".

## Step 3 — Propose

- **Axes per branch**, each with: what to check, the rubric skill (or fallback checklist), the gate command, typical blocking findings.
- **Severity and verdict mapping** to the workspace's words; the `APPROVED` criteria list.
- **Rounds:** delta review after a fix, which checks rerun, escalation after the third return of the same finding.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) axes per branch and their gates, (2) severity scale and verdict criteria, (3) rounds and escalation, (4) report location and handoff.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–05`; branched: `shared/01, 03, 04, 05`, `be/02`, `fe/02`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The order of passes and the verdict rules on one screen |
| `references/01-scope-and-order.md` | `shared/01-…` | `templates/shared/01-scope-and-order.md.tmpl` | **Mandatory** | A review of the wrong tree or in the wrong order proves nothing |
| `references/02-review-axes.md` | `be/02-…`, `fe/02-…` | `templates/branch/02-review-axes.md.tmpl` | **Mandatory** | What each axis checks, which skill grades it, which gate proves it |
| `references/03-findings-and-severity.md` | `shared/03-…` | `templates/shared/03-findings-and-severity.md.tmpl` | **Mandatory** | Findings the writer can act on, graded on one scale |
| `references/04-verdicts-and-rounds.md` | `shared/04-…` | `templates/shared/04-verdicts-and-rounds.md.tmpl` | **Mandatory** | Clear criteria stop negotiation and endless rounds |
| `references/05-report.md` | `shared/05-…` | `templates/shared/05-report.md.tmpl` | Suggested | Report template and location; may merge into 04 |

Writing rules: keep each template's purpose, give every rule its reason, link rubric skills instead of repeating them, real gate commands, workspace vocabulary kept (P5), replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Code review
   Reviews follow `.agents/skills/code-review/SKILL.md`.
   ```
2. Offer to link it from the reviewer role files (P3).
3. If `bug-hunt` exists, check its reviewer effort levels match the ones named here.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Review a real recent diff — list findings per axis and a verdict (plan only).
- A diff whose tests are happy-path only — is it CHANGES_REQUESTED with the missing cases named?
- A diff that breaks a dependency rule with a convincing reason in the handoff — does the reviewer refuse to waive it?
- A diff where a gate cannot run — is the verdict BLOCKED, not APPROVED?

Compare: bug-hunt first, fixed revision, gates rerun, rubric skills used, findings actionable, verdict per criteria.

## Step 8 — Description

Per the authoring guide: workspace name; situations (review a phase/PR/diff, re-review after fixes, "is this ready to merge"); team trigger words. Should not trigger for writing code.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/code-review/` or another review skill (e.g. `code-review-and-quality`): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep axes, finding IDs, verdict words, report location).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — R1–R14 with reasons
- `references/axes.md` — the review axes, rubric skills, gates and typical blocking findings (backend / frontend)
- `templates/` — `SKILL.md.tmpl`, `shared/01, 03, 04, 05`, `branch/02` (suggested shapes)
- `checklist.md` — topic checks
