# iMESPro Unit Testing Contracts (`app_core` & `app_util`)

> Topic: Unit testing `UseCasePower<T, P>`, `DataState<T>`, `DataMapper<Entity>`, `BaseRemoteDataSource`, and `ListViewPagingCubit` (`imespro` profile)

Applies **U2**, **U5**, **U8**, and **U11** when the workspace profile is **`imespro`**. Read `../app-core/guidance/GUIDE.md` and `../app-util/guidance/GUIDE.md` for exact package signatures.

---

## 1. Per-Layer `imespro` Unit Test Contracts

| Layer | Subject Class | Boundary Doubled (`mocktail`) | Required Assertions |
|---|---|---|---|
| **Domain UseCase** | `*UseCase extends UseCasePower<Entity, Params>` (`app_core`) | `Mock*Repository implements *Repository` | Stub `when(() => mockRepo.method(any())).thenAnswer((_) async => const DataSuccess(tEntity))` and `DataFailure(tError)`; invoke `useCase.call(params: tParams)`; assert `result.isSuccess`, `result.data`, and `result.error` |
| **Data Model / Mapper** | `*Model with DataMapper<Entity>` (`app_core`) | **None** | Test `fromJson` (using `parseString`, `parseInt`, `parseDouble`, `parseBool` from `app_util` for safe coercion), `toJson`, and `mapToEntity()` |
| **Data Repository** | `*RepositoryImpl implements *Repository` | `Mock*RemoteDataSource` | Verify `.tryCatch` (`app_util`) maps `ApiResponse` success into `DataSuccess<Entity>` and HTTP/network errors into `DataFailure<Entity>` |
| **Remote DataSource** | `*RemoteDataSource extends BaseRemoteDataSource` | `MockApiService extends Mock implements ApiService` (`app_util`) | Stub `mockApiService.get/post(...)`; verify `200`/`201` returns `ApiResponse` and `400`/`401`/`500` or timeout propagates the expected error |
| **Presentation Cubit** | `*Cubit` / `ListViewPagingCubit<T>` (`app_core`) | `Mock*UseCase` | Use `blocTest`; stub `useCase.call(params: any(named: 'params'))` returning `DataSuccess` / `DataFailure`; assert exact emitted state sequence |

---

## 2. Reference `imespro` UseCase & Cubit Test Snippet

```dart
import 'package:app_core/app_core.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockOrderRepository extends Mock implements OrderRepository {}
class FakeOrderParams extends Fake implements OrderParams {}

void main() {
  late GetOrdersUseCase useCase;
  late MockOrderRepository mockRepo;

  const tParams = OrderParams(page: 1, pageSize: 20);
  const tOrders = [OrderEntity(id: 'ord-1', total: 1500)];

  setUpAll(() => registerFallbackValue(FakeOrderParams()));

  setUp(() {
    mockRepo = MockOrderRepository();
    useCase = GetOrdersUseCase(mockRepo);
  });

  test('returns DataSuccess when repository succeeds', () async {
    when(() => mockRepo.getOrders(any()))
        .thenAnswer((_) async => const DataSuccess(tOrders));

    final result = await useCase.call(params: tParams);

    expect(result, isA<DataSuccess<List<OrderEntity>>>());
    expect(result.data, equals(tOrders));
    verify(() => mockRepo.getOrders(tParams)).called(1);
  });

  test('returns DataFailure when repository fails', () async {
    const tError = ErrorEntity(code: 'ERR_500', message: 'Server error');
    when(() => mockRepo.getOrders(any()))
        .thenAnswer((_) async => const DataFailure(tError));

    final result = await useCase.call(params: tParams);

    expect(result, isA<DataFailure<List<OrderEntity>>>());
    expect(result.error, equals(tError));
  });
}
```
