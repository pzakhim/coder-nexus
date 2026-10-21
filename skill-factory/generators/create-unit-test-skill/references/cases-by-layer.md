# Required cases by layer

Starting points for `01-what-to-test.md`. Map them onto the workspace's real layers (its clean-architecture skill, if present). "Double" = what the test replaces.

## Backend

| Layer / subject | Double | Required cases |
|---|---|---|
| Domain entity / value object / pure rule | none | Valid construction; each invariant violation raises the named error; boundary values; state transitions allowed and refused |
| Use case / application service | Fakes of its ports (repository, UoW, external services) | Success returns the expected DTO and persists via the port; each handled failure (not found, forbidden by capability guard, conflict/invariant, dependency failure) raises the right error; transaction committed on success and **not** committed on failure; guard called with the right scope |
| Mapper (ORM row ↔ entity ↔ DTO) | none | Full mapping; optional/null fields; empty collections; enum/unknown values |
| Repository / query (SQL) | — | **Integration test** on a real DB, not a unit test (U6, U13) |
| Router / controller | Use case doubled | Request validation errors (400/422); success response shape; domain errors reach the global handler (no local remapping) — or leave HTTP to integration tests if the workspace does |
| External adapter (HTTP client, LLM, ERP) | Transport doubled (`httpx` mock transport, fake server) | Parses success; maps each error status/timeout to the port's error contract |

## Frontend

| Layer / subject | Double | Required cases |
|---|---|---|
| Pure util (parse, validate, format, map) | none | Valid input; empty/null/missing; malformed; boundary values; round-trip where relevant |
| State reducer / store / URL serializer | none | Each action/transition; invalid action; initial state |
| Hook / composable | API client or fetch doubled | Loading → success; loading → error with retry; empty result; scope change mid-request ignores the stale response |
| Component (if the workspace unit-tests components) | Hooks/API doubled | Renders each UI state (loading, empty, error, populated); permission-driven visibility from capabilities; user event triggers the right callback |
| Capability/permission mapper | none | Each role/capability combination; unknown role |

## Mobile (Flutter)

| Layer / subject | Double | Required cases |
|---|---|---|
| Use case | Repository interface (`mocktail`) | Success → expected entity; failure → failure propagated; repository called with exact parameters |
| Model / mapper | none | `fromJson` valid; nulls/empty lists/type variations; `toJson`; `toEntity` |
| Remote / local data source | HTTP client (`MockDio`…) | 200/201 parsed; 400/401/404/500 → `ServerException`; timeout/socket → `NetworkException` |
| Cubit / Bloc / Notifier | Use cases | Initial state; `[loading, success]`; `[loading, error(message)]`; validation error without calling the use case |

## Everywhere

- Each test name states the behavior and the condition.
- One focused file per subject, mirroring its source path.
