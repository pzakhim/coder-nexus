# 01 — Per-Layer Test Matrix, Directory Tree & Naming (Flutter / Dart)

Rules **U2**, **U3**, **U9**, **U10**, **U11**, and **U14**.

> **Workspace Convention Rule (`C11` / `U11` — `EXTEND` vs `INIT`):**
> - **Existing project (`EXTEND`):** Inspect `pubspec.yaml`, existing `test/` directories, shared test fixtures/fakes, result types, and state-holder conventions first. Follow the workspace's established test layout and active profile contracts (`testing-contracts.md`); record any legacy drift in `Concerns` without renaming unrelated test files.
> - **Greenfield project (`INIT`):** Apply the mirrored `test/modules/<feature>/` tree, `flutter_test` + `bloc_test` + `mocktail`, and the active profile's testing contracts.

---

## 1. Per-Layer Unit Test Matrix (No Live HTTP, No Platform Channels)

Every changed behavior must cover **Pass/Default**, **every handled Fail**, and **Empty / Edge** cases derived from the test-data rows and API specifications in `design.md`:

| Layer / Subject | Example Source Path | Boundary Doubled (`mocktail`) | Required Cases (Pass / Fail / Empty & Edge) |
|---|---|---|---|
| **Domain Entity / Value Object / Validator** | `lib/modules/orders/domain/entities/order_entity.dart` | **None** (100% pure Dart) | Valid construction and equality; each invariant/validation rule refusal; boundary values (`0`, negative, empty string, max length) |
| **Domain UseCase** | `lib/modules/orders/domain/usecases/get_orders_usecase.dart` | **Repository Interface** (`MockOrderRepository`) | **Pass/Default:** Repository returns success → UseCase returns expected entity/result; **Fail:** Repository returns failure (not found, unauthorized, server error, network timeout) → UseCase propagates exact failure without swallowing; **Interaction:** Repository called once with exact parameters (`verify(...).called(1)`) |
| **Data Model & Mapper (`JSON ↔ DTO ↔ Entity`)** | `lib/modules/orders/data/models/order_model.dart` | **None** (pure in-memory conversion) | **Pass/Default:** Valid JSON map deserializes via `fromJson` and maps to Domain Entity with all fields intact; **Empty/Edge:** Null/omitted optional fields, empty lists `[]`, numeric type coercion (`"10"` vs `10`), unknown enum fallback; **`toJson`:** Serializes back to expected request/storage map |
| **Data Repository Implementation** | `lib/modules/orders/data/repositories/order_repository_impl.dart` | **Remote / Local DataSource** (`MockOrderRemoteDataSource`) | **Pass/Default:** DataSource returns model → Repository maps and returns domain success; **Fail:** DataSource throws/returns HTTP `400`/`401`/`403`/`404`/`500` or timeout exception → Repository maps to the exact domain failure type |
| **Remote / Local DataSource** | `lib/modules/orders/data/datasources/order_remote_data_source.dart` | **HTTP / Storage Client** (`MockHttpClient` / profile client) | `200`/`201` parsed into model/response; `400`/`401`/`404`/`500` throws/returns typed server exception; timeout/socket error throws/returns network exception; request path, query parameters, and body verified |
| **Presentation State Holder (`Cubit` / `Bloc` / `Notifier`)** | `lib/modules/orders/presentation/cubit/order_list_cubit.dart` | **UseCases** (`MockGetOrdersUseCase`) | **Initial state:** Verified before any action; **Pass transition:** Emits `[Loading, Loaded(items)]`; **Empty transition:** Emits `[Loading, Empty]` (or `Loaded([])` per design); **Fail transition:** Emits `[Loading, Failure(message)]`; **Validation guard:** Invalid input emits validation error without calling the UseCase (`verifyNever(...)`) |

---

## 2. Mirrored Test Directory Tree (`U10`)

Unit test file paths under `test/` must mirror `lib/` (`<source_file>_test.dart`):

```text
test/
├── fixtures/                                # Deterministic JSON maps and entity builders
│   └── order_fixtures.dart
└── modules/
    └── orders/
        ├── domain/
        │   └── usecases/
        │       └── get_orders_usecase_test.dart
        ├── data/
        │   ├── models/
        │   │   └── order_model_test.dart
        │   ├── datasources/
        │   │   └── order_remote_data_source_test.dart
        │   └── repositories/
        │       └── order_repository_impl_test.dart
        └── presentation/
            ├── cubit/
            │   └── order_list_cubit_test.dart
            └── screens/
                └── order_list_screen_golden_test.dart  # When golden_screenshot is approved
integration_test/                            # Optional Hybrid E2E (Gate 3 plan / user request)
└── orders_e2e_test.dart                     # Authored by code_writer; executed by test_runner
```

### Optional Local `integration_test/` (Hybrid E2E)
- Unit and widget tests under `test/modules/<feature>/` remain **mandatory per task** and never touch live I/O (`U4`).
- When the Gate 3 plan (`test-plan.md` / `implementation-plan.md`) or the user explicitly schedules persistent local E2E regression tests, **`code_writer`** authors `integration_test/<feature>_e2e_test.dart` (using `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` + `flutter_test`) targeting key end-to-end user flows (`E2E-01..N`).
- **`test_runner`** remains strictly read-only: it executes existing `integration_test/<feature>_e2e_test.dart` via `flutter test integration_test/<feature>_e2e_test.dart` alongside live `E2E-01..N` verification, and never creates or edits test files.

---

## 3. Naming & Regression Rules (`U3`, `U9`)

- **File Naming:** `<source_name>_test.dart` (collected automatically by `flutter test`).
- **Grouping & Descriptions:**
  - Wrap each class or method under test in `group('<ClassName>', () { ... })`.
  - Write `test(...)` and `blocTest(...)` descriptions that state **behavior + condition + expected outcome**:
    - `test('returns OrderEntity list when repository succeeds')`
    - `test('returns ServerFailure when repository fails with 500')`
    - `blocTest('emits [OrderLoading, OrderLoaded] when loadOrders succeeds', ...)`
    - `blocTest('emits [OrderLoading, OrderFailure] when loadOrders fails', ...)`
- **Bug Fix & Review Finding Regression (`U3`):**
  1. Write a unit test reproducing the broken behavior (named for the behavior rule, never the ticket ID).
  2. Run it **red** on the unfixed code and record the failure row.
  3. Fix via `{{slot:root-cause-debugging}}`, run **green**, then run the feature module test suite.
