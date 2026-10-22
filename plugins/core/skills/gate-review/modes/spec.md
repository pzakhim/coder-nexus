# Mode: spec (before Gate 1)

Reviews `requirements.md` (or `brief.md`) and `codebase-notes.md`, with `design-uiux/uiux.md` when the item has UI impact. Pass 1 is clean before this file starts. Findings use the prefix `GR-S-NN`.

Read beside the documents, when they exist in the workspace:

- `.agents/skills/domain-knowledge/` - glossary, entities, roles and data scopes (for S2).
- `.agents/skills/requirements-specification/` - its mandatory edge cases (`references/03-mandatory-edge-cases.md`) and `references/05-gate-review-questions.md` become extra S5 items (optional; skip when absent).

## S1. Vague words

Every adjective or adverb that a tester cannot check is a finding (`[Ambiguity]`, `HIGH` in a BR or AC, `MEDIUM` elsewhere), unless the same sentence or a cited `D-NN` turns it into a number, a named state, a visible message or a rule.

| Banned unless defined | Ask for |
|---|---|
| fast, quick, slow, responsive, instant, real-time | a time budget and where it is measured (e.g. list visible within 2 s on the reference device) |
| intuitive, easy, simple, user-friendly, clean, modern, seamless | the observable step, label, default or number of steps |
| robust, reliable, stable, resilient, gracefully, properly, correctly | the exact failure and what the user sees after it |
| secure, safe | the role, the data scope and the forbidden action |
| scalable, efficient, optimal, flexible | a volume, a limit or the reason it is in scope at all |
| appropriate, reasonable, sufficient, as needed, etc., some, many, few, usually, normally, prominent | the concrete value, list or condition |
| Vietnamese equivalents: nhanh, mượt, thân thiện, dễ dùng, đơn giản, hợp lý, phù hợp, ổn định, linh hoạt, đầy đủ | same as above |

Also flag a verb without its object or result ("handle the error", "support filters") and near-duplicate BR or AC rows that say the same thing twice (`LOW`, keep the clearer one).

## S2. Terminology drift

- Every domain noun in `## 0. Goals`, BR, scenarios, AC and `## Workflows` uses the term in `codebase-notes.md` `## 2. Glossary` (and in `domain-knowledge` when present).
- Two words for one concept, one word for two concepts, or a term that maps to an entity/state but is missing from the Glossary is `[Conflict]` or `[Gap]`, `MEDIUM` (`HIGH` when a role, permission or money term drifts).
- Screen and step names in `## Workflows` match `uiux.md` exactly.

## S3. Conflicts

Compare each pair and report every contradiction as `[Conflict]`:

| Pair | Look for |
|---|---|
| `BR-NN` vs `AC-NN` | an AC that a BR forbids, or a BR no AC observes |
| AC vs `## 4.` scenarios | a scenario outcome that differs from its AC |
| `## Workflows` vs `uiux.md` | different step order, a missing branch, a state a screen does not draw |
| `Scope out` / non-goals vs any BR, AC or `W-NN` | out-of-scope behavior that still appears |
| `## 2. Actors & Permissions` vs AC | an actor acting without the permission, or a role nobody uses |
| `D-NN` vs text | text that says something other than the confirmed decision (`CRITICAL`) |

## S4. Coverage map per grill dimension

For each group of the `grilling` queue order (SKILL §2.2 groups 1-7), mark the spec `Clear` (settled by text or a `D-NN`), `Partial` (mentioned, a builder would still have to choose) or `Missing`. Group 7 (technical trade-offs) is `N/A` at Gate 1.

| §2.2 group | Topic | Status | Evidence (section, IDs) |
|---|---|---|---|
| 1 | Job type and goals | | |
| 2 | Scope, actors, permissions | | |
| 3 | Main workflow and branches | | |
| 4 | Data and API source, fields, errors | | |
| 5 | Observable states (4 visual states for UI), lifecycle | | |
| 6 | Negative, boundary and edge cases | | |

`Partial` is `MEDIUM`, `Missing` is `HIGH` (`CRITICAL` for §2.2 group 1). This table is part of the coverage report.

## S5. Requirement-quality checklist

Write the checklist from this spec's actual text - no fixed list. Each item is a **question about what the spec says**, so it tests the writing, not the product.

- Allowed shapes: "Is ... defined for ...?", "Is '<word>' quantified?", "Do `BR-03` and `AC-07` agree on ...?", "Does the spec say what happens when ...?"
- Never write an item that starts with Verify, Test, Confirm, Check, Click or Open, or that describes running the system. Those belong to the Test Runner.
- Tag every item `[Gap]` (something absent), `[Ambiguity]` (present but unclear) or `[Conflict]` (two places disagree), plus the `G-NN` / `BR-NN` / `AC-NN` / `W-NN` it concerns. A `[Gap]` with nothing to cite names the section where the text should be.
- Keep about 30 items; merge items that test the same thing. An item answered "no" becomes a finding.

Examples:

- "Is the maximum number of attachments per request stated? [Gap] `BR-02`, `AC-04`"
- "Is 'recent orders' bounded by a date range or a count? [Ambiguity] `AC-03`"
- "Do `BR-05` (only managers approve) and `W-02` step 3 (any staff approves) agree? [Conflict]"

## S6. Scenario classes

For each `G-NN` (and each `W-NN` with UI), check that the scenarios and AC cover:

| Class | Meaning |
|---|---|
| primary | the main success path |
| alternate | a different valid path to the same goal (other role, other entry, optional step) |
| exception | invalid input, missing permission, empty data, API failure, timeout |
| recovery | what the user and the data look like after an exception: retry, resume, partial save, undo, nothing lost |

A missing class is `[Gap]`: `HIGH` for exception or recovery on a flow that creates, changes or deletes data, `MEDIUM` otherwise - unless a `D-NN` puts it out of scope. The classes per goal are part of the coverage report.

## S7. The case the user would be upset to see broken

Name the one behavior whose failure would upset the user most (lost data, wrong amount, wrong person sees it, a daily task blocked). It must have its own `AC-NN` and scenario with concrete values. If the documents do not let you name it, or it has no AC, raise a `HIGH` finding whose `Q-NN` asks the user which case that is.

## Coverage report (spec)

- S4 grill-dimension table.
- Scenario classes per goal: `G-01: primary, alternate, exception, recovery (missing)`.
- S5: items written, answered yes, findings raised.
- Upset case: the named behavior and its `AC-NN`, or the `Q-NN` asking for it.
