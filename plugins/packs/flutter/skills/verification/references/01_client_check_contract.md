# Client Check Contract

Read plugin-root `shared_contracts/api_handshake_protocol.md`. Only explicitly approved contract-derived development fixtures may support UI/contract checks. Record fixture provenance and contract revision separately from live integration evidence. Required live ACs remain `BLOCKED` or `NOT_RUN` until exercised against the real endpoint; fixture success cannot close the handshake or imply overall feature acceptance. Never fabricate business records, Huly data, services or production success fallbacks.


For new work, take commands and targets from `.superpowers/work-items/<slug>/vN/brief.md` or optional `implementation-plan.md`/phase, and verify them against the real Client. The feature path below is historical compatibility guidance.

## Source of commands

Use commands approved in the same feature version's `implementation-plan.md` and linked `phases/phase-XX-<behavior>.md` under `docs/features/<module>/<feature>/vN/`. Confirm them against `.fvmrc`, `pubspec.yaml`, lockfiles, launch configuration, and available devices. Never assume `dev`, `lib/main_dev.dart`, Android, or FVM when the workspace says otherwise. Old `.agents/plan` files are LEGACY read-only context.

## Check order

1. Run code generation only when changed annotations/routes require it.
2. Run the narrowest analyzer command that proves the slice, then the workspace analyzer required by the plan.
3. Run targeted behavior tests, followed by affected regression tests.
4. Build the approved flavor/entrypoint/platform at its planned checkpoint.
5. For UI impact, use `{{slot:visual-quality}}` on the approved target and states.

Before running, enumerate test cases from approved ACs. For each case record its permitted real data source or safe input, expected observable result, target/state, test path and evidence. Missing test coverage goes back to Code Writer and review; a missing required live-data path is `BLOCKED`; approved fixture-backed UI/contract checks remain separately labeled.

If the approved Client plan includes `golden_screenshot`, confirm the dependency, test and reviewed baseline exist. Run ordinary `flutter test` to compare; never use `--update-goldens` in this release check or accept newly generated images as their own baseline. Baseline creation or updates require separate visual review and a new reviewed revision. Keep runtime UI inspection for the approved data mode; fixture screenshots cannot prove a required live-data state even when golden comparison passes.

Every command record contains command, cwd, tool version, start time, exit code, concise output, artifact path, and code revision. A zero exit code proves only that command's scope.

## Status rules

| Status | Meaning |
|---|---|
| `PASS` | The required check ran on `REVIEW_REVISION` and its observable outcome passed. |
| `FAILED` | The check ran and found an actionable implementation defect. |
| `BLOCKED` | A required external capability or safe real-data path was unavailable. |
| `NOT_RUN` | The check has not been attempted. |
| `N/A` | Visual check only: approved task has no UI impact and records why. |

Baseline failures are evidence, not permission to report success. Hub lexical validation does not replace the Dart analyzer; Cubit tests do not prove rendered semantics; a build does not replace runtime UI review.

For a changed screen, check the actual resolved base-screen API and route with the Client analyzer. When the approved work relies on inherited tracking or responsive layout, collect observable analytics/tracking evidence and portrait/landscape UI evidence on the approved target. A `BaseScreen` declaration or Hub lexical result alone is `UNVERIFIED`. Dialogs and child widgets do not require the screen contract.

## Revision invalidation

Compare the current tree with the reviewed tree before each gate. If production code, test code, generated code, dependency resolution, flavor configuration, or relevant assets changed, mark affected evidence stale. A fix returns to implementation, then affected code/UI review, then verification.
