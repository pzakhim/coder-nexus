---
name: create-clean-code-skill
description: Write a workspace's own clean-code skill from the skill-factory knowledge base - naming per stack, size limits, error handling and logging, types/constants/comments, dead and debug code, self-check commands and review severities - for any stack and for fullstack repos with backend and frontend branches. Use whenever the user wants to set up, standardize or update coding standards or conventions for a workspace, or says things like "tạo skill clean code", "chuẩn đặt tên", "quy chuẩn code", "coding convention", even if they do not say "skill". Detects existing conventions and linters, gets naming and thresholds confirmed, writes .agents/skills/clean-code/, then trial-runs it on real code.
argument-hint: "[stack/framework] [existing style guide or linter]"
---

# Create Clean Code Skill

Goal: produce `<workspace>/.agents/skills/clean-code/` — how the Code Writer writes each line and function in this workspace: names, sizes, errors, types, comments, self-checks, and how reviewers grade violations.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership within the skill family: `~/.claude/skill-factory/core/coder-skill-family.md` — clean-code owns naming and size thresholds; clean-architecture owns placement; on conflict, architecture and workspace decisions win.

## Step 1 — Context Card (+ conventions)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing style skills/docs | `.agents/skills/clean-code`, `code-simplification`, `docs/standards/*`, `CONTRIBUTING.md`, `AGENTS.md` |
| Formatter / linter / type checker configs | `pyproject.toml` (`ruff`, `black`, `mypy`, `pyright`), `.eslintrc*`/`eslint.config.*`, `.prettierrc*`, `tsconfig.json` (`strict`), `analysis_options.yaml`, `.golangci.yml` |
| Gates that already enforce code rules | Architecture/clean-code tests (e.g. AST tests for debug calls, swallowed exceptions), CI lint steps, check scripts |
| Real naming in use | 10–20 file, class and function names per layer, to infer conventions instead of imposing new ones |
| Domain glossary | Glossary in docs/notes; recurring business terms in code |
| Base input (read-only) | `<coder repo>/plugins/core/skills/clean-code/SKILL.md` (Coder Nexus source) |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule C1–C14, decide: already enforced by a gate (cite it), adopted as written, adapted (workspace contract differs — e.g. a Result type instead of exceptions), or "not adopted" with a reason. Mandatory rules (C1, C3, C4, C10, C11, C14) are never "not adopted".

## Step 3 — Propose

- **Naming:** per branch, a table built from the real names found in Step 1 plus `references/naming-by-stack.md`. Where the code is inconsistent, propose one convention and list the drift.
- **Thresholds:** existing numbers if found; otherwise defaults (function ≤ ~30 lines, file ≤ ~300 lines, UI component ≤ ~150 lines, ≤ 3 parameters, nesting ≤ 2) for **new or modified** code.
- **Errors & logging:** the workspace's error contract (exceptions hierarchy, Result types, error boundaries) and logger.
- **Self-check:** commands from the real configs + `references/self-check-by-stack.md`.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) naming table per branch, (2) thresholds, (3) error/logging policy, (4) severity mapping (P1 blocking / P2 / P3) and the self-check commands.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout per `~/.claude/skill-factory/core/layouts.md` (flat: `references/01–06` + `02b`; branched: `be/01–05` + `02b`, `fe/01–05` + `02b`, `shared/06`).

| Output (flat) | Output (branched) | Template | Kind | Why it exists |
|---|---|---|---|---|
| `SKILL.md` | `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | The rule table with severities on one screen — what reviewers and coders both check |
| `references/01-naming.md` | `be/01-…`, `fe/01-…` | `templates/branch/01-naming.md.tmpl` | **Mandatory** | Names are the main documentation; one convention per branch ends naming debates |
| `references/02-size-and-structure.md` | `be/02-…`, `fe/02-…` | `templates/branch/02-size-and-structure.md.tmpl` | **Mandatory** | Thresholds owned here; clean-architecture decides where split pieces go |
| `references/02b-splitting.md` | `be/02b-…`, `fe/02b-…` | `templates/branch/02b-splitting.md.tmpl` | **Mandatory** | clean-code's half of splitting: when, which pieces, names; placement linked to clean-architecture (fallback if absent) — `~/.claude/skill-factory/core/splitting-protocol.md` |
| `references/03-errors-and-logging.md` | `be/03-…`, `fe/03-…` | `templates/branch/03-errors-and-logging.md.tmpl` | **Mandatory** | Swallowed errors are the costliest clean-code failure |
| `references/04-types-constants-comments.md` | `be/04-…`, `fe/04-…` | `templates/branch/04-types-constants-comments.md.tmpl` | Suggested | Types, magic values, comments; may merge into 02 for a small workspace |
| `references/05-self-check.md` | `be/05-…`, `fe/05-…` | `templates/branch/05-self-check.md.tmpl` | **Mandatory** | Real commands turn the rules into checks |
| `references/06-review-severity.md` | `shared/06-…` | `templates/shared/06-review-severity.md.tmpl` | Suggested | How violations are graded; may merge into `SKILL.md` |

Writing rules: keep each template's purpose, give every rule its reason, real names and commands only, rules already enforced by a gate cite the gate instead of repeating it, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Clean code
   Code written or changed here follows `.agents/skills/clean-code/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).
3. If `clean-architecture` exists: its long-file reference must **link** to this skill's thresholds instead of repeating numbers, and 02b must link to its placement steps. Offer to fix either link (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:

- Write a new use case / component for a realistic feature (names, size, errors).
- Review one real, long or messy function from the workspace and list findings with severities.
- Split one of the longest real files: are the pieces found by responsibility and named per 01, and is placement handed to clean-architecture (or the fallback)?
- Add error handling to a real call that can fail (does the plan follow the error contract, avoid swallowing?).

Compare: names match the table, thresholds respected, error contract followed, findings graded correctly, self-check commands named.

## Step 8 — Description

Per the authoring guide: workspace name; situations (writing or changing code, naming, reviewing, "is this too long"); team trigger words. Should not trigger for pure architecture questions ("where does this file go") — that is clean-architecture.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, naming drift found, trial results.

## Update mode

Existing `.agents/skills/clean-code/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace rule IDs such as C1–C10, severities and grep checks).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- `references/base-rules.md` — C1–C14 with reasons, default severity, where each goes
- `references/naming-by-stack.md` — naming conventions per stack and layer
- `references/self-check-by-stack.md` — formatter, linter, type checker and grep checks per stack
- `~/.claude/skill-factory/core/splitting-protocol.md` — who decides what when splitting; fallback without clean-architecture
- `templates/` — `SKILL.md.tmpl`, `branch/01–05` + `02b`, `shared/06` (suggested shapes)
- `checklist.md` — topic checks
