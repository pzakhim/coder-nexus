# 04 — State Management and Data Flow

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). Company setup and API examples below are **iMESPro-only**. External profiles use their approved Client mapping or standard Flutter; shared boundaries and evidence rules apply to all.

Guide for the `Behavior, data, and state` section of `design.md`.

## 1. State: follow the Client, add only what the behavior needs

1. Open an existing Cubit state in the Client (same module first, then a sibling module) and reuse its convention: sealed classes, a project state base, `Equatable` with `copyWith`, or a single state with a status field.
2. New module with no convention to copy → a sealed state with `Initial / Loading / Success / Failure` is the default. Collapse states the behavior never shows (e.g. no `Initial` when the screen loads immediately).
3. Do not invent a base class. If the Client has no state base, do not create one in `lib/core/`.
4. A screen whose list is fully driven by `ListViewPaging` uses `ListViewPagingCubit` from app_core instead of a feature Cubit for that list.

## 2. Cubit contract

- Public methods = user actions (`load()`, `submit()`, `retry()`).
- Flow: UI → Cubit → (UseCase) → Repository → `DataState<T>` → Cubit emits.
- `BlocBuilder` renders; `BlocListener` handles one-off effects (navigation, toast, dialog).

## 3. Domain: only what earns its place

Read app_core GUIDE §2.2 and app_util GUIDE §2.1, then decide per operation:

| Situation | Decision |
|---|---|
| Business rule, combines repositories, or reused by several Cubits | UseCase (`UseCasePower` / `UseCasePowerNoParams` when it fits) |
| Pure pass-through of one repository call, used once | Cubit may call the repository directly **if the Client already does this**; otherwise follow the Client's use-case convention |
| Paged list | `PagingUseCase<T>` + `ListViewPagingRepository<T>` (app_core §2.4) when the GUIDE "Use when" matches |

- **Entity**: pure Dart, immutable; only fields the UI or rules use.
- **Repository contract**: `Future<DataState<Entity>>` (app_util). Presentation never sees models or `ApiResponse`.

## Output format

```markdown
### State Machine & Domain Flow
- **State**: copies `<sibling_module>` convention — sealed `<Feature>State`: `Loading`, `Success(<Feature>Entity)`, `Failure(String)`
- **Domain Contracts**: `<Feature>Entity`; `<Feature>Repository.<action>(params) → DataState<<Feature>Entity>`; `<Action>UseCase extends UseCasePower` (validates input before calling repo)
```
