# 01 - Scope and Candidate Hunting

Systematically identify defect candidates in newly modified Flutter code.

## 1. Scope Discipline

- Review only the changes in the current diff (`git diff HEAD~1` or working tree diff).
- Do not log speculative issues on untouched legacy files. If a pre-existing defect outside the diff is discovered, note it under Concerns in the handoff.

## 2. Scanning for Candidates

Examine code looking for high-probability failure patterns:
1. **Controllers & Mixins:** Look at every `TextEditingController`, `AnimationController`, `ScrollController`, and `FocusNode`. Did the author add `dispose()`?
2. **Asynchronous Operations:** Search for `async` methods. Are there unhandled `Future` errors? Can a user trigger the action multiple times simultaneously?
3. **Data Access:** Search for `.data` on `DataState`. Is it guarded by `isSuccess`?
4. **Bang Operators:** Search for `!` null assertions. Could the value ever be null from an edge-case API response?
5. **Widget Nesting:** Look for `Row` or `Column` children with unconstrained widths or heights.
