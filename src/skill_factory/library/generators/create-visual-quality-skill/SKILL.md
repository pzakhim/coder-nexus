---
name: create-visual-quality-skill
description: Write a workspace's own visual-quality skill from the skill-factory knowledge base - how the Quality Engineer checks UI fidelity against the approved design - the reference (mockups, HTML design screens, design system, or the pre-change UI as baseline), a screen x state x viewport matrix captured with the same data, role and theme, screenshots saved in the workspace evidence path, a comparison checklist (layout and hierarchy, spacing, typography, design tokens, shared components, icons, UI states, responsiveness, copy, basic accessibility), deviations classified as blocking or minor with reasons, and a verdict - using the browser tool the workspace already has. Frontend only. Use whenever the user wants to set up, standardize or update visual or UI fidelity checks in a workspace, or says things like "tạo skill visual test", "so giao diện với design", "kiểm tra UI đúng mockup", even if they do not say "skill". Writes .agents/skills/visual-quality/, then trial-runs it.
argument-hint: "[where designs live] [browser tool]"
---

# Create Visual Quality Skill

Goal: produce `<workspace>/.agents/skills/visual-quality/` — how the Quality Engineer compares the implemented UI with the approved design in this workspace: which reference, which screens/states/viewports, how screenshots are captured and judged, and how deviations become a verdict. Frontend only.

User input: $ARGUMENTS

Follow `~/.claude/skill-factory/core/workflow.md`, starting with **Step 0** (never write into `.agents/plugins/coder-nexus/` or extension-regenerated role files; a workspace skill overrides the fixed skill of the same name). Ownership: `~/.claude/skill-factory/core/quality-skill-family.md` — quality-acceptance proves behavior; visual-quality proves fidelity to the approved design; quality-reporting carries both into the report.

## Step 1 — Context Card (+ design references)

Run the core Context Card (`~/.claude/skill-factory/core/detect-stack.md`) and P1–P2 (`~/.claude/skill-factory/core/existing-project.md`). Additionally collect:

| Field | Where to look |
|---|---|
| Design references | Approved mockups/screens (e.g. `design-uiux/screens/*.html`, Figma exports, `mockups/`), UI/UX spec, design system doc, approval revision |
| Design system | Tokens file (e.g. `styles/tokens.css`), shared UI components, icon set, typography |
| UI standards skills | `fe-component-uiux`, `ui-ux` or dashboard skills — rules the UI must follow |
| Browser tool | The tool confirmed in `quality-acceptance` (or detect as in its `references/tool-detection.md`) |
| Evidence rules | Where screenshots may be saved (some tools only write inside the workspace), naming |
| Viewports and themes | Target desktop/tablet/mobile sizes, light/dark |
| Visual diff tooling | Playwright `toHaveScreenshot`, pixelmatch, or none — only if installed |
| Base inputs (read-only) | Coder Nexus `visual-quality` slot skills and the UX validator docs, if available |

## Step 2 — Map the base rules

Read `references/base-rules.md` and `references/compare-checklist.md`. For each rule V1–V12: adopted, adapted, or "not adopted" with a reason. V1, V2, V10, V11, V12 are never "not adopted".

## Step 3 — Propose

- **Reference policy:** approved design first; baseline of the pre-change UI when no design exists; what "approved" means here.
- **Matrix:** screens × states × viewports × role/theme for a feature.
- **Capture:** tool operations, data and account per capture, file naming and location.
- **Comparison checklist** with the workspace's tokens, components and UI standards; blocking vs minor rules.

## Step 4 — Gate (user confirms)

One AskUserQuestion round where possible: (1) references and approval, (2) viewports/themes and the state set, (3) blocking vs minor classification, (4) baseline update rule.

## Step 5 — Author

Read `~/.claude/skill-factory/core/authoring-guide.md`. Templates are suggested shapes; **Mandatory** content is fixed. Layout: always **flat** (`references/01–04`), frontend only.

| Output | Template | Kind | Why it exists |
|---|---|---|---|
| `SKILL.md` | `templates/SKILL.md.tmpl` | **Mandatory** | Reference, matrix and verdict rule on one screen |
| `references/01-references-and-matrix.md` | `templates/01-references-and-matrix.md.tmpl` | **Mandatory** | Comparing against the wrong reference or state proves nothing |
| `references/02-capture.md` | `templates/02-capture.md.tmpl` | **Mandatory** | Like-for-like screenshots are the only fair comparison |
| `references/03-compare-checklist.md` | `templates/03-compare-checklist.md.tmpl` | **Mandatory** | Judging by dimensions, not by taste |
| `references/04-deviations-and-verdict.md` | `templates/04-deviations-and-verdict.md.tmpl` | **Mandatory** | Deviations with reasons and a clear verdict |

Writing rules: keep each template's purpose, give every rule its reason, real design paths, token names and components, replace every `{{…}}`, delete every `<!-- GEN … -->`, English, < ~200 lines per file, custom block at the end.

## Step 6 — Wire

1. Pointer in `CLAUDE.md` / `AGENTS.md` (unless an equivalent exists):
   ```markdown
   ## Visual quality
   UI fidelity to the approved design is checked per `.agents/skills/visual-quality/SKILL.md`.
   ```
2. Offer to link it from the tester / Quality Engineer role file and from the reviewer's UI axis (P3).

## Step 7 — Trial run

`~/.claude/skill-factory/core/trial-run.md` (plans only — no screenshots during the trial). Task ideas:

- Plan the visual check of a real feature with an approved design: matrix, captures, checklist.
- A feature with no design — is the pre-change UI used as baseline and stated as such?
- A deviation that a recorded decision allows — is it accepted, not flagged?

Compare: right reference, like-for-like captures, dimensions used, deviations reasoned and classified, verdict per rule.

## Step 8 — Description

Per the authoring guide: workspace name; situations (compare the UI with the design/mockup, visual regression, check a screen before release); team trigger words. Should not trigger for functional E2E.

## Step 9 — Verify, record & report

`checklist.md` + `~/.claude/skill-factory/core/checklist-common.md`; record provenance (`~/.claude/skill-factory/core/provenance.md`); report deviations from the suggested shape, rules adapted/not adopted, trial results.

## Update mode

Existing visual checks (e.g. "Check 4 — Visual fidelity"): registered → sync (`~/.claude/skill-factory/core/sync-protocol.md`); not registered → adopt (P3, P5: keep checklist items, evidence paths and references verbatim).

## Changing this generator

Follow `~/.claude/skill-factory/core/versioning.md` (work under `## Unreleased`, bump once per batch).

## Resources

- `references/base-rules.md` — V1–V12 with reasons
- `references/compare-checklist.md` — comparison dimensions and blocking examples
- `templates/` — `SKILL.md.tmpl`, `01–04` (suggested shapes)
- `checklist.md` — topic checks
