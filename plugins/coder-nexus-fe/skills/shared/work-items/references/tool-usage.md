# Hub tool use from a Flutter Client

Tools read Hub or Client evidence; they never approve a user gate or prove runtime Flutter behavior.

Read `architecture_profile.mode` from the approved design (brief for phase-free work) and pass it explicitly as `architecture_profile` to both architecture validators. Accepted values are `imespro`, `external-structured`, `external-standard`; omission retains legacy iMESPro rules. For external projects verify Client foundations, naming, error/state contracts and DI against the approved mapping. Company examples and Kit matching below apply only where that selected foundation exists; external-standard may use standard Flutter widgets.

| Tool | When and input | Required interpretation |
|---|---|---|
| `huly_get_my_tasks`, `huly_get_task_detail` | Spec Writer reads real Huly tasks when referenced or requested; detail uses a real ID | Read-only. A missing Huly task may be replaced by actual user requirements, never an invented ticket |
| `get_project_structure` | Spec Writer/Planning/Writer compare a root or module blueprint with the actual Client | Blueprint is guidance; inspect Client routing, state, DI and files before naming paths |
| `get_ux_error_patterns` | When loading, empty, auth, timeout or validation states apply | Use only relevant patterns; derive Visual AC from real visual and product decisions |
| `validate_proposal_spec` | Saved feature `requirements.md`, `codebase-notes.md`, `change-impact.md`, or `design.md` | Enforces straight-line docs (zero `Option A/B`, `Open Questions`, `TBD`, or `OPEN` `Q-NN` rows) and `D-NN` traceability; `valid: true` is structural only; generic `brief.md` uses the work-item contract checklist |
| `validate_plan_slices` | Only a versioned feature plan with sibling `requirements.md`, `design.md` and linked phase files | It cannot validate a brief-only item or phase-free plan; approval still comes from user |
| `validate_architecture_code` | Reviewer checks changed Dart source with correct layer | Lexical `UNVERIFIED` needs Client analyzer/inspection; never treat it as a compile pass |
| `validate_module_architecture` | Reviewer checks an affected complete module | For scoped UI work use N/A with reason and inspect changed imports/state directly |

For one viable verified Kit component choose it; for several viable components ask the user; for none check Client shared widgets and composition before a private widget. Never copy Kit code, invent a package API or call catalog failure an empty result. Commands and runtime targets come from the actual Client, not examples in the Hub.
