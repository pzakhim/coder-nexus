# 02 — Goal Framing, Split Check & The Goal Question (Stage 1A-G)

Draft everything in §1–§2 from the `Source Inventory` before asking the user. Nothing in §1–§2 is asked separately; it forms the body of the single Goal Question in §3.

## 1. Drafting Goal Candidates (Stage 1A-G Prep)

### 1.1. Read-Back
Restate the request in your own words in 2–3 lines: what is wanted, for whom, and why, according to the read sources. Add what the intake found that bears on it:
- How the touched parts work today (from the read-only codebase scan or L3 `escalation-report.md`).
- Anything that changes what is asked or how hard it is: a **constraint** (existing rule, data scope, blocked stack), a **conflict** between sources, or a **cheaper path** (an existing screen, component, or service that already covers most of the need). Offer a cheaper path as a candidate the user can pick via `Edit` or `Narrow`, never apply it silently.

### 1.2. Hypothesis & Confidence
Write your best read of the desired outcome in one sentence with an explicit confidence percentage:

```text
Read: planners need to see which work orders are blocked by a pending ECN, so they stop releasing them.
Confidence: ~55% - missing: REQ-MFG-ECN-03 (UNREACHABLE), whether "blocked" includes draft ECNs.
```

- Below `~70%`, always name what is missing on the same line; that list becomes the **Missing** line of the sufficiency summary.
- Sanity-check the number: if you cannot predict how the user will answer the next three `Q-NN` questions you would queue, the confidence percentage is too high.
- Low confidence caused by a missing source that could alter the goals means you must ask for that source in the goal question before locking goals.

### 1.3. Outcome Goals (`G-01..G-03`, Maximum 3)
Format each goal as an actor + outcome + business value with an observable, technology-agnostic success signal:

```text
G-NN: <actor> can <result> so that <business value>
Success signal: <observable check anyone can verify without reading internal code>
```

| Frame Element | Where It Lands |
|---|---|
| Outcome + Actor | The `G-NN` goal statement |
| Why now / Business value | The `so that` clause, and `## 1. Scope & Alignment` → current baseline & problem |
| Success | The `Success signal` column in `## 0. Goals` |
| Out of scope | `- **Non-goals**:` under `## 0. Goals` |

- **Measurable & technology-agnostic**: A user-visible result, a count, a duration, or a rate (e.g., *"a planner sees the blocking ECN on the work order without opening another screen"*), never internal implementation details (*"endpoint returns 200"*, *"cache hit rate rises"* — those belong to Gate 2 `design.md`).
- **Probe buzzwords**: Never accept vague words (*"faster"*, *"modern"*, *"robust"*) as a goal. Convert them into a checkable candidate signal (*"search results appear in under 1 s for 10k records"*) so the user can confirm or adjust the number.
- **Order by value**: `G-01` is the primary goal the user would keep if only one shipped. Draft at most **3 goals** (`REQ-005` warns above 3).

### 1.4. Non-Goals, Anti-Goals & Conflicts
- **Non-goals**: Items mentioned in sources that this work item will **not** deliver, each with a clear reason (closed children, `BLOCKED` stacks, deferred items, sibling tickets). An unclear topic that is still in scope is a `Q-NN`, **never** a non-goal.
- **Anti-goals**: Outcomes that count as failure **even if the feature works** (e.g., *"planners must re-enter data that already exists"*, *"existing monthly report totals change"*, *"a warehouse user sees another site's orders"*). After confirmation, write them under `## 0. Goals` as `- **Anti-goals**:` and turn each into a guard `BR-NN` or negative `AC-NN` in Stage 1B citing the `G-NN` it protects.
- **Conflicts**: List each source conflict from the inventory that affects a goal, citing both sides so the user settles it in the goal answer.

---

## 2. Split Check (When Scope Is Multiple Work Items)

Before asking the goal question, inspect the visible acceptance criteria. Propose splitting into linked work items when:
1. Groups of AC serve distinct actors/data and can ship and be verified independently;
2. One group could be dropped without rewriting the others' business rules; or
3. More than 3 goals would be required to cover the batch.

