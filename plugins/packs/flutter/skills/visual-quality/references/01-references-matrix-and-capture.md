# Design References, Visual Matrix, and Runtime Target Capture

> Topic: Visual reference priority (`FIGMA_PROVIDED` per-screen `.png` + `tokens.json` + `<stem>.spec.json`, `HTML_SITEMAP_PROVIDED` `sitemap/screens/<id>_<code>.png` + `*.spec.json`, `design.md` `## UI/UX mapping`, pre-change baseline), `Screen × State × Viewport` matrix, API data provenance (`FE_MOCKOON` vs `BE_LIVE`), Hybrid E2E driving & capture commands, and 3-role evidence paths.

Rules **V1**, **V2**, **V3**, **V4**, **V5**, **V10**, and **V11**.

---

## 1. Preconditions & Visual Reference Hierarchy (`V1`, `V10`)

Before launching a simulator, emulator, or browser target:
1. **Inspect Workspace Config**: Read `.fvmrc` (`fvm flutter` vs `flutter`), `pubspec.yaml`, `.vscode/launch.json`, `.superpowers/setup.json` (`architecture_profile`), and `design.md`. Never invent a flavor, entrypoint, or device.
2. **Resolve the Visual Reference (in strict priority order)**:
   - **Priority 1 — Extracted Figma or Interactive HTML Sitemap Renders & Spec (`FIGMA_PROVIDED` | `HTML_SITEMAP_PROVIDED`)**:
     - `FIGMA_PROVIDED`: Load `.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png` via multimodal `read_file` alongside `tokens.json` and `<stem>.spec.json`.
     - `HTML_SITEMAP_PROVIDED`: Load `.superpowers/sources/<ISSUE-ID>/sitemap/screens/<id>_<code>.png` via multimodal `read_file` alongside `sitemap/screens/<id>_<code>.spec.json` (no `tokens.json` required; styling follows active workspace profile tokens).
     - Pair both modes with `design.md` (`## UI/UX mapping`).
   - **Priority 2 — Labeled Pre-Change Baseline (`CODEBASE_ONLY` / Refactor)**: Captured before the change and labeled `baseline` — used for minor edge-case adjustments on existing screens (`CODEBASE_ONLY`) or refactoring items when approved in `requirements.md` and `design.md`.
   - **Missing Visual Reference**: Record `VISUAL_INPUT_MISSING` / `BLOCKED`. Never invent a generic fallback screen or claim `PASS` without a reference.

---

## 2. Like-for-Like Screen × State × Viewport Matrix (`V2`, `V5`, `V11`)

Every screen in scope (`UI Impact: Yes`) must be exercised across all **4 mandatory visual states** (`Loading`, `Content`, `Empty`, `Error`) plus any interactive states (form validation, dialog/bottom-sheet, keyboard inset, portrait/landscape orientation) required by `requirements.md` and `design.md`:

| Screen (`S-NN`) | Mandatory States | Viewport / Orientation | Data Mode (`FE_MOCKOON` \| `BE_LIVE`) | Artifact Path |
|---|---|---|---|---|
| `S-01 (<Feature>Screen)` | `Loading`, `Content`, `Empty`, `Error` | Confirmed viewport(s) in `design.md` (`portrait` / `landscape`) | Per `design.md` `D-NN` | `vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/S-01_<state>_<viewport>.png` (`code_writer`) or `vN/evidence/final_qa/<revision>/visual/S-01_<state>_<viewport>.png` (`test_runner`) |

- **API & Data Provenance (`shared_contracts/api_handshake_protocol.md`)**:
  - **`FE_MOCKOON` (`MOCKOON_MOCKED`)**: Ensure `mockoon-cli` is running (`mockoon-cli start --data mocks/<feature>_mockoon.json --port <port>`) and trigger the Pass (`200`), Empty (`[]`), and Fail (`400/500`) rules to capture `Content`, `Empty`, and `Error` states deterministically. Label these captures `FE_MOCKOON` with the contract revision; they prove UI/contract rendering only and never turn a required `BE_LIVE` integration AC into `PASS`.
  - **`BE_LIVE` (`BE_API_READY`)**: Exercise real services with safe test accounts. If a required live-data state cannot be safely reached, mark that state `BLOCKED` or `NOT_RUN`, never `PASS`.
