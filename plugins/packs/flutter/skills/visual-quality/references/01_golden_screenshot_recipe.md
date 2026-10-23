# 01 — Golden Screenshot Recipe and Visual Review Guide

Use a golden harness only when approved and already available, or when its dependency addition is explicitly approved. Golden evidence supplements required runtime checks; it never proves live integration. Follow `{{slot:visual-quality}}` and the shared handshake evidence policy.


Guide for using [`golden_screenshot`](https://pub.dev/packages/golden_screenshot) to generate realistic screen renders, review 4 visual states, and verify pixel fidelity without heavy device emulators.

---

## 1. Why `golden_screenshot`?

1. **Headless Execution**: Renders full-fidelity screens in headless Flutter test mode in seconds, without spinning up heavy iOS Simulators or Android Emulators.
2. **Realistic Device Frames**: Wraps screens inside authentic device bezels (iPhone, Android, iPad, Desktop with titlebar).
3. **Fuzzy Comparator & Shadows**: Enables real shadows (`testGoldens`) with configurable diff tolerance (~1%) to eliminate flaky false failures.
4. **Offline Asset Loading**: Loads custom typography and local assets via `tester.loadAssets()` to prevent black-box font placeholders.

---

## 2. Setup in Client Workspace

Add to `pubspec.yaml` under `dev_dependencies`:
```yaml
dev_dependencies:
  golden_screenshot: ^12.1.1
  flutter_test:
    sdk: flutter
```

---

## 3. Authoring Screen Golden Tests (`code_writer`)

For any phase creating or modifying a Screen destination (`presentation/screens/*_screen.dart`), create a corresponding test file:
`test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart`

### Standard 4-State Template:
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_screenshot/golden_screenshot.dart';
import 'package:my_client_app/modules/<feature>/presentation/screens/<feature>_screen.dart';

void main() {
  group('<Feature>Screen Golden Visual Tests', () {
    testGoldens('Renders all 4 visual states with realistic device frame', (tester) async {
      // 1. Load local fonts and asset bundles
      await tester.loadAssets();

      // State 1: Default / Populated State
      final defaultScreen = ScreenshotApp(
        device: GoldenScreenshotDevices.iphone.device,
        child: MaterialApp(
          home: <Feature>Screen(state: <Feature>State.initial()),
        ),
      );
      await tester.pumpWidget(defaultScreen);
      await tester.pumpAndSettle();
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '1_<feature>_default',
      );

      // State 2: Loading State
      final loadingScreen = ScreenshotApp(
        device: GoldenScreenshotDevices.iphone.device,
        child: MaterialApp(
          home: <Feature>Screen(state: <Feature>State.loading()),
        ),
      );
      await tester.pumpWidget(loadingScreen);
      await tester.pump(); // Pump frame for spinner
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '2_<feature>_loading',
      );

      // State 3: Empty State
      final emptyScreen = ScreenshotApp(
        device: GoldenScreenshotDevices.iphone.device,
        child: MaterialApp(
          home: <Feature>Screen(state: <Feature>State.empty()),
        ),
      );
      await tester.pumpWidget(emptyScreen);
      await tester.pumpAndSettle();
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '3_<feature>_empty',
      );

      // State 4: Error State (Validation / Network Failure)
      final errorScreen = ScreenshotApp(
        device: GoldenScreenshotDevices.iphone.device,
        child: MaterialApp(
          home: <Feature>Screen(state: <Feature>State.error('Connection timeout')),
        ),
      );
      await tester.pumpWidget(errorScreen);
      await tester.pumpAndSettle();
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '4_<feature>_error',
      );
    });
  });
}
```

---

## 4. Execution Commands across Roles

### Step 1: Baseline Creation (`code_writer` in Phase 3)
Run with `--update-goldens` to produce `.png` screenshot files:
```bash
flutter test test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart --update-goldens
```
Output files are stored under `test/goldens/` or `metadata/en-US/images/phoneScreenshots/`.

### Step 2: Visual Inspection & Review (`code_reviewer` in Phase 3)
Open and inspect each generated `.png` image using `view_file` or IDE image preview:
1. **Design Conformance**: Compare against `design.md` and the approved profile’s design-system guidance (iMESPro: `app_ui_kit` GUIDE).
2. **Layout Integrity**: Verify no yellow/black `RenderFlex overflowed` stripes.
3. **Safe Areas**: Confirm content respects notch, status bar, and home bar.
4. **Touch Targets & Contrast**: Verify buttons meet 48x48 dp minimum and 4.5:1 text contrast.
5. If visual differences or layout defects exist: mark `CHANGES_REQUESTED`.
6. If verified: mark `APPROVED` and commit the baseline `.png` to Git.

### Step 3: Regression Verification (`test_runner` in Phase 4)
Run standard test command **WITHOUT** `--update-goldens`:
```bash
flutter test test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart
```
- Compares current render with approved baseline.
- If pixel difference exceeds 1% tolerance: Fails automatically and generates failure diff image.
- **Strict Rule**: `test_runner` MUST NEVER run `--update-goldens`.
