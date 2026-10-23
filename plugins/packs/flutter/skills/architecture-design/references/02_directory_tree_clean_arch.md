# 02 — Target Directory Tree and Clean Architecture Layout

Apply the approved profile through [core-package-usage](../../core-package-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for Section 2 of `design.md`: **Target Directory Tree & Layer Responsibilities**.

## Purpose
Tech Lead invokes MCP tool `get_project_structure(scope="module", feature_name="<feature>")` to generate the authoritative ASCII directory tree and explicitly define the responsibility of each layer.

## Standard Module Structure (Flutter Clean Architecture)
```text
lib/modules/<feature>/
├── di.dart                     # Module Dependency Injection registration
├── domain/                     # Pure Dart, zero Flutter dependencies
│   ├── entities/               # Immutable business entities
│   ├── repo/                   # Abstract Repository contracts
│   └── usecases/               # Single-responsibility business actions
├── data/                       # Implements Domain contracts
│   ├── data_sources/           # Remote API client and local cache adapters
│   ├── models/                 # DTOs with JSON serialization (fromJson/toJson)
│   ├── mappers/                # Model -> Entity converters
│   └── repo_impl/              # Repository implementations with error handling
└── presentation/               # Flutter UI and State
    ├── bloc/                   # Cubit and State classes
    ├── screens/                # Destination screens (*_screen.dart, extends BaseScreen)
    └── widgets/                # Private widgets and subviews for this feature
```

## Prohibited Patterns
- **No top-level `views/` directory**: Top-level `views/` directly under module is strictly prohibited (violates `DESIGN-006-VIEWS`). UI destinations must reside under `presentation/screens/` and `presentation/widgets/`.
- **No bypass of Domain**: Presentation must consume Domain UseCases and Entities, never raw Models or DataSources directly.
- **No circular dependencies**: `di.dart` references Domain, Data, Presentation; Domain never references Data or Presentation.

## Output Format
```markdown
## 2. Target Directory Tree & Layer Responsibilities

```text
[ASCII Tree from get_project_structure]
```

- **Folder Roles & Responsibilities**:
  - `domain/entities/`: [List planned entity names and immutability rules]
  - `domain/usecases/`: [List discrete business actions]
  - `domain/repo/`: [List abstract repository interfaces]
  - `data/models/ & mappers/`: [List DTO models and mapping logic]
  - `data/data_sources/`: [List remote and local cache data sources]
  - `data/repo_impl/`: [List repository implementations]
  - `presentation/bloc/`: [List Cubit and state classes]
  - `presentation/screens/`: [List screen classes extending BaseScreen]
  - `presentation/widgets/`: [List private composable widgets]
  - `di.dart`: [DI module registration entry point]
```
