# Canonical UI Pattern Inventory, `DESIGN-008` Mapping, and Missing-Widget Protocol (`C-NN` / `Core gap`)

> Topic: Canonical UI pattern categories from Figma `<stem>.spec.json` (`components[]` and `screens[i].tree`), `design.md` `## UI/UX mapping` contract (`DESIGN-008`), the user notification protocol when no fitting widget/function exists (`C-NN` / `Core gap`), and `BLOCKER` / `MAJOR` / `MINOR` review grading.

Rules **K4**, **K5**, **K7**, **K8**, **K9**, and **K10**.

---

## 1. Canonical UI Pattern Inventory (`K4`, `K7`)

When `planning` reads `<stem>.spec.json` (`screens[i].components`, `screens[i].tree`, and `tokens.json` → `$extensions.com.figma.components`), classify every UI control into one of these 17 canonical UI patterns and look up its target Flutter widget in the active workspace profile contract (`ui-kit-mapping-contracts.md` injected in `SKILL.md`):

| Canonical UI Pattern | Typical Figma Node / Component Names | Semantic UI Purpose |
|---|---|---|
| `appbar` | `AppBar`, `TopBar`, `Header`, `NavHeader` | Top screen bar with back navigation, title, and trailing action icons |
| `button` | `Button`, `CTA`, `IconButton`, `PrimaryButton` (`variant_properties`: `Primary`, `Secondary`, `Outline`, `Danger`, `Loading`, `Disabled`) | Primary, secondary, outline, text, and destructive action buttons |
| `formfield` | `TextField`, `Input`, `FormField`, `PasswordInput`, `NumberInput` (`State=Error`, `State=Disabled`) | Labeled text/password/numeric form input with validation message |
| `search` | `SearchBar`, `SearchField`, `SearchInput` | Search input bar with leading search icon and clear/debounce action |
| `dropdown` | `Dropdown`, `Select`, `MultiSelect`, `ComboBox` | Single or multi-select dropdown field |
| `datepicker` | `DatePicker`, `DateInput`, `DateRangePicker` | Date or time picker trigger field |
| `dialog` | `Dialog`, `Modal`, `Alert`, `ConfirmModal` | Modal confirmation, alert, or error dialog |
| `bottomsheet` | `BottomSheet`, `ActionSheet`, `DrawerBottom` | Modal bottom sheet for contextual actions, filters, or pickers |
| `bottomnav` | `BottomNav`, `TabBar`, `NavigationBar` | Bottom navigation bar for top-level destinations |
| `badge` | `Badge`, `Tag`, `StatusPill`, `StatusChip` (`Success`, `Warning`, `Error`, `Neutral`) | Status pill / semantic tag |
| `nodata` | `EmptyState`, `NoData`, `ZeroState` | Empty state view (`Empty` state of list/detail screens) |
| `loading` | `Spinner`, `Loading`, `ProgressIndicator` | Centered loading spinner (`Loading` state) |
| `shimmer` | `Shimmer`, `Skeleton`, `LoadingSkeleton` | Skeleton loading placeholder (`Loading` state) |
| `card` | `Card`, `ItemCard`, `SummaryCard`, `Panel` | Elevated or bordered surface container |
| `list` / `list-item` | `List`, `ListItem`, `RowItem`, `DataTable` | Vertical list (including paginated list) and structured row item |
| `chip` | `Chip`, `FilterChip`, `ChoiceChip` | Filter or selection chip |
| `banner` | `Banner`, `InlineAlert`, `Toast`, `SnackBar` | Inline alert, toast, or status banner |

---

## 2. What to Do When No Fitting Widget or Function Exists (`C-NN` / `Core gap` Protocol) (`K5`, `K8`, `K9`)

When auditing `<stem>.spec.json` and `<stem>-SNN.png` against the active profile's widget catalog at Gate 2 (`planning`), an element or behavior may have **no matching widget/function in the UI kit**, **multiple partial candidates**, or **a styling conflict between the Figma frame and the kit widget**. Never hide this gap or silently invent an unapproved widget:

### Case A — Ambiguous Fit (2+ Kit Widgets Fit the Same Figma Control)
- **Action**: Queue an `OPEN` `Q-NN` (`Owner: planning`) in `codebase-notes.md` and ask the user via `ask_question` presenting the 2–3 viable kit widgets with `(Recommended)` first. Record the confirmed choice as `D-NN` and mark `Status: MAPPED (D-NN)` in `design.md`.

### Case B — Kit Styling vs. Figma Conflict (`KIT_OVERRIDE`)
- **Condition**: An existing kit widget's `"Use when"` fits the functional behavior, but its built-in geometry, border radius, or token styling differs from the Figma node in `<stem>.spec.json`.
- **Action**: Queue a `Q-NN` (`Owner: planning`) asking the user via `ask_question`:
  1. `(Recommended)` Reuse the standard kit widget and accept the kit's styling (`KIT_OVERRIDE (D-NN)`).
  2. Build a custom feature widget (`CORE_GAP (D-NN)`).
