---
name: create-bug-hunt-skill
description: Write a workspace's own bug-hunt skill from the skill-factory knowledge base - finding real defects in a fixed code revision - scope and callers, a cold pass, seven defect dimensions, adversarial disproof with given/when/then failure scenarios, effort levels, severity, report format and verdict impact, plus the workspace's own bug patterns (data scopes, authorization, async, migrations) - for any stack and fullstack repos. Use whenever the user wants to set up, standardize or update how the coder self-checks or the reviewer hunts bugs in a workspace, or says things like "tạo skill bug hunt", "tìm bug trước review", "self-check của coder", "review tìm lỗi", even if they do not say "skill". Writes .agents/skills/bug-hunt/, then trial-runs it on a real diff.
argument-hint: "[stack/framework] [review process]"
---

# Create Bug Hunt Skill

Goal: produce `<workspace>/.agents/skills/bug-hunt/` — how the Code Writer (quick self-check) and the Reviewer (standard/deep pass) find **real defects** in a fixed revision of this workspace, with the workspace's own bug patterns, vocabulary and report location.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — bug-hunt answers only "with which input or state does this change go wrong?"; compliance (architecture, clean-code, AC traceability) belongs to the review rubric, complexity to code-simplification.

## Step 1 — Context Card (+ review inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing review skills | `.agents/skills/bug-hunt`, `code-review*`, `*reviewer*` role files |
| Vocabulary | Finding IDs, verdict words, severity scale (e.g. `F-BR-NN`, `REQUEST_CHANGES`, `P0–P3`), where reports are written |
| Project risk areas | Data scopes (tenant/environment), authorization model, money/quantities, migrations/backfills, external providers, release/publish flows — from `CLAUDE.md`, `AGENTS.md`, architecture docs, past incidents/bug fixes in git log |
| Read-only commands | Focused tests, analyzer, caller search (`rg`, code-intelligence tools such as GitNexus if configured) |
| Base inputs (read-only) | Coder Nexus `plugins/core/skills/bug-hunt/SKILL.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/dimensions.md`, `references/bug-patterns-by-stack.md`. For each rule H1–H14: adopted, adapted (workspace vocabulary/report location), or "not adopted" with a reason. H1, H2, H6, H7, H8, H13 are never "not adopted".

## Step 3 — Propose

- **Bug patterns** per branch: stack patterns that apply + **project patterns** derived from the risk areas in Step 1 (each a one-line "looks like / goes wrong when" with a real path).
- **Effort triggers:** which items run `quick` / `standard` / `deep` here (e.g. auth, migrations, release pipeline → deep).
- **Mapping** of BLOCKER/MAJOR/MINOR and CONFIRMED/PLAUSIBLE to the workspace's finding levels and verdicts; where the report goes.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) project bug patterns, (2) effort triggers and caps, (3) severity/verdict mapping and report location, (4) roles (who runs which effort; reviewer read-only).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–05`; branched: `shared/01–04`, `be/05`, `fe/05`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The one question, the loop and the effort table on one screen |
| `references/01-scope-and-candidates.md` | `shared/01-…` | `templates/shared/01-scope-and-candidates.md.tmpl` | **Mandatory** | Fixed revision, callers, cold pass, seven dimensions — where real bugs are found |
| `references/02-verify.md` | `shared/02-…` | `templates/shared/02-verify.md.tmpl` | **Mandatory** | Disproving candidates keeps reports free of noise |
| `references/03-effort-severity-report.md` | `shared/03-…` | `templates/shared/03-effort-severity-report.md.tmpl` | **Mandatory** | Same scale and format for coder and reviewer |
| `references/04-verdict-and-roles.md` | `shared/04-…` | `templates/shared/04-verdict-and-roles.md.tmpl` | Suggested | How findings change the verdict, who does what; may merge into 03 |
| `references/05-bug-patterns.md` | `be/05-…`, `fe/05-…` | `templates/branch/05-bug-patterns.md.tmpl` | **Mandatory** | The workspace's own failure modes — the part generic advice cannot supply |

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
- A diff with a seeded realistic defect (described to the subagent as a normal change, e.g. a missing scope filter or an un-awaited call) — is it found and CONFIRMED with a scenario?
- A diff with no defect — does the agent report "no defect found" instead of style remarks?

Compare: every finding has a given/when/then scenario and evidence, verdict classes used correctly, cleanups kept out, project patterns applied.

## Step 8 — Description

Per the authoring guide: workspace name; situations (before handing off a phase, reviewer first pass, "find bugs in this diff"); team trigger words. Should not trigger for style/compliance review requests.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations, rules adapted/not adopted, project patterns added, trial results.

## Update mode

Existing `.agents/skills/bug-hunt/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep vocabulary, report location, project pattern file).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — H1–H14 with reasons
- `references/dimensions.md` — the seven defect dimensions with prompts
- `references/bug-patterns-by-stack.md` — stack patterns + how to derive project patterns
- `templates/` — `SKILL.md.tmpl`, `shared/01–04`, `branch/05` (suggested shapes)
- `checklist.md` — topic checks
