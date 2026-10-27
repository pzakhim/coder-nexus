# External Structured Architecture Design Contracts

> Topic: Discovering client lib/core/ and lib/shared/ foundations and authoring the Client Core Mapping table (external-structured profile)

## 1. Activation & Codebase Foundation Discovery (`external-structured`)

This profile applies when the Flutter Client does not use `imespro` packages (`app_core`, `app_util`, `app_ui_kit`) but already has an established foundation under `lib/core/`, `lib/shared/`, `lib/common/`, or internal workspace packages with real consumers.

Before drafting `design.md`, catalog the Client's existing foundation assets in `codebase-notes.md` (`## 3. Verified Baseline Facts`):

| Foundation Layer | What to Discover in the Client | What to Record in `Client Core Mapping` (`design.md`) |
|---|---|---|
| **Screen & Scaffold Base** | `BasePage`, `BaseScreen`, `BaseView`, responsive layout wrappers, or analytics mixins | Exact base class and lifecycle hooks to inherit for new screens |
| **State Management & DI** | `Bloc`, `Cubit`, `Riverpod`, `Provider`, `ChangeNotifier`, `GetIt` / `injectable` setup (`lib/injection.dart`, `lib/core/di/`) | State pattern (`@freezed` vs `Equatable`) and DI registration entry point |
| **Network & Result Types** | Shared `Dio` / HTTP client (`lib/core/network/`), auth interceptors, result wrappers (`Either<Failure, T>`, `Result<T>`, `ApiResponse<T>`) | Exact network client, error mapper, and result type returned by repositories |
| **Shared UI Kit & Tokens** | Reusable buttons, inputs, loaders, empty/error views, dialogs, and theme tokens under `lib/shared/` or `lib/core/widgets/` | Exact shared widget classes and props mapped to the 4 mandatory visual states |

---

## 2. Non-Fragmentation Rule (Zero Competing Bases)

- **Always reuse the Client's established base classes and result wrappers.**
- **Prohibited:** Never introduce a parallel base architecture (do not invent a second `Result` class, a new `BaseScreen`, or copy `imespro` classes into `lib/core/`).
- Document every mapped foundation class in the `## Foundation reuse (Client Core Mapping)` table of `design.md`, and record any missing capability as a module-local component under `lib/modules/<feature>/` (promoting to `lib/shared/` only when 2+ features share it).
