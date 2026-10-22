# Where delivery facts are found

Read-only. Skip what the workspace does not have.

| Fact | Typical places |
|---|---|
| Layout | `.agents/stack.json`, top-level folders, workspace files (`pnpm-workspace.yaml`, `melos.yaml`, `go.work`, `settings.gradle`) |
| Past plans | `.superpowers/work-items/*/v*/implementation-plan.md`, `phases/*.md`; `docs/features/**`; their `as-built.md` and review reports show rework |
| Checks | `Makefile`, `package.json` scripts, `pyproject.toml` tool sections, `analysis_options.yaml`, CI files (`.github/workflows`, `.gitlab-ci.yml`) |
| Targeted tests | Test runner filters: `pytest <path> -k`, `jest <path> -t`, `go test ./pkg/... -run`, `flutter test <file>` |
| Readiness | Migration runner, seed scripts, `docker-compose*.yml`, mock configs (Mockoon, MSW, WireMock), feature-flag service config, test-account docs |
| Change size | `git log --shortstat -50`, PR history if available; review reports and follow-up fix commits show which sizes needed rework |
| Global constraints | Item-wide values in approved `requirements.md` (BR-NN) and `design.md` of past work items: limits, version floors, formats, fixed copy |
| Review-focus gaps | Defects found in review or acceptance that no planned check covered (`as-built.md`, review and QA reports, bug tickets) |
