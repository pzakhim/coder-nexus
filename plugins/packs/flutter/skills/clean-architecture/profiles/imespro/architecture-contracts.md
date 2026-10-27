# iMESPro Architecture & Foundation Contracts

> Topic: Mandatory iMESPro Clean Architecture contracts (`BaseScreen`/`BaseScreenState`, `app_core` pure-Dart domain imports, `DataState`/`.tryCatch`, `DataMapper`, and starter templates `templates/*.dart.tpl`).

---

## 1. Prerequisites & Foundation Authority

Before modifying or scaffolding a module under the `imespro` profile:
1. Pass `coder-nexus setup flutter --check`.
2. Read `../app-core/guidance/GUIDE.md`, `../app-util/guidance/GUIDE.md`, and `../app-ui-kit/guidance/GUIDE.md` (and `../app-*/lib/` when verifying exact signatures).
3. Never edit, copy, or vendor code from `app_core`, `app_util`, or `app_ui_kit` into the Client repository.

---

## 2. Layer-Specific `imespro` Contracts

| Layer | Mandatory `imespro` Contract |
|---|---|
| **Domain (`domain/`)** | • Import only pure-Dart sub-paths from `app_core` (`package:app_core/domain/...`, `package:app_core/data/models/data_state.dart`, `package:app_core/errors/error_entity.dart`). **Never** import the barrel `package:app_core/app_core.dart` in `domain/` (`DOM-002` / `A5`).<br>• Repository contracts return `Future<DataState<T>>` (`ResultFuture<T>`).<br>• Use cases extend `UseCasePower<Output, Input>` (or `NoParamsUseCasePower<Output>`). |
| **Data (`data/`)** | • API DataSources extend the Client's verified base data source and use configured endpoint constants.<br>• DTO Models validate mandatory fields explicitly and never invent fallback values.<br>• Mappers extend `DataMapper<Model, Entity>` (`mapToEntity`, and `mapToModel` when write operations require it).<br>• Repository implementations wrap calls with `.tryCatch(...)` (synchronous mapping) or `tryCatchAsync(...)` (async callback), returning `DataSuccess` / `DataFailure` with preserved `ErrorEntity` metadata. |
| **Presentation (`presentation/`)** | • **Screen Contract (`PRE-005`, `PRE-006` — `BLOCKER`):** Every navigable screen destination in `presentation/screens/*_screen.dart` is named `*Screen` and extends the active Client `BaseScreen` paired with `BaseScreenState`.<br>• Implement `createState()`, the required metadata hook (`ScreenModel getScreen()`), and the responsive layout hook (`buildMobilePortrait(BuildContext context)`). **Never** override raw `Widget build(BuildContext context)` on a `BaseScreenState` subclass.<br>• Dialogs, bottom sheets, and child widgets in `presentation/widgets/` do **not** extend `BaseScreen`.<br>• New Cubits (`INIT`) use Pattern A (`sealed class` extending `BaseBlocState`, overriding `equatableProps`); extended modules (`EXTEND`) preserve their existing Pattern A/B convention. |

---

## 3. Starter Templates (`templates/*.dart.tpl`)

Use these `imespro` starter templates only for layers required by the approved phase behavior, and verify every import against the target Client's resolved packages:

- **Domain:** `templates/domain/entity.dart.tpl`, `templates/domain/repository.dart.tpl`, `templates/domain/usecase.dart.tpl`
- **Data:** `templates/data/data_source.dart.tpl`, `templates/data/model.dart.tpl`, `templates/data/mapper.dart.tpl`, `templates/data/repo_impl.dart.tpl`
- **Presentation:** `templates/presentation/state.dart.tpl`, `templates/presentation/cubit.dart.tpl`, `templates/presentation/screen.dart.tpl`
- **DI:** `templates/di/module_di.dart.tpl`
