# External Structured Bug-Hunt Contracts

> Topic: Defect patterns in client lib/core/ result wrappers, Dio interceptors, codegen models, and shared state holders (external-structured profile)

## 1. `external-structured` Defect Patterns (Dimension 6 Extension)

When hunting bugs in an `external-structured` Flutter project (with existing `lib/core/` or `lib/shared/` foundations), check every applicable row below:

| Looks like | Goes wrong when | Check |
|---|---|---|
| Calling `.getOrElse` / `.right` / `.data` on the project's `Result<T>` / `Either<Failure, T>` without handling the failure branch | Failure is silently ignored or throws an unwrap exception at runtime | Exhaustively fold/switch both success and failure branches in the `Cubit` / `Bloc` / `Notifier` |
| Editing a `@freezed` or `@JsonSerializable` class without regenerating `.freezed.dart` / `.g.dart` | New or renamed field is ignored during `fromJson`, `toJson`, `==`, or `copyWith` | Compare source fields against `.g.dart` / `.freezed.dart` and run `flutter analyze` |
| Feature repository bypassing `lib/core/` network client / error mapper and instantiating raw `Dio()` | Auth headers, token refresh, timeout configuration, and unified error mapping are skipped | Ensure all data sources inject the shared `lib/core/` HTTP client |
| Singleton state holder or cache in `lib/core/` retaining user-scoped data across logout | User B sees User A's cached profile or items after switching accounts | Verify logout resets or disposes user-scoped singletons/caches |
