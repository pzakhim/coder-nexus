# 06 — Report

Rule D14 of [root-cause-debugging](../SKILL.md). Why this file exists: reviewers verify the reasoning, not just the diff, and ruled-out paths save them the same detour.

Put this block in the Code Writer hand-off (or in the `FIXED` reply to a finding per `review-resolution`), with one evidence row per executed check per `evidence-standard` and the row format in [handoff-and-status §4](../../work-item-contract/references/handoff-and-status.md). Redact secrets and personal data.

```
Symptom:      <what failed, where; reported by (task check / reviewer / bug-hunt / Test Runner / user)>
Triage:       CODE_WRONG (task <id>, Expected: <...>)
Reproduction: uv run pytest <id> -q (cwd <service root>) @ <revision> -> exit 1, <key output>
Root cause:   <the defect, app/<file>.py:<line>, why it happened>
Fix:          <what changed and why at this layer>
Regression:   <tests/...::test_name> - FAIL with fix undone, PASS with fix (both runs recorded)
Evidence:     rows per evidence-standard (regression, original reproduction, suite, ruff, mypy, task check)
Ruled out:    H2 <why>, H3 <why>
Debug tags:   rg -n "[DEBUG-xxxx]" -> no matches; ruff --select T10,T20 -> clean
```

On a stop ([04](04-stop-and-escalate.md)) the same block carries `Root cause: unknown — best guess <...>`, the fix attempts `n/3`, and the missing evidence, with status `BLOCKED` or `NEEDS_CONTEXT`.

A defect you noticed but did not fix (outside Scope / Files) is reported as a finding graded per [handoff-and-status §9](../../work-item-contract/references/handoff-and-status.md) (`BLOCKER`/`MAJOR`/`MINOR` + `CONFIRMED`/`PLAUSIBLE`, with a `given … → when … → then …` scenario), not fixed silently.

Every fix is a new revision: earlier review and test evidence for the touched code is invalid until rerun.
