# 05 — Backend API Contract and Mock Strategy

Use the approved profile’s network, auth, pagination and error conventions. The app_util/app_core pipeline, `ApiConfig.domain`, ApiService refresh and `pagination.total` examples below apply only to iMESPro APIs that actually fit; external profiles use verified Client/standard contracts.


Read plugin-root `shared_contracts/api_handshake_protocol.md`. Only explicitly approved contract-derived development fixtures may support UI/contract checks. Record fixture provenance and contract revision separately from live integration evidence. Required live ACs remain `BLOCKED` or `NOT_RUN` until exercised against the real endpoint; fixture success cannot close the handshake or imply overall feature acceptance. Never fabricate business records, Huly data, services or production success fallbacks.


Guide for the `Backend API Contract & Mock Strategy` block of `design.md`.

The Frontend never changes Backend code. The design records the contract the Client will consume, how data flows through the Client, and how a mock is swapped for the real API.

## 1. Contract status (Does the feature use external BE APIs?)

| Status | Meaning | Source to cite & `PHASE-00` mode |
|---|---|---|
| `BE_API_READY` | BE API exists and specification is provided | Huly BE task / Swagger / OpenAPI / user-provided API spec. Consolidated in `PHASE-00` as **`[INFO_NOTE]`** (or `[EXECUTE]` if a live endpoint probe is needed) with explicit verification status against user spec. |
| `MOCKOON_MOCKED` | BE API does not exist yet (or is missing endpoints); user confirmed using Mockoon | Business API contract approved at Gate 1 (`requirements.md`) + **`Mockoon Trigger & Test Data Table`** agreed with user at Gate 2 (`design.md`). Executed in **`PHASE-00` (`[EXECUTE]`)** before `PHASE-01`. |
| `NONE` | Feature is UI-only or local-only without external BE API calls | Omit the external API section from `design.md` and `PHASE-00`. |

Never invent an endpoint or payload. A missing source is `BLOCKED`, not a guess.

## 2. Contract details (`BE_API_READY` & `MOCKOON_MOCKED`)

- **Endpoints**: method, path relative to `ApiConfig.domain` (never a hard-coded host), auth required or not, **verification status** (`Verified against User Spec` / `Mockoon Rule`), and the AC it serves.
- **Request body**: fields, types, required/optional.
- **Responses**: 200 payload plus the error payloads the UI must handle (400 validation, 401, 403, 500). 401 refresh is handled by `ApiService`; state only what the UI does after a refresh failure.
- **Pagination**: if the list is paged, confirm the response carries `pagination.total` (needed by `ListViewPaging` load-more).

## 3. Data pipeline (read the guides, then decide)

Whether `BE_API_READY` or `MOCKOON_MOCKED`, the Flutter Client `lib/` code **always** implements the real network pipeline (never create fake `Mock<Feature>DataSource` classes inside `lib/`):

```text
RemoteDataSource (BaseRemoteDataSource + ApiService)
  → Model.fromJson (parse_util) implements DataMapper<Entity>
  → RepoImpl: remote.call().tryCatch(handler: ...) → Future<DataState<Entity>>
  → UseCase (only if it adds a business rule or is shared) → Cubit → UI sees entities only
```

- Reuse each piece only when its GUIDE "Use when" matches. A single pass-through call may go Repo → Cubit without a use case if the Client convention allows it; say so.
- If the API does not fit the pipeline (stream/socket, file download, non-`ApiResponse` envelope), record a Core gap in `Core usage` and describe the Client-side adapter under `lib/modules/<feature>/data/`.
- Do not hide missing required fields behind defaults; validate them and fail with an explicit error.

## 4. Mockoon strategy & `Mockoon Trigger & Test Data Table` (`MOCKOON_MOCKED` only)

