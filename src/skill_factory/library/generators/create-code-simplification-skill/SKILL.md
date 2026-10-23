---
name: create-code-simplification-skill
description: Write a workspace's own code-simplification skill from the skill-factory knowledge base - when to simplify (after checks pass, changed code only), how to keep behavior exactly the same, a smell-to-technique catalog (delete, stdlib/native, YAGNI, rule of three, flatten, shrink) with the workspace's real examples, stop criteria and the report line - for any stack and for fullstack repos. Use whenever the user wants to set up, standardize or update how the coder agent simplifies or cleans up code in a workspace, or says things like "tạo skill simplify", "đơn giản hoá code", "giảm phức tạp", "over-engineering", even if they do not say "skill". Detects existing simplification rules, gets the catalog and stop rules confirmed, writes .agents/skills/code-simplification/, then trial-runs it on a real diff.
argument-hint: "[stack/framework]"
---

# Create Code Simplification Skill

Goal: produce `<workspace>/.agents/skills/code-simplification/` — how the Code Writer reduces a **working** diff to the simplest clear form without changing behavior, and when it must not.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — clean-code sets the rules and thresholds while writing; code-simplification is the pass on a working diff; clean-architecture and workspace decisions win over both (an abstraction a decision requires stays).

## Step 1 — Context Card (+ simplification inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing rules | `.agents/skills/code-simplification`, `clean-code`, no-wrapper rules, "ponytail"/YAGNI notes in `AGENTS.md` |
| Shortcut markers | Comment conventions for deliberate shortcuts (e.g. `ponytail: <ceiling>, <upgrade>`) |
| Gates | Wrapper/alias AST tests, lint rules for complexity, dead-code checks |
| Real examples | 3–5 spots of avoidable complexity in recent diffs or long files (single-implementation interfaces, pass-through wrappers, hand-rolled stdlib, deep nesting) — used as catalog examples |
| Base inputs (read-only) | `references/base-rules.md` (this generator's own base rules), `plugins/ponytail/skills/ponytail-review` and `ponytail-audit` |

## Step 2 — Map the base rules

Read `references/base-rules.md`, `references/smell-catalog.md`, `references/stack-notes.md`. For each rule S1–S13: enforced by a gate (cite it), adopted, adapted, or "not adopted" with a reason. S1, S2, S11, S12 are never "not adopted".

## Step 3 — Propose

- The catalog rows that matter in this workspace, each with a **real** example (path + one line) and its technique.
- Stop criteria including the workspace's decision notation (e.g. `D-NN` keeps an abstraction).
- The report line format and, if the workspace uses one, the shortcut marker convention.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) smell → technique catalog, (2) stop criteria, (3) report format and review severity (default: unnecessary complexity P2, small P3, P1 only for wrapper/decision violations).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–05`; branched: `shared/01, 02, 04, 05`, `be/03`, `fe/03`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | When to run, the loop, the rules — on one screen |
| `references/01-when-and-scope.md` | `shared/01-…` | `templates/shared/01-when-and-scope.md.tmpl` | **Mandatory** | Simplifying at the wrong time or outside the diff mixes refactors with behavior changes |
| `references/02-behavior-safety.md` | `shared/02-…` | `templates/shared/02-behavior-safety.md.tmpl` | **Mandatory** | A "simplification" that changes behavior is a bug |
| `references/03-smell-catalog.md` | `be/03-…`, `fe/03-…` | `templates/branch/03-smell-catalog.md.tmpl` | **Mandatory** | Real examples tell the agent what avoidable complexity looks like here |
| `references/04-stop-criteria.md` | `shared/04-…` | `templates/shared/04-stop-criteria.md.tmpl` | **Mandatory** | Knowing when *not* to simplify matters as much as how |
| `references/05-report.md` | `shared/05-…` | `templates/shared/05-report.md.tmpl` | Suggested | Report line and review severity; may merge into `SKILL.md` |

Writing rules: keep each template's purpose, give every rule its reason, catalog examples from real code (or marked illustrative), thresholds linked to clean-code (never repeated), replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Simplification
   After checks pass, the changed code is simplified per `.agents/skills/code-simplification/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).
3. If `incremental-implementation` exists, check its simplicity-pass step links here.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Simplify a real recent diff (from git log) — plan only: which smells, which technique, what stays.
- A spot where an abstraction exists because a workspace decision requires it — does the agent leave it?
- A simplification that would change an error path — does the agent stop?

Compare: only the diff touched, techniques match the catalog, behavior and tests untouched, stop criteria applied, report line present.

## Step 8 — Description

Per the authoring guide: workspace name; situations (after checks pass, "clean this up", "too complex", review finds unnecessary complexity); team trigger words. Should not trigger for new features or bug fixes — simplification never changes behavior.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/code-simplification/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace principles, decision notation, report line, markers).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — S1–S13 with reasons and severities
- `references/smell-catalog.md` — smell → technique tags (delete, stdlib, native, yagni, shrink, flatten, rename, inline)
- `references/stack-notes.md` — stdlib/native replacements and stack-specific smells
- `templates/` — `SKILL.md.tmpl`, `shared/01, 02, 04, 05`, `branch/03` (suggested shapes)
- `checklist.md` — topic checks
