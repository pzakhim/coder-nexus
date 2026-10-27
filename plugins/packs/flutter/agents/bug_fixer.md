## Flutter rules

- **Source and test folders**: `lib/` and `test/`.
- **Reproduction check**: a unit, cubit or widget test under `test/modules/<feature>/` that fails for the reported reason; run the narrowed failing test with `flutter test <test_path> --plain-name "<test_name>"` and read the full stack trace down to the first `lib/` frame with `flutter test --reporter=expanded <test_path>` (never `debugger()` or `--start-paused`).
- **Architecture profile**: take `architecture_profile.mode` from the `design.md` of the work item that built the code; without one, resolve it from `.superpowers/setup.json` (`architecture_profile`) and `{{slot:architecture-design}}`. Record the mode in `brief.md` → `## 7` → **Architecture profile** (the reviewer passes it to the validators) and fix inside that profile's `{{slot:root-cause-debugging}}` and `{{slot:clean-architecture}}` rules.
- **Floors (at least L3)**:
  - a change needed in `../app-core`, `../app-util` or `../app-ui-kit` (never edited from the Client; record it as a Core gap in `escalation-report.md`);
  - `BaseScreen` / `BaseScreenState` behavior;
  - code under `lib/core/` or `lib/shared/`;
  - route registration or DI registration.
- **Temporary instrumentation (investigation mode)**: `debugPrint` or `log` from `dart:developer` with a unique tag (for example `[DBG-<slug>]`) so every line can be found and removed; **every** inserted line carries the tag, inside the log string or as a trailing `// DBG-<slug>` comment (observer classes, `Bloc.observer = …` in `main.dart`, imports); a temporary `BlocObserver` for Cubit/BLoC transitions; run on an emulator or device and capture with `flutter run` output or `flutter logs`, and Flutter DevTools (Logging, Network) when needed. Never instrument `../app-core`, `../app-util` or `../app-ui-kit`. Before returning, `rg -n "DBG-<slug>" lib/ test/` must find nothing.
- **Local self-verification**: `dart format --output=none --set-exit-if-changed lib test`, `flutter analyze`, `dart run dart_code_linter:metrics analyze lib/modules/<feature>`, `flutter test test/modules/<feature>/` via `run_command`, and the architecture validators (`validate_architecture_code`, `validate_module_architecture`) with the resolved `architecture_profile` so an L1/L2 fix never introduces a layer boundary violation.
