# 02 — Flutter codebase scan for Planning

Planning runs this checklist during readiness and gap analysis (core `planning-and-task-breakdown`, reference 01) before writing tasks for a Flutter Client.

1. **Core packages (BaseScreen, use cases, paging, DataState, ApiService, UI kit)**:
   - Read the approved profile via `{{slot:core-usage}}`: iMESPro runs setup and reads package guides; external-structured inspects Client mappings; external-standard inspects only needed framework/project APIs.
   - Only an iMESPro setup failure blocks on company dependencies. External profiles never run company setup or require its GUIDE files. Do not invent required missing APIs.
2. **Routing & Screen Registry**:
   - Check the Client's router configuration.
   - If route definition is missing for the new screen, plan a task to register it before screen assembly.
3. **State Management & DI**:
   - Verify active state management (Bloc/Cubit) and DI (`get_it`, `Provider`).
4. **Reuse before build**:
   - For each need, decide with `{{slot:core-usage}}`: reuse a fitting core API, else the target module, else a Client shared folder when two or more modules need it. Record every gap in the `Core usage` table.
5. **Remote data**: in `lib/`, always implement the real `RemoteDataSource` calling `ApiService` (`ApiConfig.domain`) — never create fake `Mock<Feature>DataSource` classes in `lib/`.
6. **Screen work in the plan**: include affected screen/registry/route paths and the Client analyzer (`flutter analyze`) plus applicable tracking and portrait/landscape checks. A missing active base-screen API blocks the phase.
