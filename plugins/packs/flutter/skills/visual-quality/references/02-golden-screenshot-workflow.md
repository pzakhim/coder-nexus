# Headless Golden Screenshot Workflow (`golden_screenshot`)

> Topic: Headless 4-state screen rendering with `golden_screenshot`, offline font/asset loading, device frames, and strict role boundaries (`code_writer` vs `code_reviewer` vs `test_runner`).

Rules **V3**, **V4**, and **V8**. Use a golden harness when `golden_screenshot` is already present in `pubspec.yaml` (`dev_dependencies`) or explicitly approved in `implementation-plan.md`. Golden evidence supplements runtime checks (`01`); it never proves live backend integration (`BE_LIVE`).

---

## 1. Why `golden_screenshot` in Flutter

1. **Headless Speed**: Renders full-fidelity screens across all 4 visual states in `flutter test` within seconds, without booting heavy iOS Simulators or Android Emulators.
2. **Realistic Device Frames & Safe Areas**: Wraps screens inside authentic device bezels (`GoldenScreenshotDevices.iphone`, Android, iPad, Desktop) with status bar, notch, and home indicator safe areas.
3. **Real Shadows & Fuzzy Comparator**: Enables real shadows (`testGoldens`) with configurable diff tolerance (~1%) to prevent flaky sub-pixel failures.
4. **Offline Font & Asset Loading**: Loads custom typography and local assets via `await tester.loadAssets()` so text renders with real fonts instead of Ahem black boxes.

---

## 2. Authoring 4-State Screen Golden Tests (`code_writer`)

For any phase creating or modifying a Screen destination (`presentation/screens/*_screen.dart`) with approved golden coverage, create:
`test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart`

### Standard 4-State Golden Test Template (`Loading`, `Content`, `Empty`, `Error`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_screenshot/golden_screenshot.dart';
import 'package:my_client_app/modules/<feature>/presentation/screens/<feature>_screen.dart';

void main() {
  group('<Feature>Screen Golden Visual Tests', () {
    testGoldens('Renders all 4 mandatory visual states in device frame', (tester) async {
      await tester.loadAssets();

      // 1. Loading State
      await tester.pumpWidget(
        ScreenshotApp(
          device: GoldenScreenshotDevices.iphone.device,
          child: const MaterialApp(
            home: <Feature>Screen(state: <Feature>State.loading()),
          ),
        ),
      );
      await tester.pump(); // Single pump for indeterminate spinner/shimmer
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '1_<feature>_loading',
      );

      // 2. Content (Populated) State
      await tester.pumpWidget(
        ScreenshotApp(
          device: GoldenScreenshotDevices.iphone.device,
          child: MaterialApp(
            home: <Feature>Screen(state: <Feature>State.populated(fixtureItems)),
          ),
        ),
      );
      await tester.pumpAndSettle();
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '2_<feature>_content',
      );

      // 3. Empty State
      await tester.pumpWidget(
        ScreenshotApp(
          device: GoldenScreenshotDevices.iphone.device,
          child: const MaterialApp(
            home: <Feature>Screen(state: <Feature>State.empty()),
          ),
        ),
      );
      await tester.pumpAndSettle();
      await tester.expectScreenshot(
        GoldenScreenshotDevices.iphone.device,
        '3_<feature>_empty',
      );

      // 4. Error State (Validation / Network Failure with Retry)
      await tester.pumpWidget(
        ScreenshotApp(
          device: GoldenScreenshotDevices.iphone.device,
          child: const MaterialApp(
            home: <Feature>Screen(state: <Feature>State.error('Unable to load data')),
          ),
        ),
      );
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

## 3. Strict Role Execution & Baseline Governance (`V8`)

| Role | Command | Responsibility & Rules |
|---|---|---|
| **1. Code Writer (`code_writer`)** | `flutter test test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart --update-goldens` | Generates baseline `.png` files during implementation, then opens and visually self-checks every `.png` image for overflow or design drift before handing off `READY_FOR_REVIEW`. |
| **2. Code Reviewer (`code_reviewer`)** | Opens every generated `.png` image + runs `flutter test <golden_test_path>` | Visually inspects all 4 `.png` baselines against `design.md` (`## UI/UX mapping`) and extracted Figma renders (`.superpowers/sources/<ISSUE-ID>/figma/<stem>-SNN.png`) using the 10-dimension checklist ([03](03-comparison-checklist-and-verdict.md)). Any `RenderFlex overflowed` stripe or `BLOCKER`/`MAJOR` deviation triggers `CHANGES_REQUESTED`. |
| **3. Test Runner (`test_runner`)** | `flutter test test/modules/<feature>/presentation/screens/<feature>_screen_golden_test.dart` (**NO `--update-goldens`**) | Compares `REVIEW_REVISION` against the Reviewer-approved baseline. Any pixel diff exceeding tolerance is `FAIL` (`CHANGES_REQUESTED`). **`test_runner` must NEVER run `--update-goldens` or accept newly generated images as their own baseline.** |
