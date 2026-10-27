---
name: create-bug-hunt-skill
description: Write a workspace's own bug-hunt skill from the skill-factory knowledge base - finding real defects in a fixed code revision - scope and callers, a cold pass, seven defect dimensions, adversarial disproof with given/when/then failure scenarios, effort levels, unified BLOCKER/MAJOR/MINOR severity, report format and verdict impact, plus the workspace's own bug patterns - for any stack. Use whenever the user wants to set up, standardize or update how the coder self-checks or the reviewer hunts bugs in a workspace, or says things like "tạo skill bug hunt", "tìm bug trước review", "self-check của coder", "review tìm lỗi", even if they do not say "skill". Writes .agents/skills/bug-hunt/, then trial-runs it on a real diff.
argument-hint: "[stack/framework] [review process]"
---

# Create Bug Hunt Skill

Goal: produce `<workspace>/.agents/skills/bug-hunt/` — how the Code Writer (quick self-check) and the Reviewer (standard/deep pass) find **real defects** in a fixed revision of this workspace, with the workspace's own bug patterns, vocabulary, and report location.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — bug-hunt answers only "with which input or state does this change go wrong?"; compliance (architecture, clean-code, AC traceability) belongs to the review rubric, complexity to code-simplification.

## Step 1 — Context Card (+ review inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing review skills | `.agents/skills/bug-hunt`, `code-review*`, `*reviewer*` role files |
| Vocabulary | Finding IDs (`BH-NN`, `RV-NN`), verdict words (`APPROVED`, `REQUEST_CHANGES`, `BLOCKED`), unified severity scale (`BLOCKER` / `MAJOR` / `MINOR`), confidence (`CONFIRMED` / `PLAUSIBLE`), where reports are written |
| Project risk areas | Data scopes (tenant/environment), authorization model, money/quantities, migrations/backfills, lifecycle/state mutations, external providers, release/publish flows — from `CLAUDE.md`, `AGENTS.md`, architecture docs, past incidents/bug fixes in git log |
| Read-only commands | Focused tests, static analyzer/typechecker, caller search (`rg`, code-intelligence tools such as GitNexus if configured) |
| Base inputs (read-only) | [references/base-rules.md](references/base-rules.md) and [references/deriving-the-model.md](references/deriving-the-model.md) |

## Step 2 — Map the base rules

Read [references/base-rules.md](references/base-rules.md) and [references/deriving-the-model.md](references/deriving-the-model.md). Every rule `H1`–`H14` is mandatory compliance and is adapted to the workspace's stack, commands, and report location.

## Step 3 — Propose

- **Bug patterns:** stack patterns that apply to this workspace + **project patterns** derived from the risk areas in Step 1 (each a row: *Looks like* → *Goes wrong when* → *Check*, naming real workspace paths).
- **Effort triggers:** which items run `quick` / `standard` / `deep` here (e.g. auth, state/lifecycle boundaries, migrations, money arithmetic → `deep`).
- **Severity & verdict mapping:** unified `BLOCKER` / `MAJOR` / `MINOR` and `CONFIRMED` / `PLAUSIBLE` mapped to the workspace's finding tables and verdicts; where the report goes.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) project bug patterns, (2) effort triggers and caps, (3) severity/verdict mapping and report location, (4) roles (who runs which effort; reviewer read-only).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Write a cohesive 3-reference skill under `.agents/skills/bug-hunt/`:

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | [templates/SKILL.md.tmpl](templates/SKILL.md.tmpl) | **Mandatory** | The one question, read-only CLI gates, the 5-step loop, effort triggers, `H1`–`H14` index, and routing table (< 150 lines) |
| `references/01-scope-dimensions-and-patterns.md` | [templates/references/01-scope-dimensions-and-patterns.md.tmpl](templates/references/01-scope-dimensions-and-patterns.md.tmpl) | **Mandatory** | Fixed revision, whole context & callers, cold pass first, 7 defect dimensions, and stack/project bug patterns |
| `references/02-verify-and-disprove.md` | [templates/references/02-verify-and-disprove.md.tmpl](templates/references/02-verify-and-disprove.md.tmpl) | **Mandatory** | Adversarial disproof path tracing, `given → when → then` scenarios, read-only CLI verification, `CONFIRMED`/`PLAUSIBLE` rules, and typical disproofs |
| `references/03-severity-verdict-and-report.md` | [templates/references/03-severity-verdict-and-report.md.tmpl](templates/references/03-severity-verdict-and-report.md.tmpl) | **Mandatory** | Effort caps, `BLOCKER`/`MAJOR`/`MINOR` calibration, finding row format, `bug-hunt:` summary line, verdict impact, and Code Writer vs Reviewer duties |

Writing rules: keep each template's purpose, give every rule its reason, workspace vocabulary kept (P5), real paths in patterns, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Bug hunt
   Coders self-check and reviewers hunt defects per `.agents/skills/bug-hunt/SKILL.md`.
   ```
2. Offer to link it from the coder (quick self-check) and reviewer (standard/deep) role files (P3).
3. If `incremental-implementation` exists, check its phase-completion self bug-hunt step links here with the `quick` effort.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Bug-hunt a real recent diff at `quick` and at `standard` (plan the findings list only).
- A diff with a seeded realistic defect (described to the subagent as a normal change, e.g. a missing scope filter or an un-awaited/undisposed call) — is it found and `CONFIRMED` with a `given → when → then` scenario?
- A diff with no defect — does the agent report `bug-hunt: no defect found` instead of style remarks?

Compare: every finding has a `given → when → then` scenario and evidence, verdict classes used correctly, cleanups kept out (`NOTE`), project patterns applied.

## Step 8 — Description

Per the authoring guide: workspace name; situations (before handing off a phase, reviewer pass, "find bugs in this diff"); team trigger words. Should not trigger for style/compliance review requests.

## Step 9 — Verify, record & report

[checklist.md](checklist.md) + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report rules adapted, project patterns added, trial results.

## Update mode

Existing `.agents/skills/bug-hunt/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep vocabulary, report location, project patterns).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- [references/base-rules.md](references/base-rules.md) — `H1`–`H14` mandatory rules, `PASS`/`FAIL` verification gates, and `BLOCKER`/`MAJOR`/`MINOR` severities
- [references/deriving-the-model.md](references/deriving-the-model.md) — the 7 defect dimensions and how to derive stack/project bug patterns
- `templates/` — `SKILL.md.tmpl` and `templates/references/01..03.md.tmpl`
- [checklist.md](checklist.md) — topic checks
