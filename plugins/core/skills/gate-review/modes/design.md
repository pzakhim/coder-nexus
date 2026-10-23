# Mode: design (before Gate 2)

Reviews `design.md` against the Gate 1 approved `requirements.md`, `codebase-notes.md` and, when present, `design-uiux/uiux.md`. Pass 1 is clean before this file starts. Findings use the prefix `GR-D-NN`.

`DESIGN-007` already checks that every goal appears in `## Goal alignment` and `DESIGN-008` that every `S-NN` / `C-NN` is mapped. This mode goes one level finer and checks substance.

## D1. Reconcile inputs

Build one row per input item and name the design element that serves it.

| Input | Served by (section and element) | Status |
|---|---|---|
| `BR-03` | `## Behavior, data, and state`: validation rule on submit | served |
| `AC-05` | - | not served |

- Inputs: every `BR-NN`, every `AC-NN`, every `W-NN`, and every `D-NN` that binds technical work.
- An unserved `AC-NN` is `CRITICAL`; an unserved `BR-NN`, `W-NN` or `D-NN` is `HIGH`.
- Reverse direction: a design element that serves no input is gold-plating (`MEDIUM`) unless `codebase-notes.md` records why it is needed.
- Behavior the requirements do not contain (a new rule, state or permission) is scope creep (`HIGH`). It goes back to Spec Writer as a `Q-NN`; the design never changes requirements on its own.

## D2. Deferred list

- What the design deliberately leaves undecided (a cache policy, a page size, a later migration) is named in the existing sections, with why it is safe to wait and who decides it later. Do not add a heading the design template does not have.
- Something clearly undecided but not listed is `MEDIUM`.
- A deferred item that would let two units choose differently (two screens, front end and back end, two tasks) is `HIGH`: it is not deferrable, it needs a decision now.

## D3. Risks have mitigations

Every risk in `## Integration, errors, and risks` names a mitigation, a check that detects it, or a `BLOCKED` owner. A risk without one is `MEDIUM`; `HIGH` when it touches data loss, security, permissions or an AC.

## D4. Decisions bind divergence points

List the places where two units could make independent choices: names of shared entities and fields, state shape, error mapping and messages, API fields and status codes, routes, shared components, persistence keys.

- Each needs one rule in the design that cites a `D-NN` and that a reviewer can answer yes/no against. Missing is `HIGH`.
- A rule that does not actually prevent the divergence it names ("follow conventions") counts as missing.

## D5. Fit with the existing code

- Named paths, classes, packages and APIs appear in `codebase-notes.md` `## 3. Verified Baseline Facts` or are marked new. An unverified existing name is `HIGH`.
- The design follows the conventions of the selected architecture profile and the existing code unless a `D-NN` records the deviation and its reason (`MEDIUM` otherwise).

## Coverage report (design)

- D1 counts: `BR n/N, AC n/N, W n/N, D n/N served`, unserved IDs, gold-plating elements.
- Divergence points listed and how many are bound by a rule.
- Deferred items and risks: listed / with mitigation.
