# 04 — Hub validator usage for a Flutter Client

Moved from the core `work-items` tool-usage reference; applies only to Flutter Clients.

Read `architecture_profile.mode` from the approved design (brief for phase-free work) and pass it explicitly as `architecture_profile` to both architecture validators (`validate_architecture_code`, `validate_module_architecture`). Accepted values are `imespro`, `external-structured`, `external-standard`; omission retains legacy iMESPro rules. For external projects verify Client foundations, naming, error/state contracts and DI against the approved mapping. Company examples and Kit matching apply only where that selected foundation exists; external-standard may use standard Flutter widgets.

- `validate_architecture_code`: Reviewer checks changed Dart source with the correct layer. Lexical `UNVERIFIED` needs Client analyzer/inspection; never treat it as a compile pass.
- Tools never prove runtime Flutter behavior.
