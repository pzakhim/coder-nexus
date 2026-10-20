# Profile 2: External Structured Core System

Use only after Planning records this profile from actual Client evidence. Shared directories must have real consumers; empty folders do not select a profile. Downstream roles reuse the approved selection.


This profile activates when working on an **External Flutter Client** (a third-party or client codebase) that does NOT have the iMESPro `app-*` packages, but already possesses an established **core, shared, or foundation architecture**.

---

## 1. Activation & Discovery Criteria

A project qualifies for **Profile 2 (External-Structured)** if:
1. The approved Client profile does not use company foundations; unrelated neighboring folders are irrelevant. Preserve an explicit approved selection and follow `core-usage` for evidence-based resolution.
2. The codebase contains established shared directories or base modules such as:
   - `lib/core/` (base models, network clients, base use cases, storage services)
   - `lib/shared/` or `lib/common/` (reusable UI widgets, design tokens, helper utilities)
   - Dedicated internal package references (e.g. client private design system or networking package).

---

## 2. Codebase Intelligence & Pattern Matching

Before writing architecture specs or code, agents must inspect the target codebase to catalog existing patterns:

1. **Screen / View Base:**
   - Search for base widget classes: e.g. `class BasePage`, `class BaseScreen`, `class BaseView`, or `abstract class BaseStatefulWidget`.
   - Identify lifecycle hooks, analytics bindings, or responsive layout mixins already used by the client.
2. **State Management & DI Convention:**
   - Identify the client's state management approach (Bloc, Cubit, Provider, Riverpod, etc.).
   - Check Service Locator / DI setup (e.g. `lib/injection.dart`, `lib/core/di/`, or `GetIt` registrations).
3. **Network & Error Handling:**
   - Locate the client's central HTTP/Dio client (e.g. `lib/core/network/dio_client.dart` or `api_client.dart`).
   - Identify their Result/Failure pattern (e.g. `Either<Failure, T>`, `Result<T>`, `ApiResponse<T>`).
4. **UI Kit & Design System:**
   - Catalog existing shared buttons, text inputs, loaders, empty state widgets, dialogs, and color schemes under `lib/shared/` or `lib/core/widgets/`.

---

## 3. Reuse & Adaptation Protocol

### A. Non-Fragmentation Principle (No Competing Bases)
- **Rule:** If the client already has a `BasePage` or `CustomPrimaryButton`, agents MUST inherit and use it.
- **PROHIBITED:** Never introduce a second, parallel base architecture (e.g. do not invent an `AppBaseScreen` or copy iMESPro base classes if the client already has its own base framework). Doing so causes architectural fragmentation and degrades codebase maintainability.

### B. Adaptation Flow across Roles:
1. **Planning (Tech Lead):**
   - Formulate a **Client Core Mapping Table** in `design.md`:
     - Map each feature requirement (Screen, Network, UI Input, Button) to the client's existing base/shared files.
     - Place feature code in the Client’s existing feature layout recorded in the approved design.
2. **Code Writer:**
   - Strictly follow the mapping table.
   - Extend the client's base classes and invoke their established helpers.
   - Follow the approved Client feature layout; add shared code only for actual multiple-feature reuse.
3. **Code Reviewer:**
   - Verify that Coder reused the client's foundation assets.
   - Reject any PR that creates redundant base classes or re-implements existing client widgets.
4. **Test Runner:**
   - Use the client's existing test helpers, test mocks, and widget testing conventions.
