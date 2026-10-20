# 02 — Acceptance Criteria Coverage Matrix

Guide for AC Coverage mapping in `implement-plan.md`.

## 1. 100% Traceability Rule
Every Acceptance Criteria (`AC-01`, `AC-02`, etc.) defined in `requirements.md` MUST be mapped to exactly one owning phase and have a decisive check that can fail.

## 2. Table Format
```markdown
## AC coverage

| AC ID | Phase ID | Decisive check | Evidence target |
|---|---|---|---|
| AC-01 | PHASE-01 | Unit test validates DTO parsing and mapper | `<stack test path>/<feature>/data/mapper_test` |
| AC-02 | PHASE-02 | Component test validates the empty state rendered on empty list | `<stack test path>/<feature>/presentation/empty_test` |
| AC-03 | PHASE-03 | State test validates error message emitted on 400 failure | `<stack test path>/<feature>/presentation/state_test` |
```

Use the stack's test path convention from `{{slot:unit-test}}` (concrete examples in `{{slot:verification}}`).

## 3. Strict Rules
- No orphaned AC: If an AC is not mapped to any phase, `validate_plan_slices` returns `PLAN-V-006-AC-COVERAGE` error.
- No duplicate mapping: Map each requirements AC exactly once.
