# UI Kit Mapping Contracts — `external-standard` Profile (Material 3 / Cupertino)

> Topic: Mapping extracted Figma `tokens.json` (W3C DTCG) and `<stem>.spec.json` (`screens[i].tree`, `components`) to standard Flutter Material 3 / Cupertino widgets and `ThemeData` / `ColorScheme` tokens in `design.md` (`DESIGN-008`).

When `.superpowers/setup.json` sets `profile = "external-standard"`, `planning` maps Figma specifications directly to Flutter's standard Material 3 / Cupertino widget catalog and `ThemeData` (`ColorScheme`, `TextTheme`).

---

## 1. Mapping Figma Components & Patterns (`<stem>.spec.json`) → Standard Flutter (Material 3) Widgets

Use this table when `planning` populates `## UI/UX mapping` (`DESIGN-008`) in `design.md` from `<stem>.spec.json`:

| Canonical UI Pattern / Figma Node | Standard Flutter / Material 3 Widget | Notes & Variant Mapping |
|---|---|---|
| `appbar` (`AppBar`, `TopBar`, `Header`) | `AppBar`, `SliverAppBar`, `BackButton`, `IconButton` | Top app bar inside `Scaffold.appBar` |
| `button` (`Primary`, `Secondary`, `Outline`, `Text`, `Danger`, `Loading`) | `FilledButton`, `FilledButton.tonal`, `OutlinedButton`, `TextButton` | Use `colorScheme.error` for destructive actions; inline `SizedBox` + `CircularProgressIndicator` for loading state |
| `formfield` (`TextField`, `Input`, `Error`, `Disabled`) | `TextFormField` / `TextField` (`InputDecoration`) | Bind `errorText`, `enabled`, and `keyboardType` |
| `search` (`SearchBar`, `SearchField`) | `SearchBar` / `SearchAnchor` | Standard Material 3 search bar |
| `dropdown` (`Dropdown`, `Select`) | `DropdownMenu<T>` / `DropdownButtonFormField<T>` | Material 3 dropdown menu |
| `datepicker` (`DatePicker`, `DateRangePicker`) | `showDatePicker` / `showDateRangePicker` / `InputDatePickerFormField` | Material 3 date picker dialog |
| `dialog` (`Dialog`, `Modal`, `Alert`) | `AlertDialog` (`showDialog`) | Triggered via `BlocListener` or action callback |
| `bottomsheet` (`BottomSheet`, `ActionSheet`) | `showModalBottomSheet` / `BottomSheet` | Modal bottom sheet with `showDragHandle: true` |
| `bottomnav` (`BottomNav`, `NavigationBar`) | `NavigationBar` (`NavigationDestination`) / `BottomNavigationBar` | Material 3 bottom navigation bar |
| `badge` (`Badge`, `StatusPill`, `Tag`) | `Badge` / status `Chip` | Semantic colors from `Theme.of(context).colorScheme` |
| `nodata` (`EmptyState`, `NoData`) | Empty-state `Column` (icon + title + subtitle + optional retry button) | Extract to `lib/modules/<feature>/presentation/widgets/` or `lib/shared/widgets/` |
| `loading` / `shimmer` (`Spinner`, `Skeleton`) | `CircularProgressIndicator` / skeleton placeholder container | Centered loading indicator or shimmer container |
| `card`, `list-item`, `chip`, `banner` | `Card`, `ListTile`, `FilterChip` / `ChoiceChip` / `ActionChip`, `MaterialBanner` / `SnackBar` | Standard Material 3 surface, list, chip, and banner components |

---

## 2. Auditing W3C DTCG `tokens.json` ↔ `ThemeData` (`ColorScheme` & `TextTheme`)

- **Theme Tokens**: Map `{color.*}` in `.superpowers/sources/<ISSUE-ID>/figma/tokens.json` to `Theme.of(context).colorScheme` (`primary`, `onPrimary`, `primaryContainer`, `secondary`, `surface`, `onSurface`, `onSurfaceVariant`, `outline`, `outlineVariant`, `error`, `errorContainer`) and `{typography.*}` to `Theme.of(context).textTheme` (`titleLarge`, `titleMedium`, `bodyLarge`, `bodyMedium`, `labelLarge`).
- **New Custom Components (`C-NN`) Notification at Gate 2**: Any bespoke non-Material widget in `<stem>.spec.json` (`screens[i].components` or custom `screens[i].tree` subtree) must be assigned `C-01`, `C-02`..., mapped in `design.md` (`## UI/UX mapping`) to a concrete widget class under `lib/modules/<feature>/presentation/widgets/` (or `lib/shared/widgets/` when shared by 2+ modules), and surfaced for user approval at Gate 2.
