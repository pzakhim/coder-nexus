# 03 — Self-Check Commands & Review Severity (Flutter / Dart)

Consolidated pre-handoff CLI verification commands (**C14**) and the unified review grading rubric (`BLOCKER` / `MAJOR` / `MINOR`) from `shared_contracts/flags_and_statuses.md`.

---

## 1. Deterministic Pre-Handoff CLI Gates (`PASS` / `FAIL`)

Run these commands from the Flutter project root before reporting `READY_FOR_REVIEW`. Every check is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)** and must be recorded as an evidence row:

```bash
# 1. Formatting check (zero formatting drift)
dart format --output=none --set-exit-if-changed lib test

# 2. Static analyzer (very_good_analysis / flutter_lints)
flutter analyze

# 3. Code complexity, size thresholds (C6), and dead code (C2) via dart_code_linter
dart run dart_code_linter:metrics analyze lib
dart run dart_code_linter:metrics check-unused-code lib
dart run dart_code_linter:metrics check-unused-files lib

# 4. Forbidden patterns scan via ripgrep (C3, C9, C18)
git diff | rg "print\(|debugPrint\(|debugger\("
rg -nE "^export '[^']+';$" <changed_barrel_files>

# 5. Affected unit & widget tests
flutter test <affected_test_files>
```

---

## 2. Unified Review Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`)

Reviewers and authors grade all code findings using the single unified scale defined in `shared_contracts/flags_and_statuses.md` §2 and `work-item-contract` (`references/handoff-and-status.md` §9).

> Do **not** use `P1` / `P2` / `P3` for code findings. Automated CLI gates are strictly `PASS` or `FAIL`.

| Severity | Definition | Impact on Review Verdict |
|---|---|---|
| **`BLOCKER`** | 1. **Failed CLI Tool Gate (`FAIL`)**: `flutter analyze`, `dart_code_linter`, `dart format`, or `flutter test` exits non-zero.<br>2. **Mandatory Design / Runtime Safety Violation**: Pass-through wrapper or duplicate foundation widget (**C1**), dead/debug code (**C2, C3**), swallowed exception (**C4**), unchecked bang operator `!` risking `NullCheckError` (**C9**), broken workspace foundation contract (**C11**), side effect inside `build()` (**C12**), in-place state mutation (**C13**), skipped self-check (**C14**), exposed internal helper or `utils.dart` bucket (**C16**), undisposed controller/stream (**C17**), or barrel exporting `src/` internals (**C18**).<br>3. **Behavioral / Security Defect**: Broken `AC-NN`, crash, memory leak, or security leak. | **`CHANGES_REQUESTED`** (blocks approval). |
| **`MAJOR`** | Maintainability or structural smell not already blocked by CLI linters: vague identifier naming (**C5**), `_buildX()` helper method returning `Widget` instead of a `StatelessWidget` class (**C6**), oversized `build()`/method/file (**C6**), hardcoded colors/magic numbers (**C7**), drive-by edits outside task scope (**C10**), missing `const` constructor (**C15**), or barrel `export` without `show` (**C18**). | Must be fixed in the same revision when inside the phase's `Scope / Files`; triggers `CHANGES_REQUESTED` if left unaddressed in touched files. |
| **`MINOR`** | Redundant "what" comment (**C8**) or optional readability polish. | Non-blocking (`Optional`); never blocks `APPROVED`. |

## 3. Review Scope Rule

- Evaluate **only** code modified in the current task or phase diff (`BASE_REVISION..REVIEW_REVISION`).
- Pre-existing legacy debt outside the diff is recorded as an informational note in `Concerns`, never as a blocking finding.
