---
name: create-requirements-specification-skill
description: "Write a workspace's own requirements-specification skill from the skill-factory knowledge base - how the Spec Writer reads requirement sources, which questions to ask per grilling dimension, which edge cases are mandatory, how observable BR-NN and AC-NN are written, how v2+ changes (ADDED / MODIFIED / REMOVED) and bugs are specified, and how Gate 1 reviews and verifies the spec (PASS/FAIL CLI gates and BLOCKER/MAJOR/MINOR findings) - for any domain and any stack. Use whenever the user wants to set up, standardize, or update how requirements, specs, business rules, or acceptance criteria are written, or says 'tạo skill viết spec', 'chuẩn viết requirements', 'viết AC thế nào', 'hỏi gì khi làm spec'."
argument-hint: "[tracker] [language]"
---

# Create Requirements Specification Skill

Goal: produce `<workspace>/.agents/skills/requirements-specification/` — where requirements come from in this workspace, what the Spec Writer asks per `grilling` dimension, which edge cases are mandatory, how observable `BR-NN`, `AC-NN`, and `v2+` change deltas read here, and how Gate 1 verifies the specification (`PASS` / `FAIL` CLI gates and `BLOCKER` / `MAJOR` / `MINOR` review severities). It operates inside the fixed `grilling` process, `gate-review` spec mode, and `requirements.md` template without altering their gates, laws, or validated sections.

User input: $ARGUMENTS

Follow [../../core/workflow.md](../../core/workflow.md), starting with **Step 0**. Ownership and generic-vs-specific boundary: [../../core/planning-skill-family.md](../../core/planning-skill-family.md). Domain terms come from `.agents/skills/domain-knowledge/` when it exists; otherwise suggest running `create-domain-knowledge-skill` first and continue with terms marked `OPEN`.

## Step 1 — Context Card (+ requirement sources)

Run the core Context Card ([../../core/detect-stack.md](../../core/detect-stack.md)) and existing-project discovery ([../../core/existing-project.md](../../core/existing-project.md)). Then collect, read-only ([references/detection.md](references/detection.md)):

| Field | Where to look |
|---|---|
| Past specs | `.superpowers/work-items/*/v*/requirements.md`, `docs/features/**`, other spec folders — approved ones are style samples |
| Requirement sources | Tracker (Huly, Jira, Linear…) and how tickets are written; parent/child structure; attached documents; design tools |
| Acceptance style | How `AC-NN` are written today (Given/When/Then, checklists, tables), IDs, language |
| Review findings | Gate 1 feedback, review comments, and QA defects on past specs — vague words, synonyms, recurring gaps |
| Past deltas | `change-impact.md` of delivered `v2+` items — how `BR-NN` and `AC-NN` changes were classified |
| Domain skill | `.agents/skills/domain-knowledge/` (terms, banned synonyms, entities, roles × scopes) |
| Quality skills | `.agents/skills/quality-planning/` — testability expectations |
| Git skill | `.agents/skills/git-workflow/` or the fixed `git-preflight` — where bugs are found (`DEV` / `STG` / `PROD`) |
| Language | Team language for user-facing documents; code symbols in English |

## Step 2 — Map the Base Rules (`RS1`–`RS10`, Mandatory Compliance)

Read [references/base-rules.md](references/base-rules.md) and [references/edge-case-catalog.md](references/edge-case-catalog.md). Every rule `RS1`–`RS10` is **mandatory compliance** and must be adapted to the workspace's real sources, terms, and examples. From the edge-case catalog, keep every category the workspace actually has and list inapplicable ones explicitly with a reason.

## Step 3 — Propose

- **Source map (`RS1`):** each kind of requirement, where it comes from, how it is read, conflict priority, and known unreachable sources.
- **Question bank (`RS2`, `RS8`, `RS9`):** questions per `grilling` dimension in the workspace's terms with real ticket examples, linked to `G-NN`.
- **Mandatory edge cases (`RS3`):** kept catalog categories, each with one real example from this workspace.
- **Writing rules (`RS4`, `RS5`, `RS7`, `RS10`):** one `BR-NN` and two `AC-NN` rewritten from a past approved spec, one measurable `G-NN` success signal, banned vague-word replacement table, verbatim `domain-knowledge` term enforcement, bug spec fields, and one `v2+` delta (`ADDED` / `MODIFIED` / `REMOVED`).
- **Gate 1 review & CLI verification (`RS6`):** Gate 1 questions per job type tagged `[Gap]` / `[Ambiguity]` / `[Conflict]` and graded `BLOCKER` / `MAJOR` / `MINOR`, plus binary `PASS` / `FAIL` CLI checks (`validate_proposal_spec` and `rg` audits).

