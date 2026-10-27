# External Structured Code Review Contracts

> Topic: Reviewing against the client's lib/core/ foundations, Client Core Mapping table, and external-structured Hub validator profile (external-structured profile)

## 1. `external-structured` Hub Validator & Mapping Audit

Always pass `architecture_profile: "external-structured"` to `validate_architecture_code` and `validate_module_architecture`. Company-specific rules (`DAT-001`, `DAT-002`, `PRE-002`, `PRE-004`, `PRE-006`, `STY-001`) are not enforced by the Hub validator in this mode; instead, the Reviewer verifies compliance against the project's own `lib/core/` (or `lib/shared/`) foundations recorded in `design.md`:

| Audit Area | What to Verify Against `Client Core Mapping` (`design.md`) | Violation Severity |
|---|---|---|
| **Network & Result Wrappers** | Data sources and repositories use the client's existing HTTP client/interceptor (`Dio` wrapper) and result type (`Either<Failure, T>`, `Result<T>`, or custom sealed result) rather than inventing a parallel error wrapper | `BLOCKER` |
| **State Management & Screen Base** | Presentation classes follow the client's established state holder (`Bloc`, `Cubit`, `Riverpod`, `Notifier`) and screen/scaffold wrapper convention used by sibling modules | `MAJOR` |
| **Shared UI Components** | Reuses the client's design system widgets mapped in `design.md` before building one-off module widgets | `MAJOR` |
| **Codegen Consistency (`build_runner`)** | When `@freezed`, `@JsonSerializable`, or `@injectable` classes are modified, verify `.freezed.dart` / `.g.dart` / `.config.dart` files are regenerated and committed in sync, and `flutter analyze` passes cleanly | `BLOCKER` |
