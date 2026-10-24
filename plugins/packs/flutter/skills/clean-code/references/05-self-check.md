# 05 - Self-Check Commands (Flutter / Dart)

Run these verification commands before marking any task as complete or requesting code review.

## 1. Automated Verification Commands

Execute from the root of the Flutter project:

```bash
# 1. Format verification (ensures zero formatting discrepancies)
dart format --output=none --set-exit-if-changed .

# 2. Static analysis and linter checks
flutter analyze

# 3. Feature unit test suite execution
flutter test test/modules/<feature>/
```

## 2. Manual Pre-Review Checklist

- [ ] **No debug code:** Verify no `print()`, `debugPrint()`, or `debugger()` remain in the diff:
  ```bash
  git diff | grep -E "print\(|debugPrint\("
  ```
- [ ] **Const constructors added:** Verify `const` has been added to widgets and constructor calls where applicable.
- [ ] **Lifecycle adherence:** Verify all `TextEditingController`, `AnimationController`, `FocusNode`, and `StreamSubscription` instances are properly disposed.
- [ ] **BaseScreen contract:** Verify all route destination screens extend `BaseScreen` + `BaseScreenState` and implement `buildMobilePortrait()` without overriding `build()`.
- [ ] **Export surface (C18):** In every barrel the diff touches, each `export` line has `show`, and each shown symbol has an importer outside the barrel's module:
  ```bash
  rg -nE "^export '[^']+';$" <changed barrel files>
  rg -n "import '.*<barrel>.dart'" lib test
  ```
- [ ] **Kit reuse:** Verify no custom widgets duplicate `AppButton`, `AppFormField`, `AppDialog`, or typography from `app_ui_kit`.