- **Data Hygiene (`V11`)**: Never display or capture real credentials, tokens, or personal data on screen; redact sensitive values before saving artifacts.

---

## 3. Launching, Driving & Capturing Real Flutter Targets (`V3`, `V4`)

Use `fvm flutter` when `.fvmrc` is present in the Client workspace; otherwise use `flutter`. Check available targets with `flutter devices`.

| Target Platform | Launch Command | Live UI Driving (Read-Only `test_runner` / `code_writer`) | Screenshot Capture Command |
|---|---|---|---|
| **Flutter Web / Chrome** | `flutter run -d chrome --flavor <flavor> -t <entrypoint>` (or `flutter run -d web-server --web-port <port>`) | Drive flows and inspect runtime health via Antigravity's builtin **`browser` subagent** or **`chrome-devtools` MCP** (`navigate_page`, `click`, `fill`, `list_console_messages`, `list_network_requests`) resized to confirmed viewports | `chrome-devtools` `take_screenshot` or `browser` subagent screenshot saved to `<artifact-path>.png` |
| **iOS Simulator** | `xcrun simctl list devices available` → `xcrun simctl boot <device-id>` → `flutter run -d <device-id> --flavor <flavor> -t <entrypoint>` | Deep links (`xcrun simctl openurl <device-id> <uri>`), Mockoon state switches, or executing an existing approved `integration_test/` driver (`flutter test integration_test/<file> -d <device-id>`) | `xcrun simctl io <device-id> screenshot <artifact-path>.png` |
| **Android Emulator** | `flutter emulators --launch <emulator-id>` → `flutter run -d <serial> --flavor <flavor> -t <entrypoint>` | `adb -s <serial> shell input tap <x> <y>` / `text "<val>"` / `keyevent <key>`, deep links (`adb -s <serial> shell am start -a android.intent.action.VIEW -d <uri>`), or executing an existing approved `integration_test/` driver (`flutter test integration_test/<file> -d <serial>`) | `adb -s <serial> exec-out screencap -p > <artifact-path>.png` |
| **macOS / Desktop** | `flutter run -d macos --flavor <flavor> -t <entrypoint>` | Existing approved `integration_test/` driver (`flutter test integration_test/<file> -d macos`) or desktop window interaction | `screencapture -x <artifact-path>.png` (or window capture `-l <window-id>`) |

- **Strict 3-Role Evidence Ownership (No `.superpowers/ux/` Writes Here)**:
  1. **`code_writer`**: Saves revision-bound 4-state captures under `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<REVIEW_REVISION>/visual/` and lists every `.png` path in `writer-handoff.md` (`Visual Artifacts:`).
  2. **`code_reviewer`**: Read-only — inspects `writer-handoff.md` `Visual Artifacts:` PNGs side-by-side against Figma or HTML sitemap references via parallel `read_file`, and records `## Visual Comparison` in `vN/reviews/review_<phase-id>_<REVIEW_REVISION>.md`.
  3. **`test_runner`**: Performs independent `final_qa` live runtime capture ONLY under `.superpowers/work-items/<slug>/vN/evidence/final_qa/<revision>/visual/` and cites them in `acceptance-report.md`. **Never** write to `.superpowers/ux/` — `.superpowers/ux/` belongs exclusively to `docs_writer` after `ACCEPTED`.
- **Mandatory Multimodal Inspection (`V4`)**: Always load the reference `.png` (Figma or HTML sitemap) and the captured Flutter `.png` in parallel using Antigravity's native **`read_file`** tool to perform side-by-side comparison. A saved file path without `read_file` inspection is **`UNVERIFIED`**.
