# 05 - Debugging Tools and Commands

Use these developer tools to isolate defects efficiently.

## 1. CLI Commands

```bash
# Run tests with stack traces
flutter test --reporter=expanded

# Run specific test file
flutter test test/modules/orders/domain/usecases/get_orders_usecase_test.dart

# Run tests matching description
flutter test --plain-name "emits Failure when repository returns error"
```

## 2. Flutter DevTools

- **Widget Inspector:** Inspect widget constraints, flex parent/child relationships, and rebuild stats.
- **Network Tab:** Inspect raw HTTP requests and responses sent via `ApiService`.
- **Memory Profiler:** Inspect retained memory, detect leaked controllers, and review Dart heap snapshots.
