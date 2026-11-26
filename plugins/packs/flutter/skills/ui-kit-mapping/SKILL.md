---
name: ui-kit-mapping
description: "Bridge extracted Figma outputs (W3C DTCG `tokens.json`, Framelink-style `<node>.spec.json`, per-screen `<node>-SNN.png`), extracted interactive HTML sitemap outputs (`sitemap/screens/*.png` + `*.spec.json`), and existing Flutter screens in `lib/` into `design.md` (`## UI/UX mapping`, rule `DESIGN-008`) — auditing tokens and widget anatomy against the active workspace profile contract, enforcing Flutter layout/scanner/viewport conventions, and surfacing any widget ambiguity, style trade-off, or missing widget (`C-NN` / `Core gap`) to the user via `Q-NN` -> `D-NN`."
---

# Flutter UI Kit & Visual-to-Widget Mapping (`ui-kit-mapping`)

Bridge the Client's real Flutter visual foundation with extracted Figma specifications (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`), extracted interactive HTML sitemaps (`.superpowers/sources/<ISSUE-ID>/sitemap/screens/*.png`, `*.spec.json`), or existing screens in `lib/` (`CODEBASE_ONLY` minor adjustments). **`planning`** authors `design.md` (`## UI/UX mapping`, rule `DESIGN-008`) at Gate 2; **`code_writer`** and **`code_reviewer`** (alongside `test_runner`) also bind and consult this skill during implementation, per-phase/`[REVIEW_CHECKPOINT]` review, and visual QA to enforce kit reuse, token compliance, and `C-NN` / `Core gap` governance.

## 1. End-to-End Mapping & Role Usage Workflow (`planning`, `code_writer`, `code_reviewer`)

1. **Audit Figma, Extracted HTML Sitemap & Existing `lib/` Screens (`planning` at Gate 2)** ([01-design-source-and-kit-extraction.md](references/01-design-source-and-kit-extraction.md)):
   - Read the Gate 1 approved `requirements.md` (`## Screens & Visual Sources` `S-NN` and `## Workflows` `W-NN`) and `codebase-notes.md` (`## 3. Verified Baseline Facts & Cross-Agent Notes`).
   - When `Visual Source Mode` is `FIGMA_PROVIDED`, inspect `.superpowers/sources/<ISSUE-ID>/figma/tokens.json` (W3C DTCG `$type: color | typography | dimension`), `<stem>.spec.json` (`screens[i].tree`, `components` with `pattern_hint`, `design_tokens.component_catalog`, `repeatCount`/`repeatedSamples`, `icon_svg_paths`, `workflows_hint`), and inspect each `<stem>-SNN.png` render via multimodal `read_file`.
   - When `Visual Source Mode` is `HTML_SITEMAP_PROVIDED`, inspect `.superpowers/sources/<ISSUE-ID>/sitemap/screens/*.spec.json` (`viewport`, `elements[]` with `pattern_hint`, `behavior`, `business_logic`, `bbox`, `parents`/`children`) and inspect each extracted `<id>_<code>.png` render via multimodal `read_file`. Because HTML sitemaps have no `tokens.json`, align styling directly to the active workspace profile's Design System tokens (`<!-- {{profile_references}} -->`) and verify any *unverified spec hints* from HTML against the real Flutter codebase.
   - Match every DTCG token (`{color.*}`, `{typography.*}`, `{dimension.*}`), canonical UI pattern hint (`component.patternHint` / `pattern_hint`), and exported icon SVG (`icon_svg_paths`) against the active workspace profile contract (`<!-- {{profile_references}} -->`).
   - For `CHANGED` screens or `CODEBASE_ONLY` minor adjustments, inspect the target Dart screen in `lib/` and `lib/l10n/*.arb` first so modifications preserve the existing screen shell.
2. **Enforce Flutter Layout, Viewport & Hardware Scanner Conventions** ([02-flutter-screen-and-input-conventions.md](references/02-flutter-screen-and-input-conventions.md)):
   - Translate advanced `<stem>.spec.json` layout & text semantics (`layout.positioning`, `layout.scrollBehavior`, `layout.scrollDirection` + `repeatCount >= 3`, `layout.minMax`, and `textMeta.maxLines` / `truncation`) into idiomatic Flutter widgets, and verify mobile vs. tablet/desktop responsive layout from Figma `bounds` or HTML sitemap `viewport` (`width` × `height`), numeric keyboard input (`TextInputType.number`), and hardware barcode/RFID scanner focus rules (`FocusNode` + `onFieldSubmitted`).
3. **Map to Flutter Widgets & Surface `Core gap`s at Gate 2 (`planning`)** ([03-widget-mapping-and-design-handoff.md](references/03-widget-mapping-and-design-handoff.md)):
   - Map every non-`EXISTING` `S-NN` screen, reused UI pattern, and new component (`C-NN`) in `design.md` (`## UI/UX mapping`, rule `DESIGN-008`) using the active workspace profile contract (`<!-- {{profile_references}} -->`).
   - When multiple kit widgets fit or a kit widget's fixed styling differs from the Figma or HTML sitemap render, **ask the user (`Q-NN` → `D-NN`)** before overriding style or building a custom widget.
   - When a visual component or screen subtree has no matching widget in the profile's UI kit or `lib/shared/`, assign `C-01`, `C-02`... and record an explicit **`Core gap`** row in `design.md` (`## UI/UX mapping` and `## Core usage` / `## Client Core Mapping`) so the user sees and approves it at **Gate 2**.
