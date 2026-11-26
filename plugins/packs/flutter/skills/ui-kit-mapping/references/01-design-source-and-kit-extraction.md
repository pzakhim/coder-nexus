# Figma `tokens.json` & `<stem>.spec.json` Audit and Existing Screen Inspection

> Topic: Auditing W3C DTCG `tokens.json` and Framelink-style `<stem>.spec.json` (`screens[i].tree`, `components`, `<stem>-SNN.png`) against the active Flutter profile contract, and inspecting existing Flutter screens in `lib/` for `CHANGED` or `CODEBASE_ONLY` items.

Rules **K1**, **K2**, **K3**, and **K4**.

---

## 1. Inspecting the Two-Layer Figma Output (`K1`)

When a work item has `FIGMA_PROVIDED` visual sources in `.superpowers/sources/<ISSUE-ID>/figma/`, read both structured layers alongside the per-screen `.png`/`.jpg` renders:

1. **Layer 1 — File-Level W3C DTCG `tokens.json`**:
   - **`color`**: Token entries (`{color.<group>.<name>}`) with `$type: "color"`, `$value` (`#RRGGBB` / `rgba(...)`), and `$extensions.com.figma` (`styleId`, `variableId`).
   - **`typography`**: Token entries (`{typography.<group>.<name>}`) with `$type: "typography"` and `$value` (`fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`).
   - **`dimension`**: Token entries (`{dimension.radius.*}`, `{dimension.spacing.*}`) derived from frame corner radii and auto-layout item spacing / padding.
   - **`$extensions.com.figma.components` & `componentSets`**: Catalog of reusable Figma components and variant sets referenced across frames.
2. **Layer 2 — Frame-Level Normalized `<stem>.spec.json` & Per-Screen `<stem>-SNN.png`**:
   - **`screens[]`**: Each screen (`S01`, `S02`...) provides `suggested_id`, `name`, `node_id`, `bounds` (`width`, `height`), `image_path` (`<stem>-SNN.png`), `sections[]`, `components[]` (with `pattern_hint`), `texts_reading_order[]`, `interactions[]`, and the recursive Framelink-style **`tree`**.
   - **`screens[i].tree`**: Normalized hierarchy where each node carries `layout` (`mode: row | column | none`, `positioning`, `constraints`, `scrollDirection`, `scrollBehavior`, `minMax`, `gap`, `padding`, `alignItems`, `justifyContent`, `sizing`), `tokens` referencing `{color.*}`, `{typography.*}`, and `{dimension.*}`, `textMeta` (`maxLines`, `truncation`, `autoResize`, `align`), `component` (`INSTANCE` / `COMPONENT` metadata + `patternHint`), and `repeatCount` + `repeatedSamples` on deduplicated list/table runs.
   - **`design_tokens.component_catalog` & `icon_svg_paths`**: Catalog of frame-level components with `pattern_hint`, plus exported `.svg` icon paths in `.superpowers/sources/<ISSUE-ID>/figma/icons/*.svg` when fetched with `--export-icons`.
   - **Mandatory Visual Cross-Check**: Load every `<stem>-SNN.png` via multimodal `read_file` while reading `screens[i].tree` so visual hierarchy, density, and overlay states match the structural tree.

---

## 2. Auditing Tokens, `patternHint`, `repeatCount`, & Icons Against the Active Profile (`K2`, `K4`, `K5`)

Compare the tokens, pattern hints, list runs, and icons in `tokens.json` and `<stem>.spec.json` against the active profile contract (`<!-- {{profile_references}} -->` injected in `SKILL.md`):

1. **Direct Widget Matching via `patternHint` / `pattern_hint` (`K4`, `K5`)**:
   - Every `INSTANCE`/`COMPONENT` node in `screens[i].tree` (`component.patternHint`), `screens[i].components` (`pattern_hint`), and `design_tokens.component_catalog` (`pattern_hint`) provides a canonical UI pattern classification (`appbar`, `button`, `formfield`, `search`, `dropdown`, `datepicker`, `dialog`, `bottomsheet`, `bottomnav`, `badge`, `nodata`, `loading`, `list`, `card`, `chip`, `banner`, or `custom`).
   - Match `patternHint` directly against the active profile's Canonical UI Pattern table (`<!-- {{profile_references}} -->`) to select the profile's standard widget.
   - When `patternHint == "custom"` or has no profile widget match in the active profile contract or `lib/shared/`, assign `C-NN` (`C-01`, `C-02`...) and record `CORE_GAP (D-NN)` in `design.md` (`## UI/UX mapping`, rule `DESIGN-008`).
2. **Dynamic List & Pagination Mapping via `repeatCount` + `repeatedSamples` (`K1`, `K4`)**:
   - When a node in `screens[i].tree` carries `"repeatCount": N` ($\ge 3$) and `"repeatedSamples": [...]`, map the parent/item structure to the profile's dynamic list or pagination widget (`list` pattern) rather than static `Column` children. Use `repeatedSamples` to verify item variant fields (badges, subtitles, trailing actions) across rows.
