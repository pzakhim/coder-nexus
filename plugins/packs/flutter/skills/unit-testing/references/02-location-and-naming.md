# 02 - Location and Naming Conventions

Unit tests must be easily discoverable and mirror the structure of `lib/`.

## 1. Directory Structure

Unit test file paths under `test/` must directly reflect the path of the subject under test in `lib/`:

| Production Code Path | Test Code Path |
|---|---|
| `lib/modules/<feature>/domain/usecases/get_orders_usecase.dart` | `test/modules/<feature>/domain/usecases/get_orders_usecase_test.dart` |
| `lib/modules/<feature>/data/models/order_model.dart` | `test/modules/<feature>/data/models/order_model_test.dart` |
| `lib/modules/<feature>/data/datasources/order_remote_data_source.dart` | `test/modules/<feature>/data/datasources/order_remote_data_source_test.dart` |
| `lib/modules/<feature>/presentation/cubit/order_list_cubit.dart` | `test/modules/<feature>/presentation/cubit/order_list_cubit_test.dart` |

## 2. Test Naming Conventions

- Group tests using `group('<ClassName>', () { ... })`.
- Individual test descriptions must describe behavior and expected outcome:
  - `test('should return DataSuccess with order list when repository succeeds')`
  - `test('should return DataFailure when repository encounters network timeout')`
  - `blocTest('emits [Loading, Success] when GetOrdersUseCase succeeds')`
  - `blocTest('emits [Loading, Error] with message when GetOrdersUseCase fails')`
