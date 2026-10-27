# Debug item contract

The single home of what the bug-fixing department (**`bug-squad`**) exchanges: the debug folder, the two triage scales, status words and zero-re-ask hand-offs, plus investigation-only items (§8). The department orchestration lives in **`bug-squad`** (routing L1/L2/L3), `debug-investigation` (read-only investigation), and `fix-planning` (writing the documents); they point here and never restate it. Formats shared with work items (evidence row, finding severity) stay in [handoff-and-status](handoff-and-status.md).

## 1. Folder

One reported bug = one folder `${workspaceFolder}/.superpowers/debug/<bug-slug>/`.

| File | Written by | Read by | When |
|---|---|---|---|
| `brief.md` ([template](../templates/bug-brief.md.tpl)) | `bug_fixer`; the coordinator writes only `## 6` → **User confirmation** and the `## 10` → **Code review (L2)** and **Test Runner** round lines | user (level confirmation), `test_runner` | Every bug |
| `fixing-plan.md` ([template](../templates/fixing-plan.md.tpl)) | `bug_fixer` | user, `code_reviewer`, `test_runner` (scope only) | L2 only |
| `escalation-report.md` ([template](../templates/escalation-report.md.tpl)) | `bug_fixer` | `dev-team` → Spec Writer (zero-re-ask L3 handoff) | L3 only |
| `diagnosis.md` ([template](../templates/diagnosis.md.tpl)) | `bug_fixer` | user; `bug-squad` → `bug_fixer` when the user then asks for a fix | Investigation items only (§8) |
| `reviews/review_<FIX_REVISION>.md` | `code_reviewer` | coordinator, `bug_fixer`, `test_runner` | L2 only, one per reviewed revision |
| `evidence/<revision>/` | `bug_fixer` (reproduction, fix checks, self bug-hunt), `test_runner` (verification report) | coordinator, user, `code_reviewer` | Every run |

- `<bug-slug>` is `<ticket-id>-<short-kebab-title>`, or `<yyyymmdd>-<short-kebab-title>` without a ticket. A slug is never reused.
- A bug that comes back after `VERIFIED_FIXED` opens a new folder that links the old one. Reason: evidence is tied to exact revisions.
- An L3 bug moves on as a work item under `.superpowers/work-items/` in **`dev-team`**; the debug folder stays as its read-only source (`escalation-report.md`) and is not edited further.

## 2. Severity S1–S4 (impact on users)

| Level | Means |
|---|---|
| **S1** | Crash, data lost or wrong, or a main flow is blocked |
| **S2** | A main function is wrong and there is no workaround |
| **S3** | Wrong, but a workaround exists |
| **S4** | Cosmetic: layout, text, styling |

Severity decides only the branch: an S1 or S2 bug found in production takes the hotfix path of `git-preflight`. It never decides the fix level. It is not the finding severity `BLOCKER` / `MAJOR` / `MINOR` of [handoff-and-status](handoff-and-status.md) §9, which grades code findings.

## 3. Fix level L1–L3 (routing)

| Level | Conditions | Files | Flow |
|---|---|---|---|
| **L1 – Quick patch** | **All** hold: a trivial change (one line, one config value, or one file in one layer); the expected behavior is clear; no shared code is touched | `brief.md` | fix → unit test → `test_runner` |
| **L2 – Local fix** | **All** hold: contained in one feature, possibly across its layers; no change to an API contract, stored data or shared code | `brief.md` + `fixing-plan.md` | fix by plan → unit test → `code_reviewer` → `test_runner` |
| **L3 – Escalate** | **Any** holds: an API contract changes (request, response, error codes, or other consumers); a schema, migration or data correction is needed; more than one screen or flow, or a shared component or utility, is affected; a business rule or flow changes, or the spec does not say what is correct; authorization or data scope is involved; the root cause is not confirmed | `escalation-report.md` | no fix; zero-re-ask handoff to `dev-team` |

Routing rules:

