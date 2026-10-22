---
name: create-requirements-specification-skill
description: Write a workspace's own requirements-specification skill from the skill-factory knowledge base - how the Spec Writer reads this workspace's requirement sources, which questions to ask per grilling dimension, which edge cases are mandatory for its domain, how business rules and acceptance criteria are written in its style, how changes (ADDED / MODIFIED / REMOVED) and bugs are specified, and what the Gate 1 review asks about the spec text - inside the fixed grilling process, gate-review spec mode and requirements.md template, for any domain and any stack. Use whenever the user wants to set up, standardize or update how requirements, specs, business rules or acceptance criteria are written in a workspace, or says things like "tạo skill viết spec", "chuẩn viết requirements", "viết AC thế nào", "hỏi gì khi làm spec", even if they do not say "skill". Writes .agents/skills/requirements-specification/, then trial-runs it on real tickets.
argument-hint: "[tracker] [language]"
---

# Create Requirements Specification Skill

Goal: produce `<workspace>/.agents/skills/requirements-specification/` — where requirements come from in this workspace, what the Spec Writer asks, which edge cases it never skips, how BR, AC and change deltas read here, and what the Gate 1 review asks. It works inside the fixed `grilling` process, `gate-review` spec mode and `requirements.md` template; it never changes their gates, laws or validated sections.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0**. Ownership and the generic-vs-specific rule: `~/.claude/skill-factory/core/planning-skill-family.md`. Domain terms come from `.agents/skills/domain-knowledge/` when it exists; otherwise suggest running `create-domain-knowledge-skill` first and continue with terms marked `OPEN`.

## Step 1 — Context Card (+ requirement sources)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Then collect, read-only (`references/detection.md`):

| Field | Where to look |
|---|---|
| Past specs | `.superpowers/work-items/*/v*/requirements.md`, `docs/features/**`, other spec folders — approved ones are style samples |
| Requirement sources | Tracker (Huly, Jira, Linear…) and how tickets are written; parent/child structure; attached documents; design tools |
| Acceptance style | How AC are written today (Given/When/Then, checklists, tables), IDs, language |
| Review findings | Gate 1 feedback, review comments and QA defects on past specs — vague words, synonyms, recurring gaps |
| Past deltas | `change-impact.md` of delivered `v2+` items — how AC changes were classified |
| Domain skill | `.agents/skills/domain-knowledge/` (terms, entities, roles × scopes) |
| Quality skills | `.agents/skills/quality-planning/` — testability expectations |
| Git skill | `.agents/skills/git-workflow/` or the fixed `git-preflight` — where bugs are found (DEV/STG/PROD) |
| Language | Team language for user-facing documents |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/edge-case-catalog.md`. For each rule RS1–RS10: adopted, adapted, or "not adopted" with a reason. RS5 (glossary terms verbatim), RS9 (fixed process unchanged) and RS10 (delta for change jobs) are never "not adopted". From the catalog keep only the categories the workspace really has.

## Step 3 — Propose

- Source map: each kind of requirement, where it comes from, how it is read, known unreachable sources.
- Question bank per `grilling` dimension, written with the workspace's terms and real examples from past tickets.
- Mandatory edge cases for this workspace, each with one real example.
- One BR and two AC rewritten from a past approved spec in the proposed style, plus one success signal.
- Vague words found in past specs and review comments, each with what replaces it.
- One past change re-written as an ADDED / MODIFIED / REMOVED delta (when the workspace has a delivered `v2+`).
- Gate 1 review questions per job type, tagged `[Gap]` / `[Ambiguity]` / `[Conflict]`, from real past review findings.

## Step 4 — Gate (user confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Requirement sources and their priority when they conflict | Tracker ticket + its documents, then the user's words |
| Q2 | The sample BR/AC, success signal and vague-word list | As drafted from a past approved spec |
| Q3 | Mandatory edge-case categories | The categories found in Step 1 |
| Q4 | Language of user-facing documents | Team language; code names in English |

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Layout: **flat**.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | What this skill adds to grilling, on one screen |
| `references/01-sources-intake.md` | `templates/01-sources-intake.md.tmpl` | **Mandatory** | A correct Source Inventory from the first turn |
| `references/02-question-bank.md` | `templates/02-question-bank.md.tmpl` | **Mandatory** | The right questions, in the domain's words |
| `references/03-mandatory-edge-cases.md` | `templates/03-mandatory-edge-cases.md.tmpl` | **Mandatory** | Defects hide in the domain's familiar edge cases |
| `references/04-writing-rules-and-ac.md` | `templates/04-writing-rules-and-ac.md.tmpl` | **Mandatory** | BR, AC and deltas that QA can test and the user can read |
| `references/05-gate-review-questions.md` | `templates/05-gate-review-questions.md.tmpl` | **Mandatory** | The workspace part of `gate-review` spec mode: knowing when to stop asking |

Writing rules: examples from the workspace's own tickets and approved specs (never invented domain content); every rule with its reason; replace every `{{…}}`, delete every `<!-- GEN … -->`, English body (question phrasing may be in the team language), < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Requirements
   Specs follow `.agents/skills/requirements-specification/SKILL.md` inside the Coder Nexus grilling process.
   ```
2. Offer to link it from `domain-knowledge` and `quality-planning` (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Take two tickets this workspace already delivered (one feature, one bug). Compare with and without the skill: questions asked, edge cases covered, AC quality, vague words caught, what the Gate 1 review questions find. If the workspace has a delivered `v2+`, also re-write its delta. Never write into the real work items.

## Step 8 — Description

Per the authoring guide: workspace name; situations (new ticket, writing requirements, AC, business rules, bug reports, Gate 1); the team's trigger words. Should not trigger for implementation or test execution.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report rules adapted or not adopted, categories dropped from the catalog, trial results.

## Update mode

Existing `.agents/skills/requirements-specification/` or a workspace spec guide: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep the team's AC style, IDs and checklists verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — RS1–RS10 with reasons, job types
- `references/edge-case-catalog.md` — generic edge-case categories to keep or drop
- `references/detection.md` — where sources, past specs and AC style are found
- `templates/` — `SKILL.md.tmpl`, `01–05` (suggested shapes)
- `references/sources.md` — external sources and ideas not adopted
- `checklist.md` — topic checks
