---
name: root-cause-debugging
description: How the Code Writer or Bug Fixer of a Flutter / Dart app resolves a known failure - a red flutter test or flutter analyze check triaged as CODE_WRONG, a CONFIRMED review or bug-hunt finding, a NullCheckError, RenderFlex overflow, TypeError in JSON parsing, Cubit state transition hang, or setState-after-dispose crash - by reproducing it with one deterministic CLI command, reading the first real error frame, testing 3-5 ranked falsifiable hypotheses one at a time, fixing the root cause at the owning layer with a Red-to-Green regression test, never green-washing, and stopping or escalating on time. Use whenever a check is red or a defect must be fixed, before changing any code.
---

# Root-Cause Debugging — Flutter / Dart

Answer one question: **why does this fail, and what is the smallest change at the owning layer that makes it impossible?** A fix without a known cause moves the bug instead of removing it.

All CLI gates (`PASS` / `FAIL`, with `NOT_RUN` / `BLOCKED` / `UNVERIFIED` and `CODE_WRONG` / `PLAN_WRONG` / `NEEDS_CONTEXT`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

---

## 1. CLI Diagnostic & Verification Gates (`PASS` / `FAIL`)

Every verification check below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Gate | Command | Purpose |
|---|---|---|
| **1. Focused Reproduction** | `flutter test test/modules/<feature>/<path>_test.dart --plain-name "<test name>"` | Reproduce the failure deterministically (`exit != 0` on red, `exit 0` on green) (**D1**, **D8**) |
| **2. Verbose Stack / Output** | `flutter test --reporter=expanded test/modules/<feature>/<path>_test.dart` | Read full stack traces, `blocTest` diffs, and widget error details (**D2**) |
| **3. Leftover Debug Sweep** | `rg -n "DEBUG-|print\(|debugPrint\(|debugger\(" lib test` | Prove zero `[DEBUG-xxxx]` tags, `print()`, `debugPrint()`, or `debugger()` remain (**D11**) |
| **4. Static & Suite Verification** | `dart format --output=none --set-exit-if-changed lib test && flutter analyze && flutter test test/modules/<feature>/` | Verify formatting, static analysis, and module test suite pass after the fix (**D7**, **D8**) |

---

## 2. The 6-Step Debugging Loop

1. **Reproduce (`D1`–`D3`):** Run one non-interactive CLI command (`flutter test <file> --plain-name "<name>"`) that fails reliably with the reported symptom; read the **first** real error down to the first frame under `lib/` ([01](references/01-reproduce-read-and-tools.md)).
2. **Minimize & Isolate (`D4`, `D13`):** Strip non-essential inputs/widgets, diff against `<last-green-sha>` (`lib/`, `test/`, `pubspec.lock`), trace callers (`rg -n` / GitNexus), or bisect in a disposable worktree ([01](references/01-reproduce-read-and-tools.md), [02](references/02-isolate-and-hypothesize.md)).
3. **Hypothesize (`D5`, `D6`):** Write 3–5 ranked falsifiable hypotheses (`H1`..`H3`), test one variable at a time across `Widget → Cubit/Bloc/Notifier → UseCase → Repository/Mapper/DataSource`, and trace the bad value backwards to its origin ([02](references/02-isolate-and-hypothesize.md)).
4. **Fix & Regression Test (`D7`–`D9`, `D11`):** Turn the minimal case into a Red-to-Green regression test (`{{slot:unit-testing}}`), apply the smallest fix at the owning layer (`{{slot:clean-architecture}}`), and remove all `[DEBUG-xxxx]` logs ([03](references/03-fix-escalate-and-report.md)).
5. **Stop & Escalate (`D10`, `D12`):** Report environment/backend blockers as `BLOCKED`, missing context as `NEEDS_CONTEXT`, stop after **3 failed fix attempts**, and route contract/design/dependency/scope changes to `change-control` ([03](references/03-fix-escalate-and-report.md)).
6. **Report (`D14`):** Record Symptom, Triage, Reproduction, Root cause, Fix, Regression Red/Green rows, Ruled-out hypotheses, and Debug-tag cleanup proof ([03](references/03-fix-escalate-and-report.md)).

---

## 3. Core Debugging Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **D1** | **Reproduce first.** One fast, deterministic, unattended CLI command asserting the reported symptom. Cannot reproduce → `NEEDS_CONTEXT`. | A fix you cannot see fail and pass is a guess. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D2** | **Read the first real error.** Inspect the root exception and the first stack frame under `lib/`; redact secrets/tokens (`<REDACTED>`). | Fixing framework frames (`package:flutter/...`) wastes time on where the error surfaced, not why. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D3** | **One failure at a time.** Resolve the first failing test or analyzer error before inspecting downstream cascades. | Parallel fixes hide which change resolved what. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D4** | **Minimize and isolate.** Cut JSON fields, state transitions, or widget subtrees to the smallest failing case; bisect only in a disposable worktree. | The minimal case becomes the permanent regression test. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D5** | **3–5 ranked falsifiable hypotheses, one variable per probe.** Log `H1`..`H3` with prediction, probe, and `CONFIRMED` / `RULED OUT`. | Multiple simultaneous edits make results ambiguous. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D6** | **Fix the root cause, not the symptom.** Trace a null/wrong value or missing state backwards caller-by-caller to its source and check the diff for sibling bugs. | Scattering `?? ''` or magic layout offsets in the widget leaves the mapper/state bug intact. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D7** | **Smallest fix at the owning layer, inside task scope.** Place the fix per `{{slot:clean-architecture}}`; no unrelated refactoring. | Wrong-layer fixes break again and bloat review. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D8** | **Red-to-Green regression test.** Prove the test fails for the reported reason without the fix and passes with the fix (`{{slot:unit-testing}}`). | Without a regression test, the defect returns silently. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D9** | **Never green-wash.** No `skip: true`, weakened assertions, regenerated broken goldens, empty `catch (_) {}`, fake fallback data, `dynamic`/`// ignore:`, or `Future.delayed`. | Green-washing hides the bug and removes the safety net. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D10** | **Environment vs. code.** Missing `.env`, offline emulator, stale codegen (`.g.dart`/`.freezed.dart`), or live backend 500/schema breach → `BLOCKED`, never a client workaround. | Client workarounds for broken environments or backend bugs corrupt app logic. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D11** | **Remove temporary instrumentation.** Tag temporary logs `[DEBUG-xxxx]` and prove zero leftovers (`print`, `debugPrint`, `debugger()`) via `rg -n` and `flutter analyze` (`{{slot:clean-code}}` `C3`). | Leftover debug logs leak data and fail static analysis. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D12** | **Time-box (3 attempts) and escalate.** Stop after 3 failed fix attempts (`BLOCKED`); route contract/UI-design/dependency/scope changes to `change-control`. | Endless attempts burn context and violate approval gates. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D13** | **Use non-interactive tracing tools.** Use GitNexus (`query`, `context`, `impact`) and `rg -n` (`EXTEND` vs `INIT`); never invoke `debugger()` in unattended test runs. | Interactive pauses hang CLI test runners. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D14** | **Report the root-cause analysis.** Include the structured Debug Report block and Red/Green evidence rows in the hand-off. | Reviewers verify causal reasoning, not just the diff. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |

---

## 4. Reference Guides

| Topic | Reference |
|---|---|
| `EXTEND` vs `INIT` rule, reproduction hierarchy, reading Flutter/Dart stack traces, untrusted log redaction, and `flutter test`/`analyze`/`bisect`/tracing CLI commands | [01 — Reproduce, Read & Tools](references/01-reproduce-read-and-tools.md) |
| Layer isolation (`Widget → Cubit → UseCase → Data`), 3–5 ranked falsifiable hypotheses, tagged `[DEBUG-xxxx]` cleanup, and Flutter/Dart Symptom → First Moves → Cause matrix | [02 — Isolate & Hypothesize](references/02-isolate-and-hypothesize.md) |
| Red-to-Green regression fix, Never Green-Wash table, Environment (`BLOCKED`) vs Code, 3-attempt time-box, `change-control`, Debug Report, and `BLOCKER`/`MAJOR`/`MINOR` review grading | [03 — Fix, Escalate & Report](references/03-fix-escalate-and-report.md) |
<!-- {{profile_references}} -->

---

## 5. Relationship with Other Skills

- **Cold defect hunting vs. known failure fixing**: `{{slot:bug-hunt}}` finds unknown defects; this skill fixes known failures.
- **Regression test authoring**: `{{slot:unit-testing}}`, `{{slot:visual-quality}}`, and `{{slot:verification}}`.
- **Layer ownership & clean craft**: `{{slot:clean-architecture}}`, `{{slot:clean-code}}`, and `{{slot:secure-coding-standards}}`.
- **Task loop & gate escalation**: `incremental-implementation`, `change-control`, and `evidence-standard`.
