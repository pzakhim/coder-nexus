---
name: visual-verification
description: Launches approved Flutter UI targets, checks real-data states and captures revision-bound visual evidence.
---

# Flutter Visual Verification

Open and inspect the implemented UI. A successful build or widget test does not replace runtime review for UI-affecting phases.

## Preconditions

- Read the approved feature version and phase. Record its UI impact, target platform, entrypoint, flavor, device/viewport, route, required states and Visual AC.
- Fix the code revision under review. Record each state's data provenance without secrets or personal data. Follow the installed plugin's `shared_contracts/api_handshake_protocol.md`: use real services for live acceptance; explicitly approved contract-derived development fixtures may support only UI/contract checks. Record their contract revision and fixture path, never describe them as real business records or use them as production fallbacks.
- Read workspace instructions, `.fvmrc`, `pubspec.yaml`, launch configuration and device inventory. Do not invent a flavor, target or device.
- Missing credentials, safe navigation, a required live-data state or target means `BLOCKED`; an unattempted check is `NOT_RUN`. A fixture-backed UI result cannot change a required live integration check to `PASS`.

## Launch a real target

Use the Client's FVM command only when the workspace uses FVM. Inspect devices with `fvm flutter devices` or the equivalent configured command.

- **Flutter Web / Chrome:** Run the approved entrypoint and arguments, interact through the Client browser, then capture a screenshot or recording.
- **iOS Simulator:** Inspect devices with `xcrun simctl list devices available`; boot the approved device with `xcrun simctl boot <device-id>` if needed and run the app on it.
- **Android Emulator:** Inspect with `fvm flutter emulators`, launch the approved AVD, and run the app on the selected device.

Keep the Flutter process and runtime logs available during inspection. Fail explicitly if SDK tools or the approved platform are unavailable.

## Inspect required states

Exercise only approved, safely reachable states: initial/loading, populated, empty, safe error, validation, keyboard, back navigation, theme, text scale, viewport or orientation as applicable. Compare layout, spacing, typography, colors, contrast, icons, kit variants, scrolling, touch targets, focus, messages and navigation with the approved visual source and AC. Do not claim pixel-perfect equivalence without an approved baseline or golden comparison.

For a screen using `BaseScreen`, inspect portrait and landscape on the approved device/viewport when the changed behavior relies on responsive layout. Record route, orientation, expected and observed layout. A screenshot cannot prove tracking events; use the Client's actual approved tracking evidence for that claim. Mark unavailable observability `BLOCKED` or `NOT_RUN` rather than inferring a pass.

## Capture evidence

Save evidence under `.superpowers/work-items/<slug>/vN/evidence/<phase-id>/<revision>/visual/` unless the Client defines another approved location.

- iOS screenshot: `xcrun simctl io <device-id> screenshot <artifact-path>.png`
- Android screenshot: `adb -s <device-serial> exec-out screencap -p > <artifact-path>.png`
- Chrome: use the browser's screenshot or recording capability.

Open and inspect every required screenshot, then share the actual images and findings with the coordinator for pre-release review. A saved path alone is not evidence. Protect credentials and unrelated personal data. Record platform, device/viewport, flavor, entrypoint, route/state, real data provenance, timestamp and code revision. Golden comparison is optional and complementary: use it only for stable, approved states with a reviewed baseline; never treat a live-data screenshot with changing content as a deterministic golden.

## Golden Screenshot Verification (`golden_screenshot`)

For headless screen visual testing, asset rendering, and device frame preview, see [Golden Screenshot Recipe](references/01_golden_screenshot_recipe.md).
- **Headless Screen Rendering**: Generates pixel-accurate screen captures without booting an emulator or simulator.
- **Review Workflow**: `code_writer` generates initial baseline via `flutter test --update-goldens`; `code_reviewer` inspects the generated `.png` artifacts against design; `test_runner` executes regression checks with standard `flutter test` (without `--update-goldens`).

## Verdict

Return a result for each required state: `PASS` when observed and evidenced; `FAILED` for a defect or material difference from approved Visual AC; `BLOCKED` for an unavailable dependency; `NOT_RUN` when unattempted. A code fix creates a new revision and requires affected review, tests and visual states to run again. For a non-UI phase, record `UI impact: no` with the reason; do not launch an emulator just to satisfy a checkbox.