## Step 4 — Gate (User Confirms)

AskUserQuestion, ≤ 4 questions per round, recommendation first:

| # | Question | Default proposal |
|---|---|---|
| Q1 | Requirement sources and priority when they conflict | Tracker ticket + attached documents, then the user's explicit statements |
| Q2 | Sample `BR-NN` / `AC-NN`, measurable `G-NN` signal, and banned vague-word table | As drafted from a past approved spec |
| Q3 | Mandatory edge-case categories and `v2+` delta conventions | Categories found in Step 1 + `ADDED` / `MODIFIED` / `REMOVED` behavior deltas |
| Q4 | Team language for user-facing docs and Gate 1 `PASS`/`FAIL` + `BLOCKER`/`MAJOR`/`MINOR` gates | Team language with English code names; standard CLI and review gates |

## Step 5 — Author

Read [../../core/authoring-guide.md](../../core/authoring-guide.md). Consolidate into `SKILL.md` and 3 cohesive reference files:

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Deterministic `PASS`/`FAIL` CLI gates, mandatory `RS1`–`RS10` principles, and reference routing on one screen |
| `references/01-sources-and-grilling-questions.md` | `templates/references/01-sources-and-grilling-questions.md.tmpl` | **Mandatory** | Source intake map, conflict priority, `grilling` question bank linked to `G-NN`, language rule, and fixed process (`RS1`, `RS2`, `RS8`, `RS9`) |
| `references/02-edge-cases-and-writing-rules.md` | `templates/references/02-edge-cases-and-writing-rules.md.tmpl` | **Mandatory** | Mandatory domain edge cases, observable `BR-NN`/`AC-NN`, banned vague words, verbatim glossary terms, bug specs, and `v2+` deltas (`RS3`–`RS5`, `RS7`, `RS10`) |
| `references/03-gate-review-and-verification.md` | `templates/references/03-gate-review-and-verification.md.tmpl` | **Mandatory** | Gate 1 review questions per job type (`[Gap]`/`[Ambiguity]`/`[Conflict]`, `BLOCKER`/`MAJOR`/`MINOR`) and deterministic `PASS`/`FAIL` CLI gates (`RS6`) |

Writing rules: use real workspace examples, give every rule its reason, replace every `{{…}}`, delete every `<!-- GEN … -->`, keep `SKILL.md` < 105 lines and each reference < ~200 lines, and preserve `<!-- {{profile_references}} -->` and the custom block.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Requirements
   Specs follow `.agents/skills/requirements-specification/SKILL.md` inside the Coder Nexus grilling process.
   ```
2. Offer to link it from `domain-knowledge` and `quality-planning`.

## Step 7 — Trial Run

Follow [../../core/trial-run.md](../../core/trial-run.md). Replay two delivered tickets (one feature, one bugfix, plus a `v2+` delta when available) read-only: compare questions asked, edge cases checked, `AC-NN` observability, vague words caught by `rg` (`PASS`/`FAIL`), and Gate 1 findings (`BLOCKER`/`MAJOR`/`MINOR`).

## Step 8 — Description

Follow [../../core/authoring-guide.md](../../core/authoring-guide.md): include workspace name, situations (new ticket, writing `requirements.md`, `BR-NN`, `AC-NN`, bug reports, Gate 1 review), and team trigger words.

## Step 9 — Verify, Record & Report

Run [checklist.md](checklist.md) and [../../core/checklist-common.md](../../core/checklist-common.md); record provenance ([../../core/provenance.md](../../core/provenance.md)); report how `RS1`–`RS10` were adapted, which edge-case categories were kept or marked inapplicable, and trial results.

## Update Mode & Changing This Generator

Existing `.agents/skills/requirements-specification/`: registered → sync ([../../core/sync-protocol.md](../../core/sync-protocol.md)); unregistered → adopt (keep the team's `AC-NN` style, IDs, and checklists verbatim). When updating this generator, follow [../../core/versioning.md](../../core/versioning.md).

## Resources

- [Base Rules](references/base-rules.md) — Mandatory `RS1`–`RS10` rules, rationale, target files, and `PASS`/`FAIL` + `BLOCKER`/`MAJOR`/`MINOR` scales
- [Edge-Case Catalog](references/edge-case-catalog.md) — Domain edge-case categories to keep or mark inapplicable
- [Detection & CLI Audits](references/detection.md) — Where requirement facts are found and deterministic `rg` checks
- [Checklist](checklist.md) — Topic verification checks
