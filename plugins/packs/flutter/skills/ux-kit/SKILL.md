---
name: ux-kit
description: Flutter design source for UI/UX designs. Finds where the Client's look comes from (app-ui-kit, the Client's own theme, or Material 3), generates the HTML kit with `coder-nexus ux extract`, and maps kit classes back to Flutter widgets.
---

# Flutter UX kit (design source)

The designer draws HTML screens only with the kit generated from the Client's real look. This skill says where that look comes from in a Flutter Client and how kit classes map back to widgets for Planning.

## 1. Generate or refresh the kit

Run in the Client workspace (once per project, again when the UI kit or theme changes):

```sh
coder-nexus ux extract --project "${workspaceFolder}"
```

It writes `.superpowers/ux/design-system.json` and `.superpowers/ux/kit/` (`kit.css`, `kit.js`, `viewports.js`, `components.html`, fonts). Never edit `kit/` by hand.

## 2. Confirm the source with the user (first time, one `ask_question`)

Read `design-system.json` → `source`, `roles`, `font`, `warnings`, then open `kit/components.html` and look at it.

| `source.kind` | Profile | Where the look comes from | What to confirm |
|---|---|---|---|
| `app-ui-kit` | `imespro` | `app_ui_kit` package: `AppColor`, `Jakarta` font, `AppButton`, `AppFormField`, `AppDialog`, … | The package version the app really uses |
| `client-theme` | `external-structured` | The Client's own color/theme classes and shared widgets | Role mapping (`roles[*].from`), and that radius/heights match the running app (Material 3 values are used) |
| `material3` | `external-standard` | Flutter Material 3 defaults + seed/primary color from `ThemeData` | Brand color, font, Material vs Cupertino |

If `warnings` asks for a brand color or font, ask the user once, then run `coder-nexus ux extract --brand "#RRGGBB" --font "Family"`; the answer is kept as an override. Record the confirmed source as a `D-NN` and set `source.decision` in `design-system.json`. This choice must match the `architecture_profile` Planning records later (`{{slot:core-usage}}`).

When screenshots of the running app exist (`.superpowers/ux/current/`), compare them with `components.html`. Report visible differences (radius, heights, colors) to the user instead of silently restyling the kit.

## 3. Kit class → Flutter widget (for `uiux.md` and Planning)

| Kit class | `app-ui-kit` (imespro) | Material 3 / standard Flutter |
|---|---|---|
| `app-appbar` | `AppDefaultAppbar`, `AppBackButton` | `AppBar`, `BackButton` |
| `app-button` (`.secondary .outline .text .danger .is-loading`) | `AppButton` | `FilledButton`, `OutlinedButton`, `TextButton` |
| `app-formfield` (`.is-error .is-disabled`) | `AppFormField`, `AppPasswordField` | `TextFormField` |
| `app-search` | `AppSearchField` | `SearchBar` |
| `app-dropdown` | `AppMultiDropdownFormField` | `DropdownMenu` |
| `app-datepicker` | `AppDatePicker` | `showDatePicker` |
| `app-dialog` | `AppDialog` | `AlertDialog` |
| `app-bottomsheet` | `AppBottomSheetCommonLayout` | `showModalBottomSheet` |
| `app-bottomnav` | `AppBottomNavigationBar` | `NavigationBar` |
| `app-badge` | `BadgeWidget` | `Badge` / `Chip` |
| `app-nodata` | `AppNoData` | empty-state `Column` |
| `app-loading` / `app-shimmer` | `AppLoadingIndicator` / `*Shimmer` | `CircularProgressIndicator` / skeleton |
| `app-card`, `app-list-item`, `app-chip`, `app-banner` | layout (no dedicated kit widget) | `Card`, `ListTile`, `Chip`, `MaterialBanner` |

For a `client-theme` source, use the `widget` names listed in `design-system.json` → `components`. A widget with `kit_class: null` has no HTML equivalent: draw it as a `new-component` or ask.

## 4. Flutter-specific screen rules

- Mobile screens follow Material layout: app bar on top, scrolling content, primary action at the bottom (`app-footer`) or in the content, bottom navigation only where the app already has it.
- Tablet and web: use `.app-content.centered` or `cols md-2` instead of stretching phone layouts. Mark platform-only differences with a `.note`.
- Do not draw platform chrome the app does not control (status bar, OS keyboard). Note the keyboard type with a `.note` when it matters: numeric entry (`TextInputType.number`) gets `inputmode="numeric"` on the drawn input and a note.
- Hardware barcode scanners (handhelds, ring scanners) act as keyboard input into the focused field, usually ending with Enter. Draw the scan field with `data-ux-target` and a note on what keeps it focused; in the walkthrough model a scan as `scan` on that field, never as a camera screen unless the workflow uses the camera.
- Orientation (asked once per project with the viewports): tablet scanner stations and mounted warehouse terminals are usually landscape. Offer `tablet=landscape` (or `portrait+landscape`) as the recommended option only when a source shows it — a landscape design-tool frame, a screenshot of the running app, or the ticket naming the device; otherwise recommend portrait and ask.
- Tablet landscape (warehouse terminals, mounted tablets): when `viewports.json` allows landscape for the tablet, use `cols md-2` (list + detail, or scan field + result) instead of a stretched phone column, and keep primary actions reachable without scrolling.
- Text sizes: use the kit's body size; headings 16–20px. `app-ui-kit` text widgets are `Text12` … `Text34` (`.bold`, `.medium`).
