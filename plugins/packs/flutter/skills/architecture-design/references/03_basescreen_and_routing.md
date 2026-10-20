# 03 — BaseScreen, Routing, and DI Contract

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for Section 3 of `design.md`: **Screen, Routing & DI Contract**.

## Purpose
Establishes the integration contracts for UI destinations, screen lifecycle, route arguments, navigation boundaries, and Dependency Injection registration scopes.

## 1. Screen Contract & BaseScreen Integration
Read the `BaseScreen` contract in `../app-core/guidance/GUIDE.md` §2.1 (via `{{slot:core-usage}}`) and confirm the signature in its source:
- **Screen Class Naming**: File `*_screen.dart`, Class `*Screen`.
- **Inheritance**: Extends `BaseScreen` (or `BaseStatefulWidget`) with `BaseScreenState<Screen>`.
- **Hooks & Metadata**:
  - `ScreenModel getScreen()`: returns screen tracking ID and metadata.
  - Required layout hooks: safe area, app bar configuration, background color.
- **Classification**:
  - Full UI destinations with distinct routes $\implies$ **Screen**.
  - Modal sheets, dialogs, popups $\implies$ **Widget/Dialog** (resides in `presentation/widgets/`, not `screens/`).

## 2. Routing Contract
Inspect `lib/routes/` or the client's router configuration:
- **Route Name**: Define exact constant (e.g. `AppRoutes.<feature>`).
- **Route Arguments**:
  - Specify input parameters (e.g., `final String <paramId>`).
  - Specify how arguments are passed and extracted (via route constructor or `settings.arguments`).
- **Navigation Return Value**:
  - Specify what data (if any) the screen returns on `Navigator.pop(context, result)`.

## 3. Dependency Injection (DI) Contract
Inspect `lib/modules/modules_di.dart`:
- **Registration Order in `di.dart`**:
  `Mapper` $\to$ `DataSource` $\to$ `Repository` (bound to abstract interface) $\to$ `UseCase` $\to$ `Cubit`.
- **Scope Lifetimes**:
  - `registerFactory`: For screen-scoped Cubits (created on demand, destroyed when screen unmounts).
  - `registerLazySingleton`: For Repositories, DataSources, and shared application services.
- **Root Wire-up**: Specify how `feature_di.dart` is invoked inside `modules_di.dart` (e.g., `initFeatureDi()`).

## Output Format
```markdown
## 3. Screen, Routing & DI Contract

### A. Screen Architecture
- **Screen Destination**: `lib/modules/<feature>/presentation/screens/<feature>_screen.dart`
- **Class**: `<Feature>Screen extends BaseScreen`
- **State**: `<Feature>ScreenState extends BaseScreenState<<Feature>Screen>`
- **Metadata Hook**: `getScreen()` -> `ScreenModel(screenName: "...", ...)`
- **Modals & Dialogs**: [List any child dialogs/bottom-sheets]

### B. Routing & Navigation
- **Route Name**: `AppRoutes.<feature>` (`"/<feature-path>"`)
- **Route Arguments**: `final <Type> <paramName>` (extracted from ...)
- **Pop Result**: `Navigator.pop(context, <Type>)`

### C. DI Service Locator Contract
- **Module DI File**: `lib/modules/<feature>/di.dart`
- **Registration Scope**:
  - `sl.registerFactory<<Feature>Cubit>(() => <Feature>Cubit(...))`
  - `sl.registerLazySingleton<<Feature>Repository>(() => <Feature>RepositoryImpl(...))`
- **App Wiring**: Registered in `lib/modules/modules_di.dart`
```
