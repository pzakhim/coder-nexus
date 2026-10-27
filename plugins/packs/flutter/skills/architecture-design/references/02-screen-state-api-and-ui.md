# 02 — Screen, State, API/Mockoon Strategy, UI Mapping, and UX Policy

> Topic: Screen/routing/DI contract, state and domain flow, Backend API and Mockoon strategy, UI component mapping across 4 visual states, and UX error/storage policy (`AD5`–`AD8`)

## 1. Screen, Routing & DI Contract (`AD5`)

### 1.1 Screen Classification & Lifecycle
- **Route Destinations (`presentation/screens/*_screen.dart`):** Full UI destinations with distinct routes use class name `<Feature>Screen` in `<feature>_screen.dart`, inheriting from the active profile's screen base (or `StatelessWidget`/`StatefulWidget` in `external-standard`).See [03-screens-adding-and-splitting.md](../../clean-architecture/references/03-screens-adding-and-splitting.md).
- **Modals, Bottom Sheets & Child Views (`presentation/widgets/`):** Dialogs, sheets, and reusable subtrees are widgets, not screens, and reside under `presentation/widgets/`.

### 1.2 Routing & DI Registration
- **Routing Contract:** Specify the exact route constant/path from the Client router, typed route arguments (`final <Type> <arg>`), and pop return value (`Navigator.pop<ResultType>`).
- **DI Registration Order & Scopes (`di.dart`):**
  - Order: `Mapper` → `DataSource` → `Repository` (bound to abstract Domain interface) → `UseCase` → `Cubit / Notifier`.
  - **Screen-scoped State (`registerFactory`):** Always register screen-scoped Cubits/Blocs as factories so state is disposed when the screen unmounts (`DIR-001`).
  - **Stateless Collaborators (`registerLazySingleton`):** Register Repositories and DataSources as lazy singletons.

---

## 2. State Management & Domain Data Flow (`AD5`)

1. **Follow the Client's State Convention:** Inspect the target module first, then a sibling module, and reuse its state convention (Dart 3 `sealed` classes, `Equatable` with `copyWith`, or the project's base state class). Never invent a new competing state base in `lib/core/`.
2. **Domain Layer — Only What Earns Its Place:**
   - **UseCase required:** When the operation enforces a domain validation rule, orchestrates multiple repositories, or is shared across multiple screens/cubits.
   - **Direct Repository call allowed:** For a simple single-repository pass-through used by one Cubit, **if** the Client's existing convention already permits Cubit → Repository directly; otherwise follow the Client's use-case convention.
   - **Entities:** Pure Dart, immutable; include only fields used by the UI or business rules.

---

## 3. Backend API Contract & Mockoon Strategy (`AD6`)

Read `shared_contracts/api_handshake_protocol.md`. The Frontend never modifies Backend code, and production code under `lib/` **never** contains fake `Mock<Feature>DataSource` classes or hardcoded mock fallbacks.

### 3.1 API Contract Status
| Status | Meaning | `design.md` & `PHASE-00` Action |
|---|---|---|
| `BE_API_READY` | Backend API exists and specification is provided | Record verified endpoints, request/response schemas, and error codes in `design.md`; `PHASE-00` records `[INFO_NOTE]` (or `[EXECUTE]` for a live probe). |
| `MOCKOON_MOCKED` | Backend API is not ready or missing endpoints; user approved Mockoon | Agree with the user via `ask_question` on **Pass/Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)** triggers and record the **Mockoon Trigger & Test Data Table** in `design.md`; `PHASE-00` runs as `[EXECUTE]` to create and verify `mocks/<feature>_mockoon.json`. |
| `NONE` | Feature is purely local or UI-only | Omit the Backend API section from `design.md`. |

### 3.2 Mockoon Trigger & Test Data Table (`MOCKOON_MOCKED`)
This table is the single source of truth for both `mocks/<feature>_mockoon.json` (`PHASE-00`) and developer Unit Tests (`PHASE-01+`):

