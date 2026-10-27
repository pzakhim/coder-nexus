# iMESPro Bug-Hunt Contracts

> Topic: Defect patterns in BaseScreenState, ListViewPagingCubit, UseCasePower, DataState, DataMapper, parse* helpers, and app_ui_kit widgets (imespro profile)

## 1. `imespro` Defect Patterns (Dimension 6 Extension)

When hunting bugs in an `imespro` workspace (`lib/modules/<module>/<feature>/`), check every applicable row below in addition to `01-scope-dimensions-and-patterns.md`:

| Looks like | Goes wrong when | Check |
|---|---|---|
| Reading `result.data` on `DataState<T>` without checking `result is DataSuccess` / `isSuccess` | When `Repository` returns `DataFailure`, accessing `.data` yields `null` or throws a runtime error, or silently skips error handling | Pattern-match `DataSuccess` vs `DataFailure` (or check `isSuccess` / `isFailure`) on every `DataState<T>` return |
| `RepositoryImpl` catches `DioException` / `Exception` and returns `DataSuccess(const [])` instead of `DataFailure` | Network failure or 500 error looks like "0 records found" in the UI; retry banner never renders | Ensure repository methods use `.tryCatch` (`app_util`) or return `DataFailure` on every error path |
| `UseCasePower<T, P>` overrides `execute(param)` without validating `param` in `validate(param)` | Invalid/empty input parameters reach the network or repository layer instead of failing fast in domain | Verify `validate(param)` checks required domain invariants before `execute` runs |
| `Model` / `DataMapper` uses raw `json['key'] as int` / `as double` / `as bool` instead of `app_util` `parse*` helpers | Backend returns a stringified number (`"42"`) or `null`; throws `_TypeError` at runtime | Require `parseString`, `parseInt`, `parseDouble`, `parseBool`, `parseDateTime`, `parseList` (`app_util`) |
| `BaseScreenState` subclass overrides `buildMobilePortrait` but omits `buildTabletPortrait` / `buildLandscape` when target devices include tablets | Tablet layout falls back to an unadapted or broken view | Check `design.md` target viewports and responsive overrides in `BaseScreenState` |
| `ListViewPagingCubit` (`app_core`) refresh or filter change appends to existing list or uses wrong 0-based vs 1-based page index | Duplicate rows appear on pull-to-refresh or first page is skipped/repeated | Verify page reset on refresh/filter change and pagination index alignment with the API |
| `AppButton` (`app_ui_kit`) submitting a mutation without binding `isLoading` / disabling during loading state | Rapid user taps fire duplicate POST/PUT requests | Verify `AppButton` binds loading state and `Cubit` guards against concurrent submission |
| `AppLogger` (`app_util`) logging raw request/response bodies containing tokens, passwords, or PII | Credentials leak into device/crash logs | Verify sensitive fields are redacted before `AppLogger` calls |

---

## 2. Typical `imespro` Disproofs

| Suspicion | Often Disproved By |
|---|---|
| "Null crash in `Model.fromJson`" | All fields are parsed through `parseString` / `parseInt` / `parseDouble` (`app_util`), which safely coerce types and provide defaults |
| "Unhandled `DioException` in Repository" | Repository wraps the `ApiService` call in `.tryCatch`, which converts exceptions into `DataFailure` automatically |
| "401 token expiry crashes active request" | `ApiService` (`app_util`) auth interceptor refreshes the token and retries transparently |