- **Agree on Pass/Default vs. Fail Data with User (`ask_question`)**: Before finalizing `design.md`, `planning` asks and confirms with the user which input values represent **Pass / Default (`200/201`)**, **Empty (`[]`)**, and **Fail (`400/401/403/500`)**.
- **Record the `Mockoon Trigger & Test Data Table` in `design.md`**:
  - Maps each scenario (`MOCK-01`, `MOCK-02`...) to its Endpoint, Input Trigger (`body` / `query` / `header`), Mockoon Rule (`target`, `modifier`, `operator`, `value`), HTTP Status & Latency, and exact Response JSON Body.
  - This table serves as the unified contract for:
    1. `code_writer` creating `mocks/<feature>_mockoon.json` in `PHASE-00` (`[EXECUTE]`) and writing isolated developer **Unit Tests** in `PHASE-01+`.
    2. `code_reviewer` auditing `mocks/<feature>_mockoon.json` in `PHASE-00` and grading Unit Test coverage in `PHASE-01+`.
- **Consolidate in `PHASE-00` (`phases/phase-00-prepare.md`)**: Mark `PHASE-00` as **`[EXECUTE]`**. Once `code_writer` creates `mocks/<feature>_mockoon.json`, starts `mockoon-cli`, and `code_reviewer` approves it, tick **`[x] PREPARED / COMPLETED`** so `PHASE-01, 02, 03...` have all data ready without getting stuck.
- **Live Cutover**: When BE delivers the real API, update `ApiConfig.domain` in `.env` to the BE server domain and verify actual auth/schema/error behavior per `shared_contracts/api_handshake_protocol.md`.
- If the delivered BE contract differs in schema, update `Model` / `Mapper` in a new version (`vN+1`); Domain and UI stay unchanged.

## 5. Prohibited

- Modifying BE repositories, databases, or server code.
- Creating fake `Mock<Feature>DataSource` classes or hard-coded mock fallbacks inside `lib/`.
- Storing tokens or secrets in Git; they belong in the Client `.env`.
- A feature-owned `http.Client` / Dio when `ApiService` fits.

## Output format

```markdown
### Backend API Contract & Mockoon Strategy
- **Status**: `MOCKOON_MOCKED` (or `BE_API_READY`) — source: requirements.md / user API spec
- **Endpoints & Verification Status**:

  | Method | Path (relative to `ApiConfig.domain`) | Auth | Spec Verification / Status | Purpose / AC |
  |---|---|---|---|---|
  | POST | `/api/v1/<feature>/<action>` | Bearer | `MOCKOON_MOCKED` (or `Verified against User Spec`) | <Action purpose> · AC-02 |

- **Mockoon Trigger & Test Data Table** *(when `MOCKOON_MOCKED` — agreed with User for Mockoon rules & Unit Tests)*:

  | Scenario ID | Case (Pass / Fail / Empty) | Endpoint | Input Trigger (Request `body` / `query` / `header`) | Mockoon Rule | HTTP Status & Latency | Response JSON Body |
  |---|---|---|---|---|---|---|
  | `MOCK-01` | Pass / Default | `POST /api/v1/<feature>/<action>` | `body.<field_a> == "<valid_value>"` (default) | Default response (or `body.<field_a> equals <valid_value>`) | `200 OK` (300ms) | `{"result": true, "data": {"<id_field>": "<id_1>"}}` |
  | `MOCK-02` | Fail (Validation / Auth) | `POST /api/v1/<feature>/<action>` | `body.<field_a> == "<invalid_value>"` | `body` · `<field_a>` · `equals` · `<invalid_value>` | `400` / `401` (200ms) | `{"result": false, "message": "<error_message>"}` |
  | `MOCK-03` | Fail (Server Error) | `POST /api/v1/<feature>/<action>` | `body.<field_a> == "error_500"` | `body` · `<field_a>` · `equals` · `error_500` | `500` (200ms) | `{"result": false, "message": "Internal Server Error"}` |

- **Data pipeline**: `<Feature>RemoteDataSource` → `<Feature>Model` (parse_util) → `<Feature>RepoImpl.tryCatch` → `DataState<<Feature>Entity>` → `<Feature>Cubit`.
- **`PHASE-00` consolidation & cutover plan**: Prepared in `PHASE-00` (`phases/phase-00-prepare.md`) and ticked `[x] PREPARED / COMPLETED`; switch `ApiConfig.domain` in `.env` to live BE domain when BE ships.
```
