# 10 — Optional Design Subsections and Decision Scope

Apply the approved profile through [core-usage](../../core-usage/SKILL.md). These subsections are optional `###` blocks inside existing `design.md` sections. The validator does not require them; never add them as new `##` sections and never rename a validated heading.

## 1. Which decisions belong in `design.md`

Record a `D-NN` and cite it in `design.md` only when all three hold:

1. Two independently built parts could otherwise choose incompatibly (two phases, Cubit and repository, Client and BE, a screen and a shared widget).
2. The answer is not obvious from the Client's existing code or the selected profile.
3. It is a real trade-off. Present it through `solution-options` (2-3 technical options, recommended first) and close the user's choice into `D-NN`.

Anything else is left to the Code Writer inside the plan's bounds. Reason: every extra decision is one more thing to review and keep true.

## 2. Deferred decisions (`## Architectural decision`)

- List only choices this version's goals do not need (an offline cache for a later version, a second sort order nobody asked for).
- Each row: the decision, why it can wait, and the trigger or version that reopens it.
- An unknown that blocks an AC of this version is never deferred: it is a question, resolved before Gate 2. Reason: deferral is a decision with a reason; a hidden unknown is not.

## 3. Complexity justifications (`## Foundation reuse ...`)

A deviation is using something other than the approved foundation component that fits the need, or adding a layer, base class or `lib/core/` abstraction the profile does not require.

- The `D-NN` entry in `codebase-notes.md` records three fields: **Violation** (what departs from the foundation), **Why needed** (the current need, tied to an AC or `BR-NN`), **Simpler alternative rejected because** (why the foundation component or a module-local solution does not work).
- `design.md` lists one row per deviation and cites that `D-NN`.
- No justification, no deviation. Reason: it stops speculative abstractions from entering through the design.

## 4. Risk → Mitigation (`## Integration, errors, and risks`)

- Only risks that threaten an AC or goal: an unverified endpoint, a kit component missing a state, a slow list, a platform permission.
- Each mitigation is a check or a design choice with a `PHASE-NN` that owns it. Planning then schedules the riskiest phase first (`planning-and-task-breakdown`).

## 5. Migration plan and rollback (`## Integration, errors, and risks`)

Only when persisted data changes: secure-storage or preference keys, local database or cache schema, a stored file format.

- **What changes**: keys or schema before and after.
- **Steps**: expand (write the new form, still read the old) → migrate (convert existing data on first run) → contract (stop reading the old form in a later phase or version, recorded as a `D-NN`). Each step leaves the app usable.
- **Old data and older app versions**: how data written by the current release is read or converted.
- **Rollback**: how to return to the previous state and the check that proves it.

## Checklist

- [ ] Every `D-NN` in `design.md` passes the three tests in §1.
- [ ] Optional subsections that do not apply are deleted, not left empty.
- [ ] No deferred item hides an unknown that blocks this version.
- [ ] Every deviation from the foundation cites a `D-NN` with the three fields.
