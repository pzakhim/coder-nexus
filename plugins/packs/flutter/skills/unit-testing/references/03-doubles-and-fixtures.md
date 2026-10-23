# 03 - Test Doubles and Fixtures (mocktail)

Isolate unit tests by substituting external dependencies with controlled mocks or fakes using `mocktail`.

## 1. Mocks vs Fakes in `mocktail`

- **`Mock`:** Subclasses `Mock` implementing the interface. Used to stub methods and verify invocations:
  ```dart
  class MockOrderRepository extends Mock implements OrderRepository {}
  ```
- **`Fake`:** Subclasses `Fake` implementing value objects or complex parameter types:
  ```dart
  class FakeOrderParams extends Fake implements OrderParams {}
  ```
- **Registering Fallbacks:** When using `any()` with custom object types, register the fallback value before running tests:
  ```dart
  setUpAll(() {
    registerFallbackValue(FakeOrderParams());
  });
  ```

## 2. Stubbing and Verification Patterns

```dart
// Stubbing asynchronous Future return
when(() => mockRepo.getOrders(any()))
    .thenAnswer((_) async => const DataSuccess([testOrderEntity]));

// Invoking subject under test
final result = await useCase.call(params: testParams);

// Asserting return value
expect(result.isSuccess, isTrue);
expect(result.data, equals([testOrderEntity]));

// Verifying interaction
verify(() => mockRepo.getOrders(testParams)).called(1);
verifyNoMoreInteractions(mockRepo);
```

## 3. Test Fixtures

- Create immutable sample data fixtures at the top of test files or in a shared `test/fixtures/` helper.
- Avoid dynamic or randomized test fixtures; maintain static, deterministic values.
