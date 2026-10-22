# Goal candidates (Stage 1A-G, before the question)

Draft everything below from the Source Inventory. Nothing here is asked yet; it is the content of the goal question.

## 1. Read-back

Restate the request in your own words in two or three lines: what is wanted, for whom, and why, as far as the sources say. Then add what the intake found that bears on it:

- how the touched parts work today (from the codebase scan);
- anything that would change what is asked or how hard it is: a **constraint** (an existing rule, a data scope, a blocked stack), a **conflict** between sources, or a **cheaper path** (an existing screen or service that already does most of it).

A cheaper path is offered as a candidate the user can pick with Edit or Narrow, never applied on your own.

## 2. Hypothesis and confidence

Write your best read of the outcome in one sentence with an honest confidence:

```text
Read: planners need to see which work orders are blocked by a pending ECN, so they stop releasing them.
Confidence: ~55% - missing: REQ-MFG-ECN-03 (UNREACHABLE), whether "blocked" includes draft ECNs.
```

- Below ~70%, always name what is missing on the same line; that list becomes the "Missing" line of the sufficiency summary.
- Check the number: if you cannot predict how the user will answer the next three questions you would queue, the number is too high.
- Low confidence because of a missing source that could change the goals means you ask for the source in the goal question before the goals can be confirmed.

## 3. Goals (1-3)

```text
G-NN: <actor> can <result> so that <business value>
Success signal: <observable check anyone can run without reading the code>
```

Restate frame, and where each line lands:

| Frame line | Lands in |
|---|---|
| Outcome + User | the `G-NN` goal sentence |
| Why now | the "so that" clause, and `## 1. Scope & Alignment` → current baseline & problem |
| Success | the success signal column |
| Out of scope | Non-goals |

Success signals are measurable and technology-agnostic: a user-visible result, a count, a time, a rate ("a planner sees the blocking ECN on the work order without opening another screen"). Not "the endpoint returns 200" or "the cache hit rate rises"; those are design details for Gate 2.

When the source speaks in buzzwords ("make it faster", "modern", "robust"), do not accept them as a goal. Turn them into a candidate signal you can check ("search results appear in under 1 s for 10k records") and let the user correct the number.

Derive goals from ticket and parent titles, the purpose of the PO document, the AC and the comments. Order them by value; `G-01` is the one the user would keep if only one shipped.

## 4. Non-goals

Things the sources mention that this work item will not deliver, each with a reason: closed children, `BLOCKED` stacks, "later" items, siblings of a child ticket, parts the user ruled out. A topic that is in scope but not yet clear is **not** a non-goal; queue it as a `Q-NN`.

## 5. Anti-goals

Outcomes that count as failure **even if the feature works**: "planners must re-enter data that already exists", "existing monthly report totals change", "a warehouse user sees another site's orders". Look for them in the sources (complaints in comments, constraints in PO docs, data scopes in the codebase). Propose one or two; skip the line when none is credible.

After confirmation, write them under `## 0. Goals` as a `- **Anti-goals**:` line below Non-goals, and turn each into a guard rule or negative scenario in the 1B draft: a `BR-NN` or `AC-NN` that cites the `G-NN` it protects, so it is tested like any other criterion.

## 6. Conflicts

List each source conflict from the inventory that affects a goal, with both sides cited. The user settles it in the goal answer; the rest become `Q-NN`.

## Split check

Before settling on goals, look at the AC you can already see. Propose splitting into linked work items when:

- groups of AC have their own users or data and could ship and be checked separately;
- one group could be dropped without rewriting the others' rules;
- you would need more than 3 goals to cover them.

Show the split as a short table (`Work item | Delivers | Depends on`) with a build order that has no cycles, and recommend which one this work item takes. The others are recorded under Non-goals ("tracked as linked work item ...") and in the header's related items. Do not create the other work items yourself; that is the user's call.
