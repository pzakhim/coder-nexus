# 02 — Flutter codebase scan for Planning

Planning runs this checklist during readiness and gap analysis (core `implementation-planning`, reference 01) before writing tasks for a Flutter Client.

1. **Core packages & developer tools (BaseScreen, use cases, paging, DataState, ApiService, UI kit, linters, test/mock tools)**:
   - Read the approved profile via `{{slot:core-package-usage}}`: iMESPro runs `coder-nexus setup flutter --check` and reads package guides; external-structured inspects Client mappings; external-standard inspects only needed framework/project APIs.
   - Check developer tools across all profiles with `coder-nexus setup tools --pack flutter --check` (ensuring `very_good_analysis`, `dart_code_linter`, `mocktail`, `bloc_test`, `ripgrep`, and `mockoon-cli` are ready; install missing tools via `coder-nexus setup tools --pack flutter -y`).
   - Only an iMESPro setup failure blocks on company dependencies. External profiles never run company setup or require its GUIDE files. Do not invent required missing APIs.
2. **Routing & Screen Registry**:
   - Check the Client's router configuration.
   - If route definition is missing for the new screen, plan a task to register it before screen assembly.
3. **State Management & DI**:
   - Verify active state management (Bloc/Cubit) and DI (`get_it`, `Provider`).
4. **Reuse before build**:
   - For each need, decide with `{{slot:core-package-usage}}`: reuse a fitting core API, else the target module, else a Client shared folder when two or more modules need it. Record every gap in the `Core usage` table.
5. **Remote data**: in `lib/`, always implement the real `RemoteDataSource` calling `ApiService` (`ApiConfig.domain`) — never create fake `Mock<Feature>DataSource` classes in `lib/`.
6. **Screen work in the plan**: include affected screen/registry/route paths and the Client analyzer (`flutter analyze`) plus applicable tracking and portrait/landscape checks. A missing active base-screen API blocks the phase.
