---
skills:
  - {{slot:core-package-usage}}
---
## Flutter rules

### Flutter Architecture & Screen Rules
Apply the Code Writer rules of `{{slot:core-package-usage}}` for the `architecture_profile.mode` in `design.md`, with that profile's reference (`references/01_profile_imespro.md`, `02_profile_external_structured.md` or `03_profile_external_standard.md`). On top of the skill:

- **`imespro`**: `coder-nexus setup flutter --check` must be `READY`. Read the relevant `../app-*/guidance/GUIDE.md` sections, `examples/` and `lib/*.dart` signatures. Use exactly the core APIs the `Core usage` table marks as reused and build in the Client only what it records as a gap; never edit, format or copy files in `../app-*`. Route screens live in `presentation/screens/*_screen.dart`. Use a UI Kit widget (`AppButton`, `AppFormField`, `AppDialog`, `AppLoadingIndicator`, `AppNoData`, `ListViewPaging`) when its GUIDE "Use when" fits the approved need; never a raw Material button or input where a fitting UI Kit widget exists.
- **`external-structured`**: read the Client's base files in `lib/core/` and `lib/shared/` per the `Client Core Mapping` table and follow the existing feature layout recorded in design.
- **`external-standard`**: keep feature code together and create only the Domain/Data/Presentation responsibilities actually needed, with no empty layers or mandatory Cubit/DI dependencies. There is no mapping; standard Flutter widgets are correct.

- **Data layer**: In the Flutter Client (`lib/`), implement only the real **`RemoteDataSource`** calling `ApiService` (`ApiConfig.domain` pointed to the BE server or local Mockoon server in `.env`); **never** create fake `Mock<Feature>DataSource` classes inside `lib/`. When BE delivers the real API, point `ApiConfig.domain` / `.env` to the live server.
- **Unit tests**: For every domain usecase, data model/mapper, remote data source, and cubit state machine implemented in the assigned phase (`PHASE-01+`), create corresponding unit test files under `test/modules/<feature>/..._test.dart`.
- **Local Self-Verification**: For `PHASE-01+`, run `dart format` (or project linter), `flutter analyze`, and `flutter test test/modules/<feature>/` via `run_command`.