| Scenario ID | Case (Pass / Fail / Empty) | Endpoint | Input Trigger (`body` / `query` / `header`) | Mockoon Rule | HTTP Status & Latency | Response JSON Body |
|---|---|---|---|---|---|---|
| `MOCK-01` | Pass / Default | `POST /api/v1/<feature>` | `body.<field> == "<valid>"` (default) | Default response | `200 OK` (300ms) | `{"result": true, "data": {"id": "1"}}` |
| `MOCK-02` | Fail (Validation / Auth) | `POST /api/v1/<feature>` | `body.<field> == "<invalid>"` | `body` · `<field>` · `equals` · `<invalid>` | `400` / `401` (200ms) | `{"result": false, "message": "Invalid input"}` |
| `MOCK-03` | Fail (Server Error) | `POST /api/v1/<feature>` | `body.<field> == "error_500"` | `body` · `<field>` · `equals` · `error_500` | `500` (200ms) | `{"result": false, "message": "Server error"}` |
| `MOCK-04` | Empty List | `GET /api/v1/<feature>` | `query.filter == "empty"` | `query` · `filter` · `equals` · `empty` | `200 OK` (200ms) | `{"result": true, "data": []}` |

- **Live Cutover:** When the real Backend API ships, switch the base domain in `.env` and verify live integration per `shared_contracts/api_handshake_protocol.md`. Fixture/Mockoon checks never prove live acceptance.

---

## 4. Foundation Reuse, UI Component Mapping & 4 Visual States (`AD7`)

### 4.1 Sequential Reuse Ladder
For every UI element in `requirements.md`, evaluate in strict order:
1. **Approved Profile Design System / UI Kit** (see active profile guide: `app_ui_kit` / `app_core` in `imespro`, or client design system in `external-structured`). If multiple kit components fit, ask the user via `ask_question` (2–3 options, recommended first).
2. **Shared Client Widgets** (`lib/commons/widgets/` or `lib/shared/widgets/`).
3. **Composition** of existing verified components.
4. **Feature-Private Widget** (`lib/modules/<feature>/presentation/widgets/`), recording a justified `Core gap` row in `## Foundation reuse` (promote to shared only when 2+ modules need it).
- When deviating from an approved foundation component, add an optional `### Complexity justifications` table under `## Foundation reuse` citing `D-NN` (`Violation`, `Why needed`, `Simpler alternative rejected because`).

### 4.2 Four Mandatory Visual States
Every screen and primary data view in `## UI design system` must specify:
1. **Loading State:** Skeleton/shimmer or loading indicator component.
2. **Content State:** Populated layout and interactive elements.
3. **Empty State:** Empty illustration/message and optional CTA (or `N/A` with reason if impossible).
4. **Error State:** Inline vs full-screen error presentation, message source, and retry action calling the state holder.

### 4.3 `## UI/UX mapping` (When Non-`EXISTING` Screens or New Components Exist)
When `requirements.md` (`## Screens & Visual Sources`) contains any non-`EXISTING` screen (`NEW` or `CHANGED`) or new/custom components (`C-NN`), audit the extracted Figma tokens/tree (`tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`) or codebase tokens (`CODEBASE_ONLY`) via `{{slot:ui-kit-mapping}}`, and include `## UI/UX mapping` mapping every `S-NN` (except `EXISTING`) and every `C-NN` to its target screen/widget class, kit mapping (`{{slot:ui-kit-mapping}}`), and owning phase/task (`DESIGN-008`). Delete the section when `UI Impact: NO_UI_IMPACT` and no non-`EXISTING` screens exist.

---

## 5. UX Error Handling, Storage Policy & Optional Risk/Migration Subsections (`AD8`)

- **UX Error Matrix (`get_ux_error_patterns`):**
  - `AUTH_401`: Auth interceptor attempts silent token refresh; on failure, emits global logout/redirect to Login.
  - `VALIDATION_400` / `422`: Map field-level errors to inline input error text or form banner.
  - `NETWORK_TIMEOUT`: Non-blocking Toast/SnackBar with `Retry` (or full-screen error view on initial load failure).
  - `SERVER_500`: Friendly generic error dialog/banner; log details via the project logger (never expose raw stack traces to users).
- **Local Storage & Cache Invalidation:**
  - Store tokens, credentials, and secrets exclusively in encrypted `FlutterSecureStorage` (`S4`).
  - Use `SharedPreferences` or local DB (`Drift`/`Hive`/`SQLite`) only for non-sensitive preferences/cache, and specify cache purge hooks on `AuthLogout` and pull-to-refresh.
- **Optional Subsections in `## Integration, errors, and risks` (delete when not applicable):**
  - `### Risk → Mitigation`: Known risks to an AC/goal, mitigation check, and owning `PHASE-NN`.
  - `### Migration plan and rollback`: When local storage keys or cache schemas change (expand → migrate → contract steps, backward compatibility, and rollback check).
