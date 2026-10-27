# iMESPro Root-Cause Debugging Contracts

> Topic: Debugging BaseScreenState, ListViewPagingCubit, UseCasePower, DataState, DataMapper, parse* helpers, and ApiService (imespro profile)

## 1. Layer-by-Layer Fault Isolation (`imespro`)

When isolating a defect in an `imespro` feature module (`lib/modules/<module>/<feature>/`), bisect along the 4-layer boundary:

| Boundary Check | What to Inspect | Common Root Causes |
|---|---|---|
| **Presentation (`Screen` / `BaseScreenState` / `Cubit`)** | `BlocBuilder` / `BlocConsumer` `buildWhen`/`listenWhen` predicates; `ListViewPagingCubit` page state; `AppForm` field controllers | Missing field in `Equatable.props`; `buildWhen` returning `false` on status change; reading `context` after `await` without `if (!mounted) return;` |
| **Domain (`UseCasePower` / `UseCaseStreamPower` / `Entity`)** | `validate(param)` return value; `execute(param)` orchestration; `Entity` equality and domain getters | `validate(param)` returning a validation error string before `execute` runs; mutating input `Param` across retries |
| **Data (`RepositoryImpl` / `DataMapper`)** | `DataState.Success` vs `DataState.Error` branching; `mapToModel(dto)` / `mapToEntity(dto)` field mapping | Swallowing `DioException` inside repository and returning empty `DataState.Success([])` (violates R4); omitting a field in `DataMapper.mapToModel` |
| **Remote / Local (`ApiService` / `Model` / `parse*`)** | Raw JSON payload vs `Model.fromJson`; `app_util` `parseString` / `parseInt` / `parseDouble` / `parseBool` / `parseDateTime` / `parseList` | Unsafe `json['key'] as int` cast on a string-typed numeric API field instead of `parseInt(json['key'])`; mismatched JSON key casing (`snake_case` vs `camelCase`) |

---

## 2. Inspecting `DataState<T>` and `UseCasePower` Silently Failing Flows

- **Symptom**: UI stays in loading state or shows empty state without an error banner.
- **Bisection**:
  1. Log or breakpoint at `RepositoryImpl` return site: verify whether `DataState.Error(message, errorCode)` or `DataState.Success(data)` is returned.
  2. Check `UseCasePower.execute(param)`: ensure errors from `Repository` are returned as `DataState.Error`, not caught and converted into a default `Entity`.
  3. Check `Cubit` state transition: verify `result` handles both `DataState.Success` and `DataState.Error` and emits a new state with updated `props`.

---

## 3. Debugging `ListViewPagingCubit` and Pagination Defects

- **Symptom**: Duplicate items on scroll, infinite load loop, or pull-to-refresh not resetting list.
- **Root-Cause Checklist**:
  - Verify `page` and `pageSize` parameters passed to the paging request match the backend's 1-based vs 0-based index contract.
  - Check whether `hasReachedMax` / empty page detection checks `items.length < pageSize` vs `items.isEmpty`.
  - Confirm pull-to-refresh resets the page counter before firing the first page request rather than appending to existing state.

---

## 4. Core Package Escalation (`../app-core`, `../app-util`, `../app-ui-kit`)

- **Do not edit `../app-core`, `../app-util`, or `../app-ui-kit` from inside a client workspace.**
- If bisection proves the root cause is inside `BaseScreenState`, `ApiService`, `UseCasePower`, `parse*`, or an `app_ui_kit` widget:
  1. Record the exact file, line, and reproduction test in the Root-Cause Report (`03-fix-escalate-and-report.md`).
  2. Trigger an **H5 Stop & Escalate** if fixing requires changing the shared package contract, or apply a minimal local adapter in the feature module only when explicitly approved.
