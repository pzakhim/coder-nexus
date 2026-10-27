# External Standard Unit Testing Contracts (Standard Dart 3 & Flutter)

> Topic: Unit testing with standard Dart 3 sealed classes, `flutter_test`, `bloc_test`, and `mocktail` without custom company wrappers (`external-standard` profile)

Applies **U2**, **U5**, **U8**, and **U11** when the workspace profile is **`external-standard`**.

---

## 1. Per-Layer `external-standard` Unit Test Rules

| Aspect | Contract |
|---|---|
| **Result & State Types** | Test standard Dart 3 `sealed class` results/states or typed exceptions directly. Never invent `UseCasePower`, `DataState`, `BaseRemoteDataSource`, or `DataMapper` wrappers |
| **UseCase / Repository Layer** | Test only the layers present in the approved `design.md`. If a simple feature calls the repository directly from the `Cubit` without a pass-through UseCase, unit-test the `Repository` and `Cubit` directly |
| **Doubles & Tooling** | Use `flutter_test`, `mocktail`, and `bloc_test` (when `flutter_bloc` is used). Keep fixtures as plain `const` Dart objects or JSON maps in `test/fixtures/` |
