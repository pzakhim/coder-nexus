# Clean Architecture Rule Source Matrix

Pass the approved `architecture_profile` to both validators. Omitted values retain legacy iMESPro behavior. `DAT-001`, `DAT-002`, `PRE-002`, `PRE-004`, `PRE-005`, `PRE-006` and `STY-001` apply only to iMESPro. External module validation does not enforce company folder/DI conventions; verify those against the approved Client mapping and record missing evidence as `UNVERIFIED` or `BLOCKED`.


This matrix maps FastMCP lexical checks to their source and practical limits. `valid: true` covers only executed lexical checks; it does not prove compile, integration or user approval.

| Rule | Layer | Severity | Source | Hub check |
|---|---|---|---|---|
| `DOM-001` Domain No Flutter | Domain | ERROR | Clean Architecture guide | Reject Flutter imports. |
| `DOM-002` Domain Independence | Domain | ERROR | Clean Architecture guide | Reject Data/Presentation imports. |
| `DOM-003` Entity Immutability | Domain | WARNING | Clean Architecture guide | Inspect mutable entity fields. |
| `DAT-001` BaseDataSource | Data | ERROR/WARNING | API and Data rules | Direct missing base is error; indirect inheritance needs Client verification. |
| `DAT-002` Repo TryCatch/DataState | Data | ERROR | API and Data rules | Inspect applicable RepoImpl methods. |
| `DAT-003` Safe DTO Parsing | Data | WARNING | API and Data rules | Flag unsafe raw casts. |
| `PRE-001` No Throw in UI | Presentation | ERROR | Senior AGENTS | Flag direct UI throws. |
| `PRE-002` State Pattern | Presentation | WARNING | State rules | State matches the Client convention used by sibling modules; no invented state base. |
| `PRE-003` Resource Disposal | Presentation | WARNING | Lifecycle review | Inspect resources owned by a State. |
| `PRE-004` UI Kit Reuse | Presentation | INFO | Catalog | Prompt source-backed component review. |
| `PRE-005` Screen Naming | Presentation | ERROR | Screen contract | Flag `*Page` screen classes; paths require module validation. |
| `PRE-006` BaseScreen | Presentation | ERROR/WARNING | Screen contract | Flag obvious direct Flutter widget inheritance; indirect inheritance, hooks and active package need Client verification. |
| `MOD-006` Screen Paths | Module | ERROR/WARNING | Screen contract | Flag screen files outside `presentation/screens/*_screen.dart`; warn on legacy `pages/` awaiting approved scope. |
| `DIR-001` Cubit Lifetime | Core/module | UNVERIFIED | DI rules | Client confirms screen factory or approved singleton. |
| `STY-001` AppLogger | All | WARNING | Dart style | Flag uncontrolled print calls. |
| `RTE-001` Route Annotation | Presentation | INFO | Routing rules | Inspect annotation ownership. |

## Boundaries

`validate_architecture_code` sees only the Dart file supplied by the Client. It reports unsupported cross-file checks in `unsupported_checks`. The Client must inspect imports, actual package resolution, DI and router integration, then run the analyzer on the same revision. `gate_status: FAILED` blocks review; `gate_status: UNVERIFIED` requires those Client checks before PASS.

Neither validator proves screen analytics events or portrait/landscape rendering. Those require Client runtime evidence on the reviewed revision when affected.
