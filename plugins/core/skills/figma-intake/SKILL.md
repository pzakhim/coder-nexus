---
name: figma-intake
description: "Extract Figma frames/sections into W3C DTCG `tokens.json`, Framelink-normalized `<node>.spec.json`, and per-screen `.png`/`.jpg` renders (`<node>-S01.png`...), then translate them with Huly ticket flows into Gate 1 Screens (`S-NN`) and Workflows (`W-NN`) in `requirements.md` and hand off design tokens and components to Gate 2 (`planning`)."
---

# Figma & Visual Intake (`tokens.json` + `<node>.spec.json` + Screen Renders)

Convert PO-supplied Figma links and Huly ticket flows into structured Gate 1 requirements (`## Screens & Visual Sources` and `## Workflows` in `requirements.md`) and a deterministic Gate 2 design-system handoff (`tokens.json` + `<node>.spec.json` $\to$ `design.md` `## UI/UX mapping`, rule `DESIGN-008`).

## 1. End-to-End Intake & Handoff Workflow

1. **Fetch & Classify Visual Source (`spec_writer` at Stage `1A` / `1A-UX`)** ([01-screen-and-workflow-extraction.md](references/01-screen-and-workflow-extraction.md)):
   - Run `huly_get_task_detail(..., download=True)` or `coder-nexus figma fetch "<url>" --workspace-path "${workspaceFolder}" [--export-icons]` to populate `.superpowers/sources/<ISSUE-ID>/figma/`.
   - Classify the work item into one of three visual intake modes:
     - **`FIGMA_PROVIDED` (`READ`)**: PO supplied Figma link(s); extractor wrote `tokens.json` (W3C DTCG), `<stem>.spec.json` (Framelink-style normalized tree with `patternHint`, list deduplication `repeatCount`/`repeatedSamples`, and advanced `layout`/`textMeta`), `<stem>.summary.md`, per-screen images (`<stem>-S01.png`, `<stem>-S02.png`...), and optional SVG icons (`icons/*.svg` in `icon_svg_paths` when `--export-icons` is passed).
     - **`CODEBASE_ONLY` (No Figma — Small Edge-Case Adjustment)**: PO provided no Figma link because the change is a minor adjustment or edge case on an existing screen. Inspect the existing screen in the codebase (`S01` as `CHANGED`), confirm the minimal adjustment with the user (`Q-NN` $\to$ `D-NN`), and proceed without inventing new screens.
     - **`NO_UI_IMPACT`**: Work item changes nothing user-visible. Record `No UI impact` in `requirements.md` (`## 1. Scope & Alignment`).
   - If a Figma link is present in the ticket/request but returns `NOT_PROVIDED` (missing `FIGMA_TOKEN`) or `UNREACHABLE` (`401`/`403`/`404` or whole-file link without `node-id`), stop and ask the user — never guess screen contents.
2. **Extract Screens (`S-NN`) & Reconstruct Workflows (`W-NN`) at Gate 1 (`spec_writer`)** ([01-screen-and-workflow-extraction.md](references/01-screen-and-workflow-extraction.md)):
   - View every rendered screen image (`<stem>-S01.png`...) with `view_file` alongside `screens[]` in `<stem>.spec.json` (using `patternHint` / `pattern_hint` to identify controls and `repeatCount` + `repeatedSamples` to recognize dynamic/paginated lists or tables without drowning in repetitive JSON nodes).
   - Populate `## Screens & Visual Sources` (`S01`, `S02`... with `NEW` | `CHANGED` | `EXISTING`, dimensions, Figma node ID, and rendered image path) and `## Workflows` (`W-01`, `W-02`... linking `G-NN`, ordered `S-NN` steps, and `AC-NN` scenarios) in `requirements.md` (`REQ-006`).
   - Cross-check Huly business rules against Figma screens (`texts_reading_order`, `components`, `interactions`). Queue any mismatch or missing state (`Default`, `Loading`, `Empty`, `Error`) as an `OPEN` `Q-NN` in `codebase-notes.md`.
