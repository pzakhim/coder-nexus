# 09 — Flutter Delivery Conventions

Flutter values for the stack placeholders used by the core `dev-team`, `feature-planner`, `brainstorming`, `clean-code`, `code-simplification` and `docs` skills and the core feature templates.

## Profiles and kit matching

- Kit-matching rules apply to iMESPro or a verified Client design system; `external-standard` uses standard Flutter widgets. Only an iMESPro setup failure blocks on company packages; external profiles require no company setup or GUIDE.
- In `design.md`: company setup/GUIDEs apply only to iMESPro. External profiles use Client mappings or standard Flutter; create only necessary layers. Only iMESPro requires `BaseScreen`/`BaseScreenState`; external-structured follows Client conventions and external-standard may use standard Flutter.
- Feature documents live in the Flutter Client Git (`docs/features/<module>/<feature>/vN/` or `.superpowers/work-items/<slug>/vN/`).
- Proposal template `{{PackageName}}` comes from `pubspec.yaml`. Inspect the real Flutter workspace before naming files, APIs, constructors, DI anchors, or routes.
- Gate 3 phase rows name the verified UI Kit / Flutter API source.

## Implementation, tests and evidence

- Code Writer implements business logic and UI according to [clean-architecture](../../clean-architecture/SKILL.md) and the selected [core-usage](../../core-usage/SKILL.md) profile.
- Developer unit tests (AAA, `unit-test` slot) cover UseCases, Mappers and Cubits under `test/modules/<feature>/`.
- Local self-verification: `dart format` (or project linter), `flutter analyze`, and the targeted `flutter test` suite. Phase task files use `.dart` paths and acceptance checks such as `flutter analyze <path>`.
- Screen visual baseline (when approved): use the Client's approved golden harness and dependencies for stable applicable states; generate a baseline only for independent visual review. Goldens supplement runtime UI evidence. A golden requires a reviewed baseline and a Client-approved dev dependency; the pre-release command must not update goldens.
- Reviewer inspects generated `.png` golden screenshot artifacts with `view_file` for layout fidelity, safe areas, touch targets and contrast.
- Final QA executes widget test suites (`flutter test test/modules/<feature>/widgets/`) and integration tests across the unified feature; isolated UseCase/Mapper/Cubit logic is already covered by Code Reviewer.
- UI provenance: match the selected profile's reuse mapping (iMESPro Core usage, external Client Core Mapping, or standard widgets); imports resolve in the Client.

## Clean code and simplification (Dart / Flutter)

- Apply readable, maintainable Dart and Flutter practices; preserve `DataState`/`ErrorEntity`, nullability, lifecycle and package contracts.
- Simplify recently changed Dart or Flutter code only with formatter (`dart format`) and analyzer (`flutter analyze`) re-run on the affected scope.

## Documentation

- Reader-facing Flutter Client docs describe routing, UI Kit use and setup only where relevant to the reader's task.
