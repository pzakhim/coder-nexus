---
name: clean-code
description: Flutter & Dart clean code standard (Effective Dart, very_good_analysis, flutter_lints, dart_code_linter) - deterministic CLI gates plus mandatory design rules for naming, const constructors, widget decomposition, error handling, sound null safety, resource disposal, and unified review severities.
---

# Flutter Clean Code Standard

Goal: Dart & Flutter code that is readable on first pass, rebuild-efficient, and maintainable in one place.
All check flags (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9). Foundation and profile-specific conventions are governed by `flutter-core-package-usage`.

---

## 1. Deterministic Tool Gates (`PASS` / `FAIL`)

Installed and verified via `coder-nexus setup tools --pack flutter`. Every command below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)** and must pass before `READY_FOR_REVIEW`:

| Tool Gate | Command | Enforces Rules Automatically |
|---|---|---|
| **Static Analyzer** | `flutter analyze` | `very_good_analysis` / `flutter_lints` rules, unused imports/elements (**C2**), `print()` calls (**C3**), sound null-safety & type checks (**C9**), missing `const` (**C15**) |
| **Metrics & Dead Code Linter** | `dart run dart_code_linter:metrics analyze lib` & `check-unused-code lib` | Cyclomatic complexity, method/file length, parameter count (**C6**), and dead code (**C2**) |
| **Formatter** | `dart format --output=none --set-exit-if-changed lib test` | Canonical Dart formatting across touched files |

---

## 2. Core Design & Craft Principles (Mandatory Compliance)

Rules written below govern design, architecture, and Flutter runtime behavior. **Every rule is mandatory to follow**:

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **C1** | **One concept, one place.** Reuse the workspace's established foundation/UI components (`flutter-core-package-usage`). No pass-through wrappers, compatibility aliases, duplicate helper widgets, or copy-pasted mappers. | Copies drift; bug fixes land in only one copy. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C2** | **No dead code.** Remove unused widgets, state fields, dead imports, commented-out blocks, and orphan `TODO`s. | Dead code creates confusion and false assumptions during debugging. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C3** | **No debug leftovers.** No `print()`, `debugPrint()`, `debugger()`, or temporary inspection flags in committed code. | Leaks sensitive data into system logs and clutters console output. | [02-errors-lifecycle-and-logging](references/02-errors-lifecycle-and-logging.md) |
| **C4** | **No swallowed errors.** Catch specific exceptions, map them to typed Failure/Result states at the repository boundary, and log via the workspace's structured logger. | Silent failures mask defects and leave the UI in broken or perpetual loading states. | [02-errors-lifecycle-and-logging](references/02-errors-lifecycle-and-logging.md) |
| **C5** | **Intention-revealing names.** `lowerCamelCase` for methods/variables, `UpperCamelCase` for classes/widgets/enums, `lowercase_with_underscores` for files. | Descriptive names eliminate ambiguity across presentation, domain, and data layers. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C6** | **Small, focused units.** Widget `build()` ≤ 40 lines, methods ≤ 30 lines, files ≤ 250 lines. Extract private `StatelessWidget` classes with `const` constructors instead of `_buildX()` helper methods. | Monolithic build methods and `_buildX()` helpers trigger full-tree repaints and hinder readability. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C7** | **No magic values.** Use theme tokens (`Theme.of(context)` / workspace design tokens) and named constants instead of hardcoded colors (`Color(0xFF...)`), text styles, or raw numeric paddings. | Scattered magic values break theme consistency and responsive adaptation. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C8** | **Comments explain WHY.** Document architectural rationale and external constraints; never restate what Dart code self-evidently does. | Outdated "what" comments mislead; "why" comments explain trade-offs. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C9** | **Full sound null safety.** Avoid unchecked bang operators (`!`) and `dynamic`. Use null-aware operators (`?.`, `??`), guard clauses, or pattern matching. | Unchecked bang operators throw runtime `NullCheckError` in production. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C10** | **Scope discipline.** Modify only files within the approved phase task. Record out-of-scope legacy debt in `Concerns` instead of doing drive-by edits. | Drive-by modifications complicate reviews and trigger merge conflicts. | [03-self-check-and-review](references/03-self-check-and-review.md) |
| **C11** | **Workspace contracts win.** Honor the approved `architecture_profile` (`flutter-core-package-usage`) for base screens, state holders, result types, DI, and UI components. | Competing architectural patterns splinter the codebase. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C12** | **Visible side effects.** Keep widget `build()` pure; trigger navigation, dialogs, and network requests inside Cubits/Blocs, listeners, or user event callbacks. | Side effects in `build()` execute repeatedly on every frame rebuild. | [02-errors-lifecycle-and-logging](references/02-errors-lifecycle-and-logging.md) |
| **C13** | **Immutable state.** States emitted by state holders (Cubit/Bloc/Notifier) and domain value objects must be immutable; never mutate state fields in place. | In-place mutation prevents UI builders from detecting state transitions. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C14** | **Self-check before handoff.** Run `dart format`, `flutter analyze`, `dart_code_linter`, `rg`, and unit tests before `READY_FOR_REVIEW`. | An unrun check is `NOT_RUN`, never `PASS`. | [03-self-check-and-review](references/03-self-check-and-review.md) |
| **C15** | **Const constructors.** Add `const` to widget constructors and instances wherever properties are compile-time constants. | Eliminates unnecessary widget rebuilds during state tree invalidation. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C16** | **Helper locality.** Keep single-file helpers private (`_camelCase` / `class _Widget`). Move to a shared module only when imported by 2+ files—never create generic `utils.dart` or `helpers.dart` buckets. | Leading underscore enforces file-private scope; generic utility buckets become junk drawers. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |
| **C17** | **Dispose controllers and streams.** Always cancel `StreamSubscription` and dispose `TextEditingController`, `AnimationController`, `FocusNode`, `ScrollController` in `dispose()` / `close()`. | Leaked controllers and uncancelled streams cause memory leaks and runtime crashes. | [02-errors-lifecycle-and-logging](references/02-errors-lifecycle-and-logging.md) |
| **C18** | **Explicit export surface.** Barrel files export with `show` only the symbols other modules actually import; no bare `export 'x.dart';` and no export of `src/` internals or test hooks. | Every export is a contract to keep; bare exports leak internals and hide unused code. | [01-structure-naming-and-types](references/01-structure-naming-and-types.md) |

---

## 3. Reference Guides

| Topic | Reference |
|---|---|
| Naming, size thresholds, widget splitting, sound types, constants, helper locality, and barrel exports | [01 — Structure, Naming & Types](references/01-structure-naming-and-types.md) |
| Error handling, pure `build()`, controller/stream disposal, and structured logging | [02 — Errors, Lifecycle & Logging](references/02-errors-lifecycle-and-logging.md) |
| Pre-review CLI gates (`PASS` / `FAIL`) and review grading (`BLOCKER` / `MAJOR` / `MINOR`) | [03 — Self-Check & Review](references/03-self-check-and-review.md) |
<!-- {{profile_references}} -->

## 4. Relationship with Other Skills

- **Foundation & profile routing**: `{{slot:core-package-usage}}` (`imespro`, `external-structured`, `external-standard`).
- **Layer boundaries & placement**: `{{slot:clean-architecture}}`.
- **Post-green refactoring**: `{{slot:code-simplification}}`.
- **Security rules**: `{{slot:secure-coding-standards}}`.
- **Debugging & unit tests**: `{{slot:root-cause-debugging}}` and `{{slot:unit-testing}}`.
