---
name: core-usage
description: Multi-profile Flutter architecture & core foundation skill. Routes agents across iMESPro Core packages, External Structured client core, and External Standard minimalist architectures.
---

# Core Foundation & Architecture Usage (Multi-Profile)

This skill governs how agents (**Planning**, **Code Writer**, **Code Reviewer**, and **Test Runner**) discover, inspect, and reuse foundation libraries, design systems, and base architectures across different project environments.

The primary objective is **Knowledge Preservation & Zero Reinvention**:
- In internal company projects, never lose or reinvent the company's shared assets (`app-core`, `app-util`, `app-ui-kit`).
- In structured external projects, discover and reuse the client's existing architectural bases and design tokens.
- In standard/vanilla projects, build minimal, idiomatic, feature-first Clean Architecture without speculative bloat.

---

## 1. The 3 Architecture Profiles

Planning resolves the project's **Architecture Profile** once; downstream agents read the approved selection:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURE PROFILE MATRIX                     │
├─────────────────────┬──────────────────────────┬───────────────────────┤
│ Profile 1: imespro  │ Profile 2: external-     │ Profile 3: external-  │
│                     │            structured    │            standard   │
├─────────────────────┼──────────────────────────┼───────────────────────┤
│ • Sibling packages: │ • External project with  │ • External vanilla    │
│   app-core,         │   its own established    │   Flutter project     │
│   app-util,         │   lib/core/, lib/shared/ │ • No pre-existing     │
│   app-ui-kit        │   or base classes        │   central core        │
│ • "Core-First &     │ • "Pattern Matching &    │ • "Ponytail Minimalist│
│   Zero Duplication" │   Reuse Client Bases"    │   Clean Architecture" │
│ • Ref: [01_profile] │ • Ref: [02_profile]      │ • Ref: [03_profile]   │
└─────────────────────┴──────────────────────────┴───────────────────────┘
```

Detailed profile guidelines:
- [Profile 1: iMESPro Core System (Internal)](references/01_profile_imespro.md)
- [Profile 2: External Structured Core System](references/02_profile_external_structured.md)
- [Profile 3: External Standard (Vanilla / Minimalist)](references/03_profile_external_standard.md)

---

## 2. Gate & Profile Resolution Protocol

### Step 1: Resolve once from Client evidence
1. Honor an explicit user/workspace selection and the existing approved `architecture_profile` in `design.md`. For phase-free work, record it in `brief.md`. Do not silently change it during implementation or review; changed evidence goes back to Planning and the affected approval gate.
2. Without an approved choice, inspect the Client's `pubspec.yaml`, resolved dependency configuration, imports and actual consumers:
   - `imespro`: the Client uses company foundations (`app_core`, `app_util`, `app_ui_kit`), or the user explicitly selects them for a new project. Neighboring `../app-*` directories are discovery hints only; their existence never selects this profile.
   - `external-structured`: the Client has established foundations/design tokens with real consumers. An empty `core/`, `shared/` or `common/` directory alone is not evidence.
   - `external-standard`: the Client has no established foundation to reuse.
3. Record `mode`, `core_source`, evidence paths and selection rationale in the design. Resolve genuine ambiguity with the user; do not downgrade a broken iMESPro dependency to external to bypass setup.
4. Only for `imespro`, run `coder-nexus setup flutter --check` in the Client root. `STATUS: READY` permits proceeding; otherwise report `BLOCKED` and the required setup repair. External profiles never run company setup or require company GUIDE files.

### Shared skill dispatch
Shared skills define the job; these profile references define foundation policy. Company examples/templates in Clean Architecture, design, unit testing and UI references apply only to `imespro`. External structured work uses the approved Client Core Mapping; external standard work uses standard Flutter and only necessary layers. Never introduce `BaseScreen`, `DataState`, `ApiService`, `AppLogger`, `Equatable`, Cubit or a DI library solely because a company example mentions it.

Pass the exact approved `mode` as `architecture_profile` to **both** `validate_architecture_code` and `validate_module_architecture`. Their omitted argument defaults to `imespro` for legacy callers; agents must not omit it. External results cannot prove Client-specific conventions: Reviewer must inspect the approved mapping and resolved source, with analyzer/runtime evidence. `UNVERIFIED` is not `PASS`.

---

## 3. Knowledge Access & Reading Rules

1. **Profile 1 (`imespro`):**
   - Read `../app-core/guidance/GUIDE.md`, `../app-util/guidance/GUIDE.md`, and `../app-ui-kit/guidance/GUIDE.md`.
   - Read pattern implementations in `../app-*/guidance/examples/`.
   - Read source files in `../app-*/lib/` to confirm signatures and parameters (**Source wins** over guide).
   - **Never edit or copy files from `../app-*` into the Client.**
2. **Profile 2 (`external-structured`):**
   - Read client's base files in `lib/core/` and `lib/shared/`.
   - Read existing feature implementations to understand client naming and structure conventions.
3. **Profile 3 (`external-standard`):**
   - Rely on standard Flutter SDK documentation and clean code principles.

---

## 4. Role Playbook Across All 4 Agents

### Planning (Tech Lead)
- Determine and record the profile in `design.md`:
  ```yaml
  architecture_profile:
    mode: imespro | external-structured | external-standard
    core_source: "../app-*" | "lib/core/" | "none"
    evidence: ["actual Client dependency/base/consumer paths"]
  ```
- **If `imespro`:** Fill the `Core usage` table mapping every feature need to `app-core`, `app-util`, `app-ui-kit`. Any unmapped need must be an explicit, justified `Core gap`.
- **If `external-structured`:** Fill the `Client Core Mapping` table mapping needs to the client's existing base classes and shared widgets.
- **If `external-standard`:** Design a minimal Clean Architecture under `lib/modules/<feature>/` without speculative abstractions.

### Code Writer (Coder)
- Read `architecture_profile.mode` from `design.md`.
- **If `imespro`:**
  - Route destination screens **MUST** extend `BaseScreen`/`BaseScreenState`, override `getScreen()`, `createState()`, `buildMobilePortrait()`, and **NEVER override `build()`**.
  - Use pure Dart deep imports for domain (`package:app_core/domain/...`, `package:app_util/domain/...`), barrels for data/presentation.
  - Reuse `AppButton`, `AppFormField`, `AppDialog`, `ListViewPaging`, `DataState`, and `ApiService` only where their GUIDE “Use when” matches the approved need.
  - Only write new components if recorded as an approved `Core gap`.
- **If `external-structured`:**
  - Extend client's base screens/views and reuse client's shared components.
  - Prohibited from creating duplicate competing base classes.
- **If `external-standard`:**
  - Construct clean, idiomatic Flutter widgets under `lib/modules/<feature>/presentation/widgets/`. Follow Ponytail minimalism.

### Code Reviewer
- Review code against `architecture_profile.mode`:
  - **If `imespro`:** Check `setup --check` is READY; zero changes in `../app-*`; zero Client duplicates of fitting core APIs; domain imports pure; all route screens extend `BaseScreen` (no `build()` override); `Core usage` table matches code. Any violation = `FAIL`.
  - **If `external-structured`:** Ensure client base classes and design tokens are reused. Flag any unnecessary competing base classes as `CHANGES_REQUESTED`.
  - **If `external-standard`:** Ensure simplicity, clear Clean Architecture boundaries, and no over-engineering.

### Test Runner
- Adapt test harness to `architecture_profile.mode`:
  - Check only APIs and behaviors actually used by the approved feature; a profile is not a requirement to add paging, network, state libraries or tests for unused components.
  - **If `imespro`:** Test suites verify `BaseScreen` lifecycle, `ListViewPaging` (pagination total, load-more, empty/error), and `DataState` success/failure branches.
  - **If `external-structured`:** Use client's test helpers and mock utilities.
  - **If `external-standard`:** Standard Flutter widget and integration tests against BDD scenarios.

## 5. Flutter Reuse Ladder for Core UI Intake

The core `feature-planner` UI/UX intake is stack-neutral; its Flutter reuse ladder (`app_ui_kit` → `lib/commons/widgets/` → composition → feature-private widget) lives in [04_flutter_reuse_ladder.md](references/04_flutter_reuse_ladder.md).
