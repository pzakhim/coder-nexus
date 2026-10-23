# 05 - Test Execution & Evidence Capture

Verify test results and report deterministic evidence rows in task handoffs.

## 1. Running Unit Tests via CLI

Execute tests from the Flutter project workspace:

```bash
# Run unit tests for a specific feature module
flutter test test/modules/<feature>/

# Run a specific unit test file
flutter test test/modules/orders/domain/usecases/get_orders_usecase_test.dart

# Run tests with detailed reporting
flutter test --reporter=expanded test/modules/<feature>/
```

## 2. Red-to-Green Evidence Reporting

When fixing a bug or review finding, record both the failing (red) and passing (green) runs in the handoff:

```text
- Red Run: flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart
  Expected: FAIL (emits OrderFailure on 404)
  Observed: Expected: [OrderLoading, OrderFailure], Actual: [OrderLoading] (timeout)
- Green Run: flutter test test/modules/orders/presentation/cubit/order_list_cubit_test.dart
  Result: 4 tests passed, 0 failed.
```
