# 03 — Screen Classification, Adding/Splitting & Review Rubric

> Scope: Screen destination vs. child widget contract, `INIT` vs. `EXTEND` implementation steps, splitting oversized files, and the `BLOCKER` / `MAJOR` / `MINOR` review rubric (`A2`, `A6`, `A9`, `A10`).

---

## 1. Screen Classification & Destination Contract (`A2`, `A6`)

Before naming files or choosing a widget superclass, classify every UI component in the approved scope:

| UI Component Type | Location & Naming | Superclass & Lifecycle Contract |
|---|---|---|
| **Navigable Screen Destination** (full-screen route entry in the app router) | `lib/modules/<feature>/presentation/screens/*_screen.dart` · class `*Screen` (never `*Page`) | Uses the active workspace profile's verified Screen contract (see the active profile reference in `SKILL.md`), route annotation (`@RoutePage()` where `auto_route` is used), and screen-scoped `BlocProvider` wiring |
| **Dialog / Bottom Sheet / Feature Child Widget** (not an independent route destination) | `lib/modules/<feature>/presentation/widgets/*.dart` | Standard `StatelessWidget` or `StatefulWidget` (when local controller/animation disposal is needed). Does **not** use the full-screen base class or screen analytics registration |
| **Cross-Feature Shared Widget** (reused across 2+ modules) | `lib/commons/widgets/*.dart` | Pure, reusable widget parameterized via constructor props and callbacks; zero feature Cubit or Domain imports |

### Screen Implementation Rules
1. **Verify before coding:** Inspect the Client's `pubspec.yaml`, router declarations, and at least one working `*Screen` in a sibling module to confirm route annotations, `BlocProvider` ownership (`AutoRouteWrapper` or route builder), and base class hooks.
2. **Pure rendering (`A6`):** Never fire Cubit load triggers, network requests, or navigation calls directly inside `build()` or responsive layout builders. Trigger initial loads in `BlocProvider` creation or `initState()` / lifecycle hooks.
3. **Scoped migration:** When extending an existing feature (`EXTEND`), rename or migrate only the screens within the approved task scope—update routes, imports, and widget tests together while leaving unrelated historical screens untouched.

---

## 2. Adding or Extending a Feature Module (`INIT` vs. `EXTEND`)

### Workflow (`A9`)
1. **Check Scope (`INIT` vs. `EXTEND`):**
   - **`INIT` (New feature module):** Create `lib/modules/<feature>/` with only the layers required by the approved phase. Copy the verified DI and Cubit state pattern from a working sibling module.
   - **`EXTEND` (Existing feature module):** Preserve the module's existing state convention and folder layout. A UI-only extension reuses existing UseCases/Cubits without adding empty Domain/Data classes.
2. **Build Bottom-Up (when adding a full data flow):**
   - **Step 1 — Domain (`domain/`):** Define immutable `Entity` (`entities/`), abstract `Repository` (`repo/`), and focused `UseCase` (`usecases/`).
   - **Step 2 — Data (`data/`):** Implement `Model` (`models/`) with fail-fast field validation, `Mapper` (`mappers/`), `DataSource` (`data_sources/`) using verified endpoint constants, and `RepositoryImpl` (`repo_impl/`).
   - **Step 3 — Presentation (`presentation/`):** Implement `State` and `Cubit` (`bloc/`), navigable `*Screen` (`screens/`), and cohesive child widgets (`widgets/`).
   - **Step 4 — DI & Routing (`di.dart`, `modules_di.dart`, router):** Register Mapper → DataSource → Repository → UseCase → Cubit in `di.dart`, wire `modules_di.dart` (if `INIT`), and register the route.

---

## 3. Splitting Oversized Files (`A10`)

Enforce structural budgets from `{{slot:clean-code}}` (`C6`: file ≤ 300 LOC, class ≤ 200 LOC, function/build method ≤ 50 LOC, parameters ≤ 4):

| Smell | How to Split |
|---|---|
| `*Screen` file > 300 LOC or stacks multiple `_buildSection*()` methods | Extract self-contained visual sections into dedicated `StatelessWidget` classes under `presentation/widgets/<feature>_<section>_widget.dart` receiving typed data and callbacks |
| `Cubit` mixes unrelated sub-flows or exceeds ~200 LOC | Split into focused screen/sub-flow Cubits or extract domain coordination into a dedicated `UseCase` |
| `Model` file contains multiple nested DTOs > 300 LOC | Split sub-models into cohesive files under `data/models/` and keep `Mapper` methods focused per entity |

---

## 4. Architecture Review Rubric (`BLOCKER` / `MAJOR` / `MINOR`)

During Code Review, grade architectural findings using `plugins/shared_contracts/flags_and_statuses.md` §3:

| Severity | Architectural Triggers |
|---|---|
| **`BLOCKER`** | • `validate_architecture_code` or `validate_module_architecture` returns `ERROR` / `FAILED`<br>• `domain/` imports `package:flutter/*`, `data/`, `presentation/`, or third-party HTTP/storage packages (`A5`)<br>• `presentation/` directly calls `DataSource`, `Dio`, or imports DTO `Model`s (`A1`, `A2`)<br>• Missing mandatory DTO fields silently fallback to `0`, `""`, `[]`, or fabricated mock records in `lib/` (`A8`)<br>• Screen destination violates the active profile's required base screen contract (`PRE-005` / `PRE-006`)<br>• Side-effecting network/Cubit calls triggered inside `build()` (`A6`) |
| **`MAJOR`** | • Cross-module import of another feature's private `Cubit`, `State`, `DataSource`, `Model`, or `RepositoryImpl` (`A7`)<br>• Screen-scoped `Cubit` registered as a singleton instead of `registerFactory` (`DIR-001`, `A4`)<br>• Business rules or multi-step orchestration placed inside a Widget instead of a `Cubit` / `UseCase` (`A2`, `A3`)<br>• Unapproved empty boilerplate layers created for a UI-only change (`A9`) |
| **`MINOR`** | • Minor file/folder naming drift within the correct layer<br>• Screen file approaching 300 LOC that can be cleaner with an extracted sub-widget (`A10`) |
