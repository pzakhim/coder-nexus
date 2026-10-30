---
skills:
  - {{slot:visual-quality}}
---
## Frontend rules

- **In-Flight E2E QA (`dev-team` Mode C) & `bug-squad` UI Reproduction**:
  - Name the screen (`S-NN`), state (`Loading`, `Content`, `Empty`, `Error`), and viewport where the failure shows, and capture before-and-after evidence with `{{slot:visual-quality}}`.
  - Never edit `vN/test-plan.md` or update reviewed visual baselines during pre-release verification to make a failing `E2E-i` pass.
- **Runtime Browser, Console & Network Inspection**:
  - When reproducing or tracing a UI/Web bug on a browser target, use `chrome-devtools` MCP (`list_console_messages`, `get_console_message`, `list_network_requests`, `get_network_request`, `take_screenshot`, `take_snapshot`) to capture live console errors/stack traces, inspect failing HTTP 4xx/5xx requests and payloads, and snapshot DOM/UI state.
  - Use `coder-nexus` `get_ux_error_patterns` to verify whether a visual or interaction defect stems from a known UX anti-pattern.
- **API-dependent bugs**: reproduce against the environment the report names. When that backend is not reachable, use the approved Mockoon fixture of the work item that built the screen (`mocks/<feature>_mockoon.json`) if one exists; never create fake data-source classes in the Client source. A backend response that breaks the agreed contract is not a Client fix: escalate as **L3** (`PCR-NN.md` to `planning` in `dev-team`, or `escalation-report.md` in `bug-squad`) with the request and response as evidence.
- **Visual states**: after the fix, verify that the affected screen still renders the right `Loading`, `Content`, `Empty` and `Error` states; record them in `writer-handoff.md` (`dev-team` Mode C) or `brief.md` → `## 10` (`bug-squad`).
- **Floors (at least L3 — escalate to `planning` via `PCR-NN.md` in `dev-team` or `escalation-report.md` in `bug-squad`)**: a shared UI component, theme or design token used by more than one screen; a UI Kit `Core gap` in `design.md` (`## UI/UX mapping`); a navigation or route contract.
- **UI trace (investigation mode)**: record the screens visited in order, the state each screen shows (`Loading`, `Content`, `Empty`, `Error`), the requests each screen sends with their status and payload shape, and the state-holder transitions between them. Capture screenshots per step with `{{slot:visual-quality}}`; mask tokens and personal data in captured requests.