1. **Change, not defect**: if the request changes intended behavior rather than restoring it, it is L3. Reason: a behavior change needs a spec the user approves.
2. **Floors**: each layer and pack names code areas whose change is at least L3 (in its `bug_fixer` profile). A floor only raises a level.
3. **Doubt**: between two levels, take the higher one.
4. **Loop limit**: the third `STILL_BROKEN` on the same bug makes it L3.
5. **No level before reproduction**: a bug that is not reproduced gets no level.
6. **Confirmation**: `bug_fixer` proposes S and L with the matched conditions; the user confirms or changes them. The answer is recorded in `brief.md` → `## 6. Level decision`. No fix starts before it.
7. **Growth**: if the fix outgrows the confirmed level (a new file outside scope, a shared symbol, a contract), stop, return `TRIAGED` with the new proposal, and wait for the user again.
8. **Triage test**: a reproduction test written during triage stays uncommitted. After an L1/L2 confirmation it moves to the fix branch with the debug folder, the way `git-preflight` carries an uncommitted spec. For L3 its path and content are quoted in `escalation-report.md` → `## 2` and it is removed from the working tree. Reason: no code lands before the level is confirmed.
9. **Review loop (L2)**: every new `FIX_REVISION`, after `CHANGES_REQUESTED` or `STILL_BROKEN`, is reviewed again before `test_runner` runs; evidence from an older revision does not carry over. A third `CHANGES_REQUESTED` on the same bug sends it back to triage (usually L3), with both positions stated. Reason: a fix that review keeps rejecting is rarely local.

## 4. Status words

| Word | Returned by | Means | Next |
|---|---|---|---|
| `NOT_REPRODUCED` | `bug_fixer` | The reported behavior could not be produced; the attempts are recorded in `brief.md` → `## 3. Reproduction` | Coordinator asks the user for more information or closes the bug |
| `TRIAGED` | `bug_fixer` | Reproduced; root cause, impact and proposed S and L are written | Coordinator asks the user to confirm the level (one question) |
| `READY_FOR_TEST` | `bug_fixer` | L1 fix committed; reproduction check failed before and passes after; unit tests, verification and self bug-hunt run; evidence rows written | Coordinator assigns `test_runner` |
| `READY_FOR_REVIEW` | `bug_fixer` | L2 fix committed with the same evidence as `READY_FOR_TEST`, plus every `fixing-plan.md` task ticked | Coordinator assigns `code_reviewer` |
| `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED` | `code_reviewer` | Review verdict on one L2 `FIX_REVISION`, as in [handoff-and-status](handoff-and-status.md) §3 | `APPROVED` → coordinator assigns `test_runner`; `CHANGES_REQUESTED` → back to `bug_fixer` (rule 9) |
| `VERIFIED_FIXED` | `test_runner` | The reproduction no longer shows the bug and the regression checks in scope pass on the fix revision | Coordinator reports to the user and closes the bug |
| `STILL_BROKEN` | `test_runner` | The bug still shows, or a regression check in scope fails; steps, expected vs actual and evidence are attached | Coordinator returns it to `bug_fixer`; the third one triggers rule 4; for L2 the new revision is reviewed again (rule 9) |
| `DIAGNOSED` | `bug_fixer` | Investigation item done (§8): `diagnosis.md` written, captured logs saved, temporary instrumentation removed | Coordinator reports to the user; for a bug, offers `bug-squad`; otherwise closes |
| `ESCALATED` | `bug_fixer` | L3 confirmed; `escalation-report.md` written; no code changed | Coordinator starts `dev-team` with `escalation-report.md` as a zero-re-ask source |
| `BLOCKED` | any role | Cannot continue without something outside its authority (environment, access, an answer); names the blocker | Coordinator resolves the blocker before re-assigning |

`NOT_RUN`, `BLOCKED`, and `UNVERIFIED` never count as `VERIFIED_FIXED`.

## 5. Hand-offs

All hand-offs go through the coordinator running **`bug-squad`**; no agent starts another.

