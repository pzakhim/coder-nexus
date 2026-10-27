# External Structured Root-Cause Debugging Contracts

> Topic: Debugging against the client's lib/core/ network interceptors, result wrappers, and state holders (external-structured profile)

## 1. Layer-by-Layer Fault Isolation (`external-structured`)

Before bisecting a defect, inspect `lib/core/` (or `lib/shared/`) to identify the project's existing base abstractions:

| Boundary Check | What to Inspect | Common Root Causes |
|---|---|---|
| **Presentation (`Cubit` / `Bloc` / `Notifier` / Screen)** | State equality (`Equatable`, `@freezed`, or `==`); listener/builder rebuild conditions; route parameters | State mutated in-place instead of `copyWith` emitting a new instance; missing `if (!context.mounted) return;` after async gap |
| **Domain (UseCases / Services / Entities)** | Input validation and domain invariants; orchestration across multiple repositories | Partial state update when the second repository call fails without rollback or failure propagation |
| **Data (Repositories / Mappers / DTOs)** | Mapping between `lib/core/` network exceptions and project `Result<T>` / `Either<Failure, T>` types; DTO `fromJson` | Catch-all `catch (_)` returning a generic or empty success instead of mapping the failure; stale generated `.g.dart` / `.freezed.dart` |
| **Core Infrastructure (`lib/core/`)** | HTTP interceptors (auth token refresh, error transformation), local cache/storage adapters, DI registrations | Auth refresh interceptor swallowing non-401 errors; singleton vs factory DI registration holding stale state across logouts |

---

## 2. Inspecting Generated Code (`build_runner`)

When a serialization or state equality bug appears in a project using `freezed` or `json_serializable`:
1. Compare the `.dart` source fields against the generated `.g.dart` / `.freezed.dart` file.
2. Check if a field was added or renamed without re-running `dart run build_runner build --delete-conflicting-outputs`.
3. Never hand-edit `.g.dart` or `.freezed.dart` files to fix a bug—fix the source annotation and regenerate.

---

## 3. Core Infrastructure Escalation (`lib/core/`)

- If bisection traces the root cause to a shared `lib/core/` interceptor, base class, or DI module used across multiple features:
  - Check blast radius across all callers (`git grep <Symbol>`).
  - If fixing `lib/core/` changes behavior for other modules or exceeds 3 files (H5), stop and escalate with the Root-Cause Report.
