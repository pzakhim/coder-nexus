---
name: create-visual-quality-skill
description: "Write a workspace's own visual-quality skill from the skill-factory knowledge base — how agents verify UI visual fidelity against the approved design across mobile, desktop, or web targets: reference hierarchy (HTML/UIUX screens, design-tool exports, design system, or labeled pre-change baseline), Screen x State x Viewport matrix, headless golden and runtime target capture, 10-dimension comparison checklist, BLOCKER / MAJOR / MINOR deviation grading, and PASS / FAIL / BLOCKED / NOT_RUN / N/A verdicts. Writes .agents/skills/visual-quality/, then trial-runs it."
argument-hint: "[where designs live] [target runtime or golden tool]"
---

# Create Visual Quality Skill

Goal: produce `<workspace>/.agents/skills/visual-quality/` — how Code Writer, Code Reviewer, and Test Runner verify that the implemented UI matches the approved visual design across all required states (`Loading`, `Content`, `Empty`, `Error`) and viewports.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed pack skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — `quality-acceptance` proves functional behavior; `visual-quality` proves visual fidelity to the approved design; `quality-reporting` carries both into the verification report.

## Step 1 — Context Card (+ Design & Target Discovery)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to Look |
|---|---|
| **Design references** | Extracted Figma per-screen `.png` renders & `<stem>.spec.json`, `design.md` (`## UI/UX mapping`), design-system docs, and approval revision |
| **Design system & tokens** | Theme/token definitions, shared UI kit or component library, typography scale, icon set |
| **Architecture profile** | Workspace profile in `.superpowers/setup.json` (if multi-profile) |
| **Runtime UI targets** | Simulator / emulator / desktop / browser launch and screenshot commands |
| **Headless / golden diff tooling** | Headless golden screenshot runner or visual diff tool — only when installed or approved in the workspace |
| **Viewports, orientations & states** | Confirmed viewports (`.superpowers/ux/viewports.json`), portrait/landscape rules, light/dark themes, and the 4 mandatory states (`Loading`, `Content`, `Empty`, `Error`) |
| **Evidence & catalog paths** | Revision-bound evidence folder and screen catalog screenshot path |

## Step 2 — Map the Mandatory Base Rules (`V1`–`V12`)

Read `references/base-rules.md` and `references/compare-checklist.md`. All 12 rules (`V1`–`V12`) are **mandatory compliance** — map each rule to the workspace's concrete design paths, runtime targets, golden/screenshot tools, and component library. Never include a `"not adopted"` section.

## Step 3 — Propose

Present a concise proposal covering:
1. **Reference hierarchy**: Extracted Figma per-screen `.png` renders + `design.md` (`## UI/UX mapping`) first; labeled pre-change UI baseline only when the approved plan allows it.
2. **Matrix**: `Screen × State (Loading, Content, Empty, Error) × Viewport/Orientation × Theme`.
3. **Capture workflow**: Runtime target launch & screenshot commands + optional headless golden comparison workflow (`Code Writer` baseline creation vs. `Code Reviewer` visual inspection vs. `Test Runner` regression check).
4. **10-Dimension Comparison & Grading**: `BLOCKER` / `MAJOR` / `MINOR` deviation scale and `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` / `UNVERIFIED` / `N/A` gate results (`shared_contracts/flags_and_statuses.md`).

## Step 4 — Gate (User Confirms)

Confirm in one round where possible: (1) design reference hierarchy, (2) target viewports/orientations and 4 states, (3) headless golden vs. runtime capture tools, and (4) baseline update approval rules.

## Step 5 — Author (Cohesive 3-Reference Layout)

Read `~/.claude/skill-factory/core/authoring-guide.md`. Always generate a concise `SKILL.md` (< 120 lines) and **3 cohesive reference files** under `references/`:

| Output File | Template | Purpose |
|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | Routing table, `V1`–`V12` mandatory rules, 4 visual states, and `PASS` / `FAIL` verdict rules |
| `references/01-references-matrix-and-capture.md` | `templates/references/01-references-matrix-and-capture.md.tmpl` | Reference hierarchy, Screen × State × Viewport matrix, data provenance, and runtime target capture |
| `references/02-headless-and-runtime-targets.md` | `templates/references/02-headless-and-runtime-targets.md.tmpl` | Headless golden screenshot recipe and role boundaries (authoring vs. review vs. regression check) |
| `references/03-comparison-checklist-and-verdict.md` | `templates/references/03-comparison-checklist-and-verdict.md.tmpl` | 10-dimension comparison checklist, `BLOCKER` / `MAJOR` / `MINOR` deviation grading, and per-screen report |

If the target pack supports multiple workspace profiles (`imespro`, `external-structured`, `external-standard`), place profile-specific visual contracts in `profiles/<profile>/visual-quality-contracts.md` and keep `<!-- {{profile_references}} -->` in `SKILL.md`.

## Step 6 — Wire

1. Add a pointer in `CLAUDE.md` / `AGENTS.md` (unless already present):
   ```markdown
   ## Visual Quality
   UI visual fidelity across all 4 states is verified per `.agents/skills/visual-quality/SKILL.md`.
   ```
2. Offer to link it from the Reviewer and Test Runner role definitions.

## Step 7 — Trial Run

Follow `~/.claude/skill-factory/core/trial-run.md` (plan verification without mutating source files):
- Plan the visual verification matrix for a feature with an approved design across `Loading`, `Content`, `Empty`, and `Error` states.
- Verify how a `D-NN`-approved visual deviation is recorded as `ACCEPTED (D-NN)` rather than `FAIL`.

## Step 8 — Description & Metadata

Ensure YAML frontmatter quotes any description containing colons (`:`) and clearly states when the skill triggers.

## Step 9 — Verify, Record & Report

Run `checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`, record provenance (`~/.claude/skill-factory/core/provenance.md`), and report trial results.

## Resources

- `references/base-rules.md` — Mandatory rules `V1`–`V12` with reasons and placement
- `references/compare-checklist.md` — 10 comparison dimensions and `BLOCKER` / `MAJOR` / `MINOR` grading
- `templates/` — `SKILL.md.tmpl` and `templates/references/01..03-*.md.tmpl`
- `checklist.md` — Topic verification checks
