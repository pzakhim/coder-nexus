---
name: create-code-review-skill
description: Write a workspace's own code-review skill from the skill-factory knowledge base - the Code Reviewer's process and stack rubric - review a fixed revision read-only, run bug-hunt first, then grade each review axis (plan and scope, architecture, code quality, adversarial tests, security, contract/UI/migrations) against the workspace's own skills and gates, rerun checks independently, trace acceptance criteria, write findings with unified BLOCKER/MAJOR/MINOR severity and fix direction, decide APPROVED / CHANGES_REQUESTED / BLOCKED, handle rounds and escalation - for any stack. Use whenever the user wants to set up, standardize or update how the reviewer agent reviews code in a workspace, or says things like "tạo skill code review", "quy trình review", "reviewer chấm thế nào", even if they do not say "skill". Writes .agents/skills/code-review/, then trial-runs it on a real diff.
argument-hint: "[stack/framework] [review process]"
---

# Create Code Review Skill

Goal: produce `<workspace>/.agents/skills/code-review/` — how the Code Reviewer reviews one revision in this workspace: fixed revision scope, order of passes, deterministic gates and validators, review axes graded against the workspace's own rubric skills, findings, verdicts, rounds, and the revision-bound report.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/reviewer-skill-family.md` — `code-review` owns the stack rubric, validators, and verdict criteria; the Engineering skills are the rubrics; `bug-hunt` is the cold defect pass.

## Step 1 — Context Card (+ review process)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing review skills / roles | `.agents/skills/*review*`, `.agents/agents/*reviewer*`, `AGENTS.md` review sections |
| Rubric skills present | `clean-architecture`, `clean-code`, `code-simplification`, `unit-testing`, `secure-coding-standards`, `bug-hunt`, plus domain/stack skills — and their gates |
| Inputs a review receives | Handoff format, plan/phase files, acceptance criteria IDs, locked decisions (`D-NN`), approved contracts/designs |
| Gates and validators | Architecture validators, boundary scripts, static analyzers, typecheckers, test suites, contract/migration checks, visual checks |
| Vocabulary | Verdict words (`APPROVED`, `CHANGES_REQUESTED`, `BLOCKED`), finding IDs (`RV-NN`), unified severities (`BLOCKER` / `MAJOR` / `MINOR`), report location, rounds/escalation rules |
| Base inputs (read-only) | [references/base-rules.md](references/base-rules.md) and [references/deriving-the-model.md](references/deriving-the-model.md) |

## Step 2 — Map the base rules

Read [references/base-rules.md](references/base-rules.md) and [references/deriving-the-model.md](references/deriving-the-model.md). Every rule `R1`–`R14` is mandatory compliance and is adapted to the workspace's stack, validators, commands, and report location.

## Step 3 — Propose

- **Review axes & validators:** each axis with what to check, the linked rubric skill (or fallback checklist), the deterministic gate command (`PASS` / `FAIL`), and typical blocking findings.
- **Severity and verdict mapping:** unified `BLOCKER` / `MAJOR` / `MINOR` finding scale and the exact `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED` criteria list.
- **Rounds & escalation:** delta review after a fix, which checks rerun, no reviewer waivers (`PLAN_CONFLICT` routing), and escalation after the 3rd review round.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) review axes and their gate commands/validators, (2) severity scale and verdict criteria, (3) rounds and escalation, (4) report location and handoff.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Write a cohesive 3-reference skill under `.agents/skills/code-review/`:

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | Order of passes, CLI/validator gates, `R1`–`R14` index, verdict summary, and routing table (< 150 lines) |
| `references/01-scope-gates-and-validators.md` | [templates/references/01-scope-gates-and-validators.md.tmpl](templates/references/01-scope-gates-and-validators.md.tmpl) | **Mandatory** | Fixed revision, read-only rule, order of passes, preparation/phase gates, architecture validators, and cross-boundary checks |
| `references/02-review-axes-and-rubric.md` | [templates/references/02-review-axes-and-rubric.md.tmpl](templates/references/02-review-axes-and-rubric.md.tmpl) | **Mandatory** | What each review axis checks, which rubric skill grades it, which gate proves it, and AC/test anti-tamper rules |
| `references/03-findings-verdict-and-report.md` | [templates/references/03-findings-verdict-and-report.md.tmpl](templates/references/03-findings-verdict-and-report.md.tmpl) | **Mandatory** | Unified `BLOCKER`/`MAJOR`/`MINOR` finding rows, no-waiver / `PLAN_CONFLICT` rules, verdict thresholds, 3-round cap, delta re-review, and revision-bound report |

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
- A diff whose tests are happy-path only — is it `CHANGES_REQUESTED` with the missing negative/error cases named?
- A diff that breaks a dependency rule with a convincing reason in the handoff — does the reviewer refuse to waive it (`R7`)?
- A diff where a required gate cannot run — is the verdict `BLOCKED`, not `APPROVED` (`R6`)?

Compare: `bug-hunt` first, fixed revision, gates rerun, rubric skills used, findings actionable (`BLOCKER`/`MAJOR`/`MINOR`), verdict per criteria.

## Step 8 — Description

Per the authoring guide: workspace name; situations (review a phase/PR/diff, re-review after fixes, "is this ready to merge"); team trigger words. Should not trigger for writing code.

## Step 9 — Verify, record & report

[checklist.md](checklist.md) + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report rules adapted, trial results.

## Update mode

Existing `.agents/skills/code-review/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep axes, finding IDs, verdict words, report location).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- [references/base-rules.md](references/base-rules.md) — `R1`–`R14` mandatory rules, `PASS`/`FAIL` verification gates, and `BLOCKER`/`MAJOR`/`MINOR` severities
- [references/deriving-the-model.md](references/deriving-the-model.md) — how to derive review axes, rubric links, and validators for any stack
- `templates/` — `SKILL.md.tmpl` and `templates/references/01..03.md.tmpl`
- [checklist.md](checklist.md) — topic checks
