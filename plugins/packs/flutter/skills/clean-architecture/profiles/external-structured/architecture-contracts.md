# External-Structured Architecture Contracts

> Topic: Mapping Clean Architecture layers (`domain/`, `data/`, `presentation/`, DI) to an existing structured Client's `lib/core/` and `lib/shared/` foundations.

---

## 1. Client Core Mapping Authority

Under the `external-structured` profile, the Client workspace owns its foundational abstractions under `lib/core/`, `lib/shared/`, or `lib/commons/`. Do not import or assume `iMESPro` packages (`app_core`, `app_util`, `app_ui_kit`).

Before writing or reviewing module code, inspect `design.md` (`## Client Core Mapping`) and verify the real Client source for each layer contract:

| Architectural Need | How to Resolve in `external-structured` |
|---|---|
| **Domain Result & Error Contract** | Inspect sibling modules' `domain/repo/` to identify the project's result wrapper (e.g., `Either<Failure, T>`, `Result<T>`, or typed custom exceptions). Keep `domain/` 100% pure Dart. |
| **Base DataSource & Network Stack** | Reuse the Client's existing HTTP client wrapper (`Dio` / `HttpClient` service in `lib/core/network/`) and endpoint configuration table. |
| **Mapper & DTO Strategy** | Follow the Client's established DTO/Mapper pattern (`json_serializable`, `freezed`, or manual `fromJson` with explicit mandatory-field checks). |
| **Screen Superclass & Routing** | Inspect existing screens in `presentation/screens/`. If the Client defines a shared screen base class or route wrapper (`AutoRouteWrapper`, `GoRouter` builder), follow it consistently; otherwise use standard `StatelessWidget`/`StatefulWidget` named `*Screen` in `*_screen.dart`. |
| **State Management & DI** | Match the Client's existing state holder (`Cubit`, `Bloc`, `Riverpod`, etc.) and DI registration order in `di.dart` / `modules_di.dart`. |
