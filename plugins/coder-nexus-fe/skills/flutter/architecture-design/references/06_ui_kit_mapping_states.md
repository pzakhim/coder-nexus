# 06 — UI Component Mapping and 4 Visual States

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for the `UI design system` section of `design.md`.

## 1. Read, then decide (Flutter)

Source of truth: `../app-ui-kit/guidance/GUIDE.md` (decision table §1), read through the `{{slot:core-usage}}` skill. Screen base, paged list and form label live in the app_core guide.

For each UI element in the requirements:

1. **Kit row fits ("Use when" matches)** → reuse it. Kit styling wins over small visual differences; record the difference in the mapping.
2. **Several rows could fit** → ask the user with `ask_question` (2–3 options, one recommended).
3. **No fit, or a "Do not use when" applies** → compose kit widgets, else plain Flutter in `lib/modules/<feature>/presentation/widgets/`. Record a Core gap row in `Core usage`. Move it to a shared folder only when two or more modules need it.

Do not invent widget names, props or variants. Confirm each signature in the guide or package source.

## 2. Four mandatory visual states

Every screen and primary view defines:

1. **Loading** — the guide's loading/skeleton widget when it fits.
2. **Content** — the normal layout with interactions.
3. **Empty** — the guide's empty-state widget when it fits, with message and optional action.
4. **Error** — inline vs full-screen, message source, retry action.

A state that cannot occur gets `N/A` with a reason.

## Output format

```markdown
## UI design system

### UI Component Mapping
| UI Element / AC | Component | Source Package | Variant / Props | Rationale |
|---|---|---|---|---|
| Primary action button · AC-02 | `AppButton` | app_ui_kit · §2.1 | primary | Kit row fits |
| Paged item list · AC-01 | `ListViewPaging<<Feature>Entity>` | app_core · §2.4 | pageSize 20 | API returns `pagination.total` |
| Custom status chip · AC-03 | `<Feature>StatusChip` (Client) | `lib/modules/<feature>/presentation/widgets/` | — | Gap: no chip in kit |

### Four Mandatory Visual States
- **1. Loading State**: `AppLoadingIndicator` as `ListViewPaging.loadingIndicator`.
- **2. Content State**: list rows with status chip.
- **3. Empty State**: `AppNoData` with empty state message.
- **4. Error State**: full-screen message + retry calling `cubit.loadData()`.
```

Example rows illustrate the format; take real names from the guides read for this work item.
