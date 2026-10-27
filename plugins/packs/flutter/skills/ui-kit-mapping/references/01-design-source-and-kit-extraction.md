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
   - **`screens[]`**: Each screen (`S-01`, `S-02`...) provides `id`, `name`, `node_id`, `bounds` (`width`, `height`), `image_path` (`<stem>-SNN.png`), `sections[]`, `components[]`, `texts_reading_order[]`, `interactions[]`, and the recursive Framelink-style **`tree`**.
   - **`screens[i].tree`**: Normalized hierarchy where each node carries `layout` (`mode: row | column | stack | none`, `gap`, `padding`, `align`), `fills` / `strokes` referencing `{color.*}`, `text` + `text_style` referencing `{typography.*}`, `corner_radius` referencing `{dimension.radius.*}`, and `component_ref` (`INSTANCE` / `COMPONENT`) with `variant_properties`.
   - **Mandatory Visual Cross-Check**: Open every `<stem>-SNN.png` via `view_file` while reading `screens[i].tree` so visual hierarchy, density, and overlay states match the structural tree.

---

## 2. Auditing Tokens Against the Active Workspace Profile (`K2`, `K4`)

Compare the tokens and components in `tokens.json` and `<stem>.spec.json` against the active profile contract (`ui-kit-mapping-contracts.md` injected in `SKILL.md`):

| `architecture_profile.mode` | Visual Foundation Source | Token & Component Audit Rule |
|---|---|---|
| `imespro` | Shared company UI kit package (`app_ui_kit`) resolved in `.dart_tool/package_config.json` | Map `{color.*}` $\to$ `AppColor.*`, `{typography.*}` $\to$ `Jakarta` (`Text12`–`Text34`), and `components[]` $\to$ `package:app_ui_kit/app_ui_kit.dart` widgets per `../app-ui-kit/guidance/GUIDE.md` |
| `external-structured` | Client's own theme/color classes and shared widgets under `lib/shared/` or `lib/core/` | Map `{color.*}` and `{typography.*}` to the Client's theme tokens (`AppColors`, `ThemeExtension`) and `components[]` to `lib/shared/widgets/` |
| `external-standard` | Standard Flutter Material 3 / Cupertino `ThemeData` & `ColorScheme` | Map `{color.*}` $\to$ `Theme.of(context).colorScheme`, `{typography.*}` $\to$ `Theme.of(context).textTheme`, and `components[]` $\to$ standard Material 3 / Cupertino widgets |

- **Token Mismatch Handling**: If `tokens.json` introduces a color hex, font size/weight, or radius that does not exist in the codebase's Design System tokens:
  - Do **not** hardcode raw `Color(0xFF...)` or `TextStyle(fontSize: ...)` in feature screens.
  - Queue a `Q-NN` (`Owner: planning`) asking the user whether to snap to the nearest existing Design System token (`KIT_OVERRIDE (D-NN)`, Recommended) or register a new semantic token (`D-NN`).

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