| From → To | Status | Carries | Lives at |
|---|---|---|---|
| User (or `debug-investigation` / `feature-testing`) → `bug_fixer` | — | The report: symptom, where it happens, expected result, environment, ticket if any; or existing `diagnosis.md` / `test-run-report.md` (ingested without re-asking) | `brief.md` → `## 1`, `## 2` |
| `bug_fixer` → user | `TRIAGED` | Reproduction evidence row, root cause, impact with evidence, proposed S and L with the matched conditions and floors | `brief.md` → `## 3`–`## 6` |
| `bug_fixer` → `test_runner` (L1), `bug_fixer` → `code_reviewer` (L2) | `READY_FOR_TEST` (L1), `READY_FOR_REVIEW` (L2) | `BASE_REVISION..FIX_REVISION` (committed, never `+dirty`); staged / unstaged / untracked scope; tasks ticked; evidence rows for the red reproduction, the green re-run, unit tests, verification and self bug-hunt; for L2 from round 2, the `review-resolution` reply table | `brief.md` → `## 10`, `evidence/<FIX_REVISION>/` (reply: `evidence/<FIX_REVISION>/review-reply.md`) |
| `code_reviewer` → coordinator (L2) | `APPROVED` / `CHANGES_REQUESTED` / `BLOCKED` | The review report in the shape of [handoff-and-status](handoff-and-status.md) §5, round `N` of 3; for `APPROVED`, the same `FIX_REVISION` goes to `test_runner` | `reviews/review_<FIX_REVISION>.md` |
| `test_runner` → coordinator | `VERIFIED_FIXED` / `STILL_BROKEN` | Per-check `PASS` / `FAIL` / `BLOCKED` / `NOT_RUN` rows; for `STILL_BROKEN`, steps, expected vs actual and evidence path | `evidence/<FIX_REVISION>/test-report.md` |
| `bug_fixer` (`bug-squad`) → `dev-team` (`spec_writer`) — **Zero-Re-Ask L3 Handoff** | `ESCALATED` | Full `escalation-report.md` (reproduction evidence, root cause, affected contracts/layers, quoted triage test) and the user's L3 confirmation. `dev-team` (`spec_writer`) ingests `escalation-report.md` directly into `codebase-notes.md` (`## 3. Verified Baseline Facts`) without re-asking symptom or reproduction steps | `escalation-report.md` |

Evidence rows use [handoff-and-status](handoff-and-status.md) §4. Self bug-hunt and review findings use §9 of the same file.

## 6. No code review for L1

L1 fixes go to `test_runner` without a Code Reviewer. This is a deliberate exception to the no-self-approval rule, limited to bugs the user confirmed as L1. It rests on four checks that stay mandatory:

1. A reproduction check that fails before the fix and passes after it.
2. The user's level confirmation (§3 rule 6).
3. A self `{{slot:bug-hunt}}` at `quick` effort on the fix diff; a `CONFIRMED` `BLOCKER` or `MAJOR` finding outside the fix scope stops the run and goes back to triage.
4. The independent `test_runner` verdict.

L2 fixes are reviewed: they cross layers and run several tasks, and `test_runner` sees behavior, not code that sits in the wrong layer, opens a security gap or breaks an untested path. `test_runner` accepts a debug item without an `APPROVED` review only when `brief.md` records a confirmed L1; an L2 item needs an `APPROVED` review of the same `FIX_REVISION`.

## 7. Never

- Fix before the level is confirmed, or outside the files listed in `brief.md` / `fixing-plan.md`.
- Split an L3 bug into several L1/L2 bugs to avoid escalation.
- Fabricate a reproduction, data or a result; report `NOT_RUN` as passed.
- Edit code on an `ESCALATED` bug.

## 8. Investigation items

Started by `debug-investigation` when the user wants to **understand** something, not fix it. Same folder rules (§1); no level is proposed and no code change is kept.

| Kind | Input | Ends with |
|---|---|---|
| **Bug** | A symptom, as in a bug report | Reproduction, root cause and impact in `diagnosis.md`, or `NOT_REPRODUCED` |
| **Trace** | A question about how a feature runs (data flow, state changes, calls made) and the scenario to run | The observed flow in `diagnosis.md` |

Temporary instrumentation (log, trace or print statements, and stack observers) is allowed, under these rules:

1. **Observe only**: it adds output, never changes behavior, logic, data or dependencies.
2. **Never committed**: it lives in the working tree only, and each statement is listed in `diagnosis.md` → `## 3` (file and line).
3. **Removed before returning**: record `git status` and `git diff` of the files before instrumenting; after removal they must show the same status and diff again. Leftover instrumentation is `BLOCKED`, never `DIAGNOSED`.
4. **No secrets in logs**: mask tokens, passwords and personal data before saving captured output.
5. **Captured output is evidence**: saved under `evidence/<revision>/` and quoted in `diagnosis.md` → `## 4`.
6. **Reproduction tests too**: a test written to reproduce or trace is a code change like any other: its path and content are quoted in `diagnosis.md` → `## 2` and it is removed from the working tree, as §3 rule 8 does for L3. A later fix writes it again from that quote.

**From diagnosis to fix (Zero-Re-Ask Handoff)**: when the user asks to fix a diagnosed bug, **`bug-squad`** hands `diagnosis.md` to `bug_fixer`. If the code is still at the revision recorded in `diagnosis.md`, its reproduction, root cause, and impact become `brief.md` → `## 3`–`## 5` without repeating the investigation or re-asking the user; otherwise the reproduction check is re-run first. The level is then proposed and confirmed as in §3.

**Never** on an investigation item: keep a code change, commit instrumentation, or propose a fix level the user did not ask for.
