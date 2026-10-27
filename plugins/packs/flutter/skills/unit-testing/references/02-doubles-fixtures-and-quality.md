# 02 — Test Doubles, Fixtures & Assertion Quality (Flutter / Dart)

Rules **U1**, **U4**, **U5**, **U6**, **U7**, **U8**, **U9**, and **U11**.

---

## 1. Doubles Hierarchy in `mocktail`: `Real > Fake > Stub > Mock` (`U4`, `U5`, `U6`)

| Dependency | What to Use in `test/` | Forbidden (`BLOCKER` / `MAJOR`) |
|---|---|---|
| **Subject under test & pure collaborators (`Entity`, `ValueObject`, `Model`, `Mapper`, validator)** | **Real** implementation | Mocking the UseCase, Mapper, or Cubit under test (`U5`) |
| **Port boundaries (`Repository` interface in UseCase test, `UseCase` in Cubit test, `DataSource` in Repository test)** | `class MockX extends Mock implements X {}` (`mocktail`) | Calling live network, disk storage, or platform channels (`U4`) |
| **Custom parameter types passed to `any()` / `captureAny()`** | `class FakeXParams extends Fake implements XParams {}` registered via `registerFallbackValue(FakeXParams())` in `setUpAll` | Leaving fallback unregistered (causes `mocktail` runtime failure) |
| **Permission, role & input validation guards** | **Real** validation/guard code | Mocking a guard to bypass validation or permission checks (`U6`) |

---

## 2. Reference Unit Test Patterns (Stack-Generic)

*(For workspace profile-specific types such as `UseCasePower` / `DataState`, see the active profile's `testing-contracts.md` guide.)*

### Pattern A — Domain UseCase Test (`mocktail`)

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockOrderRepository extends Mock implements OrderRepository {}
class FakeGetOrdersParams extends Fake implements GetOrdersParams {}

void main() {
  late GetOrdersUseCase useCase;
  late MockOrderRepository mockRepository;

  const tParams = GetOrdersParams(page: 1, limit: 20);
  const tOrders = [OrderEntity(id: 'ord-1', totalCents: 1500)];

  setUpAll(() {
    registerFallbackValue(FakeGetOrdersParams());
  });

  setUp(() {
    mockRepository = MockOrderRepository();
    useCase = GetOrdersUseCase(mockRepository);
  });

  group('GetOrdersUseCase', () {
    test('returns order list when repository succeeds', () async {
      // Arrange
      when(() => mockRepository.getOrders(any()))
          .thenAnswer((_) async => const Success(tOrders));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, equals(const Success(tOrders)));
      verify(() => mockRepository.getOrders(tParams)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('propagates Failure when repository fails', () async {
      // Arrange
      const tFailure = Failure<List<OrderEntity>>(message: 'Network timeout');
      when(() => mockRepository.getOrders(any()))
          .thenAnswer((_) async => tFailure);

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, equals(tFailure));
      verify(() => mockRepository.getOrders(tParams)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });
  });
}
```

### Pattern B — Data Model & Mapper Test (Pass + Boundary / Null / Empty Cases)

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('OrderModel', () {
    test('fromJson parses complete valid JSON and maps to OrderEntity', () {
      // Arrange
      final json = <String, dynamic>{
        'id': 'ord-1',
        'total_cents': 1500,
        'notes': 'Priority',
        'items': <Map<String, dynamic>>[],
      };

      // Act
      final model = OrderModel.fromJson(json);
      final entity = model.toEntity();

      // Assert
      expect(entity.id, equals('ord-1'));
      expect(entity.totalCents, equals(1500));
      expect(entity.notes, equals('Priority'));
      expect(entity.items, isEmpty);
    });

    test('fromJson handles missing optional fields and null list safely', () {
      // Arrange
      final json = <String, dynamic>{
        'id': 'ord-2',
        'total_cents': 0,
        'notes': null,
        'items': null,
      };

      // Act
      final entity = OrderModel.fromJson(json).toEntity();

      // Assert
      expect(entity.id, equals('ord-2'));
      expect(entity.totalCents, equals(0));
      expect(entity.notes, isNull);
      expect(entity.items, isEmpty);
    });
  });
}
```

### Pattern C — Presentation Cubit State Machine Test (`bloc_test`)

Always close the Cubit in `tearDown` and assert exact state objects (not only `isA<State>()` when state holds data):

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockGetOrdersUseCase extends Mock implements GetOrdersUseCase {}

void main() {
  late OrderListCubit cubit;
  late MockGetOrdersUseCase mockGetOrders;

  const tOrders = [OrderEntity(id: 'ord-1', totalCents: 1500)];

  setUp(() {
    mockGetOrders = MockGetOrdersUseCase();
    cubit = OrderListCubit(getOrders: mockGetOrders);
  });

  tearDown(() => cubit.close());

  test('initial state is OrderListInitial', () {
    expect(cubit.state, equals(const OrderListInitial()));
  });

  group('loadOrders', () {
    blocTest<OrderListCubit, OrderListState>(
      'emits [OrderListLoading, OrderListLoaded] when useCase succeeds',
      build: () {
        when(() => mockGetOrders(any()))
            .thenAnswer((_) async => const Success(tOrders));
        return cubit;
      },
      act: (c) => c.loadOrders(),
      expect: () => const [
        OrderListLoading(),
        OrderListLoaded(orders: tOrders),
      ],
      verify: (_) => verify(() => mockGetOrders(any())).called(1),
    );

    blocTest<OrderListCubit, OrderListState>(
      'emits [OrderListLoading, OrderListFailure] when useCase fails',
      build: () {
        when(() => mockGetOrders(any())).thenAnswer(
          (_) async => const Failure(message: 'Server unavailable'),
        );
        return cubit;
      },
      act: (c) => c.loadOrders(),
      expect: () => const [
        OrderListLoading(),
        OrderListFailure(message: 'Server unavailable'),
      ],
    );
  });
}
```

---

## 3. Right-Reason Red Failure, Independent Expectations & Mutation Check (`U7`, `U8`, `U14`)

| Red Run Output | Meaning | Action |
|---|---|---|
| `TestFailure` (`Expected: ... Actual: ...`) naming the missing behavior | **Right reason** | Write the minimal production code to make it pass |
| Test passes immediately (`+1: All tests passed!`) | Behavior already exists or assertion is tautological | Fix the test so it fails when the target behavior is absent |
| Compilation error, missing `registerFallbackValue`, `NullCheckError` in test setup | **Not red yet** (broken test setup) | Fix the setup and re-run until the assertion itself fails |
| `No tests match regular expression` / skipped | **Not run (`NOT_RUN`)** | Fix `--plain-name` or file path; never record as red or green |

- **Independent Literal Expectations (`U8`):** Assert concrete expected literals from `design.md` (`equals(1500)`). Never write `expect(result, isNotNull)` or `expect(true, isTrue)` as the sole assertion.
- **Determinism (`U7`):** Inject `DateTime Function()` for time-sensitive logic, use `Random(seed)` for random values, await all futures/streams, and close Cubits/controllers in `tearDown`.
- **Pre-Handoff Mental Mutation Check:** Verify at least one test fails if you: (1) flip a branch condition, (2) return `Failure` instead of `Success`, (3) omit a state emission in the Cubit, or (4) drop a field mapping in `toEntity()`.
