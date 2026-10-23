# Mode: planning — Core gaps, trade-offs, test data (`planning`, Gate 2)

Use with [SKILL.md](../SKILL.md). Business behavior is settled at Gate 1; this mode only asks what the design needs. Present the options of each trade-off with `solution-options` (technical options), then close the choice here as a `D-NN`.

## 1. Before asking

- Read `requirements.md` and `codebase-notes.md` (`## 1. Decision Log`, `## 2. Glossary`, `## 3. Verified Baseline Facts`) first. Never re-ask a `D-NN`.
- Run the codebase scans of `{{slot:architecture-design}}` and record facts in `## 3`. Facts are looked up, never asked (SKILL §4).

## 2. What to queue

| Topic | Queue a `Q-NN` when |
|---|---|
| Core gap | The foundation (`{{slot:core-package-usage}}`) lacks a component, service or pattern the behavior needs: build it privately, extend the foundation, or change the behavior. |
| Core risk | A requirement conflicts with the existing architecture or with overlapping business logic in the code. |
| Architecture trade-off | Two or more viable layer splits, state approaches, data flows or integration shapes remain after the scan. |
| Component choice | Several viable kit or framework components match one need. One viable match is chosen without asking and recorded as a fact. |
| API contract shape | spec_writer settled the business input/output, but the technical contract (paths, error codes, pagination) has more than one viable form. |
| Test data | Always, once per work item (§3). |

Each technical `Q-NN` names the `G-NN` it serves. If a goal cannot be met technically, raise it with `spec_writer` and the user; never narrow a goal silently.

## 3. Test data convention

Agree one row per behavior so fixtures and developer unit tests share a contract:

| Case | Agree with the user |
|---|---|
| Pass / Default | Which input or data set represents the normal success. |
| Fail | Which input triggers each error the requirements name (validation, permission, server error). |
| Empty | Which input returns no data, and what the user then sees. |

Record the agreement as one `D-NN` (several rows may be confirmed together when they only restate the requirements; see [batch-confirm](batch-confirm.md)).

## 4. Role rules

- Never write `design.md` with `Option A / Option B`, an open question or an unconfirmed trade-off. Close every technical row first, then write `design.md` in one straight line citing `D-NN`; `## Goal alignment` (DESIGN-007) maps each goal to the design.
- Record `Owner: planning` on every row and decision this mode creates.
- A business-rule, permission or scope question found while designing goes to spec_writer's queue (Gate 1 again when it changes a goal or scope).
- Keep `codebase-notes.md` in the version folder for the whole `vN/` lifecycle; code_writer, code_reviewer, test runner and docs writer read it.
