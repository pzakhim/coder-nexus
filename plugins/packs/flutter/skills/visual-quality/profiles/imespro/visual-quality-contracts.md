# iMESPro Visual Quality Contracts (`app_ui_kit`, `BaseScreen`, `ListViewPaging`)

> Topic: Visual fidelity verification for `imespro` workspaces using `app_ui_kit` components, `BaseScreen` portrait/landscape responsiveness, and `ListViewPaging` states.

This reference is auto-injected when `.superpowers/setup.json` sets `"architecture_profile": "imespro"`.

---

## 1. Verifying `app_ui_kit` Component & Token Fidelity

During runtime visual inspection (`01-references-matrix-and-capture.md`) and golden review (`02-golden-screenshot-workflow.md`), compare the rendered screen against `design.md` (`Core usage` and `## UI/UX mapping` tables), extracted Figma per-screen `.png` renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`), and `../app-ui-kit/guidance/GUIDE.md`:

| `app_ui_kit` Area | Visual Verification Check (`BLOCKER` on violation) |
|---|---|
| **Buttons (`AppButton`, `AppButton.rounded`)** | Verify primary, secondary, outline, destructive, disabled, and loading spinner states use `AppButton` rather than raw Material `ElevatedButton` / `TextButton`. |
| **Inputs & Pickers (`AppFormField`, `AppDatePicker`, `AppMultiDropdownFormField`)** | Verify focus border, inline error message (`is-error`), disabled state (`is-disabled`), password visibility toggle, and required field markers (`LabelText` from `app_core`). |
| **Dialogs & Bottom Sheets (`AppDialog`, `AppBottomSheetCommonLayout`)** | Verify modal header, close action, content padding, and action button layout match `app_ui_kit`. |
| **4 Visual States (`AppLoadingIndicator`, `AppNoData`, `ImageShimmer`, `ListViewPaging`)** | • `Loading`: `AppLoadingIndicator` or `*Shimmer` rendered without layout jump.<br>• `Content`: `ListViewPaging` items, pull-to-refresh, and load-more footer.<br>• `Empty`: `AppNoData` illustration and message.<br>• `Error`: Standardized error feedback and retry trigger. |
| **Typography & Colors (`Text12`–`Text34`, `AppColor.*`)** | Verify text uses `Jakarta` font tokens (`Text12`…`Text34`) and `AppColor.*` palette without hardcoded `Color(0x...)` values. |

- **Kit Styling Wins (`ACCEPTED (D-NN)`)**: When `AppButton`, `AppFormField`, or `AppNoData` styling differs slightly from a raw mockup because `app_ui_kit` enforces company tokens, treat the `app_ui_kit` rendering as authoritative (`ACCEPTED (D-NN)`).

---

## 2. `BaseScreen` Responsive Layout & Tracking Evidence

For any screen extending `BaseScreen` / `BaseScreenState` (`app_core`):
1. **Portrait & Landscape / Tablet Verification**: When the approved requirements or `viewports.json` include tablet or landscape support (`buildTabletPortrait`, `buildMobileLandscape`, `buildTabletLandscape`), capture and inspect both orientations on the target device/simulator. Record route, orientation, expected layout, and observed layout.
2. **Screen Analytics / Route Observer (`getScreen()`)**: A screenshot alone cannot prove analytics/tracking events. Verify `getScreen()` / `MatomoHelper` tracking via runtime logs or unit/widget assertions; mark unavailable tracking observability as `BLOCKED` or `NOT_RUN`, never `PASS`.
