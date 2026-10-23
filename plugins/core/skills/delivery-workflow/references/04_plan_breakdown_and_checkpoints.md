# 04 — Behavior Phases, Checkpoints and Version History

## Vertical Slices

Split the approved work by observable behavior and AC, not by technical layer. A phase may touch Domain, Data, Presentation, DI and tests when its behavior needs them. A scoped UI-only phase may reuse existing layers. Do not create phases that only assemble widgets, then screens, then routing before any behavior can be checked.

If a phase is too large to review or verify, divide it by independent behavior and explicit `depends_on` links. Each phase must have a concrete outcome, affected files and owner, `READY when` condition, verification commands/target, and done criteria. Derive commands from the actual Client configuration rather than assuming FVM, flavor or test path.

## Checkpoints and status

A checkpoint follows a completed behavior phase or another approved milestone. Coordinator records actual analyzer, test, review and UI evidence in `as-built.md`, then advances only when dependencies and approvals still cover the next phase.

- `READY`: prerequisites passed, source contracts verified and file ownership is clear.
- `IN_PROGRESS`: work started on the approved phase.
- `BLOCKED`: a required decision, source, service, environment or target is unavailable; record the exact blocker.
- `PASS`: all required AC, review and verification evidence matches the code revision.
- `FAIL`: an executed check found a defect (older files write `FAILED`; same meaning).

A code fix invalidates affected evidence and returns that scope to implementation/review/verification. `NOT_RUN` or `BLOCKED` cannot be promoted to `PASS`.

## Archive and version ownership

The active plan is `${workspaceFolder}/docs/features/<module>/<feature>/vN/implementation-plan.md`, linking `phases/phase-XX-<behavior>.md`. One approved change batch owns one vN. Keep the completed version in Git as its historical contract; actual progress and deviations live in `as-built.md`. A later batch creates vN+1 with `change-impact.md`, comparing prior approved docs and code. Never overwrite an unfinished version. A cancelled version stays indexed as `CANCELLED` and the next batch uses the next number. Legacy `.agents/plan/implementation_plan.md` and `task.md` are read-only migration context.
