# 02 — Verify and Disprove Candidates

> Topic: Adversarial disproof workflow, concrete failure scenarios, read-only CLI checks, and confidence grading (`H6`–`H8`)

A candidate that survives an honest attempt to refute it is worth the reader's time; everything else is noise. Verify every candidate from [01-scope-dimensions-and-patterns.md](01-scope-dimensions-and-patterns.md) before it becomes a finding.

## 1. Adversarial Disproof Steps per Candidate (`H6`–`H8`)

1. **Trace the Real Path (`H6`):** Walk from an entry point to the suspect line: a route transition, a widget lifecycle hook (`initState`, `didUpdateWidget`, `dispose`), a user gesture (`onPressed`, `onChanged`, pull-to-refresh, scroll threshold), a `Cubit` / `Bloc` / `Notifier` method, a domain use case, or a repository/datasource call. On the way, read upstream guards, form validators, `BlocBuilder` / `BlocListener` `buildWhen` / `listenWhen` predicates, and parent widget constraints.
2. **Write the Failure Scenario (`H7`):** State concrete values:
   ```text
   given <input/state> → when <action> → then <observed wrong result>
   ```
   Example: `given OrderCubit in OrderLoadFailure(error: "Timeout") → when user taps Retry and fetchOrder emits copyWith(isLoading: true, error: null) → then state.error remains "Timeout" because copyWith uses error ?? this.error, re-triggering the error dialog on loading`.
3. **Run Read-Only CLI Checks (`H6`):** When a read-only command decides the question, run it and quote its exit code (`PASS` / `FAIL`) and key output:
   - Static analysis: `flutter analyze` (catches `use_build_context_synchronously`, `cancel_subscriptions`, `close_sinks`, unused fields, type mismatches)
   - Focused tests: `flutter test test/unit/<file>_test.dart --plain-name "<name>"`
   - Caller & symbol search: `rg -n -w "<symbol>" lib test`
   - Git history: `git show <REVIEW_REVISION>:<path>`, `git log -L <start>,<end>:<path>`
   Never modify application code, generated `.g.dart`/`.freezed.dart` files, or tests during the hunt.
4. **Classify Confidence (`H8`):**
   - `CONFIRMED` — the execution path is traced end-to-end and nothing on it prevents the failure, or a read-only command demonstrated it.
   - `PLAUSIBLE` — the failure depends on something not visible in the repository: a real backend API payload shape not documented in the contract, device-specific keyboard/viewport inset behavior, or race timing under slow network conditions. Name exactly what would confirm it.
   - **Rejected** — an upstream guard, non-null type guarantee, parent layout constraint, or framework lifecycle hook prevents it. Drop silently.

---

## 2. What Does Not Survive

- **No failure scenario → no finding.** "Might be fragile", "consider adding a null check", "missing `const`", and style remarks are not findings.
- **Impossible input:** A scenario where the value is already guaranteed non-null by the Dart type system and validated at the DTO boundary before constructing the domain entity is rejected.
- **Pure cleanup:** A scenario that only notes a minor rebuild or code duplication without wrong behavior, jank, or memory leak is a `NOTE` (`H14`).

---

## 3. Typical Disproofs in Flutter / Dart

| Suspicion | Often Disproved By |
|---|---|
| "`NullCheckError` on `item!`" | The enclosing widget only builds inside a branch or pattern match that already narrows `item` to non-null |
| "`setState` after `dispose` on async callback" | The state class checks `if (!mounted) return;` immediately before `setState`, or uses `BlocBuilder` which manages its own subscription lifecycle |
| "`RenderFlex` overflow in `Row`" | The dynamic child is wrapped in `Expanded` / `Flexible`, or parent constraints bound the width via `LayoutBuilder` |
| "Duplicate API call on double tap" | The button disables `onPressed` when `state.isLoading` is true, and the cubit method returns early if `state.isLoading` |
| "Uncancelled `Stream` in widget" | The stream is consumed via `StreamBuilder` or `BlocProvider` (with `create:`), which automatically cancels/closes on widget disposal |

Check the actual code for each disproof; an assumed disproof is as weak as an assumed finding.
