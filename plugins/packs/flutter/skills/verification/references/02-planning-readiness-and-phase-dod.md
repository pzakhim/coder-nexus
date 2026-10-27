# Planning Readiness Scan, Phase Slicing, and Review DoD

> Topic: Flutter `PHASE-00` codebase readiness scan for Planning, vertical vs. horizontal phase slicing, task/phase check conventions, and Review Definition of Done.

Core `implementation-planning` and `incremental-implementation` skills are stack-neutral and delegate Flutter-specific readiness, phase slicing, and Definition of Done rules to this reference.

---

## 1. Flutter Codebase Readiness Scan for Planning (`PHASE-00`)

Before writing tasks in `implementation-plan.md`, Planning executes this readiness checklist and records findings in `codebase-notes.md` and `phases/phase-00-prepare.md`:

| Scan Area | Verification Action |
|---|---|
| **1. Developer Tools (`G0`)** | Run `coder-nexus setup tools --pack flutter --check` to verify `very_good_analysis`, `dart_code_linter`, `mocktail`, `bloc_test`, `ripgrep` (`rg`), and `mockoon-cli` (`PASS` when `TOOLS: READY`; install missing via `coder-nexus setup tools --pack flutter -y`). |
| **2. Architecture Profile Foundations** | Inspect `.superpowers/setup.json` (`architecture_profile`) and follow the profile verification contract in `SKILL.md` (`imespro`, `external-structured`, or `external-standard`). Only an `imespro` workspace runs `coder-nexus setup flutter --check`; external profiles never run company monorepo checks. |
| **3. Routing & Screen Registry** | Inspect the Client's router configuration with `rg -n`. If the target route is missing, plan a task to register the route constant and builder before or alongside screen assembly. |
| **4. State Management & DI** | Confirm active state management (`Cubit` / `Bloc`) and DI registration pattern (`get_it` `registerFactory` for screen state holders, `registerLazySingleton` for repositories/datasources). |
| **5. Real Network Pipeline in `lib/`** | Verify how `RemoteDataSource` calls the HTTP client (`ApiConfig.domain` / `Dio`). Never plan or create fake `Mock<Feature>DataSource` classes inside `lib/`; when Backend APIs are not ready (`FE_MOCKOON`), plan a `PHASE-00` task to generate `mocks/<feature>_mockoon.json`. |
| **6. Screen & Responsive Requirements** | For screen tasks, include `flutter analyze`, `dart_code_linter`, and `{{slot:visual-quality}}` checks covering all 4 visual states (`Loading`, `Content`, `Empty`, `Error`) and applicable orientation/tracking requirements. |

---

## 2. Vertical vs. Horizontal Phase Slicing (Flutter)

### Wrong (Horizontal Layer Slices — Unobservable Until the End)

| Phase | Content | Observable Behavior? |
|---|---|---|
| `01` | Entities, repository contract, use cases | No |
| `02` | DTO models, `RemoteDataSource`, repository implementation | No |
| `03` | `Cubit`, screen, widgets | Only at the very end |

### Right (Vertical End-to-End Slices After `PHASE-00`)

| Phase | End-to-End User Behavior | Layers & Files Touched |
|---|---|---|
| **`PHASE-01`** | Open the screen and view the `<feature>` list (`Loading` → `Content`) | Entity + Repo contract + `RemoteDataSource`/Model/Repo impl for list endpoint + `Cubit`/paging controller + Screen + Route + DI + Unit/Golden tests |
| **`PHASE-02`** | Handle `Empty` and `Error` states with retry | `Cubit` empty/failure states + Screen empty/error views + Widget/Golden tests |
| **`PHASE-03`** | Tap an item to open the detail screen | Detail endpoint across Domain/Data + Detail `Cubit` + Detail Screen + Route + Tests |
| **`PHASE-04`** | Submit form action with validation and error feedback | Write endpoint + Request DTO + Form widgets + `Cubit` submit state + Tests |

---

## 3. Task and Phase Fields in `implementation-plan.md`

- **Task Order Inside a Vertical Phase**: Domain (`entities`, `repositories`, `usecases` if needed) → Data (`models`, `datasources`, `repositories`) → Presentation (`cubit`/`state`, `screens`, `widgets`) & Route/DI → Unit/Widget/Golden Tests.
- **Scope / Files**: Explicit relative paths under `lib/modules/<feature>/...` and `test/modules/<feature>/...`.
- **Reused Components**: Exact entries from `design.md` (`Core usage` or `Client Core Mapping` table, or standard Flutter SDK widgets for `external-standard`).
- **Task-Level `Acceptance Criteria`**: Narrow, fast deterministic command per task:
  - Domain/Data task: `flutter analyze lib/modules/<feature>/` + targeted unit test `flutter test test/modules/<feature>/data/<name>_test.dart`.
  - Presentation task: `flutter analyze lib/modules/<feature>/` + `flutter test test/modules/<feature>/presentation/<name>_cubit_test.dart`.
- **Phase-Level `Verification`**: Full module gates (`G2` `flutter analyze`, `G3` `dart_code_linter`, `G4` MCP architecture validators, `G5` `flutter test test/modules/<feature>/`, plus `G6`/`G7` when `UI Impact: Yes`).

---

## 4. AC Traceability Matrix Examples

Every confirmed goal (`G-NN`) from `requirements.md` (`## 0. Goals`) must map to at least one phase through its `AC-NN` rows (`validate_plan_slices` `PLAN-V-010`):

| AC ID | Phase ID | Decisive Check | Evidence Target | Goal |
|---|---|---|---|---|
| `AC-01` | `PHASE-01` | Unit test verifies DTO parsing, null safety, and entity mapping | `test/modules/<feature>/data/mapper_test.dart` | `G-01` |
| `AC-02` | `PHASE-02` | Widget/Golden test verifies `Empty` state view rendered on `[]` payload | `test/modules/<feature>/presentation/empty_state_test.dart` | `G-01` |
| `AC-03` | `PHASE-03` | `bloc_test` verifies error state emitted on `400` / `422` response | `test/modules/<feature>/presentation/cubit_test.dart` | `G-02` |

---

## 5. Review Definition of Done (Flutter)

Before Code Reviewer issues `APPROVED` on `REVIEW_REVISION`:
1. **Static Analysis, Metrics & Architecture (`G2`–`G4`)**:
   - `flutter analyze` and `dart run dart_code_linter:metrics analyze lib` pass with `0` errors, `0` warnings, and `0` metrics violations.
   - `validate_architecture_code` and `validate_module_architecture` return `PASS`.
2. **Developer Unit & Cubit Tests (`G5` — `{{slot:unit-testing}}`)**:
   - Model/Mapper tests verify JSON serialization, null-safe parsing, and entity conversion.
   - Repository/UseCase tests verify error mapping and delegation via `mocktail`.
   - `Cubit`/`Bloc` tests verify state emission sequences (`loading → success`, `loading → empty`, `loading → error`) via `bloc_test`.
3. **Screen Visual & Golden Gate (`G6`–`G7` — Mandatory when `UI Impact: Yes`)**:
   - When `golden_screenshot` is in the approved plan, Code Writer authors a golden test covering all 4 visual states (`Loading`, `Content`, `Empty`, `Error`) and generates baseline `.png` images via `flutter test --update-goldens`.
   - Code Reviewer visually inspects the rendered `.png` artifacts (and runtime screenshots from `{{slot:visual-quality}}`) against `design.md` (`UI/UX mapping` `S-NN` / `C-NN`) and the active profile's design-system contract before approving the phase.