Present the split as a concise table (`| Work item | Delivers | Depends on |`) with an acyclic build order, and recommend which item this `vN` tackles first. Record the remaining items under **Non-goals** (*"tracked as linked work item …"*) and in the document header. Never create the other work items without user confirmation.

---

## 3. Asking the Goal Question (Single `ask_question` Call)

Ask the Goal Question via a single `ask_question` call containing **one** question, before any other `Q-NN` (only the job-type question, when required for a non-new ticket, precedes it). Keep the body concise:

1. **Your request, in my words** — the 2–3 line read-back plus constraints, conflicts, or cheaper path (§1.1).
2. **Read & Confidence** — one line with confidence `%` and what is missing if `< ~70%` (§1.2).
3. **Sources** — counts per read status (`READ` / `UNREACHABLE` / `NOT_PROVIDED`) and every missing/unreachable source by name.
4. **Job type & size** — the `Type` (and job-type `D-NN` if asked), artifact path (`brief.md` vs `requirements.md` + `codebase-notes.md`), and any split proposal (§2).
5. **Goals (`G-01..G-03`)** — each with its observable success signal (§1.3).
6. **Non-goals, Anti-goals & Conflicts** — concise bulleted list citing sources (§1.4).
7. **Sufficiency summary** (`grilling` §2.1) — **Enough for** (what read sources settle), **Missing** (what only the user can attach/supply), **Next** (queued `Q-NN` count by topic).

### Selectable Options

| Option | Meaning |
|---|---|
| `(Recommended) Confirm goals` | Goals `G-NN`, non-goals, anti-goals, and work size stand as presented |
| `Edit goals` | User adjusts goals, scope, or supplies a missing source in their own words |
| `Narrow to G-01 only` | Keep `G-01` for this work item; move `G-02+` to Non-goals / linked work items |

*(If a missing source could change the goals, place `(Recommended)` on `Edit goals` and name the missing source.)*

### Handling the User's Reply

| User Reply | Required Action |
|---|---|
| `Confirm goals` | Record `D-NN` in `codebase-notes.md`; write `## 0. Goals` (`Status: CONFIRMED`). |
| `Narrow to G-01 only` | Record `D-NN`; move dropped goals to `- **Non-goals**:` (*"narrowed by `D-NN`"*). |
| `Edit goals` or free-text changes | Fold the changes in, re-check against sources and stack scope, and re-ask the Goal Question with the revised goals. |
| Missing document supplied | Read it, update `## 0A. Source Inventory` to `READ`, re-check goals/conflicts, and re-ask. |
| Counter-question | Answer with evidence from sources/codebase and re-ask; the Goal Question remains open. |
| Ambiguous delegation (*"sounds good"*, *"whatever you think"*, *"just start"*) | Not a valid confirmation (`GF9`). Re-ask with the concrete choice between `Confirm goals` and `Narrow to G-01 only`. |

---

## 4. Locking `## 0. Goals` & Feeding Stage 1B / `figma-intake`

1. Fill the `## 0. Goals` table in `requirements.md` (`Goal ID | Goal | Success signal | Source | Status`) without renaming headings or columns. Set `Status: CONFIRMED` and cite both the source and the confirming `D-NN`. Keep `- **Non-goals**:` and add `- **Anti-goals**:` below the table.
2. In the **same turn**, Stage 1B writes the initial `DRAFT` of `requirements.md` and `codebase-notes.md` and queues the remaining `Q-NN` (each tagged with the `G-NN` it serves).
3. Once `G-NN` are `CONFIRMED`, Stage 1A-UX (`figma-intake`) maps workflows `W-NN` and screens `S-NN` against the confirmed `G-NN` (every `W-NN` maps to a confirmed `G-NN`). When Gate 1 is later `APPROVED` and handed to `planning`, `planning` inherits `## 0. Goals` and `codebase-notes.md` directly without re-running `requirements-elicitation`.
