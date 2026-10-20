# 03 — Flutter plan, phase and DoD conventions

The core `planning-and-task-breakdown` and `incremental-implementation` skills are stack-neutral. For a Flutter Client, use these concrete conventions.

## 1. Phase slicing example (Flutter)

Wrong (horizontal):

| Phase | Content | Observable? |
|---|---|---|
| 01 | Entities, repository contract, use cases | No |
| 02 | Models, data source, repo impl, mocks | No |
| 03 | Cubit, screen, widgets | Only now |

Right (vertical, after `PHASE-00`):

| Phase | Behavior | Layers / Files touched |
|---|---|---|
| `PHASE-01` | Open the screen and see the `<feature>` list (Loading → Content) | Entity + repo contract + `RemoteDataSource`/model/repo impl for the list call + Cubit/`ListViewPaging` + screen + route + DI |
| `PHASE-02` | Empty and error states with retry | Cubit state + screen states; no new data code |
| `PHASE-03` | Tap an item → detail screen | Detail call through all layers + new screen + route |
| `PHASE-04` | Submit form action with validation errors | Write call + request model + form widgets + Cubit action |

Never create fake `Mock<Feature>DataSource` classes in `lib/`.

## 2. Task and phase fields

- Typical task order inside a phase: Domain → Data → Cubit/State → Screen/Widgets & Route/DI → Unit Tests.
- **Scope / Files**: `lib/modules/.../file.dart`.
- **Reused Components**: entries from the design's `Core usage` / `Client Core Mapping` table, or `standard Flutter` for external-standard.
- **Acceptance Criteria** per task: e.g. `dart analyze <path>` / `flutter analyze lib/modules/...`, or a targeted unit test.
- **Verification** per phase: real Flutter/Dart commands (`flutter analyze`, `flutter test test/modules/<feature>/`).

## 3. AC coverage examples

| AC ID | Phase ID | Decisive check | Evidence target |
|---|---|---|---|
| AC-01 | PHASE-01 | Unit test validates DTO parsing and mapper | `test/modules/<feature>/data/mapper_test.dart` |
| AC-02 | PHASE-02 | Widget test validates EmptyStateView rendered on empty list | `test/modules/<feature>/presentation/empty_test.dart` |
| AC-03 | PHASE-03 | Bloc test validates error message emitted on 400 failure | `test/modules/<feature>/presentation/cubit_test.dart` |

## 4. Review Definition of Done (Flutter)

Use a golden harness only when approved and already available, or when its dependency addition is explicitly approved. Golden evidence supplements required runtime checks; it never proves live integration. Follow `{{slot:visual-verification}}`.

- **Static Analysis Gate**: `flutter analyze` runs on affected files with 0 warnings, 0 errors, and 0 linter violations.
- **Developer Unit Tests** (`{{slot:unit-test}}`):
  - Entity & Mapper unit tests: Verify transformation logic and null-safety.
  - UseCase unit tests: Verify delegation to Repository with mock parameters.
  - Cubit / Bloc unit tests: Verify expected stream of state emissions using `bloc_test`.
- **Screen Visual Review Gate (Mandatory for Screen Phases)** — if a phase creates or modifies a Screen (`UI Impact: Yes`):
  - `code_writer` authors a Golden Test using `golden_screenshot` covering the 4 visual states (Default, Loading, Empty, Error).
  - `code_writer` generates baseline `.png` artifacts via `flutter test --update-goldens`.
  - `code_reviewer` inspects the rendered `.png` images against `design.md` and the approved profile’s design-system guidance (iMESPro: `app_ui_kit` GUIDE) to verify visual fidelity, layout integrity, touch targets, and contrast before approving the phase.

## 5. Incremental implementation commands

- Per task: `dart analyze <changed_file>` or a single unit test; fix analyzer errors immediately.
- Per phase: `flutter analyze` and `flutter test test/modules/<feature>/`.
