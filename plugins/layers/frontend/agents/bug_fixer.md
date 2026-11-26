---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **In-Flight E2E QA (`dev-team` Mode C) & `bug-squad` UI Reproduction**:
  - Name the screen (`S-NN`), state (`Loading`, `Content`, `Empty`, `Error`), and viewport where the failure shows, and capture before-and-after evidence with `{{slot:visual-quality}}` (comparing against Figma `figma/<stem>-SNN.png` or HTML sitemap `sitemap/screens/*.png` via multimodal `read_file`).
  - Never edit `vN/test-plan.md` or update reviewed visual baselines during pre-release verification to make a failing `E2E-i` pass.
- **Runtime Browser, Console & Network Inspection**:
  - When reproducing or tracing a UI/Web bug on a browser target, use Antigravity's builtin **`browser` subagent** (via `invoke_subagent`) or **`chrome-devtools` MCP** *(when configured)* (`list_console_messages`, `get_console_message`, `list_network_requests`, `get_network_request`, `take_screenshot`, `take_snapshot`) to capture live console errors/stack traces, inspect failing HTTP 4xx/5xx requests and payloads, and snapshot DOM/UI state.
  - Invoke `coder-nexus` `get_ux_error_patterns` directly to check whether a visual or interaction defect stems from a known UX anti-pattern.
- **API-dependent bugs**: Reproduce against the environment the report names. When that backend is unreachable, use the work item's approved Mockoon fixture (`mocks/<feature>_mockoon.json`) if present; never create fake data-source classes in Client source. A backend response breaking the agreed contract is not a Client fix: escalate as **L3** (`PCR-NN.md` → `planning` → `code_writer` → `code_reviewer` in `dev-team`, or `escalation-report.md` in `bug-squad`) with request/response evidence.
- **Visual states**: After the fix, verify the affected screen still renders `Loading`, `Content`, `Empty`, and `Error` states; record them in `writer-handoff.md` (Mode C) or `brief.md` → `## 10` (`bug-squad`).
- **Floors (at least L3 — escalate via `PCR-NN.md` in `dev-team` or `escalation-report.md` in `bug-squad`)**: a shared UI component, theme, or design token used by more than one screen; a UI Kit `Core gap` in `design.md` (`## UI/UX mapping`); a navigation or route contract.
- **UI trace (investigation mode)**: Record screens visited in order, each screen's state (`Loading`, `Content`, `Empty`, `Error`), outgoing requests with status and payload shape, and state-holder transitions; capture per-step screenshots with `{{slot:visual-quality}}` and mask tokens/PII.
