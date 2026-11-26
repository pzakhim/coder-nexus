---
name: figma-intake
description: "Extract UI/UX specs from either Figma frames/sections (W3C DTCG `tokens.json`, Framelink-normalized `<node>.spec.json`, per-screen renders) or interactive HTML sitemaps (`coder-nexus sitemap extract` into `index.md`, per-screen `.spec.json`, `.md`, and `.png`), translate them with Huly ticket flows into Gate 1 Screens (`S-NN`) and Workflows (`W-NN`) in `requirements.md`, and hand off design tokens/elements to Gate 2 (`planning`)."
---

# Figma & Visual Spec Intake (`FIGMA_PROVIDED` + `HTML_SITEMAP_PROVIDED`)

Convert PO-supplied visual designs — **Figma links** or **interactive HTML sitemaps** — and Huly ticket flows into structured Gate 1 requirements (`## Screens & Visual Sources` and `## Workflows` in `requirements.md`) and a deterministic Gate 2 design-system handoff (`design.md` `## UI/UX mapping`, rule `DESIGN-008`).

## 1. End-to-End Intake & Handoff Workflow

1. **Fetch / Extract & Classify Visual Source (`spec_writer` at Stage `1A` / `1A-UX`)** ([01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md)):
   - Run `huly_get_task_detail(..., download=True)` — it auto-fetches linked Figma frames into `.superpowers/sources/<ISSUE-ID>/figma/` and auto-indexes downloaded interactive HTML sitemaps into `.superpowers/sources/<ISSUE-ID>/sitemap/`.
   - For pasted Figma URLs run `coder-nexus figma fetch "<url>" --workspace-path "${workspaceFolder}" [--export-icons]`. For local or manually placed interactive HTML sitemaps run `coder-nexus sitemap extract "<html-path>" --out "${workspaceFolder}/.superpowers/sources/<ISSUE-ID>/sitemap" [--stage ... | --screens ... | --index-only]`.
   - Classify the work item into one of four visual intake modes:
     - **`FIGMA_PROVIDED` (`READ`)**: PO supplied Figma link(s); extractor wrote `tokens.json` (W3C DTCG), `<stem>.spec.json` (Framelink-style normalized tree with `patternHint`, list deduplication `repeatCount`/`repeatedSamples`, and advanced `layout`/`textMeta`), `<stem>.summary.md`, per-screen images (`<stem>-S01.png`...), and optional SVG icons (`icons/*.svg` when `--export-icons` is passed).
     - **`HTML_SITEMAP_PROVIDED` (`READ`)**: PO supplied an interactive HTML sitemap (auto-extracted from Huly or manually placed when > 150 MB); extractor wrote lightweight `index.json` / `index.md` plus filtered per-screen `<id>_<code>.png`, `<id>_<code>.spec.json` (`overview`, `elements[]` with `pattern_hint`, `behavior`, `business_logic`, hotspot `bbox`, `parents`/`children`), and `<id>_<code>.md`. **Never open raw multi-megabyte `.html` files directly.**
     - **`CODEBASE_ONLY` (No External Design — Small Edge-Case Adjustment)**: PO provided no Figma or HTML sitemap because the change is a minor adjustment or edge case on an existing screen. Inspect the existing screen in the codebase (`S-01` as `CHANGED`), confirm the minimal adjustment with the user (`Q-NN` $\to$ `D-NN`), and proceed without inventing new screens.
     - **`NO_UI_IMPACT`**: Work item changes nothing user-visible. Record `No UI impact` in `requirements.md` (`## 1. Scope & Alignment`).
   - If a Figma link returns `NOT_PROVIDED`/`UNREACHABLE`, or an oversized HTML attachment returns `UNREACHABLE` (exceeding the 150 MB auto-download limit), stop and ask the user (provide token/link or place the file at the exact `.superpowers/sources/<ISSUE-ID>/` path) — never guess screen contents.
2. **Extract Screens (`S-NN`) & Workflows (`W-NN`) at Gate 1 (`spec_writer`)** ([01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md)):
   - Inspect every in-scope rendered screen image (`<stem>-S01.png`... or `sitemap/screens/<id>_<code>.png`) with multimodal `read_file` alongside its extracted `.spec.json` / `.md`.
   - Populate `## Screens & Visual Sources` (`S-01`, `S-02`... with `NEW` | `CHANGED` | `EXISTING`, dimensions, source ref, and rendered image path) and `## Workflows` (`W-01`, `W-02`... linking `G-NN`, ordered `S-NN` steps, and `AC-NN` scenarios) in `requirements.md` (`REQ-006`).
   - For `HTML_SITEMAP_PROVIDED`, pre-fill actors/RBAC, business rules, and scenarios from extracted `elements[]` tables, apply **Delta Grilling** (confirm explicit sitemap rules via `batch-confirm`; open `Q-NN` only for scope boundary, 4 visual states, API contract, extra viewports, and conflicts), and isolate any technical hints into `codebase-notes.md`.
   - Cross-check Huly business rules against the visual spec; queue any mismatch or missing state (`Default`, `Loading`, `Empty`, `Error`) as an `OPEN` `Q-NN` in `codebase-notes.md`.
