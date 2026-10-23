# 01 - What to Test per Layer

Map unit test coverage across Clean Architecture layers in Flutter applications.

## 1. Domain Layer (UseCases)

- **Subject:** `*UseCase` implementing `UseCasePower<T, P>`.
- **Collaborators:** Repository interface mocked with `mocktail`.
- **Required Test Cases:**
  1. **Success Case:** Repository returns `DataSuccess(Entity)` $\to$ UseCase returns expected entity.
  2. **Failure Case:** Repository returns `DataFailure(ErrorEntity)` $\to$ UseCase propagates failure.
  3. **Interaction Verification:** Verify repository method called with exact expected arguments.

## 2. Data Layer (Mappers & Models)

- **Subject:** `*Model` implementing `DataMapper<Entity>`.
- **Collaborators:** None (pure data transformations).
- **Required Test Cases:**
  1. **Standard `fromJson`:** Valid JSON map deseralizes into Model with correct properties.
  2. **Boundary & Edge `fromJson`:** Optional fields null, empty lists `[]`, numeric parsing (`"10"` vs `10`).
  3. **`toJson` Serialization:** Model serializes back into expected JSON payload map.
  4. **`mapToEntity`:** DTO properties correctly map to Domain Entity.

## 3. Data Layer (Data Sources)

- **Subject:** `*RemoteDataSource` extending `BaseRemoteDataSource`.
- **Collaborators:** Mock `ApiService` from `app_util`.
- **Required Test Cases:**
  1. Successful HTTP 200 response returns parsed raw data or `ApiResponse`.
  2. Throws `ApiException` or returns error entity on HTTP 400/401/500 responses.
  3. Network timeouts properly propagate error entities.

## 4. Presentation Layer (Cubit / State Machine)

- **Subject:** `*Cubit` managing feature state.
- **Collaborators:** Mock UseCases.
- **Tool:** `bloc_test` (`blocTest<OrderCubit, OrderState>(...)`).
- **Required Test Cases:**
  1. Initial state check: `expect(cubit.state, equals(const OrderInitialState()))`.
  2. Success transition: Emits `[OrderLoadingState, OrderSuccessState]` when UseCase succeeds.
  3. Error transition: Emits `[OrderLoadingState, OrderFailureState(message: ...)]` when UseCase fails.
