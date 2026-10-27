# External Structured Unit Testing Contracts (`lib/core/` Mapping)

> Topic: Unit testing against the client's existing `lib/core/` result types, base classes, and shared test helpers (`external-structured` profile)

Applies **U2**, **U5**, **U8**, and **U11** when the workspace profile is **`external-structured`**. Follow the `Client Core Mapping` recorded in `design.md`.

---

## 1. Per-Layer `external-structured` Unit Test Rules

| Aspect | Contract |
|---|---|
| **Result / Failure Wrapper** | Use the exact result type defined in the client's `lib/core/` (e.g., `Either<Failure, T>` from `fpdart`/`dartz`, or the client's custom `Result<T>`). Never import `DataState`, `UseCasePower`, or `ApiService` unless the client repository defines them |
| **Shared Test Helpers** | Reuse the client's existing `test/helpers/`, `test/fixtures/`, and mock registration utilities before creating new ones (`U11`) |
| **State Holder Testing** | Match the client's state management library (`bloc_test` for `Bloc`/`Cubit`, `ProviderContainer` for `Riverpod`, or `ChangeNotifier` listener tests) |
| **Network / DataSource Boundary** | Mock the client's configured HTTP wrapper (e.g., `Dio`, `Chopper`, `Retrofit`, or custom `ApiClient` in `lib/core/network/`) using the mocking library already in `pubspec.yaml` (`mocktail` or `mockito`) |

---

## 2. Reference `external-structured` UseCase Test (`Either<Failure, T>`)

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockOrderRepository extends Mock implements OrderRepository {}

void main() {
  late GetOrdersUseCase useCase;
  late MockOrderRepository mockRepo;

  const tOrders = [OrderEntity(id: 'ord-1', totalCents: 1500)];

  setUp(() {
    mockRepo = MockOrderRepository();
    useCase = GetOrdersUseCase(mockRepo);
  });

  test('returns Right(orders) when repository succeeds', () async {
    when(() => mockRepo.getOrders(page: 1))
        .thenAnswer((_) async => const Right(tOrders));

    final result = await useCase(page: 1);

    expect(result, equals(const Right<Failure, List<OrderEntity>>(tOrders)));
    verify(() => mockRepo.getOrders(page: 1)).called(1);
  });

  test('returns Left(ServerFailure) when repository fails', () async {
    const tFailure = ServerFailure('Backend unavailable');
    when(() => mockRepo.getOrders(page: 1))
        .thenAnswer((_) async => const Left(tFailure));

    final result = await useCase(page: 1);

    expect(result, equals(const Left<Failure, List<OrderEntity>>(tFailure)));
  });
}
```
