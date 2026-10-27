---
name: create-code-simplification-skill
description: Write a workspace's own code-simplification skill from the skill-factory knowledge base - when to simplify (after checks pass, changed code only), how to keep behavior exactly the same, a smell-to-technique catalog grouped by four lenses (reuse, simplification, efficiency, altitude) with the workspace's real examples, stop criteria, the report line and unified review severities - for any stack. Use whenever the user wants to set up, standardize or update how the coder agent simplifies or cleans up code in a workspace, or says things like "tạo skill simplify", "đơn giản hoá code", "giảm phức tạp", "over-engineering", even if they do not say "skill". Detects existing simplification rules, gets the catalog and stop rules confirmed, writes .agents/skills/code-simplification/, then trial-runs it on a real diff.
argument-hint: "[stack/framework]"
---

# Create Code Simplification Skill

Goal: produce `<workspace>/.agents/skills/code-simplification/` — how the Code Writer reduces a **working** diff to the simplest clear form without changing behavior, through four lenses (**Reuse, Simplification, Efficiency, Altitude**), and when it must not.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/coder-skill-family.md` — clean-code sets the rules and thresholds while writing; code-simplification is the pass on a working diff; clean-architecture and workspace decisions win over both (an abstraction a decision requires stays).

## Step 1 — Context Card (+ simplification inputs)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing rules | `.agents/skills/code-simplification`, `clean-code`, no-wrapper rules, YAGNI notes in `AGENTS.md` |
| Shortcut markers | Comment or hand-off conventions for deliberate shortcuts (limit + upgrade path) |
| Gates | Wrapper/alias tests, complexity and dead-code lint rules, the per-step check commands |
| Real examples | 1–2 spots per lens in recent diffs or long files, found with `references/discovery-and-checks.md` §1 |
| Kept abstractions | Abstractions required by decision records or clean-architecture ports |
| Base inputs (read-only) | `references/base-rules.md`, `references/smell-catalog.md`, `references/discovery-and-checks.md`; optionally `plugins/ponytail` skills as background reading |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule S1–S14, decide: enforced by a gate (cite it), adopted, adapted to the workspace's contract, or "not adopted" with a stated reason. S1, S2, S12, S13 are never "not adopted". Rules owned by clean-code (C1 wrappers, C2 dead code, C6 thresholds) are linked, never repeated.

## Step 3 — Propose

Using `references/smell-catalog.md` and `references/discovery-and-checks.md`:
- **Catalog:** the rows that occur in this workspace, grouped by the four lenses, each with a **real** example (path + one line) or marked illustrative, plus the "already shipped" replacement table.
- **Safety and stop:** the per-step check commands, protected boundaries, behavior traps of the stack and the workspace's decision notation (e.g. `D-NN` keeps an abstraction).
- **Report:** the workspace's `simplify:` hand-off line, how skipped findings go to Concerns, and the shortcut convention if one exists.

## Step 4 — Gate (user confirms)

One confirmation round where possible: (1) catalog by lens, (2) stop criteria and per-step checks (`PASS` / `FAIL`), (3) report line and review grading (`BLOCKER` / `MAJOR` / `MINOR`, defaults in `references/base-rules.md`).

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | When to run, the loop with the four lenses, the rules — on one screen |
| `references/01-scope-and-safety.md` | `templates/references/01-scope-and-safety.md.tmpl` | **Mandatory** | Wrong timing, a reach outside the diff or a changed behavior turns a cleanup into an unreviewed feature change |
| `references/02-smell-catalog.md` | `templates/references/02-smell-catalog.md.tmpl` | **Mandatory** | Real examples per lens tell the agent what avoidable complexity looks like here |
| `references/03-report-and-review.md` | `templates/references/03-report-and-review.md.tmpl` | **Mandatory** | Report line, skipped findings and unified review severity |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific reuse contracts synced into `references/` and linked at `<!-- {{profile_references}} -->` |

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

- Simplify a real recent diff (from git log) — plan only: which lens and smell, which technique, what stays.
- A spot where an abstraction exists because a workspace decision requires it — does the agent leave it?
- A simplification that would change an error path, or an Altitude fix whose right depth is outside the diff — does the agent stop and record it in Concerns?

Compare: only the diff touched, findings named by lens and catalog row, behavior and tests untouched, stop criteria applied, report line present.

## Step 8 — Description

Per the authoring guide: workspace name; situations (after checks pass, "clean this up", "too complex", review finds unnecessary complexity); team trigger words. Should not trigger for new features or bug fixes — simplification never changes behavior.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, trial results.

## Update mode

Existing `.agents/skills/code-simplification/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace principles, rule IDs, decision notation, report line, markers).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — S1–S14 with reasons, target files and the unified `BLOCKER`/`MAJOR`/`MINOR` scale
- [Smell Catalog](references/smell-catalog.md) — smell → technique rows by lens (Reuse, Simplification, Efficiency, Altitude)
- [Discovery & Checks](references/discovery-and-checks.md) — finding real examples per lens and the per-step checks
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — topic verification checks
