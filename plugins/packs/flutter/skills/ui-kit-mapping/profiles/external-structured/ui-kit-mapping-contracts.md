# UI Kit Mapping Contracts — `external-structured` Profile (`lib/shared/` & Client Theme)

> Topic: Mapping extracted Figma `tokens.json` (W3C DTCG) and `<stem>.spec.json` (`screens[i].tree`, `components`) to the Client's own theme tokens and shared widgets (`lib/shared/` or `lib/core/`) in `design.md` (`DESIGN-008`), and surfacing `C-NN` / `Core gap`s at Gate 2.

When `.superpowers/setup.json` sets `profile = "external-structured"`, `planning` resolves visual foundations from the Client's internal design system (`lib/core/theme/`, `lib/shared/widgets/`, or `lib/commons/widgets/`).

---

## 1. Mapping Figma Components & Patterns (`<stem>.spec.json`) → Client Shared Widgets

Inspect the Client's shared UI directory (`lib/shared/` or `lib/core/`) alongside `<stem>.spec.json` (`screens[i].components` and `screens[i].tree`) when populating `## UI/UX mapping` (`DESIGN-008`) and `## Client Core Mapping` in `design.md`:

| Canonical UI Pattern / Figma Node | Primary Mapping Target (`lib/shared/` or `lib/core/`) | Fallback (When Client Has No Dedicated Shared Widget) |
|---|---|---|
| `appbar` (`AppBar`, `TopBar`, `Header`) | Client shared AppBar widget | Material 3 `AppBar` with Client theme tokens |
| `button` (`Primary`, `Secondary`, `Outline`, `Danger`, `Loading`) | Client shared Button widget | `FilledButton` / `OutlinedButton` / `TextButton` styled via Client theme |
| `formfield` / `search` / `dropdown` / `datepicker` | Client shared Input / Search / Dropdown / DatePicker widgets | `TextFormField` / `SearchBar` / `DropdownMenu` / `showDatePicker` |
| `dialog` / `bottomsheet` | Client shared Dialog / BottomSheet helpers | `AlertDialog` / `showModalBottomSheet` |
| `nodata` / `loading` / `shimmer` | Client shared Empty / Loading / Shimmer widgets | Reusable state widget under `lib/shared/widgets/` |
| `badge` / `card` / `list-item` / `chip` / `banner` | Client shared surface/tag widgets | `Badge` / `Card` / `ListTile` / `Chip` / `MaterialBanner` |

---

## 2. Auditing W3C DTCG `tokens.json` ↔ Client Theme Tokens

- **Color & Typography Tokens**: Compare `{color.*}`, `{typography.*}`, and `{dimension.*}` in `.superpowers/sources/<ISSUE-ID>/figma/tokens.json` against the Client's theme classes (`AppColors`, `AppTextStyles`, `ThemeExtension`, `Theme.of(context).colorScheme`).
- Always reference the Client's theme tokens in Flutter code — never hardcode raw `Color(0xFF...)` or `TextStyle` literals inside feature screens.
- If `tokens.json` contains a color or typography scale that differs from the Client theme, queue a `Q-NN` (`Owner: planning`) asking the user whether to use the existing Client theme token (`KIT_OVERRIDE (D-NN)`) or add a new token to the Client theme (`D-NN`).

---

## 3. Missing Shared Widgets (`C-NN` / `Core gap` Notification at Gate 2)

When a Figma component (`screens[i].components`) or custom subtree in `<stem>.spec.json` is not present in the Client's `lib/shared/` catalog:
- Assign `C-01`, `C-02`... and record it in `## UI/UX mapping` and `## Client Core Mapping` in `design.md` (`CORE_GAP (D-NN)`) with its Figma `node_id`, the `lib/shared/` paths searched, and its target destination (`lib/modules/<feature>/presentation/widgets/` for 1 module, or `lib/shared/widgets/` when reused across 2+ modules) for user approval at Gate 2.
