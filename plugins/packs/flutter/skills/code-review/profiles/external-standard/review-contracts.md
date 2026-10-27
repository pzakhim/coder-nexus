# External Standard Code Review Contracts

> Topic: Reviewing standard Flutter widgets, Dart 3 sealed states, DI/routing, and external-standard Hub validator profile (external-standard profile)

## 1. `external-standard` Hub Validator & Architecture Audit

Always pass `architecture_profile: "external-standard"` to `validate_architecture_code` and `validate_module_architecture`. Universal Clean Architecture rules (`DOM-001..003`, `DAT-003`, `PRE-001`, `PRE-003`, `PRE-005`, `MOD-006`, `CRX-001..004`) apply:

| Audit Area | Reviewer Check (`external-standard`) | Violation Severity |
|---|---|---|
| **Domain Purity (`DOM-001..003`)** | Domain entities and use cases have zero imports of `package:flutter/*`, HTTP clients, or DTO classes | `BLOCKER` |
| **Safe JSON & Numeric Parsing (`DAT-003`)** | DTO `fromJson` methods cast numeric fields safely via `num` (`(json['x'] as num?)?.toDouble()`) and guard nullable fields without raw `!` bang operators | `BLOCKER` / `MAJOR` |
| **Dart 3 State Exhaustiveness** | UI `switch` expressions/statements over `sealed class` states handle `Initial`, `Loading`, `Success`, and `Failure` branches explicitly without swallowing errors in a wildcard `_` branch | `MAJOR` |
| **Widget & Resource Lifecycle (`PRE-003`)** | `StatelessWidget` / `StatefulWidget` screens and child widgets dispose all owned controllers, `FocusNode`s, `StreamSubscription`s, and `Timer`s, and guard post-`await` `BuildContext` usage with `if (!context.mounted) return;` | `BLOCKER` / `MAJOR` |