4. **Bind & Enforce in Build, Review, and Visual QA (`code_writer`, `code_reviewer`, `test_runner`)** ([03-widget-mapping-and-design-handoff.md](references/03-widget-mapping-and-design-handoff.md)):
   - **`code_writer`** consults `design.md` (`## UI/UX mapping`) and the active profile contract while coding widgets and stops with `BLOCKED` (`Q-NN`) if an unmapped component appears mid-phase.
   - **`code_reviewer`** (at every UI phase end & `[REVIEW_CHECKPOINT]`) and **`test_runner`** (at `final_qa`) audit implemented widgets against `## UI/UX mapping` and side-by-side `read_file` screenshots: report approved `KIT_OVERRIDE (D-NN)` / `CORE_GAP (D-NN)` as `ACCEPTED (D-NN)`, and flag unapproved custom widgets or bypassed kit widgets as `BLOCKER` (`FAIL`).

## 2. Mandatory Rules (`K1`–`K10`)

| ID | Rule | Reference |
|---|---|---|
| **K1** | **Ground mapping in extracted visual specs (`tokens.json` + `<stem>.spec.json` for Figma, or `sitemap/screens/*.png` + `*.spec.json` paired with active profile tokens for HTML sitemaps)** — never guess structure or raw literals from a thumbnail alone. | [01](references/01-design-source-and-kit-extraction.md) |
| **K2** | **Confirm target viewports and orientations (`D-NN`)** from Figma screen `bounds` and align with `architecture_profile.mode`. | [01](references/01-design-source-and-kit-extraction.md), [02](references/02-flutter-screen-and-input-conventions.md) |
| **K3** | **Audit existing `lib/` screens (`CHANGED` / `CODEBASE_ONLY` / sibling `NEW`)** before designing widget trees so existing routes, state holders, and `lib/l10n/*.arb` keys stay intact. | [01](references/01-design-source-and-kit-extraction.md) |
| **K4** | **Reuse the active profile's UI kit / shared widgets first** (`<!-- {{profile_references}} -->`); never hardcode raw `Color(0xFF...)` or `TextStyle` literals when profile tokens exist. | [01](references/01-design-source-and-kit-extraction.md), [03](references/03-widget-mapping-and-design-handoff.md) |
| **K5** | **Assign `C-NN` to every Figma component/widget not in the kit** and surface all `C-NN` / `Core gap` items to the user at Gate 2. | [03](references/03-widget-mapping-and-design-handoff.md) |
| **K6** | **Respect Flutter layout, orientation, and hardware scanner rules** (2-column adaptive layout on tablet/web, no hardcoded OS chrome, `FocusNode` retention for hardware barcode scanners). | [02](references/02-flutter-screen-and-input-conventions.md) |
| **K7** | **Map every non-`EXISTING` `S-NN` and every `C-NN` in `design.md` (`DESIGN-008`)** using the active profile's widget catalog. | [03](references/03-widget-mapping-and-design-handoff.md) |
| **K8** | **Ask the user (`Q-NN` → `D-NN`) on widget ambiguity or kit-vs-Figma styling trade-offs** — never silently alter an approved design. | [03](references/03-widget-mapping-and-design-handoff.md) |
| **K9** | **Surface every unmapped widget/function as a `Core gap` in `design.md` (Gate 2)** and create an explicit build task for each `C-NN` at Gate 3. | [03](references/03-widget-mapping-and-design-handoff.md) |
| **K10** | **Grade unapproved custom widgets or broken mappings with `BLOCKER` / `MAJOR` / `MINOR`** (`shared_contracts/flags_and_statuses.md`). | [03](references/03-widget-mapping-and-design-handoff.md) |

## 3. CLI & Validator Gates (`PASS` / `FAIL`)

| Gate | Command / Tool | Pass Criteria (`PASS` / `FAIL`) |
|---|---|---|
| **Figma Extraction** | `coder-nexus figma fetch "<url>" --workspace-path "${workspaceFolder}" [--export-icons]` (or `huly_get_task_detail(..., download=True)`) | `PASS` when `tokens.json`, `<stem>.spec.json`, `<stem>.summary.md`, and per-screen `<stem>-SNN.png` renders (plus `icons/*.svg` when `--export-icons` is set) are written under `.superpowers/sources/<ISSUE-ID>/figma/` |
| **HTML Sitemap Extraction** | `coder-nexus sitemap extract "<html-path>" --out "${workspaceFolder}/.superpowers/sources/<ISSUE-ID>/sitemap" [--stage ... \| --screens ...]` | `PASS` when `index.json`, `index.md`, and in-scope `screens/*.png`, `*.spec.json`, `*.md` are written under `.superpowers/sources/<ISSUE-ID>/sitemap/` |
| **Technical Design Mapping** | `validate_proposal_spec` (`DESIGN-008`) | `PASS` when `design.md` `## UI/UX mapping` maps every non-`EXISTING` `S-NN` and every `C-NN` to concrete Flutter classes |

## 4. Reference Guides

| Topic | Reference File |
|---|---|
| Auditing W3C DTCG `tokens.json` and Framelink-style `<stem>.spec.json` (`screens[i].tree`, `components`), comparing with profile tokens, and inspecting existing `lib/` screens | [01-design-source-and-kit-extraction.md](references/01-design-source-and-kit-extraction.md) |
| Flutter mobile/tablet/web layout rules, viewport/orientation selection from Figma `bounds`, numeric keyboards, and hardware barcode scanners | [02-flutter-screen-and-input-conventions.md](references/02-flutter-screen-and-input-conventions.md) |
| Canonical UI pattern inventory, `DESIGN-008` mapping in `design.md`, missing-widget (`C-NN` / `Core gap`) user notification protocol, and `BLOCKER` / `MAJOR` / `MINOR` grading | [03-widget-mapping-and-design-handoff.md](references/03-widget-mapping-and-design-handoff.md) |
<!-- {{profile_references}} -->
