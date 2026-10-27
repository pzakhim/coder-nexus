---
name: create-clean-code-skill
description: Write a workspace's own clean-code skill from the skill-factory knowledge base - deterministic CLI gates, naming conventions, size thresholds, error handling and logging, types/constants/comments, dead and debug code, self-check commands, and unified review severities - for any stack. Use whenever the user wants to set up, standardize, or update coding standards or conventions for a workspace, or says things like "tạo skill clean code", "chuẩn đặt tên", "quy chuẩn code", "coding convention", even if they do not say "skill". Detects existing conventions and linters, gets naming and thresholds confirmed, writes .agents/skills/clean-code/, then trial-runs it on real code.
argument-hint: "[stack] [existing style guide or linter]"
---

# Create Clean Code Skill

Goal: produce `<workspace>/.agents/skills/clean-code/` — how the Code Writer writes each unit in this workspace (deterministic CLI tool gates, naming, size thresholds, errors, types, comments, self-checks) and how reviewers grade violations (`BLOCKER` / `MAJOR` / `MINOR`).

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership within the skill family: `~/.claude/skill-factory/core/coder-skill-family.md` — `clean-code` owns naming and size thresholds; `clean-architecture` owns placement; on conflict, architecture and workspace decisions win.

## Step 1 — Context Card (+ conventions)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Existing style skills/docs | `.agents/skills/clean-code`, `code-simplification`, `docs/standards/*`, `CONTRIBUTING.md`, `AGENTS.md` |
| Formatter / linter / type checker configs | Workspace linter, formatter, static analyzer, complexity checker, and type-checker configuration files |
| Gates that already enforce code rules | Automated architecture/clean-code tests, CI lint steps, and check scripts |
| Real naming in use | 10–20 file, type/class, and function names across layers, to infer conventions instead of imposing new ones |
| Module-level state, helpers, and exports | Top-level assignments, generic `utils`/`helpers`/`common` files, package entry/barrel files, and the language's file-private visibility convention (C15–C17) |
| Domain glossary | Glossary in docs/notes; recurring business terms in code |
| Base inputs (read-only) | `references/base-rules.md` and `references/discovery-and-checks.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule C1–C17, decide: already enforced by a CLI gate (cite it), adopted as written, adapted to the workspace's contract, or "not adopted" with a stated reason. Mandatory rules (C1, C3, C4, C10, C11, C14, C15, C16, C17) are never "not adopted". For C15–C17, take the language's private convention, entry-file names, and real export lists from the workspace before proposing.

## Step 3 — Propose

Using `references/discovery-and-checks.md`:
- **Naming:** a table built from the real names sampled in Step 1 covering each symbol category (File/Module, Type/Class, Function/Method, Boolean, Variable, Constant/Enum, Private symbol, Test). Where code is inconsistent, propose one canonical rule and list the drift.
- **Thresholds:** existing configured numbers if found; otherwise defaults (function ≤ ~30 lines, file ≤ ~300 lines, ≤ 3 parameters, nesting ≤ 2) for **new or modified** code.
- **Errors & logging:** the workspace's error/result contract, boundary translation, lifecycle/disposal rules, and structured logger.
- **Self-check:** the 5 standard CLI gates (Formatter, Static Linter & Complexity, Type Checker, `rg` Pattern Audit, Unit Tests) derived from real workspace configs.

## Step 4 — Gate (user confirms)

One confirmation round where possible: (1) naming table, (2) size thresholds, (3) error/logging policy, (4) CLI self-check commands (`PASS`/`FAIL`) and `BLOCKER`/`MAJOR`/`MINOR` review grading.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Deterministic tool gates (`PASS`/`FAIL`) and mandatory design principles on one screen |
| `references/01-structure-naming-and-types.md` | `templates/references/01-structure-naming-and-types.md.tmpl` | **Mandatory** | Consolidates naming, size thresholds, splitting, wrappers, globals, helper locality, exports, static types, constants, and comments |
| `references/02-errors-lifecycle-and-logging.md` | `templates/references/02-errors-lifecycle-and-logging.md.tmpl` | **Mandatory** | Specific error handling, boundary translation, pure import/render lifecycle, resource disposal, and structured logging |
| `references/03-self-check-and-review.md` | `templates/references/03-self-check-and-review.md.tmpl` | **Mandatory** | Deterministic CLI commands (`PASS`/`FAIL`) and unified review severity (`BLOCKER`/`MAJOR`/`MINOR`) |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific contracts (`imespro`, `external-structured`, `external-standard`) synced into `references/` and linked at `<!-- {{profile_references}} -->` |

Writing rules: keep each template's purpose, give every rule its reason, real names and commands only, rules already enforced by a gate cite the gate instead of repeating it, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Clean code
   Code written or changed here follows `.agents/skills/clean-code/SKILL.md`.
   ```
2. Offer to link it from the coder and reviewer role files (P3).
3. If `clean-architecture` exists: its long-file reference must **link** to this skill's thresholds (`01-structure-naming-and-types.md`) instead of repeating numbers, and `01-structure-naming-and-types.md` must link to its placement steps. Offer to fix either link (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:
- Write a new use case or component for a realistic feature (names, size, errors).
- Review one real, long or messy function from the workspace and list findings with `BLOCKER` / `MAJOR` / `MINOR` severities.
- Split one of the longest real files: are the pieces found by responsibility and named per `01`, and is placement handed to `clean-architecture` (or the fallback)?
- Add error handling to a real call that can fail (does the plan follow the error contract and avoid swallowing?).

## Step 8 — Description

Per the authoring guide: workspace name; concrete situations (writing or changing code, naming, reviewing, "is this too long"); team trigger words. Should not trigger for pure architecture placement questions ("where does this file go") — that belongs to `clean-architecture`.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, naming drift found, trial results.

## Update mode

Existing `.agents/skills/clean-code/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace rule IDs, gates, and `rg` checks).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — Universal C1–C17 rules, rationale, target files, and unified `BLOCKER`/`MAJOR`/`MINOR` severity scale
- [Discovery & Checks](references/discovery-and-checks.md) — Stack-neutral naming taxonomy and the 5 standard CLI verification & `rg` audit gates
- `~/.claude/skill-factory/core/splitting-protocol.md` — Who decides what when splitting; fallback without `clean-architecture`
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — Topic verification checks
