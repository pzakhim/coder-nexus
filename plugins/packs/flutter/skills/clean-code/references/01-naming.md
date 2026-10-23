# 01 - Naming Conventions (Flutter / Dart)

Follow **Effective Dart** naming standards and iMESPro Clean Architecture layer designations.

## 1. Identifier Casing

| Element | Rule | Good | Bad |
|---|---|---|---|
| Classes, Mixins, Enums, Extensions, Typedefs | `UpperCamelCase` | `OrderRepository`, `AuthCubit` | `order_repository`, `authCubit` |
| Libraries, packages, files, directories | `lowercase_with_underscores` | `order_details_screen.dart` | `OrderDetailsScreen.dart`, `orderDetails.dart` |
| Variables, parameters, getters, setters, methods | `lowerCamelCase` | `fetchOrders()`, `itemCount` | `FetchOrders()`, `item_count` |
| Constants | `lowerCamelCase` or `kCamelCase` | `kDefaultTimeout`, `primaryPadding` | `DEFAULT_TIMEOUT`, `k_default_timeout` |
| Type parameters | Single uppercase letter or `UpperCamelCase` | `T`, `ResultType` | `t`, `item` |
| Private members / helper classes | Prefixed with `_` | `_buildHeader()`, `class _OrderSummaryCard` | `buildHeader()`, `class OrderSummaryCard` (if file-private) |

## 2. Layer & Architectural Naming

| Layer / Role | Suffix / Pattern | Example |
|---|---|---|
| Screen (Route destination) | `*Screen` (must extend `BaseScreen`) | `OrderListScreen`, `OrderDetailScreen` |
| Screen State | `*ScreenState` (must extend `BaseScreenState`) | `OrderListScreenState` |
| Sub-widget (private/local) | `_*Widget` or `_*Section` / `_*Card` | `_OrderItemCard`, `_HeaderSection` |
| Cubit | `*Cubit` (extends `Cubit<*State>`) | `OrderListCubit`, `UserProfileCubit` |
| State | `*State` (sealed class / Equatable) | `OrderListState`, `OrderListLoading` |
| UseCase | `*UseCase` (implements `UseCasePower<T, P>`) | `GetOrdersUseCase`, `CreateOrderUseCase` |
| Repository Interface | `*Repository` (abstract class in domain) | `OrderRepository` |
| Repository Implementation | `*RepositoryImpl` (class in data) | `OrderRepositoryImpl` |
| Remote Data Source | `*RemoteDataSource` (extends `BaseRemoteDataSource`) | `OrderRemoteDataSourceImpl` |
| Data Model / DTO | `*Model` (implements `DataMapper<Entity>`) | `OrderModel`, `OrderItemModel` |
| Domain Entity | `*Entity` (pure Dart, no Flutter imports) | `OrderEntity`, `OrderItemEntity` |

## 3. Semantic Rules

- **Booleans:** Prefix with `is`, `has`, `can`, `should`: `isLoading`, `hasMore`, `canSubmit`.
- **Collections:** Plural nouns: `orders`, `items`, `statusList`.
- **Event handlers:** Prefix with `on*` or `handle*`: `onPressed`, `onItemTapped`, `handleRefresh`.
- **Vague names forbidden:** Do not use `data`, `info`, `temp`, `item`, `process()`, or `doStuff()`.
