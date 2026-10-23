# 01 — When and scope

Rules SM9 and SM3. Reason: simplifying at the wrong time or outside the diff mixes refactoring with behavior change and bloats review.

## When

| Situation | Simplify? |
|---|---|
| The phase's checks pass (`ruff check`, `mypy`, affected `pytest`) and the diff has a named smell | Yes, inside the changed code only — the simplicity pass of `incremental-implementation` |
| A review finding names unnecessary complexity in the phase's code | Yes, as the fix revision for that finding (`review-resolution`) |
| Checks are red | No: fix behavior first with `{{slot:root-cause-debugging}}` |
| The smell is outside the diff | No: record it in the hand-off's Concerns as a separate item |
| The code is already clear, or a later task in the plan rewrites it | No |
| Writing a new feature, endpoint or migration, or fixing a bug | No: that changes behavior and follows the plan, not this skill |

## Scope

Only the files and lines changed in this phase. List them with:

```bash
git diff --name-only <base>...HEAD -- '*.py'
```

`<base>` is the branch point of the task. Conventional locations are `app/`, `tests/unit/`, `tests/integration/` and `alembic/versions/`; the workspace may use other paths.

- Inside the diff: dead code, pass-through layers and avoidable complexity are fair game.
- Outside the diff: report it, never touch it. A drive-by change invalidates evidence for code nobody asked to change (`{{slot:clean-code}}` scope rule).
- Alembic revisions that already ran anywhere other than a local database are history: never "simplify" them; a new revision is planned work.
- Generated code (OpenAPI clients, protobuf stubs) is regenerated, not hand-simplified.

## A named smell first

Before editing, write the candidate line for each spot:

`<smell> at <path:line>: <what to cut> -> <replacement>`

No catalog row ([03](03-smell-catalog.md)) and no `{{slot:clean-code}}` rule fits → leave the code. "I had to read it twice" is a smell only when you can say what forced the second read (a flag argument, a hop that adds nothing, a dict whose keys you had to trace).
