# UI Kit Mapping Contracts — `imespro` Profile (`app_ui_kit`, `app_core`, `app_util`)

> Topic: Mapping extracted Figma `tokens.json` (W3C DTCG) and `<stem>.spec.json` (`screens[i].tree`, `components`) to `package:app_ui_kit/app_ui_kit.dart` widgets, `AppColor` tokens, `Jakarta` (`Text12`–`Text34`) typography, `BaseScreen` / `BaseScreenState`, and surfacing `Core gap`s (`C-NN`) at Gate 2 (`DESIGN-008`).

When `.superpowers/setup.json` sets `profile = "imespro"`, verify package resolution first with `coder-nexus setup flutter --check` and read `../app-ui-kit/guidance/GUIDE.md`, `../app-core/guidance/GUIDE.md`, and `../app-util/guidance/GUIDE.md` before mapping any `S-NN` screen or `C-NN` component in `design.md`.

---

## 1. Mapping Figma Components & Patterns (`<stem>.spec.json`) → `app_ui_kit` Widgets

Use this canonical table when `planning` audits `screens[i].components` and `screens[i].tree` in `<stem>.spec.json` to populate `## UI/UX mapping` (`DESIGN-008`) and `## Core usage` in `design.md`:

| Canonical UI Pattern / Figma Node | `app_ui_kit` Widget (`package:app_ui_kit/app_ui_kit.dart`) | Notes & Variant Mapping |
|---|---|---|
| `appbar` (`AppBar`, `TopBar`, `Header`) | `AppDefaultAppbar`, `AppBackButton` | Standard top bar with title, back navigation, and trailing actions (returned from `buildAppBar` on `BaseScreenState`) |
| `button` (`Primary`, `Secondary`, `Outline`, `Danger`, `Loading`, `Disabled`) | `AppButton`, `AppButton.rounded` | Use `AppButton` style/loading parameters; never wrap or replace with raw Material `ElevatedButton` / `TextButton` |
| `formfield` (`TextField`, `Input`, `PasswordInput`, `NumberInput`) | `AppFormField`, `AppPasswordField` | Bind validation errors, `FocusNode`, `LabelText` (`app_core`), and `TextInputType` (`TextInputType.number` for numeric entry) |
| `search` (`SearchBar`, `SearchField`) | `AppSearchField` | Standard search input with debounce and clear support |
| `dropdown` (`Dropdown`, `Select`, `MultiSelect`) | `AppMultiDropdownFormField` | Single or multi-select dropdown form field |
| `datepicker` (`DatePicker`, `DateRangePicker`) | `AppDatePicker` | Date / date-range picker field |
| `dialog` (`Dialog`, `Modal`, `ConfirmModal`) | `AppDialog` | Trigger via `BlocListener` for confirmations, alerts, and error modals |
| `bottomsheet` (`BottomSheet`, `ActionSheet`) | `AppBottomSheetCommonLayout` | Standard modal bottom sheet container |
| `bottomnav` (`BottomNav`, `NavigationBar`) | `AppBottomNavigationBar` | Top-level bottom navigation bar |
| `badge` (`Badge`, `StatusPill`, `Tag`) | `BadgeWidget` | Status pill / semantic tag |
| `nodata` (`EmptyState`, `NoData`) | `AppNoData` | Mandatory widget for the `Empty` visual state |
| `loading` / `shimmer` (`Spinner`, `Skeleton`, `Shimmer`) | `AppLoadingIndicator` / `*Shimmer` (`ListViewShimmer`, `ImageShimmer`) | Mandatory widgets for the `Loading` visual state |
| `list` + pagination (`List`, `InfiniteList`) | `ListViewPaging` | Paginated list with built-in load-more and pull-to-refresh handling |
| `card`, `list-item`, `chip`, `banner` | Composition with `AppColor` tokens + `Text12`–`Text34` | Compose cleanly using `AppColor.*` and kit typography tokens |

---

## 2. Auditing W3C DTCG `tokens.json` ↔ `AppColor` & `Jakarta` (`Text12`–`Text34`)

