---
name: bug-hunt
description: Defect hunting across 7 review dimensions for Flutter code - lifecycle leaks, async races, layout overflows, null crashes, rebuild bottlenecks, missing UX feedback, and security risks.
---

# Flutter Bug Hunt

Proactively hunt for hidden defects in Flutter code changes before they reach review or production. Severity (`BLOCKER` / `MAJOR` / `MINOR`), confidence (`CONFIRMED` / `PLAUSIBLE`), verdict impact, and effort caps follow [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## 1. The 7 Review Dimensions

| Dimension | Common Defect Pattern | Severity | Reference |
|---|---|---|---|
| **1. Lifecycle & State** | `setState` after dispose, undisposed controllers, Cubit in-place mutation. | **BLOCKER / MAJOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **2. Async & Concurrency** | Double-tap duplicate API calls, uncancelled streams, race conditions. | **MAJOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **3. Layout & Responsive** | RenderFlex overflow, fixed widths clipping on small phones or tablets. | **MAJOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **4. Data & Null Safety** | Reading `DataState.data` on failure, `!` bang operator, missing JSON fallbacks. | **BLOCKER / MAJOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **5. Rebuilds & Performance** | Logic in `build()`, missing `const`, rebuild storms from unbounded `BlocBuilder`. | **MAJOR / MINOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **6. UX & Accessibility** | Silent failure (no user feedback), stuck spinners, hit targets < 48dp. | **MAJOR / MINOR** | [05-bug-patterns](references/05-bug-patterns.md) |
| **7. Security & Input** | Plaintext token storage, unvalidated deep links, SSL check bypasses. | **BLOCKER** | [05-bug-patterns](references/05-bug-patterns.md) |

## 2. Reporting Syntax

Record verified findings using the standard single-line format:

```text
bug-hunt: <file:line> | <severity> <confidence> | <dimension> | <description> | <fix>
```

Example:
```text
bug-hunt: lib/modules/orders/presentation/screens/order_screen.dart:42 | BLOCKER CONFIRMED | lifecycle | TextEditingController created without dispose() call | add dispose() override in _OrderScreenState
```

See [03-effort-severity-report](references/03-effort-severity-report.md) for grading and reporting rules.
