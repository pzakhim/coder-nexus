# External-Standard Architecture Contracts

> Topic: Minimalist standard Flutter Clean Architecture (`domain/`, `data/`, `presentation/`) without external company packages or custom framework wrappers.

---

## 1. Standard Flutter Clean Architecture Rules

Under the `external-standard` profile, the project uses standard Flutter/Dart packages (`flutter_bloc`, `equatable`, `get_it`, `dio` / `http`, `auto_route` / `go_router`) without `iMESPro` packages or heavy custom base wrappers.

| Layer | `external-standard` Contract |
|---|---|
| **Domain (`domain/`)** | • Pure Dart `Entity` classes (`Equatable`), abstract `Repository` interfaces, and single-action `UseCase` classes.<br>• Zero `package:flutter/*`, Data, or Presentation imports (`A5`). |
| **Data (`data/`)** | • `DataSource` receives the configured HTTP/storage client via constructor injection.<br>• `Model` parses JSON with explicit mandatory-field validation (zero silent fallback data — `A8`) and converts to Domain `Entity` via `Mapper` or `toEntity()`. |
| **Presentation (`presentation/`)** | • Navigable screens live in `presentation/screens/*_screen.dart` (`class *Screen extends StatelessWidget` or `StatefulWidget`) and wire their `Cubit`/`Bloc` at the route boundary.<br>• Use `BlocBuilder` for rendering and `BlocListener` for side effects (navigation, dialogs, snackbars). |
| **Ponytail Proportionality (`A9`)** | • Create only the layers and classes required by the approved feature scope. Do not invent speculative base classes, single-implementation wrapper interfaces for local helpers, or empty boilerplate layers. |