- Never silently deviate from either the kit or the Figma spec without a confirmed `D-NN`.

### Case C — New Widget / Missing Kit Capability (`C-NN` / `Core gap`)
- **Condition**: A Figma component (`screens[i].components`) or custom visual subtree in `screens[i].tree` has **no matching widget** in the profile's UI kit (`app_ui_kit` / `lib/shared/` / standard Material 3), or a required utility/base helper is missing from core packages.
- **Action at Gate 2 (`planning` → `design.md`)**:
  1. Assign a deterministic component ID: **`C-01`**, **`C-02`**...
  2. Record an explicit **`Core gap`** row in **both** `## UI/UX mapping` and `## Core usage` / `## Client Core Mapping` in `design.md`:
     - **Missing item**: `C-NN` + Figma component/node name and `node_id` from `<stem>.spec.json`.
     - **Evidence checked**: Exact guide/shared paths searched (`../app-ui-kit/guidance/GUIDE.md`, `lib/shared/`, etc.) and why existing widgets do not fit.
     - **Client target**: `lib/modules/<feature>/presentation/widgets/<name>_widget.dart` (single module) or `lib/shared/widgets/<name>_widget.dart` (reused by 2+ modules).
  3. Confirm the `Core gap` with the user (`Q-NN` → `D-NN`) before locking Gate 2, and create an explicit task to build `C-NN` at Gate 3 (`implementation-plan.md`).

### Case D — Enforcement During Build, Review & QA (`code_writer`, `code_reviewer`, `test_runner`)
- **`code_writer`**: If an unmapped UI element is discovered mid-implementation that was not approved in `design.md`, stop and return **`BLOCKED`** with a `Q-NN` — never invent an unapproved custom widget or edit external kit packages.
- **`code_reviewer` & `test_runner`**:
  - Report any approved `KIT_OVERRIDE (D-NN)` or `CORE_GAP (D-NN)` as **`ACCEPTED (D-NN)`** in the review/verification report.
  - Flag any custom widget built without an approved `Core gap` (`D-NN`), or any bypassed kit widget, as **`BLOCKER`** (`FAIL`).

---

## 3. Required `## UI/UX mapping` Table in `design.md` (`DESIGN-008`) (`K7`, `K9`)

Whenever `requirements.md` has non-`EXISTING` `S-NN` screens in `## Screens & Visual Sources`, `design.md` must include `## UI/UX mapping` covering every non-`EXISTING` `S-NN`, key mapped kit widgets/tokens, and every `C-NN` new component (validated by `validate_proposal_spec` rule `DESIGN-008`):

| Screen / Component ID | Figma / Source Ref (`<stem>.spec.json` / `S-NN`) | Kind (`NEW` \| `CHANGED` \| `KIT_WIDGET` \| `NEW COMPONENT`) | Target Flutter Class / Widget & Route | Target File Path / Package | Phase & Status (`MAPPED` \| `KIT_OVERRIDE (D-NN)` \| `CORE_GAP (D-NN)`) |
|---|---|---|---|---|---|
| `S-01` | `Figma 1150:10051` (`work-orders.spec.json`, `work-orders-S01.png`) | `NEW` | `<Feature>ListScreen` (`/work-orders`) | `lib/modules/<feature>/presentation/screens/...` | `PHASE-01` · `MAPPED` |
| `button` / `search` | `S-01`, `S-02` (`Instance: PrimaryButton`, `SearchBar`) | `KIT_WIDGET` | `<Profile Button & Search Widgets>` | `<Package or Shared Path>` | `PHASE-01` · `MAPPED` |
| `C-01` | `S-02` (`Node 1150:10200` `GanttTimelineBar`) | `NEW COMPONENT` | `GanttTimelineBarWidget` | `lib/modules/<feature>/presentation/widgets/gantt_timeline_bar_widget.dart` | `PHASE-02` · `CORE_GAP (D-04)` — not in kit; approved at Gate 2 |

---

## 4. Review & Audit Severity Grading (`K10`)

| Finding | Severity (`shared_contracts/flags_and_statuses.md`) |
|---|---|
| Custom widget written where a profile kit widget fits without an approved `Core gap` (`D-NN`); `S-NN` or `C-NN` omitted from `design.md` (`DESIGN-008` `FAIL`); hardcoded raw `Color(0xFF...)` / `TextStyle` bypassing profile tokens; editing external core packages directly | **`BLOCKER`** |
| Wrong kit widget variant used (e.g., raw `TextFormField` instead of profile search/dropdown widget, or missing numeric/scanner focus handling specified in `design.md`) | **`MAJOR`** |
| Minor wrapper redundancy around a mapped kit widget with no visual or behavioral impact | **`MINOR`** |
