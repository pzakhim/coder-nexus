# Design References, Visual Matrix, and Runtime Target Capture

> Topic: Visual reference priority (extracted Figma per-screen `.png` renders & `<stem>.spec.json`, `design.md` `## UI/UX mapping`, pre-change baseline), `Screen × State × Viewport` matrix, API data provenance (`FE_MOCKOON` vs `BE_LIVE`), and runtime screenshot capture on iOS, Android, and Web/Desktop.

Rules **V1**, **V2**, **V3**, **V4**, **V5**, **V10**, and **V11**.

---

## 1. Preconditions & Visual Reference Hierarchy (`V1`, `V10`)

Before launching a simulator, emulator, or browser target:
1. **Inspect Workspace Config**: Read `.fvmrc` (`fvm flutter` vs `flutter`), `pubspec.yaml`, `.vscode/launch.json`, `.superpowers/setup.json` (`architecture_profile`), and `design.md`. Never invent a flavor, entrypoint, or device.
2. **Resolve the Visual Reference (in strict priority order)**:
   - **Priority 1 — Extracted Figma Per-Screen Renders & Spec (`FIGMA_PROVIDED`)**: Open `.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` alongside `<stem>.spec.json` (`screens[i].bounds` and `tree`), `tokens.json`, and `design.md` (`## UI/UX mapping`).
   - **Priority 2 — Labeled Pre-Change Baseline (`CODEBASE_ONLY` / Refactor)**: Captured before the change and labeled `baseline` — used for minor edge-case adjustments on existing screens (`CODEBASE_ONLY`) or refactoring items when approved in `requirements.md` and `design.md`.
   - **Missing Visual Reference**: Record `VISUAL_INPUT_MISSING` / `BLOCKED`. Never invent a generic fallback screen or claim `PASS` without a reference.

---

## 2. Like-for-Like Screen × State × Viewport Matrix (`V2`, `V5`, `V11`)

Every screen in scope (`UI Impact: Yes`) must be exercised across all **4 mandatory visual states** (`Loading`, `Content`, `Empty`, `Error`) plus any interactive states (form validation, dialog/bottom-sheet, keyboard inset, portrait/landscape orientation) required by `requirements.md` and `design.md`:

| Screen (`S-NN`) | Mandatory States | Viewport / Orientation | Data Mode (`FE_MOCKOON` \| `BE_LIVE`) | Artifact Path |
|---|---|---|---|---|
| `S-01 (<Feature>Screen)` | `Loading`, `Content`, `Empty`, `Error` | Confirmed viewport(s) in `design.md` (`portrait` / `landscape`) | Per `design.md` `D-NN` | `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<revision>/visual/S-01_<state>_<viewport>.png` |

- **API & Data Provenance (`shared_contracts/api_handshake_protocol.md`)**:
  - **`FE_MOCKOON` (`MOCKOON_MOCKED`)**: Ensure `mockoon-cli` is running (`mockoon-cli start --data mocks/<feature>_mockoon.json --port <port>`) and trigger the Pass (`200`), Empty (`[]`), and Fail (`400/500`) rules to capture `Content`, `Empty`, and `Error` states deterministically. Label these captures `FE_MOCKOON` with the contract revision; they prove UI/contract rendering only and never turn a required `BE_LIVE` integration AC into `PASS`.
  - **`BE_LIVE` (`BE_API_READY`)**: Exercise real services with safe test accounts. If a required live-data state cannot be safely reached, mark that state `BLOCKED` or `NOT_RUN`, never `PASS`.
- **Data Hygiene (`V11`)**: Never display or capture real credentials, tokens, or personal data on screen; redact sensitive values before saving artifacts.

---

## 3. Launching Real Flutter Targets & Capturing Screenshots (`V3`, `V4`)

Use `fvm flutter` when `.fvmrc` is present in the Client workspace; otherwise use `flutter`. Check available targets with `flutter devices`.

| Target Platform | Launch Command | Screenshot Capture Command |
|---|---|---|
| **iOS Simulator** | `xcrun simctl list devices available` → `xcrun simctl boot <device-id>` → `flutter run -d <device-id> --flavor <flavor> -t <entrypoint>` | `xcrun simctl io <device-id> screenshot <artifact-path>.png` |
| **Android Emulator** | `flutter emulators --launch <emulator-id>` → `flutter run -d <device-serial> --flavor <flavor> -t <entrypoint>` | `adb -s <device-serial> exec-out screencap -p > <artifact-path>.png` |
| **Flutter Web / Chrome** | `flutter run -d chrome --flavor <flavor> -t <entrypoint>` (resize browser to `.superpowers/ux/viewports.json`) | Capture browser viewport screenshot to `<artifact-path>.png` |
| **macOS / Desktop** | `flutter run -d macos --flavor <flavor> -t <entrypoint>` | Capture window screenshot to `<artifact-path>.png` |

- **Evidence & Screen Catalog Locations**:
  1. **Phase Evidence**: Save under `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<revision>/visual/`.
  2. **Screen Catalog Update**: Save the populated `Content` screenshot at each confirmed viewport to `.superpowers/ux/current/<catalog-slug>/<viewport>.png`.
- **Mandatory Visual Inspection (`V4`)**: Open and inspect every saved `.png` file, and share the actual images and findings with the coordinator. A saved file path without visual inspection is **`UNVERIFIED`**.
