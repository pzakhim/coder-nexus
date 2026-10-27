# Mode: Spec — Gate 1 Pre-Gate Verification (`spec_writer` in `dev-team`)

Reviews `requirements.md` (or `brief.md`) and `codebase-notes.md`, alongside extracted Figma outputs (`.superpowers/sources/<ISSUE-ID>/figma/` `tokens.json`, `<stem>.spec.json`, `<stem>-SNN.png`) when the item has UI impact. Pass 1 (`validate_proposal_spec` = `PASS`) must be clean before starting Pass 2. Findings use `GR-S-NN`.

When present in `.agents/skills/`, also load:
- `.agents/skills/domain-knowledge/` — glossary, entities, roles, and data scopes (for `S2`).
- `.agents/skills/requirements-specification/` — mandatory edge cases (`references/02-edge-cases-and-writing-rules.md`) and workspace Gate 1 review questions (`references/03-gate-review-and-verification.md`) for `S5`.

---

## Pass 2 — Spec Checklist (`S1`–`S7`)

### S1. Vague Words (`[Ambiguity]`)
Every adjective or adverb that a tester cannot verify deterministically is a finding (`BLOCKER` inside a `BR-NN` or `AC-NN`, `MAJOR` elsewhere), unless the same sentence or a cited `D-NN` defines a concrete threshold, named state, visible message, or rule:

| Banned Unless Quantified | What to Require Instead |
|---|---|
| `fast`, `quick`, `slow`, `responsive`, `instant`, `real-time` (`nhanh`, `mượt`, `tức thì`) | Concrete time budget and measurement point (e.g., list visible within `2 s` on reference device) |
| `intuitive`, `easy`, `simple`, `user-friendly`, `clean`, `modern`, `seamless` (`thân thiện`, `dễ dùng`, `đơn giản`) | Observable workflow step, label, default value, or maximum tap/step count |
| `robust`, `reliable`, `stable`, `resilient`, `gracefully`, `properly`, `correctly` (`ổn định`, `đúng đắn`) | Exact failure condition and what the user sees / what happens to data afterward |
| `secure`, `safe` (`an toàn`, `bảo mật`) | Specific actor role, data scope, and forbidden action |
| `scalable`, `efficient`, `optimal`, `flexible` (`linh hoạt`, `tối ưu`) | Volume/concurrency limit or explicit reason it is in scope |
| `appropriate`, `reasonable`, `sufficient`, `as needed`, `etc.`, `some`, `many`, `usually`, `normally` (`hợp lý`, `phù hợp`, `đầy đủ`, `v.v.`) | Exhaustive list, concrete value, or explicit condition |

Also flag verbs without an object/outcome (*"handle the error"*, *"support filters"*) as `BLOCKER`, and near-duplicate `BR-NN` or `AC-NN` rows as `MINOR`.

### S2. Terminology Drift (`[Conflict]` / `[Gap]`)
- Every domain noun in `## 0. Goals`, `BR-NN`, scenarios, `AC-NN`, and `## Workflows` must match `codebase-notes.md` → `## 2. Glossary` (and `domain-knowledge` when present).
- Two words for one concept, one word for two concepts, or an entity/state term missing from the Glossary is `MAJOR` (`BLOCKER` when a role, permission, or financial/quantity term drifts).
- Screen IDs (`S-NN`) in `## Workflows` must match `## Screens & Visual Sources` exactly (`BLOCKER`).

### S3. Internal Conflicts (`[Conflict]`)
Compare each pair and grade contradictions:

| Pair Compared | What to Flag | Severity |
|---|---|---|
| `BR-NN` vs `AC-NN` | An `AC-NN` that a `BR-NN` forbids, or a `BR-NN` no `AC-NN` observes | `BLOCKER` |
| `AC-NN` vs `## 4.` Scenarios | A scenario outcome that differs from its corresponding `AC-NN` | `BLOCKER` |
| `## Workflows` vs `## Screens & Visual Sources` | Missing `S-NN` screen row, different step order, or unreferenced screen | `BLOCKER` |
| `Scope out` / Non-goals vs `BR`/`AC`/`W-NN` | Out-of-scope behavior that still appears as an active requirement | `BLOCKER` |
| `## 2. Actors & Permissions` vs `AC-NN` | An actor performing an action without permission, or an unused actor role | `BLOCKER` |
| Confirmed `D-NN` vs Spec Text | Spec text contradicting a locked `D-NN` in `codebase-notes.md` | `BLOCKER` |

