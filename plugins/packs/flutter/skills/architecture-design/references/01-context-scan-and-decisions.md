# 01 — Flutter Context Scan, Decisions, and Directory Layout

> Topic: Evidence-based profile resolution, 6 codebase intelligence scans, Scope Classification, D-NN decision rules, and Clean Architecture directory layout (`AD1`–`AD4`)

## 1. Evidence-Based `architecture_profile` Resolution (`AD1`)

Before proposing any classes, resolve and record `architecture_profile` once in `design.md` (or `brief.md` for phase-free items) from actual Client workspace evidence:

```yaml
architecture_profile:
  mode: imespro | external-structured | external-standard
  core_source: "../app-*" | "lib/core/" | "none"
  evidence: ["pubspec.yaml", "actual Client base/consumer paths"]
```

1. Honor an existing user/workspace selection in `.superpowers/setup.json` or an approved `design.md`.
2. Without a prior selection, inspect `pubspec.yaml` and actual consumers in `lib/`:
   - `imespro`: Client `pubspec.yaml` resolves the company foundation packages or the user explicitly selects `imespro`.
   - `external-structured`: Client has established foundations under `lib/core/`, `lib/shared/`, or internal packages with real consumers across features (empty directories do not count).
   - `external-standard`: Vanilla Flutter project without a pre-existing central foundation.
3. Follow the active workspace profile guide for foundation setup gates, component tables, and base class rules.

---

## 2. Six Codebase Intelligence Scans & Scope Classification (`AD1`, `AD2`)

Scan the actual Flutter Client at `${workspaceFolder}` read-only and record every verified path/symbol in `codebase-notes.md` → `## 3. Verified Baseline Facts`:

| Scan Anchor | What to Inspect | What to Record in `codebase-notes.md` |
|---|---|---|
| **1. `pubspec.yaml`** | Package name (`{{PackageName}}`), Flutter/Dart SDK, state management (`flutter_bloc`, `riverpod`, `provider`), router, DI (`get_it`, `injectable`), HTTP (`dio`, `http`) | Exact installed dependencies and lint package (`very_good_analysis` / `flutter_lints`) |
| **2. Foundation / Shared Core** | Active profile packages or `lib/core/`, `lib/shared/`, `lib/commons/widgets/` | Existing base screens, result wrappers, HTTP interceptors, design tokens, and shared widgets |
| **3. Client Router** | `lib/routes/` or router config (`GoRouter`, `AutoRoute`, `onGenerateRoute`) | Route constants, path parameters, typed route arguments, `Navigator.pop` return conventions |
| **4. Client DI Entry** | `di.dart`, `lib/modules/modules_di.dart`, or DI bootstrap | Registration order, factory vs singleton conventions |
| **5. Target & Sibling Modules** | `lib/modules/<feature>/` and sibling modules | Existing folder structure, state class pattern (`sealed` vs `Equatable` `copyWith` vs project base), repository/mapper patterns |
| **6. UX Error Taxonomy** | MCP tool `get_ux_error_patterns` | Standard UX recovery behaviors for `401`, `400/422`, network timeout, and `500` |

### Scope Classification (`AD2`)
- **`INIT`**: New feature module — confirm a `lower_snake_case` module owner at Gate 2, include only the layers required by the approved behavior, and wire DI in the composition root.
- **`EXTEND`**: Modifying an existing feature module — preserve the module's existing state pattern, naming, and folder conventions (`C11`) unless a migration is explicitly approved.
- **`CORE IMPACT`**: Modifying shared core/auth/network/storage/boot files under `lib/core/` — document blast radius across all consuming modules.

---

## 3. Pre-Design `grilling` & Which Decisions Belong in `design.md` (`AD3`)

- **Strict Boundary with `spec_writer`:** `spec_writer` owns business API Input/Output and screen UX requirements. `planning` owns the **Data Pipeline architecture** (`DataSource` → `Model/Mapper` → `Repository` → `UseCase` → `State/Cubit` → `DI`), the **Mockoon Trigger & Test Data Table**, and **exact foundation/widget class mapping**.
- **Three Tests for Recording a `D-NN` Decision:** Record a `Q-NN` → `D-NN` in `codebase-notes.md` and cite it in `design.md` **only** when all three hold:
  1. Two independently built parts (two phases, Cubit and Repository, Client and Backend, a screen and a shared widget) could otherwise choose incompatibly.
  2. The answer is not obvious from the Client's existing code or the active profile.
  3. It is a genuine trade-off. Present 2–3 options with `(Recommended)` first via `grilling` (`01-solution-options-and-divergent-pass.md`) / `ask_question` **one question at a time**, and close the user's answer into `D-NN` (`Owner: planning`).
- **Optional Subsections in `## Architectural decision` (delete when not applicable):**
  - `### Deferred decisions`: Only choices this version's goals do not need (`Decision deferred`, `Why it can wait`, `Revisit when`). Never defer an unknown that blocks an AC of this version.

---

## 4. Target Directory Tree & Clean Architecture Layout (`AD4`)

Invoke `get_project_structure(scope="module", feature_name="<feature>")` and include **only** the directories and files the approved behavior actually needs:

```text
lib/modules/<feature>/
├── di.dart                     # Module Dependency Injection registration (when DI is used)
├── domain/                     # Pure Dart, zero Flutter or Data imports
│   ├── entities/               # Immutable business entities
│   ├── repo/                   # Abstract Repository contracts
│   └── usecases/               # Single-responsibility business actions (when needed)
├── data/                       # Implements Domain contracts
│   ├── data_sources/           # Remote API and local storage data sources
│   ├── models/                 # DTOs with JSON serialization (fromJson/toJson)
│   ├── mappers/                # DTO <-> Entity mappers (or Model implementing mapper)
│   └── repo_impl/              # Repository implementations mapping errors to result types
└── presentation/               # Flutter UI and State
    ├── bloc/                   # Cubit / Bloc / Notifier and immutable State classes
    ├── screens/                # Route destination screens (*_screen.dart)
    └── widgets/                # Feature-private child widgets, modals, and dialogs
```

- **Prohibited:**
  - **No top-level `views/` directory** under `lib/modules/<feature>/` (violates `DESIGN-006-VIEWS`); route destinations live in `presentation/screens/` and subviews/dialogs live in `presentation/widgets/`.
  - **No empty layer scaffolding:** A UI-only phase does not add empty `domain/` or `data/` folders.
  - **No Domain bypass:** Presentation consumes Domain Entities and UseCases/Repositories, never raw DTO Models or DataSources.
