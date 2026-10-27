---
name: code-simplification
description: Simplification standard for a Flutter / Dart app - reduces the code changed in the current task or phase to the simplest form a newcomer understands on first read while behavior and layout stay exactly the same - only after flutter analyze and flutter test are green, through four lenses (reuse, simplification, efficiency, altitude) with one named smell at a time (home-grown widget the UI kit already has, `_buildX()` helper methods, layout pyramids, unused StatefulWidget, work in `build()`, whole-tree rebuilds, special cases in shared widgets), small steps with checks, never weakening tests, validation, error states or dispose calls, with stop rules and the one-line `simplify:` report. Use after implementation checks pass and before the self-check for READY_FOR_REVIEW, when asked to "clean this up", "simplify", "this widget is too complex" or "over-engineered", or when a review finding names unnecessary complexity in the diff, even if the word "simplify" is not used. Not for red code, code outside the diff, new screens, bug fixes or any behavior or layout change.
---

# Code Simplification — Flutter / Dart

Goal: Dart and Flutter code a newcomer reads, understands and maintains on the first read. Not the fewest lines: a change is a simplification only when a reader holds **fewer concepts** afterwards (widgets, flags, branches, layers). Moving the same complexity somewhere else is not simpler.

All check flags (`PASS` / `FAIL`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9). Foundation and profile-specific reuse is governed by the active workspace profile (`architecture_profile`) and its reference below.

## 1. The loop

1. `flutter analyze` and the affected `flutter test` are green; take only the phase's diff ([01](references/01-scope-and-safety.md)).
2. Read callers, routes, DI, widget lifecycle, state-holder conditions and tests of the code ([01](references/01-scope-and-safety.md)).
3. Pass the diff through the four lenses — **Reuse, Simplification, Efficiency, Altitude** — and name each smell from the catalog or the profile reference; skip code that is already clear ([02](references/02-smell-catalog.md)).
4. One small simplification → rerun `dart format`, `flutter analyze` and the affected tests (`PASS` / `FAIL`).
5. Stop at the stop criteria; findings that would change behavior or layout, or reach outside the diff, go to Concerns ([01](references/01-scope-and-safety.md) §7).
6. Report one `simplify:` line ([03](references/03-report-and-review.md)).

A simplification made after READY_FOR_REVIEW is a new revision: rerun the affected checks; earlier review and test evidence for that code no longer counts (`evidence-standard`).

## 2. Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **S1** | **Only after checks pass, only the changed code.** Anything outside the phase's diff goes into the hand-off's Concerns. | Simplifying red code or code outside the diff mixes refactoring with behavior change. | [01](references/01-scope-and-safety.md) |
| **S2** | **Behavior and layout identical.** Same rendered layout, visual states, navigation, emitted states, side effects, focus/scroll/input behavior and semantics. Existing tests and goldens pass unchanged. | A "simplification" that changes behavior is an unreviewed feature change. | [01](references/01-scope-and-safety.md) |
| **S3** | **Understand first.** Read callers, routes, DI, lifecycle methods, `buildWhen`/`listenWhen` and tests. | A widget that looks redundant often preserves state, focus or a listener. | [01](references/01-scope-and-safety.md) |
| **S4** | **A named smell is required.** One catalog or profile row under one of the four lenses, or a `{{slot:clean-code}}` rule. | Simplifying clear code is churn that costs a review round. | [02](references/02-smell-catalog.md) |
| **S5** | **Reuse before writing** *(Reuse)*. Needed? → in the repo or the foundation packages? → Flutter SDK / Dart? → only then the minimum. No new `pubspec.yaml` dependency for a few lines. | Home-grown copies of kit widgets drift in style and behavior. | [02](references/02-smell-catalog.md) |
| **S6** | **YAGNI.** No abstract class, base widget, base Cubit or factory with one implementation, unless the approved profile, a `D-NN` or a `{{slot:clean-architecture}}` boundary requires it. | Speculative flexibility costs every reader. | [02](references/02-smell-catalog.md) |
| **S7** | **Rule of three.** Extract shared logic or widgets on the third repetition; definitions are never duplicated (`{{slot:clean-code}}` C1). | Early extraction grows boolean flags for each caller. | [02](references/02-smell-catalog.md) |
| **S8** | **Flat and plain** *(Simplification)*. No `_buildX()` helpers, layout pyramids, unused `StatefulWidget`, derivable state, nested ternaries or clever cascades. | Flat widget trees read at once and rebuild less. | [02](references/02-smell-catalog.md) |
| **S9** | **No wasted work** *(Efficiency)*. No sorting/parsing or futures started in `build()`, no whole-screen rebuilds for one field, no per-item requests from the UI. Hot-path changes need a measurement. | Work in `build()` runs on every frame that rebuilds. | [02](references/02-smell-catalog.md) |
| **S10** | **Fix at the right depth** *(Altitude)*. No screen-specific special cases inside shared widgets, theme or base classes; fix the mapper or state, not the symptom in the widget. Outside the diff → Concerns. | A patched symptom leaves special cases every reader must remember. | [02](references/02-smell-catalog.md) |
| **S11** | **Small steps with checks.** One simplification at a time; checks after each, with evidence. | A failing check after one small step points straight at the cause. | [01](references/01-scope-and-safety.md) |
| **S12** | **Never weaken protection.** No edited tests or regenerated goldens, no removed validation, error states, permission checks or DI, no lost `dispose()` (C17), no leftover wrapper/alias/re-export (C1, C18), no `// ignore:` to pass. | These remove safety, not complexity. | [01](references/01-scope-and-safety.md) |
| **S13** | **Stop** when behavior, layout or a contract would change, the profile or a `D-NN` keeps the abstraction, the gain is cosmetic, a rebuild path changes unmeasured, or the next step leaves the diff. | Past these points it needs `change-control`, not simplification. | [01](references/01-scope-and-safety.md) |
| **S14** | **Report one line.** The §9 `simplify:` line; skipped findings in Concerns; shortcuts with their limit and upgrade path. | Reviewers see intent; nothing is silently dropped or made permanent. | [03](references/03-report-and-review.md) |

## 3. Reference Guides

| Topic | Reference |
|---|---|
| When and scope, behavior and layout safety with Flutter traps, per-step checks, never-rules and stop criteria | [01 — Scope & Safety](references/01-scope-and-safety.md) |
| Smell → technique catalog by lens (Reuse, Simplification, Efficiency, Altitude), rule of three, what to leave alone | [02 — Smell Catalog](references/02-smell-catalog.md) |
| `simplify:` report line, skipped findings, shortcuts and review grading (`BLOCKER` / `MAJOR` / `MINOR`) | [03 — Report & Review](references/03-report-and-review.md) |
<!-- {{profile_references}} -->

## 4. Relationship with Other Skills

- Thresholds (`build()`, method and file length), naming, `const`, dead code, wrappers, dispose and exports: `{{slot:clean-code}}` — linked, not repeated here.
- Foundation packages, UI kit and profile routing: `.superpowers/setup.json` (`architecture_profile`) and `{{slot:architecture-design}}`.
- Placement and layer boundaries: `{{slot:clean-architecture}}`; decisions (`D-NN`) keep the abstractions they require.
- Guards from `{{slot:secure-coding-standards}}` are never simplified away; layout changes are checked with `{{slot:visual-quality}}`.
- Called from the simplicity pass of `incremental-implementation`, before the `bug-hunt` self-check hand-off; findings are graded by `{{slot:code-review}}`.
- Red checks: fix with `{{slot:root-cause-debugging}}` first.
