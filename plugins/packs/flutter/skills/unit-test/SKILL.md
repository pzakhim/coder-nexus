---
name: unit-test
description: Write, run, and verify Flutter Clean Architecture unit tests across UseCases, Data Mappers/Models, Data Sources, and Cubit states using mocktail and bloc_test.
---

# Flutter Clean Architecture Unit Testing

Apply the approved profile through [core-usage](../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Use this skill when writing or reviewing Developer Unit Tests in a Flutter Client workspace. Unit tests verify code logic, state transitions, data conversions, and error handling in complete isolation from the network, database, and UI rendering.

## 1. Core Principles (AAA Pattern)

Every unit test must follow the **Arrange - Act - Assert** pattern:
- **Arrange**: Set up test fixtures, initialize subjects under test, and stub mock behaviors.
- **Act**: Invoke the single method or trigger the specific event.
- **Assert**: Verify returned values, emitted states, and mock invocation counts.

### Golden Rules
1. **100% Isolated & Fast**: Never call live HTTP endpoints, disk files, or device plugins. All external dependencies must be mocked.
2. **Deterministic**: Tests must never rely on system clocks, random values, or race conditions.
3. **Location Mirrors Source**: Unit test file paths must mirror the `lib/` directory structure under `test/`:
   - `lib/modules/<feature>/domain/usecases/<name>_usecase.dart` $\to$ `test/modules/<feature>/domain/usecases/<name>_usecase_test.dart`
   - `lib/modules/<feature>/data/models/<name>_model.dart` $\to$ `test/modules/<feature>/data/models/<name>_model_test.dart`
   - `lib/modules/<feature>/data/datasources/<name>_remote_data_source.dart` $\to$ `test/modules/<feature>/data/datasources/<name>_remote_data_source_test.dart`
   - `lib/modules/<feature>/presentation/cubit/<name>_cubit.dart` $\to$ `test/modules/<feature>/presentation/cubit/<name>_cubit_test.dart`
4. **Zero-Tolerance for Test Bias (No Tautological Tests)**:
   - Writing tests that solely pass because they avoid error states is strictly prohibited.
   - **Reject Happy-Path Bias**: Never test only HTTP 200 with complete valid payloads. Always write dedicated negative tests for HTTP 400, 401, 500, and timeout failures.
   - **Reject Shallow Assertions**: Do not settle for `expect(result, isNotNull)` or `expect(true, isTrue)`. Assert specific error messages, emitted failure objects, and data structures.
   - **Mandatory Boundary Probing**: Cover null/missing optional fields, empty lists `[]`, zero `0`, blank strings `""`, and type variations in JSON parsing.

---

## 2. Layer-Specific Testing Patterns

### A. Domain Layer (UseCases)
- **Subject**: `*UseCase` class.
- **Dependency**: Mock Repository interface using `mocktail` (e.g. `class MockAuthRepository extends Mock implements AuthRepository {}`).
- **Required Cases**:
  1. **Success Case**: Repository returns valid data/Entity $\to$ UseCase returns `Right(Entity)` or expected data.
  2. **Failure Case**: Repository returns `Left(Failure)` or throws an exception $\to$ UseCase handles or propagates `Left(Failure)`.
  3. **Verification**: Verify the repository method was called with exact parameters: `verify(() => mockRepo.login(any(), any())).called(1)`.

### B. Data Layer (Models & Mappers)
- **Subject**: `*Model` / `*Mapper`.
- **Required Cases**:
  1. `fromJson`: Deserializes standard valid JSON Map into Model correctly.
  2. `fromJson with edge cases`: Handles null optional fields, empty lists, and numeric type coercion without crashing.
  3. `toJson`: Serializes Model back to valid Map with expected keys.
  4. `toEntity`: Correctly maps Data Model fields to pure Domain Entity fields.

### C. Data Layer (Data Sources)
- **Subject**: `*RemoteDataSource` / `*LocalDataSource`.
- **Dependency**: Mock HTTP Client (e.g. `MockHttpClient` or `MockDio`).
- **Required Cases**:
  1. Returns parsed Model when HTTP status code is 200/201.
  2. Throws `ServerException` when HTTP status code is 400, 401, 404, or 500.
  3. Throws `NetworkException` on timeout or socket failure.

### D. Presentation Layer (Cubit & State Machine)
- **Subject**: `*Cubit`.
- **Tool**: `bloc_test` package (`blocTest<MyCubit, MyState>(...)`).
- **Required Cases**:
  1. Initial state check: `expect(cubit.state, equals(InitialState()))`.
  2. Happy path flow: emits `[LoadingState, SuccessState]` when UseCase succeeds.
  3. Error path flow: emits `[LoadingState, ErrorState(message: ...)]` when UseCase fails.
  4. Form validation: emits validation error state when input is invalid without triggering UseCase.

---

## 3. Starter Templates

Reference implementations are available under `templates/`:
- `templates/usecase_test.dart.tpl`
- `templates/mapper_test.dart.tpl`
- `templates/cubit_test.dart.tpl`

---

## 4. Execution & Verification

Run unit tests via terminal command:
```bash
flutter test test/modules/<feature>/
```
All unit tests must pass with 0 failures before code can be submitted for review.