3. **Exported SVG Icon Mapping via `icon_svg_paths` (`--export-icons`)**:
   - Check the active profile's built-in icon catalog first. When a Figma `ICON` node is not already in the profile's icon set, map its exported `.svg` file from `icon_svg_paths` (`.superpowers/sources/<ISSUE-ID>/figma/icons/*.svg`, generated via `coder-nexus figma fetch ... --export-icons`) to the project's SVG icon asset pipeline.
4. **Token Audit & Mismatch Handling (`{color.*}`, `{typography.*}`, `{dimension.*}`)**:
   - Map DTCG tokens to the active profile's semantic color, typography, and spacing/radius tokens defined in `<!-- {{profile_references}} -->` (never hardcode raw `Color(0xFF...)` or `TextStyle(fontSize: ...)` literals in feature screens).
   - If `tokens.json` introduces an unlinked token (`{color.unlinked.*}`, `{typography.unlinked.*}`) or off-scale value absent from the profile's Design System tokens, queue a `Q-NN` (`Owner: planning`) asking the user whether to snap to the nearest existing Design System token (`KIT_OVERRIDE (D-NN)`, Recommended) or register a new semantic token (`D-NN`).

---

## 2B. Inspecting Extracted Interactive HTML Sitemaps (`HTML_SITEMAP_PROVIDED`) (`K1`, `K2`, `K4`, `K5`)

When `Visual Source Mode` is `HTML_SITEMAP_PROVIDED` (extracted into `.superpowers/sources/<ISSUE-ID>/sitemap/` via `coder-nexus sitemap extract`):

1. **Read Extracted Per-Screen Specs & Inspect Full-Res `.png` Renders**:
   - Inspect each in-scope `sitemap/screens/<id>_<code>.spec.json` (`viewport`, `role`, `parents`/`children`, `overview`, `elements[]` with `name`, `pattern_hint`, `behavior`, `business_logic`, `bbox`) and load `sitemap/screens/<id>_<code>.png` via multimodal `read_file`. Never open the raw multi-MB `.html` directly.
2. **Map Elements Without `tokens.json` (Profile-First Token Alignment)**:
   - Interactive HTML sitemaps do **not** emit a W3C DTCG `tokens.json` file — do **not** treat missing `tokens.json` as `BLOCKED`.
   - Match each element's `pattern_hint` and visual appearance in the `.png` directly against the active workspace profile's widget catalog and semantic tokens (`<!-- {{profile_references}} -->`).
   - If the screenshot's color/spacing styling differs from the standard profile kit widget, confirm via `Q-NN` → `D-NN` whether to snap to the standard kit styling (`KIT_OVERRIDE (D-NN)`, Recommended) or build a custom widget (`C-NN` / `CORE_GAP (D-NN)`).
3. **Verify Unverified Technical Hints from HTML**:
   - Sitemap overview/element prose may mention author-assumed libraries, storage engines, route strings, or raw Material widget names (logged as *unverified spec hints* in `codebase-notes.md`). Always verify against `pubspec.yaml`, `lib/`, and the active `architecture_profile` (screen base, state holder, UI kit, DI, Router) before locking `design.md` — never copy unverified spec hints blindly.
4. **Viewport & Responsive Check (`K2`)**:
   - Read `viewport` (`width × height`, e.g., `2560×1600` tablet landscape) from `<id>_<code>.spec.json` and check whether `requirements.md` also requires mobile or portrait layouts; specify responsive layout overrides in `design.md` per the active profile contract.

---

## 3. Auditing Existing Flutter Screens in `lib/` (`CHANGED` & `CODEBASE_ONLY`) (`K3`)

For any screen marked `CHANGED` in `requirements.md` → `## Screens & Visual Sources` (including `CODEBASE_ONLY` minor edge-case adjustments when PO provides no Figma link) or when building a `NEW` screen inside an existing module:

1. **Locate Target (`CHANGED`) or Sibling (`NEW`) Screens**:
   - Search `lib/` for the target screen (`CHANGED`) or 1–2 sibling screens in the same module (`NEW`) (`rg --files lib/ -g "*{screen,page,view}.dart"`) along with the module's localization strings (`lib/l10n/*.arb`).
2. **Inventory the Existing Screen's Structural Layers**:
   - Read the screen's Dart widget tree to identify: (a) screen base class and app bar, (b) top search/filter/chip controls, (c) body list/card/form layout and field order, (d) bottom sticky action bar vs. inline CTA, (e) `Loading` / `Content` / `Empty` / `Error` and dialog/bottom-sheet branches, and (f) existing route arguments and Cubit/Bloc state shape.
3. **Minimal Delta for `CHANGED` / `CODEBASE_ONLY` Screens**:
   - Preserve existing widget reuse, state management bindings, and localization keys outside the approved change scope.
   - Map only the added or modified controls in `design.md` → `## UI/UX mapping` (`DESIGN-008`).
