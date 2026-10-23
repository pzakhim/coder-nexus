# Mode: plan

Turn the approved specs into a test plan before touching the environment. Write it to `vN/evidence/test-plan.md` (one plan per work-item version; later phases add cases, never rewrite earlier ones).

## 1. Testability check

Read every `AC-NN` and Given/When/Then scenario. Flag, as a question to the coordinator (for Spec Writer, logged as `Q-NN`), any AC that:

- has no observable outcome (screen state, message, persisted data, status code, file);
- uses vague words ("fast", "easy", "correct") without a measure;
- needs data, a role or a provider nobody can supply.

Do not invent the missing expectation. Such an AC stays `BLOCKED` until a `D-NN` answers it. Reason: a guessed expectation tests the guess, not the requirement.

## 2. Two-way traceability

| Direction | Rule |
|---|---|
| AC → cases | Every `AC-NN` and every scenario of every `W-NN` has at least one case |
| Case → source | Every case cites `AC-NN`, `BR-NN`, `W-NN`, a `## Review focus` line, or is labelled `guard` (Scope Out) or `regression` |

An AC without a case is a gap; a case without a source is an orphan. Fix both before executing. Reason: gaps hide untested risk, orphans test things nobody asked for.

## 3. Coverage categories

For each AC, consider each category and write a case or a one-line reason it does not apply:

| Category | Typical case |
|---|---|
| Happy path | The scenario as approved, persisted and visible after re-read / reload |
| Validation | Each invalid input class rejected with the specified message; nothing persisted |
| Permissions per role | Each role × action allowed or denied; a direct forbidden call (bypassing the UI) is refused |
| States | Empty (no data vs no match), loading, error with retry, populated |
| Boundaries | 0, 1, max, max+1; first / last page; longest text |
| External failures | Provider timeout, error, malformed response (sandbox or labelled stub) |
| Repeat / concurrency | Double submit, retry after failure, stale view after a change elsewhere |
| Review focus | Each `## Review focus` line from `implementation-plan.md` that is observable from outside |
| Out-of-scope guard | Nothing listed under Scope Out was built or changed |
| Regression | Existing flows sharing the changed components, data or permissions |

## 4. Cheapest level that proves it

| Level | Proves | Use for |
|---|---|---|
| Service / API acceptance | Rules, permissions, status codes, persisted data, side effects through the real interface and real auth | Business rules, role denials, idempotency, error codes |
| UI end-to-end | What the user sees and does on the running app | Flows, the four states, role-driven visibility |
| Visual | Fidelity to the approved `uiux.md` screens `S-NN` | UI items with an approved design ({{slot:visual-verification}}) |
| Manual | What cannot be automated now | Only with a written reason and step-by-step evidence |

Developer unit tests belong to the Code Writer ({{slot:unit-test}}); cite them, never count them as acceptance. Reason: each case at the most expensive level makes the run slow and flaky; each case at too cheap a level proves nothing the user sees.

## 5. Case format

```
TC-NN  covers <AC-NN | BR-NN | W-NN#step | RF-n | guard | regression>  priority P1|P2|P3  level api|ui|visual|manual
Given:  <data and state, with its source (seed, fixture, approved record)>
When:   <action, as which role, on which target>
Then:   <observable result: state / message / persisted value / status code>
Check:  <command or tool action, cwd> — from {{slot:verification}} or {{slot:visual-verification}}
```

Priority: P1 = critical flows, permissions and data scopes, data integrity; P2 = validation, states, shared-component regression; P3 = rare or cosmetic. Run P1 first so that a short run still covers what matters.

## 6. Plan table and gaps

End the plan with:

| AC | Cases | Levels | Gaps / reason |
|---|---|---|---|

and a list of open questions. The coordinator sees the plan before execution; when an AC or `D-NN` changes later, update the plan and say which cases changed.
