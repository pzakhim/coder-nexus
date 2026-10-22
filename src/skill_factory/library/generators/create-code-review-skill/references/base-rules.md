# Base rules (generic, every workspace)

Generalised from Coder Nexus `plugins/core/agents/code_reviewer.md` and the stack `code-review` rubrics. Each rule goes into the generated skill with the workspace's vocabulary, gates and report location **and its reason**, or is marked "not adopted" with a reason.

| # | Rule | Why | Goes into |
|---|---|---|---|
| R1 | **Review a fixed revision.** Record base and review revisions plus the full uncommitted scope of the item; review exactly that tree. | A verdict on a moving tree certifies code nobody reviewed. | 01 |
| R2 | **Read-only.** Never edit application code, tests, generated code or dependencies; write only the review report. Any edit (even a comment) is a new revision that needs review. | A reviewer who fixes code becomes the author and nobody reviews them. | 01 |
| R3 | **Bug-hunt first, then compliance.** Run bug-hunt at `standard` (`deep` for risky or repeatedly returned items) from the code before reading design documents; then grade the axes. | Reading intent first hides what the code actually does. | 01 |
| R4 | **Grade each applicable axis with the workspace's own rubric skill** (clean-architecture, clean-code, unit-testing, secure-coding-standards, database-migrations) or the fallback checklist when the skill is missing. | One standard for writer and reviewer ends "but I thought…" debates. | 02 |
| R5 | **Trace acceptance criteria.** Every applicable AC maps to implementation and to a test or a named manual check with evidence; work serving no approved goal is scope creep. | Untraced AC are the ones that ship broken. | 02 |
| R6 | **Rerun the checks yourself.** Gates, validators, analyzers and the phase's tests on the review revision; the writer's evidence is input, not proof. `NOT_RUN` / `BLOCKED` are never `PASS`. | Evidence produced on another tree or not at all proves nothing. | 01, 04 |
| R7 | **No reviewer waivers.** The reviewer cannot excuse a rule violation, however good the argument; a real conflict with an approved design goes back to planning / the user. | Waivers in reviews quietly rewrite the standards. | 04 |
| R8 | **Actionable findings.** ID, severity, axis/rule, file:line, the problem, why it matters, fix direction (not the code). Most severe first. | Vague findings come back as questions and cost a round. | 03 |
| R9 | **Only the change.** Review the diff and the callers it breaks; legacy debt outside it is a note, never a blocker. | Blocking on old debt stalls every phase. | 01 |
| R10 | **Verdict by criteria.** `APPROVED` only when every applicable AC is traced, bug-hunt left no CONFIRMED BLOCKER/MAJOR, no other blocking finding, required gates and tests pass, and UI/visual review is done when there is UI. Otherwise `CHANGES_REQUESTED`, or `BLOCKED` when required evidence is missing. | Criteria make the verdict reproducible. | 04 |
| R11 | **Rounds and escalation.** The same finding returned a third time → escalate with both positions; nobody waives it. Disputes go through the workspace's objection path. | Endless ping-pong wastes both roles. | 04 |
| R12 | **No cosmetic demands.** Require changes only for a concrete problem; style preferences and cleanups are non-blocking notes (cleanups for code-simplification). | Cosmetic blocking erodes trust in real findings. | 03 |
| R13 | **Revision-bound report.** Written to the workspace's report location, naming the revision, checks run with results, findings and verdict; handed to the next role. | The report is the evidence trail for the phase. | 05 |
| R14 | **Delta re-review.** After a fix, review the new revision: the fix diff, the findings it claims to close, and rerun the checks it affects. | A fix can break something else; only rerun checks prove it did not. | 04 |

**Never "not adopted":** R1, R2, R3, R6, R7, R10.
