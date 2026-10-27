---
name: create-clean-architecture-skill
description: Write a workspace's own clean-architecture skill from the skill-factory knowledge base - deterministic boundary gates, folder layout, layer responsibilities, dependency direction, DI composition, how to add a feature, and how to split oversized files - for any stack. Use whenever the user wants to set up, standardize, document, or update the architecture or folder structure of a workspace, or says things like "tạo skill clean architecture", "chuẩn hoá cấu trúc thư mục", "kiến trúc cho project này", "folder structure", even if they do not say "skill". Inspects real layout and boundaries, gets the folder tree confirmed, writes .agents/skills/clean-architecture/, then trial-runs it on real tasks.
argument-hint: "[stack] [short project description]"
---

# Create Clean Architecture Skill

Goal: produce `<workspace>/.agents/skills/clean-architecture/` — a skill **owned by the workspace** that codifies its confirmed folder tree, layer boundaries, dependency direction, DI wiring, feature addition steps, and file-splitting rules.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership within the skill family: `~/.claude/skill-factory/core/coder-skill-family.md` — `clean-architecture` owns module structure, layer boundaries, and where split pieces land; `clean-code` owns naming and size thresholds.

## Hard rules

1. **Folder-tree gate:** Do NOT create or modify any file in the workspace before the user confirms the folder tree in Step 4.
2. **Tailored to the workspace:** Use the real project name, real feature/domain names, and the real stack. Never paste a generic unverified tree.
3. **Evidence-based:** Ground every proposal in `references/base-rules.md`, `references/discovery-and-structure.md`, and verified workspace code.
4. **Existing code:** Never move project code on your own. Describe the current tree, note any drift, and only migrate when the user requests it separately.
5. **Existing decisions win:** Honor related skills (`clean-code`), ADRs, and automated boundary gates already in the workspace (`~/.claude/skill-factory/core/existing-project.md`).

## Step 1 — Context Card (+ architectural inventory)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Current directory layout | Top-level source directories (`layer-first` vs. `feature-first`) and 3–7 real domain modules |
| Architecture-shaping libraries | Dependency injection / composition root, state management, persistence/ORM, routing, and error/result types |
| Existing boundary gates | Import-boundary linters, architecture validator scripts, CI checks, and existing `clean-architecture` or `clean-code` skills |
| Cross-layer imports | Sample imports across entry/delivery, application/use-case, domain, data, and core modules to verify actual dependency direction |
| Base inputs (read-only) | `references/base-rules.md` and `references/discovery-and-structure.md` |

## Step 2 — Map the base rules

Read `references/base-rules.md`. For each rule A1–A10, decide: already enforced by an automated gate (cite it), adopted as written, adapted to the workspace's contract, or "not adopted" with a stated reason. Mandatory rules (A1, A2, A3, A5, A6, A7, A8, A10) are never "not adopted".

## Step 3 — Propose

Using `references/discovery-and-structure.md`:
- **Directory tree & layer roles:** If the architecture is already established (P4), present the verified current tree and any drift; for a new or loosely structured workspace, present 2–3 tailored folder-tree options with pros/cons and recommend one.
- **Dependency matrix & boundary gates:** Define what each layer may import and never imports, plus the deterministic CLI validator/linter and `rg` boundary commands (`PASS` / `FAIL`).
- **DI, unit-of-work/state & splitting:** Document the composition root registration order, unit-of-work/state ownership, and how oversized files are split across layers (referencing `clean-code` for size thresholds).

## Step 4 — Gate (user confirms)

Ask the user to confirm: (1) the folder tree and layer roles, (2) the dependency matrix and boundary check commands (`PASS`/`FAIL`), (3) the feature addition & splitting rules and `BLOCKER`/`MAJOR`/`MINOR` review grading.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Deterministic boundary gates (`PASS`/`FAIL`) and mandatory architecture principles (A1–A10) on one screen |
| `references/01-layout-and-layer-roles.md` | `templates/references/01-layout-and-layer-roles.md.tmpl` | **Mandatory** | Confirmed folder tree, layer ownership table, naming patterns, and test tree mirror |
| `references/02-dependencies-di-and-contracts.md` | `templates/references/02-dependencies-di-and-contracts.md.tmpl` | **Mandatory** | Dependency direction matrix, boundary check commands (`PASS`/`FAIL`), DI wiring, unit-of-work/state ownership, and startup purity |
| `references/03-adding-splitting-and-review.md` | `templates/references/03-adding-splitting-and-review.md.tmpl` | **Mandatory** | Step-by-step feature addition order, splitting oversized files (`clean-code` C6 coordination), and `BLOCKER`/`MAJOR`/`MINOR` review rubric |
| `profiles/<profile>/*.md` (optional, pack skills) | — | **Suggested** | Profile-specific architecture contracts (`imespro`, `external-structured`, `external-standard`) synced into `references/` and linked at `<!-- {{profile_references}} -->` |

Writing rules: keep each template's purpose, give every rule its reason, use real workspace paths and commands only, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Architecture
   Before creating folders/files, wiring dependencies, or splitting modules, read `.agents/skills/clean-architecture/SKILL.md`.
   ```
2. Update inbound links agreed in Step 4 (P3).
3. Coordinate with `clean-code`: ensure `03-adding-splitting-and-review.md` links to `clean-code` (`01-structure-naming-and-types.md`) for size thresholds instead of duplicating numbers.

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md`. Task ideas:
- Add a new feature/module touching every required layer.
- Split one of the longest real files found in Step 1 and verify placement per `01` and `03`.
- Check an import between two existing modules against the dependency matrix in `02`.

## Step 8 — Description

Per the authoring guide: workspace name; concrete situations (creating files/folders, adding imports, wiring DI, splitting files, reviewing architecture); team trigger words.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report files written, deviations from suggested shape, and trial results.

## Update mode

Existing `.agents/skills/clean-architecture/`: registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep workspace rule IDs, gates, and custom blocks).

## Changing this generator

Bump `VERSION` and add a `CHANGELOG.md` entry with **Affects** and **Migration** (`~/.claude/skill-factory/core/versioning.md`).

## Resources

- [Base Rules](references/base-rules.md) — Universal A1–A10 architectural rules, rationale, target files, and unified `BLOCKER`/`MAJOR`/`MINOR` severity scale
- [Discovery & Structure](references/discovery-and-structure.md) — Stack-neutral layer taxonomy, dependency matrix construction, and feature addition/splitting guide
- `~/.claude/skill-factory/core/splitting-protocol.md` — `clean-code` ↔ `clean-architecture` splitting coordination
- `templates/` — `SKILL.md.tmpl` and `references/01–03.md.tmpl`
- [Checklist](checklist.md) — Topic verification checks
