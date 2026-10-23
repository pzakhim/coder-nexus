# 03 - Errors and Logging (Flutter / iMESPro)

Adhere strictly to the workspace's error handling contracts from `app_util` and logging conventions.

## 1. No Swallowed Errors

Swallowing exceptions creates silent bugs and leaves screens hung in loading states.

```dart
// BAD: Catching and ignoring
try {
  await useCase.call(params: params);
} catch (e) {
  // Silent ignore - P1 violation!
}

// GOOD: Return DataState and handle state transition
final result = await useCase.call(params: params);
if (result.isSuccess) {
  emit(OrderSuccess(orders: result.data));
} else {
  AppLogger.I.e('Failed to load orders: ${result.message}');
  emit(OrderFailure(message: result.message));
}
```

## 2. Repository Error Handling with `.tryCatch`

Repositories in iMESPro must use the `.tryCatch` extension from `package:app_util/app_util.dart`:

```dart
@override
Future<DataState<List<OrderEntity>>> getOrders() {
  return remoteDataSource
      .getOrders()
      .tryCatch(
        handler: (response) {
          final list = parseList(response.data);
          return list.map((e) => OrderModel.fromJson(e).mapToEntity()).toList();
        },
      );
}
```
- `.tryCatch` converts all HTTP errors, timeouts, network disconnections, and JSON parse exceptions into `DataFailure<T>`.
- The UI layer receives a clean `DataState<T>` and never experiences an unhandled asynchronous crash.

## 3. Logging Rules: `AppLogger.I`

- **Forbidden:** Never use `print()` or `debugPrint()` in committed code. Both are flagged as **P1 violations**.
- **Standard:** Use `AppLogger.I` from `app_util`:
  - `AppLogger.I.d(...)` - Diagnostic debugging details during local development.
  - `AppLogger.I.i(...)` - Key lifecycle events (screen transitions, successful sync).
  - `AppLogger.I.w(...)` - Recoverable warnings, fallback handling.
  - `AppLogger.I.e(...)` - Unrecoverable operational errors with stack traces.
- **Privacy & Security:** NEVER log auth tokens, passwords, bearer headers, credit card numbers, or customer PII.