3. **Hand Off Design Artifacts to Gate 2 (`planning`)** ([02](references/02-design-tokens-and-gap-handoff.md), [03](references/03-html-sitemap-intake.md)):
   - At Gate 2, `planning` inspects either `tokens.json` + `<stem>.spec.json` (`FIGMA_PROVIDED`) or extracted `sitemap/screens/*.png` + `*.spec.json` (`HTML_SITEMAP_PROVIDED`, aligned against the active workspace profile's design system tokens) via `{{slot:ui-kit-mapping}}`.
   - `planning` verifies architecture alignment, maps every non-`EXISTING` `S-NN` and UI component in `design.md` (`## UI/UX mapping`, rule `DESIGN-008`), and surfaces any styling trade-off (`KIT_OVERRIDE (D-NN)`) or new component (`C-NN` / `CORE_GAP (D-NN)`) for user approval at Gate 2.

## 2. Mandatory Rules (`FI-1`–`FI-9`)

| ID | Rule | Reference |
|---|---|---|
| **FI-1** | **Never guess an `UNREACHABLE` or `NOT_PROVIDED` visual source** — ask the user for `FIGMA_TOKEN`, a frame link with `node-id`, or manual placement of an oversized HTML file. | [01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md) |
| **FI-2** | **Inspect both the rendered `.png`/`.jpg` image (multimodal `read_file`) and extracted `.spec.json`** for every in-scope screen (`S-01`..`S-NN`). | [01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md) |
| **FI-3** | **Treat no-design UI items strictly as `CODEBASE_ONLY` minor adjustments** on existing screens; confirm scope via `Q-NN` $\to$ `D-NN`. | [01](references/01-screen-and-workflow-extraction.md) |
| **FI-4** | **Map every PO workflow into `## Workflows` (`W-NN`) and `## Screens & Visual Sources` (`S-NN`)** in `requirements.md` (`REQ-006`). | [01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md) |
| **FI-5** | **Cross-check Huly descriptions against visual fields, buttons, and navigation links**; every discrepancy becomes a `Q-NN`. | [01](references/01-screen-and-workflow-extraction.md), [03](references/03-html-sitemap-intake.md) |
| **FI-6** | **Preserve extracted structured outputs** (Figma `tokens.json` + `<stem>.spec.json` + raw `<stem>.json`, or Sitemap `index.json`/`index.md` + per-screen `screens/*.spec.json` + `.png`). | [02](references/02-design-tokens-and-gap-handoff.md), [03](references/03-html-sitemap-intake.md) |
| **FI-7** | **Audit tokens (`{*.unlinked.*}` for Figma) or profile token alignment (for HTML sitemaps) and unmapped components at Gate 2** via `{{slot:ui-kit-mapping}}` before locking `design.md`. | [02](references/02-design-tokens-and-gap-handoff.md), [03](references/03-html-sitemap-intake.md) |
| **FI-8** | **Declare every missing UI kit control as `C-NN` (`CORE_GAP (D-NN)`) in `design.md` (`DESIGN-008`)** and create a dedicated build task at Gate 3. | [02](references/02-design-tokens-and-gap-handoff.md) |
| **FI-9** | **Never open raw multi-MB HTML sitemaps directly; filter master sitemaps to ticket scope, apply Delta Grilling, and isolate unverified technical hints into `codebase-notes.md`.** | [03](references/03-html-sitemap-intake.md) |

## 3. CLI & Validator Gates (`PASS` / `FAIL`)

| Gate | Command / Tool | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|
| **Figma Extraction** | `coder-nexus figma fetch "<url>" --workspace-path "${workspaceFolder}" [--format png\|jpg] [--export-icons]` | `PASS` when status is `READ` and `tokens.json`, `<stem>.spec.json`, `<stem>.summary.md`, screen `.png`/`.jpg` files are saved |
| **HTML Sitemap Extraction** | `coder-nexus sitemap extract "<html-path>" --out "${workspaceFolder}/.superpowers/sources/<ISSUE-ID>/sitemap" [--stage ... \| --screens ... \| --ids ... \| --index-only]` | `PASS` when status is `READ` and `index.json`, `index.md`, plus in-scope `screens/*.png`, `*.spec.json`, and `*.md` are saved |
| **Gate 1 Spec Validation** | `validate_proposal_spec` (`REQ-001`..`REQ-006`) | `PASS` when `requirements.md` has `0` open `Q-NN`, all `G-NN` confirmed, and every `W-NN` in `## Workflows` links goals, `S-NN` screens, and `AC-NN` |
| **Gate 2 Mapping Validation** | `validate_proposal_spec` (`DESIGN-008`) | `PASS` when `design.md` `## UI/UX mapping` maps every non-`EXISTING` `S-NN` from `requirements.md` and every `C-NN` new component |

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Extracting screens (`S-NN`), reading per-screen `.png`/`.jpg` + `<stem>.spec.json`, handling no-design edge cases, and writing `## Workflows` (`W-NN`) at Gate 1 | [01-screen-and-workflow-extraction.md](references/01-screen-and-workflow-extraction.md) |
| Understanding two-layer `tokens.json` (W3C DTCG) + `<stem>.spec.json` (Framelink tree) and handing off to `planning` (`{{slot:ui-kit-mapping}}`) for architecture & `Core gap` checks at Gate 2 | [02-design-tokens-and-gap-handoff.md](references/02-design-tokens-and-gap-handoff.md) |
| Extracting interactive HTML sitemaps (`coder-nexus sitemap extract`), manual-drop fallback for oversized files, scope filtering, Delta Grilling, and Gate 2 handoff without `tokens.json` | [03-html-sitemap-intake.md](references/03-html-sitemap-intake.md) |
