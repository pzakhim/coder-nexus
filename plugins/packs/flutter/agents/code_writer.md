---
skills:
  - {{slot:core-usage}}
---
## Flutter rules

### Flutter Architecture & Screen Rules
Execute according to `architecture_profile.mode` specified in `design.md`:

1. **Mode 1 (`imespro`) — Core-First & Company Knowledge Preservation**:
   - Apply `{{slot:core-usage}}` and `references/01_profile_imespro.md`. Setup gate: `coder-nexus setup flutter --check` must be `READY`. Read relevant sections of `../app-*/guidance/GUIDE.md`, inspect `examples/`, and view `lib/*.dart` for signatures. Implement against approved `Core usage` table in `design.md`.
   - Use exactly the core APIs the table marks as reused. Build in the Client only what it records as a gap. Never edit, format, or copy files in `../app-*`.
   - Strict import boundaries: Domain is pure Dart (deep domain imports only: `package:app_core/domain/...`, `package:app_util/domain/...`, no Flutter, no barrel). Data and Presentation use package barrels (`package:app_core/app_core.dart`, `package:app_util/app_util.dart`, `package:app_ui_kit/app_ui_kit.dart`).
   - Route screens live in `presentation/screens/*_screen.dart`, extend `BaseScreen`/`BaseScreenState`, override `getScreen()`, `createState()`, `buildMobilePortrait()`, and never override `build()`.
   - Mandatory UI Kit widgets: `AppButton`, `AppFormField`, `AppDialog`, `AppLoadingIndicator`, `AppNoData`, `ListViewPaging`. Prohibit raw Material buttons/inputs when UI kit covers them.

2. **Mode 2 (`external-structured`) — Pattern Matching & Client Core Reuse**:
   - Apply `{{slot:core-usage}}` and `references/02_profile_external_structured.md`. Read client's base files in `lib/core/` and `lib/shared/` per the `Client Core Mapping` table in `design.md`.
   - Inherit client's existing base classes (e.g. `BasePage`/`BaseScreen`, custom network wrapper, shared UI widgets).
   - Prohibit creating duplicate competing base classes. Follow the existing Client feature layout recorded in design.

3. **Mode 3 (`external-standard`) — Minimalist Clean Architecture**:
   - Apply `{{slot:core-usage}}` and `references/03_profile_external_standard.md`. Follow Ponytail minimalism (smallest clear solution, no speculative layers).
   - Keep feature code together and create only the Domain/Data/Presentation responsibilities actually needed; no empty layers or mandatory Cubit/DI dependencies.
   - Construct clean standard Flutter widgets (`StatefulWidget`/`StatelessWidget`, `ElevatedButton`, `TextFormField`) under the approved screen/widget paths.

- **Data layer**: In the Flutter Client (`lib/`), implement only the real **`RemoteDataSource`** calling `ApiService`; **never** create fake `Mock<Feature>DataSource` classes inside `lib/`.
- **Mapping under `external-standard`**: there is no mapping and standard Flutter widgets are correct.
- **No screen-contract bypass**: route screens follow the approved profile's screen contract (`imespro`: `BaseScreen`/`BaseScreenState`, `buildMobilePortrait()`, never `build()`).
- **No construction in UI**: UI classes never construct data sources, repositories or use cases.
- **Unit tests**: For every domain usecase, data model/mapper, remote data source, and cubit state machine implemented in the assigned phase (`PHASE-01+`), create corresponding unit test files under `test/modules/<feature>/..._test.dart`.
- **Local Self-Verification**: For `PHASE-01+`, run `dart format` (or project linter), `flutter analyze`, and `flutter test test/modules/<feature>/` via `run_command`.
