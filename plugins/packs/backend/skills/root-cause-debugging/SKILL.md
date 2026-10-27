---
name: root-cause-debugging
description: How the Code Writer or Bug Fixer of a Backend (Python 3.12+ / FastAPI / Pydantic v2 / SQLAlchemy 2.x async / Alembic / PostgreSQL) service resolves a known failure - a red pytest, ruff, or mypy check triaged as CODE_WRONG, a CONFIRMED review or bug-hunt finding, a failing request, a 500 traceback, a broken Alembic migration, or an N+1/slow query - by reproducing it with one deterministic CLI command, reading the first real error, testing 3-5 ranked falsifiable hypotheses one at a time, fixing the root cause at the owning layer with a Red-to-Green regression test, never green-washing, and stopping or escalating on time. Use whenever a check is red or a defect must be fixed, before changing any code.
---

# Root-Cause Debugging — Backend (Python / FastAPI)

Answer one question: **why does this fail, and what is the smallest change at the owning layer that makes it impossible?** A fix without a known cause moves the bug instead of removing it.

All CLI gates (`PASS` / `FAIL`, with `NOT_RUN` / `BLOCKED` / `UNVERIFIED` and `CODE_WRONG` / `PLAN_WRONG` / `NEEDS_CONTEXT`) and review severities (`BLOCKER` / `MAJOR` / `MINOR`) follow `shared_contracts/flags_and_statuses.md` and `work-item-contract` (`references/handoff-and-status.md` §9).

---

## 1. CLI Diagnostic & Verification Gates (`PASS` / `FAIL`)

Every verification check below is **binary (`exit 0` = `PASS`, `exit != 0` = `FAIL`)**:

| Gate | Command | Purpose |
|---|---|---|
| **1. Focused Reproduction** | `uv run pytest tests/unit/<path>/test_<module>.py::test_<name> -q` | Reproduce the failure deterministically (`exit != 0` on red, `exit 0` on green) (**D1**, **D8**) |
| **2. Verbose Stack / Locals** | `uv run pytest <id> -vv -s --tb=long --showlocals --log-cli-level=DEBUG` | Read the full first traceback and local variables without opening `--pdb` (**D2**) |
| **3. Leftover Debug Sweep** | `uv run ruff check --select T10,T20 app tests && rg -n "DEBUG-" app tests` | Prove zero `breakpoint()`, `pdb`, `print()`, or `[DEBUG-xxxx]` tags remain (**D11**) |
| **4. Static & Suite Verification** | `uv run ruff check app tests && uv run mypy app tests && uv run pytest tests/unit -q` | Verify lint, static types, and unit suite pass after the fix (**D7**, **D8**) |

---

## 2. The 6-Step Debugging Loop

1. **Reproduce (`D1`–`D3`):** Run one non-interactive CLI command (`uv run pytest <file>::<test> -q`) that fails reliably with the reported symptom; read the **first** chained exception down to the first frame under `app/` ([01](references/01-reproduce-read-and-tools.md)).
2. **Minimize & Isolate (`D4`, `D13`):** Strip non-essential inputs/fixtures, diff against `<last-green-sha>` (`app/`, `tests/`, `alembic/`, `uv.lock`), trace callers (`rg -n` / GitNexus), or bisect in a disposable worktree ([01](references/01-reproduce-read-and-tools.md), [02](references/02-isolate-and-hypothesize.md)).
3. **Hypothesize (`D5`, `D6`):** Write 3–5 ranked falsifiable hypotheses (`H1`..`H3`), test one variable at a time, and trace the bad value backwards caller-by-caller to its origin ([02](references/02-isolate-and-hypothesize.md)).
4. **Fix & Regression Test (`D7`–`D9`, `D11`):** Turn the minimal case into a Red-to-Green regression test (`{{slot:unit-testing}}`), apply the smallest fix at the owning layer (`{{slot:clean-architecture}}`), and remove all `[DEBUG-xxxx]` logs ([03](references/03-fix-escalate-and-report.md)).
5. **Stop & Escalate (`D10`, `D12`):** Report environment problems as `BLOCKED`, missing context as `NEEDS_CONTEXT`, stop after **3 failed fix attempts**, and route contract/schema/dependency/scope changes to `change-control` ([03](references/03-fix-escalate-and-report.md)).
6. **Report (`D14`):** Record Symptom, Triage, Reproduction, Root cause, Fix, Regression Red/Green rows, Ruled-out hypotheses, and Debug-tag cleanup proof ([03](references/03-fix-escalate-and-report.md)).

---

## 3. Core Debugging Rules (Mandatory Compliance)

