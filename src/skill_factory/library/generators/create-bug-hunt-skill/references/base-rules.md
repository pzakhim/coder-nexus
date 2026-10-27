# Base Rules (Mandatory Across Every Workspace)

Generalised from Coder Nexus bug-hunt rules (`H1`–`H14`). Every rule is mandatory compliance and is adapted to the workspace's stack, read-only commands, and report location.

## 1. Mandatory Bug-Hunt Rules (`H1`–`H14`)

| # | Rule | Why | Goes into |
|---|---|---|---|
| **H1** | **One question:** with which input or state does this change produce a wrong result, a crash, a hang, a leak, a data-scope breach, or a security hole? Compliance, style, and complexity are out of scope. | Mixing compliance into the hunt drowns real defects in noise. | `SKILL.md`, `01` |
| **H2** | **Fixed revision.** Record `BASE_REVISION` and `REVIEW_REVISION` plus the staged, unstaged, and untracked files of the item; review exactly that tree. | Findings must refer to code that will actually ship, not a moving target. | `01` |
| **H3** | **Whole context and callers.** Read each changed hunk with its whole enclosing function/class/module; for each changed public symbol (signature, return type, nullability, raised errors, state shape, route, serialized key), find and read its callers. A broken caller outside the diff is in scope. | Most regressions show up in callers, not in the changed lines. | `01` |
| **H4** | **Cold pass first.** Hunt from the code before reading requirements, design, or plan; read them afterwards only to decide whether a suspicious behavior is intended. | Knowing the intent makes the reader see what the code should do instead of what it does. | `01` |
| **H5** | **Seven dimensions.** Walk the scope once per dimension and write every suspicion down as `file:line — hypothesis`. | A systematic walk finds what an intuitive read skips. | `01` |
| **H6** | **Disprove every candidate.** Trace the real path from an entry point to the line, reading guards, defaults, and framework behavior; use read-only commands where they decide it. Never modify application code or tests during the hunt. | A candidate that survives an honest attempt to refute it is worth the reader's time. | `02` |
| **H7** | **No scenario, no finding.** Every finding states `given <input/state> → when <action> → then <wrong result>` with concrete values. "Might be fragile" is not a finding. | Scenarios are reproducible and turn directly into regression tests. | `02` |
| **H8** | **Confidence classes.** `CONFIRMED` (path traced end to end or a read-only command demonstrated it), `PLAUSIBLE` (depends on something not visible — name what would confirm it), Rejected (drop silently). | Readers must know how certain a finding is. | `02` |
| **H9** | **Unified Severity.** `BLOCKER` (data loss/corruption, scope breach, authorization bypass, crash/hang on a normal path, approved behavior broken), `MAJOR` (wrong result/crash on a realistic edge path, resource/lifecycle leak), `MINOR` (rare or self-correcting defect). | One unified scale across Code Writer and Reviewer avoids negotiation. | `03` |
| **H10** | **Effort follows the item.** `quick` (Code Writer self-check, small item: dimensions 1–4 on changed hunks, cap 5), `standard` (every phase review: dimensions 1–7, cap 10), `deep` (high-risk code or a phase returned twice: dimensions 1–7 + callers one level further, no cap). | Effort matched to risk keeps reviews fast where they can be and thorough where they must be. | `SKILL.md`, `03` |
| **H11** | **Report format.** One row per finding (`ID`, `Pass`, `Severity`, `Confidence`, `File:line`, `Problem`, `Failure scenario / evidence`, `Fix direction`), most severe and `CONFIRMED` first; end with the `bug-hunt:` summary line naming effort and dimensions covered. | A fixed format is easy to act on and to compare across rounds. | `03` |
| **H12** | **Verdict impact.** `CONFIRMED` `BLOCKER`/`MAJOR` blocks approval (`REQUEST_CHANGES`); `PLAUSIBLE` `BLOCKER` blocks (`BLOCKED`) until the named evidence arrives; other `PLAUSIBLE` go to the writer as questions; `MINOR` does not block alone. The same finding returned a third time escalates instead of looping. | Clear consequences stop endless review rounds. | `03` |
| **H13** | **Roles.** Reviewer: `standard`/`deep`, strictly read-only, writes findings to the review report (`RV-NN`). Code Writer: `quick` self-check after targeted checks pass, fixes `CONFIRMED` findings inside the approved scope **with the missing test first**, lists open `PLAUSIBLE` in the hand-off; a fix that changes behavior/API/design goes back to planning (`change-control`). | The writer catches cheap bugs early; the reviewer stays independent. | `03` |
| **H14** | **Cleanups are notes.** Reuse, simplification, or efficiency without a failure are listed below the table as `NOTE: <path:line> — <cleanup>` for `code-simplification` and never block or count toward the cap. | Keeps the defect list strictly about defects. | `01`, `03` |

---

## 2. Unified Verification Gates & Severity Scale

- **Read-Only CLI Verification Gates (`PASS` / `FAIL` / `NOT_RUN`):**
  - Any read-only command run during disproof (`H6`) is recorded with its exact command, exit code, and `PASS` or `FAIL` status.
  - Never claim a check passed without running it; an unrun command is `NOT_RUN`.
- **Single Finding Severity Scale (`BLOCKER` / `MAJOR` / `MINOR`):**
  - Never invent `P0`–`P3` or ad-hoc severity labels. Both `bug-hunt` (Pass 2) and `code-review` (Pass 1) use `BLOCKER` / `MAJOR` / `MINOR`.