When `planning` reads `.superpowers/sources/<ISSUE-ID>/figma/tokens.json` and `<stem>.spec.json`:

1. **Color Tokens (`tokens.json` → `color` ↔ `AppColor`)**:
   - Map Figma color token references (`{color.*}`) and hex `$value`s to `AppColor` in `package:app_ui_kit/app_ui_kit.dart`:
     - Primary / Brand: `AppColor.primary`, `AppColor.textOnPrimary`, `AppColor.primaryLight`, `AppColor.secondary`
     - Surfaces & Backgrounds: `AppColor.appBgColor`, `AppColor.surfaceColor`
     - Text Hierarchy: `AppColor.textPrimary`, `AppColor.textSecondary`, `AppColor.textTertiary`, `AppColor.hintColor`
     - Borders & Dividers: `AppColor.borderColor`, `AppColor.dividerColor`, `AppColor.inputBorder`, `AppColor.disabledColor`
     - Semantic Statuses: `AppColor.error` / `AppColor.errorLight`, `AppColor.success` / `AppColor.successLight`, `AppColor.warning` / `AppColor.warningLight`, `AppColor.infoLight`, `AppColor.shadowColor`
   - Never hardcode `Color(0xFF...)` in feature code. If a Figma node uses a one-off hex shade close to an `AppColor` token, propose snapping to the `AppColor` token (`KIT_OVERRIDE (D-NN)`).
2. **Typography Tokens (`tokens.json` → `typography` ↔ `Text12`–`Text34`)**:
   - Font family in `imespro` is `Jakarta` (provided by `app_ui_kit`).
   - Map Figma `fontSize` / `fontWeight` in `{typography.*}` to `Text12`, `Text14`, `Text16`, `Text18`, `Text20` … `Text34` (`.bold`, `.medium`, `.regular`) instead of raw `TextStyle(fontSize: ...)`.

---

## 3. Clean Architecture Screen Shell (`BaseScreen` / `BaseScreenState`)

Every mapped screen (`S-NN`) in an `imespro` workspace must align with the `app_core` screen architecture in `design.md`:
- Extend `BaseScreen` / `BaseScreenState` (`package:app_core/app_core.dart`), implementing `buildAppBar(BuildContext context)`, `buildScreen(BuildContext context)`, and `getScreen()` for analytics/route tracking.
- When Figma `bounds` or Huly requirements include tablet or landscape viewports, specify the responsive overrides (`buildTabletPortrait`, `buildMobileLandscape`, `buildTabletLandscape`) in `design.md`.
- Keep Domain entities and use cases 100% free of Flutter and `app_ui_kit` imports; handle one-shot dialogs (`AppDialog`), bottom sheets (`AppBottomSheetCommonLayout`), and navigation inside `BlocListener`.

---

## 4. Handling Unmapped Components (`C-NN` / `Core gap`) & Notifying the User

1. **Reuse First (`KIT_OVERRIDE (D-NN)`)**: If an `app_ui_kit` widget's `"Use when"` in `../app-ui-kit/guidance/GUIDE.md` fits the behavior — even if its visual styling differs slightly from the Figma render — ask the user (`Q-NN` → `D-NN`) to confirm reusing the `app_ui_kit` widget (`ACCEPTED (D-NN)` in visual verification).
2. **Record `Core gap` in `design.md` (Gate 2 Notification)**: When a Figma component or custom visual subtree has no match in `../app-ui-kit/guidance/GUIDE.md`:
   - Assign `C-01`, `C-02`... and record a **`Core gap`** row (`CORE_GAP (D-NN)`) in both `## UI/UX mapping` and `## Core usage` in `design.md`, naming the `C-NN`, the Figma `node_id` in `<stem>.spec.json`, the `GUIDE.md` sections checked, and the target Client path (`lib/modules/<feature>/presentation/widgets/` for one module, or `lib/shared/widgets/` for 2+ modules).
   - Never edit, copy, or fork `../app-core`, `../app-util`, or `../app-ui-kit` source files.
