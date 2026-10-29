# Two-Layer Token & Spec Handoff to Gate 2 (`tokens.json` + `<node>.spec.json`)

> Topic: Structure of file-level W3C DTCG `tokens.json` and per-frame Framelink-style `<node>.spec.json`, and how `planning` (`{{slot:ui-kit-mapping}}`) uses them at Gate 2 to verify Design System conformance, Clean Architecture, and new widget gaps (`C-NN` / `Core gap`).

Rules **FI-6**, **FI-7**, and **FI-8**.

---

## 1. Two-Layer Output Architecture (`FI-6`)

Instead of forcing agents to parse raw multi-megabyte Figma JSON files (`<stem>.json`), `coder-nexus figma fetch` produces two structured layers alongside the per-screen `.png`/`.jpg` images:

### Layer 1: File-Level `tokens.json` (W3C DTCG Standard)
Located at `.superpowers/sources/<ISSUE-ID>/figma/tokens.json` (merged across all fetched frames of the same Figma file):
- **`$schema`**: `"https://tr.designtokens.org/format/"` (compatible with **Style Dictionary v4+** for code generation and direct design-system auditing).
- **`color`**: Named Figma fill/stroke styles (e.g., `color.primary.brand-500` $\to$ `{"$type": "color", "$value": "#0055AA", "$extensions": {"com.figma": {"styleId": "...", "styleName": "Primary/Brand 500"}}}`) plus `color.unlinked.*` for inline colors that lack a Figma style.
- **`typography`**: Named Figma text styles (e.g., `typography.button.label-m` $\to$ `{"$type": "typography", "$value": {"fontFamily": "...", "fontSize": "16px", "fontWeight": 600, "lineHeight": "24px"}}`) plus `typography.unlinked.*`.
- **`dimension.radius` & `dimension.spacing`**: Corner radii (`8px`, `12px`...) and auto-layout gaps/paddings (`12px`, `16px`...) with any bound Figma variable IDs.
- **`shadow`**: Drop/inner shadow tokens (`$type: "shadow"`).
- **`$extensions.com.figma.componentSets` & `components`**: Complete catalog of reusable Figma components and component sets referenced by the screens.

### Layer 2: Frame-Level `<stem>.spec.json` (Framelink-Normalized Tree)
Located at `.superpowers/sources/<ISSUE-ID>/figma/<stem>.spec.json`:
- **`screens[]`**: Ordered list of screens (`S01`, `S02`...) with `image_path` (`<stem>-S01.png`), `bounds`, `sections`, `components` (including `pattern_hint`), `texts_reading_order`, `interactions`, and **`tree`**.
- **`design_tokens.component_catalog`**: Frame-level summary of reusable components with `pattern_hint`.
- **`icon_svg_paths`**: Mapping of exported pure-vector `ICON` node IDs to `.superpowers/sources/<ISSUE-ID>/figma/icons/*.svg` when `coder-nexus figma fetch ... --export-icons` is used.
- **`screens[i].tree`**: Recursive, noise-free UI hierarchy (hidden nodes removed, pure vector icon subtrees collapsed to `"type": "ICON"`):
  - **`layout`**: Flex-normalized and responsive layout semantics:
    - Base flex: `mode` (`"row" | "column" | "none"`), `justifyContent`, `alignItems`, `sizing` (`{"horizontal": "fixed"|"hug"|"fill", "vertical": "fixed"|"hug"|"fill"}`), `gap`, `padding`, `wrap`, `clipsContent`.
    - Positioning & constraints: `layout.positioning: "absolute"` + `layout.constraints` (`horizontal`, `vertical`) for floating/overlay elements.
    - Scroll semantics: `layout.scrollDirection` (`"vertical" | "horizontal" | "both"`) and `layout.scrollBehavior` (`"fixed" | "sticky"`) for scrollable regions vs. pinned headers/bottom bars.
    - Responsive bounds: `layout.minMax` (`minWidth`, `maxWidth`, `minHeight`, `maxHeight`) for responsive sizing bounds.
  - **`textMeta`**: Present on `TEXT` nodes with `maxLines`, `truncation: "ellipsis"`, `autoResize`, and `align`.
  - **`tokens`**: Every visual property references `tokens.json` by DTCG token name (`"fill": "{color.primary.brand-500}"`, `"textStyle": "{typography.button.label-m}"`, `"radius": "{dimension.radius.8px}"`, `"gap": "{dimension.spacing.12px}"`).
  - **`component` & `patternHint`**: Component ID, name, `componentSet`, variant `properties`, and deterministic `patternHint` (`appbar`, `button`, `formfield`, `search`, `dropdown`, `datepicker`, `dialog`, `bottomsheet`, `bottomnav`, `badge`, `nodata`, `loading`, `list`, `card`, `chip`, `banner`, or `custom`) for `INSTANCE` / `COMPONENT` nodes.
  - **`repeatCount` & `repeatedSamples`**: Contiguous runs of $\ge 3$ structurally identical children in `screens[i].tree` are collapsed into the first child with `"repeatCount": N` and `"repeatedSamples": [...]`, while `screens[i].texts_reading_order` and `screens[i].components` retain 100% of items.
  - **`navigateTo`**: Prototype destination node ID when an interaction is attached.

---

## 2. Gate 2 Inspection Protocol for `planning` (`FI-7`, `FI-8`)

When `planning` starts Stage 1 (`design.md` at Gate 2), it reads `requirements.md` (`## Screens & Visual Sources` and `## Workflows`), `tokens.json`, and `<stem>.spec.json` using `{{slot:ui-kit-mapping}}`:

1. **Design System Token Check (`tokens.json` vs. Workspace Foundation)**:
   - Compare named tokens (`color.*`, `typography.*`, `dimension.*`) against the workspace's active design system tokens.
   - Check `color.unlinked.*` and `typography.unlinked.*`: if a Figma screen uses unlinked hex colors or off-scale fonts that differ from the project's theme tokens, queue a `Q-NN` (`Owner: planning`) recommending the closest existing project token (`D-NN`).
2. **Clean Architecture & Screen Lifecycle Check (`screens[*].tree` + `## Workflows`)**:
   - Verify each `S-NN` (`NEW` or `CHANGED`) maps cleanly to the project's presentation/state/routing architecture (screen base / page class, state holder, route arguments, and back-navigation lifecycle across multi-screen `W-NN` flows).
3. **Component Mapping & New Widget Detection (`C-NN` / `Core gap`) (`DESIGN-008`)**:
   - Inspect `screens[*].components` (`pattern_hint`), `design_tokens.component_catalog` (`pattern_hint`), `screens[*].tree` (`component.patternHint`, `repeatCount`/`repeatedSamples`, and custom-drawn `FRAME`/`GROUP` subtrees), and `icon_svg_paths`:
     - **Existing UI Kit / Shared Widget Fits**: Match `patternHint` (`appbar`, `button`, `formfield`, `list`, etc.) against the workspace profile's widget catalog and map in `design.md` $\to$ `## UI/UX mapping` with `Status: MAPPED` (or `KIT_OVERRIDE (D-NN)` after user confirmation when kit styling differs slightly from Figma).
     - **New Widget Required (`C-NN` / `Core gap`)**: When `patternHint == "custom"` or no existing widget in the project's UI kit or shared library satisfies the Figma component/subtree, assign `C01`, `C02`..., record `CORE_GAP (D-NN)` in `design.md` (`## UI/UX mapping`), get user approval at **Gate 2**, and create an explicit widget-build task in `implementation-plan.md` at **Gate 3**.
