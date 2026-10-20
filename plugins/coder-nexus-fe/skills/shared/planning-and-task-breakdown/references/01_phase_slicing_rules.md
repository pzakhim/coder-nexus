# 01 — Phase Slicing and Dependency Order

Guide for Phase Order and task breakdown in `implement-plan.md`.

## 1. A phase is a thin vertical slice

A phase delivers one behavior a user (or a test) can observe end to end. It cuts through every layer the behavior needs, and only as much of each layer as that behavior needs.

**Self-check before writing a phase:** *"When this phase is done, what can I run or show that I could not before?"* If the answer is "a class exists" or "a layer is done", it is a horizontal slice — re-cut it.

### Wrong (horizontal)

| Phase | Content | Observable? |
|---|---|---|
| 01 | Entities, repository contract, use cases | No |
| 02 | Models, data source, repo impl, mocks | No |
| 03 | Cubit, screen, widgets | Only now |

### Right (`PHASE-00` Prepare Phase + Vertical Behavior Phases)

| Phase | Mode (`[EXECUTE]` vs `[INFO_NOTE]`) | Behavior / Consolidation | Layers / Files touched |
|---|---|---|---|
| `PHASE-00` (`phase-00-prepare.md`) | **`[EXECUTE]`** (if `MOCKOON_MOCKED`) or **`[INFO_NOTE]`** (if `BE_API_READY` / no API) | Consolidate Huly context (fetched once) + API specs. If `MOCKOON_MOCKED`, create & verify `mocks/<feature>_mockoon.json` (Pass/Default & Fail rules). If `BE_API_READY`, record verified BE API notes. Tick **`[x] PREPARED / COMPLETED`** when ready. | `phases/phase-00-prepare.md`, `mocks/<feature>_mockoon.json` (if `MOCKOON_MOCKED`) |
| `PHASE-01` | `[EXECUTE]` | Open the screen and see the `<feature>` list (Loading → Content) | Entity + repo contract + `RemoteDataSource`/model/repo impl for the list call + Cubit/`ListViewPaging` + screen + route + DI |
| `PHASE-02` | `[EXECUTE]` | Empty and error states with retry | Cubit state + screen states; no new data code |
| `PHASE-03` | `[EXECUTE]` | Tap an item → detail screen | Detail call through all layers + new screen + route |
| `PHASE-04` | `[EXECUTE]` | Submit form action with validation errors | Write call + request model + form widgets + Cubit action |

`PHASE-00` consolidates all external context/API readiness in one place, and `PHASE-01` is the "walking skeleton": thin but complete from API (or Mockoon HTTP server) to pixels. Later phases widen it.

## 2. Rules

- **`PHASE-00` (`phases/phase-00-prepare.md`) Single Source & Readiness Tick**:
  - Consolidates all Huly context (fetched once) and external API details so downstream agents (`code_writer`, `code_reviewer`, `test_runner`) read only from `PHASE-00` and `design.md` without hunting for scattered information.
  - **`MOCKOON_MOCKED` (`[EXECUTE]`)**: `PHASE-00` includes executable tasks to create `mocks/<feature>_mockoon.json` (implementing all Pass/Default, Empty, and Fail rules from the `Mockoon Trigger & Test Data Table` in `design.md`) and verify `mockoon-cli`. Once `code_writer` finishes and `code_reviewer` approves `PHASE-00`, tick **`[x] PREPARED / COMPLETED`** in `phase-00-prepare.md` and `implement-plan.md`. Never create fake `Mock<Feature>DataSource` classes in `lib/`.
  - **`BE_API_READY` (`[INFO_NOTE]`)**: `PHASE-00` summarizes the existing BE APIs, whether they have been verified, and whether they match the user-supplied spec, pre-ticking **`[x] PREPARED (INFO_READY)`**.
  - **No External API (`[INFO_NOTE]`)**: Omit the API section in `PHASE-00` and pre-tick **`[x] PREPARED (NO_EXTERNAL_API)`**.
- **Readiness Gate for `PHASE-01, 02, 03...`**: Feature phases (`PHASE-01`+) only start once `PHASE-00` is ticked **`[x] PREPARED / COMPLETED`**, guaranteeing all data and API contracts are ready so `code_writer` never gets stuck.
- Every phase file lists **only** the files that behavior needs. No placeholder classes or empty DI entries for later phases.
- Shared pieces (an entity, a DI file) belong to the first phase that needs them; later phases extend them.
- UI-only phases (layout, a new state) are valid vertical slices — they need no Domain/Data work.
- **Strict Sequential Phase Order**: Phases run one by one in sequence (`PHASE-00` $\to$ `PHASE-01` $\to$ `PHASE-02` $\to$ ...). Each phase's verified output serves as the foundation and input for the next phase.

## 3. Phase file contract

- Path: `phases/phase-NN-<behavior-slug>.md`, ID `PHASE-NN`.
- `Behavior`: one sentence, user-observable.
- `Files`: create / modify / reuse, each tied to the behavior.
- `READY when` and `Done when`: concrete, checkable.
- `Verification`: real Flutter/Dart commands (`flutter analyze`, the phase's tests).

## 4. Ordered Task Breakdown Within a Phase (Single `code_writer` Execution)

Inside each Phase file, the `## Tasks` section lists the ordered micro-tasks that a single `code_writer` executes sequentially from top to bottom (e.g., Domain $\to$ Data $\to$ Cubit/State $\to$ Screen/Widgets & Route/DI $\to$ Unit Tests). Do **not** split tasks into `[PARALLEL]` / `[SEQUENTIAL]` tracks or `Join points`.

1. **Task Specification Standard**:
   Every task entry MUST follow this exact 4-field format:
   ```markdown
   - [ ] **Task X.Y**: <Clear Actionable Name>
     - **Scope / Files**: `lib/modules/.../file.dart`
     - **Reused Components**: the entries from the design's `Core usage` / `Client Core Mapping` table this task must use (or `standard Flutter` for external-standard)
     - **Produces**: public symbols/signatures later tasks consume (or `none`)
     - **Acceptance Criteria**: Command or condition to verify this task immediately (e.g. `flutter analyze lib/modules/...`, unit test pass)
   ```
2. **Execution & Plan Re-Grounding Rule (Anti-Bulk Coding)**:
   - Each task requires all preceding tasks in the phase to be marked `- [x]` before starting.
   - **Mandatory Re-Reading of Plan Between Tasks**:
     * After completing each task's verification, `code_writer` MUST return to the phase file (`phase-NN-*.md`).
     * Mark the completed task `- [x]`.
     * Re-read the phase plan: inspect the scope, required reuse components, and acceptance criteria of the next task before touching any code.
     * Prohibit "blind coding runs": executing multiple tasks in one unverified pass causes context drift and logic breakage.