3. **Hand Off `tokens.json` & `<stem>.spec.json` to Gate 2 (`planning`)** ([02-design-tokens-and-gap-handoff.md](references/02-design-tokens-and-gap-handoff.md)):
   - At Gate 2, `planning` inspects file-level `tokens.json` (W3C DTCG `$type` / `$value` tokens and `$extensions.com.figma.components` / `componentSets`), `design_tokens.component_catalog`, and per-screen `screens[*].tree` (`patternHint`, `repeatCount`, `layout`, `textMeta`, and `icon_svg_paths`) in `<stem>.spec.json` via `{{slot:ui-kit-mapping}}`.
   - `planning` verifies Clean Architecture alignment, checks token conformance (flagging `{color.unlinked.*}` or `{typography.unlinked.*}` deviations), maps every non-`EXISTING` `S-NN` and UI component in `design.md` (`## UI/UX mapping`, rule `DESIGN-008`), and surfaces any new widget (`C-NN` / `Core gap`) as a `Q-NN` $\to$ `D-NN` for user approval at Gate 2.

## 2. Mandatory Rules (`FI-1`–`FI-8`)

| ID | Rule | Reference |
|---|---|---|
| **FI-1** | **Never guess an `UNREACHABLE` or `NOT_PROVIDED` Figma link** — ask the user for `FIGMA_TOKEN` or a frame link with `node-id`. | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-2** | **Inspect both the rendered `.png`/`.jpg` image (`view_file`) and `<stem>.spec.json`** for every screen (`S01`..`SNN`). | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-3** | **Treat No-Figma UI items strictly as `CODEBASE_ONLY` minor adjustments** on existing screens; confirm scope via `Q-NN` $\to$ `D-NN`. | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-4** | **Map every PO workflow into `## Workflows` (`W-NN`) and `## Screens & Visual Sources` (`S-NN`)** in `requirements.md` (`REQ-006`). | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-5** | **Cross-check Huly descriptions against Figma fields, buttons, and prototype `interactions`**; every discrepancy becomes a `Q-NN`. | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-6** | **Preserve the two-layer Figma output (`tokens.json` DTCG + `<stem>.spec.json` Framelink tree)** alongside raw `<stem>.json`. | [02](references/02-design-tokens-and-gap-handoff.md) |
| **FI-7** | **Audit `{*.unlinked.*}` tokens and unmapped components at Gate 2** via `{{slot:ui-kit-mapping}}` before locking `design.md`. | [02](references/02-design-tokens-and-gap-handoff.md) |
| **FI-8** | **Declare every missing UI kit control as `C-NN` (`CORE_GAP (D-NN)`) in `design.md` (`DESIGN-008`)** and create a dedicated build task at Gate 3. | [02](references/02-design-tokens-and-gap-handoff.md) |

## 3. CLI & Validator Gates (`PASS` / `FAIL`)

| Gate | Command / Tool | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|
| **Figma Extraction** | `coder-nexus figma fetch "<url>" --workspace-path "${workspaceFolder}" [--format png\|jpg] [--export-icons]` | `PASS` when status is `READ` and `tokens.json`, `<stem>.spec.json`, `<stem>.summary.md`, screen `.png`/`.jpg` files (plus `icons/*.svg` when `--export-icons` is set) are saved |
| **Gate 1 Spec Validation** | `validate_proposal_spec` (`REQ-001`..`REQ-006`) | `PASS` when `requirements.md` has `0` open `Q-NN`, all `G-NN` confirmed, and every `W-NN` in `## Workflows` links goals, `S-NN` screens, and `AC-NN` |
| **Gate 2 Mapping Validation** | `validate_proposal_spec` (`DESIGN-008`) | `PASS` when `design.md` `## UI/UX mapping` maps every non-`EXISTING` `S-NN` from `requirements.md` and every `C-NN` new component |

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Extracting screens (`S-NN`), reading per-screen `.png`/`.jpg` + `<stem>.spec.json`, handling no-Figma edge cases, and writing `## Workflows` (`W-NN`) at Gate 1 | [01-screen-and-workflow-extraction.md](references/01-screen-and-workflow-extraction.md) |
| Understanding two-layer `tokens.json` (W3C DTCG) + `<stem>.spec.json` (Framelink tree) and handing off to `planning` (`{{slot:ui-kit-mapping}}`) for architecture & `Core gap` checks at Gate 2 | [02-design-tokens-and-gap-handoff.md](references/02-design-tokens-and-gap-handoff.md) |
