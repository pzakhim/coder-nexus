---
name: root-cause-debugging
description: Systematic root-cause debugging for Flutter applications - deterministic reproduction, layer isolation (UI, Cubit, Domain, Data), regression testing, and escalation criteria.
---

# Flutter Root-Cause Debugging

Systematically isolate, diagnose, and resolve defects in Flutter applications using scientific debugging workflows. Never patch symptoms or paper over exceptions with blanket catches.

Findings and resolution reports align with [work-item-contract handoff-and-status section 9](../work-item-contract/references/handoff-and-status.md).

## 1. Five-Step Debugging Protocol

```
1. REPRODUCE    Write a deterministic unit, cubit, or widget test reproducing the defect
       │
2. ISOLATE      Binary search down through UI -> Cubit -> Domain -> Data layers
       │
3. HYPOTHESIZE  Formulate testable explanation based on data flow and state transitions
       │
4. FIX & VERIFY Fix the root cause; confirm regression test passes and no breaks
       │
5. ESCALATE     If the cause is an upstream package or backend defect, follow stop criteria
```

## 2. Layer Isolation Matrix

| Symptom | Probable Layer | Investigation Tool | Reference |
|---|---|---|---|
| Red screen / `RenderFlex overflowed` | Presentation (UI Layout) | Flutter DevTools Inspector, constraints inspection | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| `setState() called after dispose()` | Lifecycle / Async callback | Check `mounted` flag, uncancelled timers/streams | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| Screen stuck on loading spinner | Cubit / State transition | `bloc_test`, verify error state emission | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| Missing data / `TypeError` on load | Data (JSON Parsing) | Check model `fromJson` and `parse*` helpers | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |
| HTTP 401 retry loop | Data (Network Auth) | Check `ApiService.refreshToken` implementation | [02-isolate-and-hypothesize](references/02-isolate-and-hypothesize.md) |

## 3. Fast Diagnostic Commands

```bash
# 1. Run targeted regression test
flutter test test/modules/<feature>/<path_to_test>.dart

# 2. Run with verbose stack traces
flutter test --reporter=expanded test/modules/<feature>/
```
