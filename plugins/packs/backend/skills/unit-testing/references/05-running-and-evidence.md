# 05 — Running and evidence

Detail for [unit-testing](../SKILL.md). Rules U12, U14. Real commands and proof that the new test ran are what turn "tests pass" into evidence.

## Command prefix

Run from the folder holding `pyproject.toml` (the service root; in a monorepo, the service's own folder).

| Found | Prefix | Focused run example |
|---|---|---|
| `uv.lock` (baseline) | `uv run` | `uv run pytest tests/unit/application/test_orders.py -q` |
| `poetry.lock` | `poetry run` | `poetry run pytest tests/unit/application/test_orders.py -q` |
| `requirements*.txt` only | activated venv | `python -m pytest tests/unit/application/test_orders.py -q` |

## Commands

| When | Command (cwd = service root) |
|---|---|
| Red / green for one test (task check) | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_order_not_cancellable -q` |
| Prove it was collected | same with `-v` (the test id is listed with `PASSED` / `FAILED`) or `--collect-only -q` |
| After the task, the touched module | `uv run pytest tests/unit/application/test_orders.py -q` |
| Phase end, full unit suite | `uv run pytest tests/unit -q` |
| Lint and types on test code too | `uv run ruff check tests app` and `uv run mypy app tests` (when the workspace runs mypy on tests) |
| Coverage (`pytest-cov`, installed by default) | `uv run pytest tests/unit --cov=app --cov-report=term-missing -q` |

Do not introduce a new coverage failure threshold (`--cov-fail-under`) without a plan task. Reason: a strict threshold number is a project decision (`D-NN`), and coverage counts lines run, not behaviors proven.

The focused command must match the task-level check in `incremental-implementation` and the task's **Acceptance Criteria** line. Reason: the reviewer reruns exactly that command on the same revision.

## Confirm the new test ran

- The `-v` output lists `tests/unit/...::test_<name> PASSED` (or `FAILED` on the red run).
- The summary line count rose by the number of tests you added: read `N passed, M skipped`.
- A skip, `xfail`, `xpass`, a deselected test, a missing dependency or `no tests ran` (exit code 5) is **not** a pass and not a red.
- `pytest-randomly` is installed by default via `coder-nexus setup tools --pack backend` to catch hidden state ordering bugs; record the printed seed of a failing run and rerun with `-p randomly --randomly-seed=<seed>`. Reason: an order-dependent failure must be reproducible; disabling the plugin (`-p no:randomly`) hides it.

## Red and green

For a test-first task the task's **Expected** states both runs ([plan-and-task-contract §2](../../work-item-contract/references/plan-and-task-contract.md)). Record both as evidence rows ([handoff-and-status §4](../../work-item-contract/references/handoff-and-status.md), `evidence-standard`):

| Claim | Command (+cwd) | Revision | Exit code | Key output | Result |
|---|---|---|---|---|---|
| Task 2.1 red: cancel shipped order not refused | `uv run pytest tests/unit/application/test_orders.py::test_cancel_order_when_already_shipped_raises_order_not_cancellable -q` (cwd: `service/`) | `abc1234` | 1 | `Failed: DID NOT RAISE <class 'OrderNotCancellable'>` | `FAIL` (expected red) |
| Task 2.1 Expected met | same | `def5678` | 0 | `1 passed` | `PASS` |

Then compare the real output with **Expected** and triage `MATCH` / `CODE_WRONG` / `PLAN_WRONG` ([plan-and-task-contract §3](../../work-item-contract/references/plan-and-task-contract.md)). Never edit the test, the check or the **Expected** line to make the output match.

## Results that are not PASS

| Situation | Status | Reason |
|---|---|---|
| Command not run (tool missing, no time, environment absent) | `NOT_RUN` with the reason | A check that did not run proves nothing |
| Cannot run without something outside your authority | `BLOCKED`, name the blocker | The coordinator must change something first |
| A claim with no executed check | `UNVERIFIED` | Never becomes `PASS` |

## TDD mode

Failing test first follows the table in [SKILL.md](../SKILL.md#when-the-test-comes-first); a task that says otherwise explicitly wins. In test-first work the red row is recorded before any green row for the same test.