### S4. Coverage Map Across `grilling` Dimensions
For each `grilling` queue group (`SKILL.md` §2.2 groups 1–6; group 7 is `N/A` at Gate 1), mark coverage as `Clear` (settled by text or `D-NN`), `Partial` (`MAJOR`), or `Missing` (`BLOCKER`):

| Group | Topic | Status (`Clear` / `Partial` / `Missing`) | Evidence (Section, IDs) |
|---|---|---|---|
| 1 | Job type and goals (`G-NN`) | | |
| 2 | Scope, actors, permissions | | |
| 3 | Main workflow (`W-NN`) and branches | | |
| 4 | Data and API source, fields, errors | | |
| 5 | Observable states (4 visual states for UI), lifecycle | | |
| 6 | Negative, boundary, and edge cases | | |

### S5. Requirement-Quality Questions (~30 Spec-Text Checks)
Write concise questions testing **what the spec text states** (never runtime test steps starting with *Verify/Test/Click*):
- Tag each question `[Gap]`, `[Ambiguity]`, or `[Conflict]` with the `G-NN` / `BR-NN` / `AC-NN` / `W-NN` it checks.
- Any question answered *"no"* becomes a `BLOCKER` (if two developers would build different behavior) or `MAJOR` finding.

### S6. Scenario Classes per Goal (`primary`, `alternate`, `exception`, `recovery`)
Verify each `G-NN` (and each UI `W-NN`) covers:
1. `primary` (main success path)
2. `alternate` (valid alternative path/actor/entry)
3. `exception` (invalid input, missing permission, empty data, API failure, timeout)
4. `recovery` (post-exception state: retry, input preservation, rollback, zero data loss)
- A missing `exception` or `recovery` class on a flow that mutates data is `BLOCKER`; other missing classes without a `D-NN` exclusion are `MAJOR`.

### S7. Primary Failure / Upset Case
Identify the single failure that would upset the user most (data loss, wrong calculation, unauthorized visibility, blocked daily workflow). It must have an explicit `AC-NN` and scenario with concrete values (`BLOCKER` if missing).

---

## S8. Pass 3 — Cold-Reader Subagent Check (Reader Plays `planning`)

After Pass 1 (`PASS`) and Pass 2 (`0 BLOCKER`, `0 MAJOR`), spawn one fresh read-only subagent with this exact prompt:

```text
You are the Planning agent (Tech Lead) of this team. You have been handed the
Gate 1 documents of a work item and must next write its technical architecture
design (design.md). You cannot talk to the author, and you have no chat history.

Read:
- {{vN_path}}/requirements.md
- {{vN_path}}/codebase-notes.md

You may open files these documents cite by path, read-only, only to verify that
a cited fact exists. Do not use the codebase to fill gaps left by the documents.
Do not write or modify any file.

Report only the questions you would still need answered before you could design
this without guessing: places where you would have to guess about behavior,
business rules, actors, data, visual states, or scope, and a wrong guess would
change the architecture.
For each question provide:
1. The question
2. Where it comes from (section, BR-NN / AC-NN / G-NN / W-NN)
3. Why the answer changes the design
4. What you would guess if forced
Rank by importance, at most 10.

Skip technical choices that belong to Planning at Gate 2, anything explicitly
delegated to Planning, and wording nits.
If nothing important is left, reply: nothing important left
```

Sort every returned question per [`SKILL.md` §5](../SKILL.md#5-pass-3--fresh-cold-reader-subagent-check) (`Answered already`, `Minor — Agent's call`, or `User's call — OPEN Q-NN`).