| Rule | Principle | Why | Reference |
|---|---|---|---|
| **D1** | **Reproduce first.** One fast, deterministic, unattended CLI command asserting the reported symptom. Cannot reproduce → `NEEDS_CONTEXT`. | A fix you cannot see fail and pass is a guess. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D2** | **Read the first real error.** Read the root exception above `The above exception was the direct cause` down to the first frame under `app/`; redact secrets (`<REDACTED>`). | Fixing the bottom wrapper (`HTTPException`, `DBAPIError`) wastes time on the wrong line. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D3** | **One failure at a time (`pytest -x`).** Resolve the first failure before inspecting downstream cascades. | Parallel fixes hide which change resolved what. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D4** | **Minimize and isolate.** Cut inputs/fixtures to the smallest failing case; diff since last green; run `git bisect` only in a disposable worktree. | The minimal case becomes the permanent regression test. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D5** | **3–5 ranked falsifiable hypotheses, one variable per probe.** Log `H1`..`H3` with prediction, probe, and `CONFIRMED` / `RULED OUT`. | Multiple simultaneous edits make results ambiguous. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D6** | **Fix the root cause, not the symptom.** Trace the bad value backwards caller-by-caller to its source and check the diff for sibling bugs. | Symptom patches (`or 0`, broad `except`) move the bug and leave siblings intact. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D7** | **Smallest fix at the owning layer, inside task scope.** Place the fix per `{{slot:clean-architecture}}`; no unrelated refactoring. | Wrong-layer fixes break again and bloat review. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D8** | **Red-to-Green regression test.** Prove the test fails for the reported reason without the fix and passes with the fix (`{{slot:unit-testing}}`). | Without a regression test, the defect returns silently. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D9** | **Never green-wash.** No `@pytest.mark.skip`/`xfail`, weakened assertions, `except Exception: pass`, fake fallbacks, `Any`/`# type: ignore`, `asyncio.sleep`, or `# noqa`. | Green-washing hides the bug and removes the safety net. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D10** | **Environment vs. code.** Unreachable PostgreSQL, missing env var, unapplied Alembic migration, or drifted `.venv` → `BLOCKED`, never a code workaround. | Code workarounds for broken environments break everyone else. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D11** | **Remove temporary instrumentation.** Tag temporary logs `[DEBUG-xxxx]` and prove zero leftovers with `rg -n` and `ruff --select T10,T20` (`{{slot:clean-code}}` `C3`). | Leftover debug logs leak data and clutter output. | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| **D12** | **Time-box (3 attempts) and escalate.** Stop after 3 failed fix attempts (`BLOCKED`); route contract/schema/dependency/scope changes to `change-control`. | Endless attempts burn context and violate approval gates. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |
| **D13** | **Use non-interactive tracing tools.** Use GitNexus (`query`, `context`, `impact`) and `rg -n` (`EXTEND` vs `INIT`); never run `--pdb` or `breakpoint()` in agent shells. | Interactive debuggers hang unattended CLI execution. | [01-reproduce-read-and-tools](references/01-reproduce-read-and-tools.md) |
| **D14** | **Report the root-cause analysis.** Include the structured Debug Report block and Red/Green evidence rows in the hand-off. | Reviewers verify causal reasoning, not just the diff. | [03-fix-escalate-and-report](references/03-fix-escalate-and-report.md) |

---

## 4. Reference Guides

| Topic | Reference |
|---|---|
| `EXTEND` vs `INIT` rule, reproduction hierarchy, reading chained tracebacks, untrusted log redaction, and `pytest`/`alembic`/`bisect`/tracing CLI commands | [01 — Reproduce, Read & Tools](references/01-reproduce-read-and-tools.md) |
| Diff/layer isolation, 3–5 ranked falsifiable hypotheses, tagged `[DEBUG-xxxx]` cleanup, and FastAPI/SQLAlchemy/Pydantic/Alembic Symptom → First Moves → Cause matrix | [02 — Isolate & Hypothesize](references/02-isolate-and-hypothesize.md) |
| Red-to-Green regression fix, Never Green-Wash table, Environment (`BLOCKED`) vs Code, 3-attempt time-box, `change-control`, Debug Report, and `BLOCKER`/`MAJOR`/`MINOR` review grading | [03 — Fix, Escalate & Report](references/03-fix-escalate-and-report.md) |

---

## 5. Relationship with Other Skills

- **Cold defect hunting vs. known failure fixing**: `{{slot:bug-hunt}}` finds unknown defects; this skill fixes known failures.
- **Regression test authoring**: `{{slot:unit-testing}}` and `{{slot:verification}}`.
- **Layer ownership & clean craft**: `{{slot:clean-architecture}}`, `{{slot:clean-code}}`, and `{{slot:secure-coding-standards}}`.
- **Task loop & gate escalation**: `incremental-implementation`, `change-control`, and `evidence-standard`.
