# Hub tool use from a Client

Tools read Hub or Client evidence; they never approve a user gate or prove runtime Client behavior.

The architecture validators are stack-specific: read the approved design (brief for phase-free work) and follow `{{slot:code-review}}` for which validators apply to this stack and which profile argument they need. Verify Client foundations, naming, error/state contracts and DI against the approved mapping. Kit matching below applies only where the selected foundation provides a Kit.

| Tool | When and input | Required interpretation |
|---|---|---|
| `huly_get_my_tasks`, `huly_get_task_detail` | Spec Writer reads real Huly tasks when referenced or requested; detail takes an ID or a pasted Huly link and returns status, people, parent, sub-issues, comments and `sources`. Use `download: true` to save PDFs, images, attachments and readable PO documents to `.superpowers/sources/<ISSUE-ID>/` (Git-ignored, local only), then open them | Read-only. `UNREACHABLE` sources are reported to the user, never guessed. A missing Huly task may be replaced by actual user requirements, never an invented ticket |
| `get_project_structure` | Spec Writer/Planning/Writer compare a root or module blueprint with the actual Client | Blueprint is guidance; inspect Client routing, state, DI and files before naming paths |
| `get_ux_error_patterns` | When loading, empty, auth, timeout or validation states apply | Use only relevant patterns; derive Visual AC from real visual and product decisions |
| `validate_proposal_spec` | Saved feature `requirements.md`, `codebase-notes.md`, `change-impact.md`, or `design.md` | Enforces straight-line docs (zero `Option A/B`, `Open Questions`, `TBD`, or `OPEN` `Q-NN` rows) and `D-NN` traceability; `valid: true` is structural only; generic `brief.md` uses the work-item contract checklist |
| `validate_plan_slices` | Only a versioned feature plan with sibling `requirements.md`, `design.md` and linked phase files | It cannot validate a brief-only item or phase-free plan; approval still comes from user |
| `validate_architecture_code` | Reviewer checks changed source with correct layer, when `{{slot:code-review}}` lists it for this stack | Lexical `UNVERIFIED` needs Client analyzer/inspection; never treat it as a compile pass |
| `validate_module_architecture` | Reviewer checks an affected complete module | For scoped UI work use N/A with reason and inspect changed imports/state directly |

For one viable verified Kit component choose it; for several viable components ask the user; for none check Client shared widgets and composition before a private widget. Never copy Kit code, invent a package API or call catalog failure an empty result. Commands and runtime targets come from the actual Client, not examples in the Hub.
