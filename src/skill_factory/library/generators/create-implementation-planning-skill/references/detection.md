# Delivery Facts Detection (Read-Only)

Inspect the workspace read-only to ground `IP1`–`IP17` in real repository evidence. Skip artifacts the workspace does not use.

| Fact | Where to Inspect | Used For |
|---|---|---|
| **Module & Layer Layout** | `.agents/stack.json`, top-level directories, workspace manifests (`pyproject.toml`, `package.json`, `pubspec.yaml`, `pnpm-workspace.yaml`, `melos.yaml`, `go.work`, `Cargo.toml`) | `IP1`, `IP3` |
| **Delivered Plans & Rework History** | `.superpowers/work-items/*/v*/implementation-plan.md`, `phases/*.md`, `docs/features/**`, `as-built.md`, review reports | `IP1`, `IP11`, `IP12` |
| **Static Analysis & Check Commands** | `Makefile`, `package.json` scripts, `pyproject.toml`, `analysis_options.yaml`, CI workflows (`.github/workflows/`, `.gitlab-ci.yml`) | `IP4`, `IP6` |
| **Targeted Test Runners** | Runner filter syntax with `cwd`: `uv run pytest <path> -k`, `flutter test <file>`, `npm test -- <path>`, `go test ./pkg/... -run` | `IP4`, `IP17` |
| **`PHASE-00` Readiness Tooling** | Migration runners, seed scripts, `docker-compose*.yml`, mock configs, feature-flag configs, `.env.example`, test-account fixtures | `IP5`, `IP8`, `IP9` |
| **Commit Size & Checkpoint History** | `git log --shortstat -50`, branch naming and commit subjects (`<SUB-TICKET>`, `<PARENT-TICKET>`, `PHASE-NN`), follow-up fix commits | `IP7`, `IP12` |
| **Global Constraints in Specs** | Item-wide constants in approved `requirements.md` (`BR-NN`) and `design.md` (`D-NN`): limits, timeouts, version floors, formats, fixed copy | `IP10` |
| **Uncovered Edge-Case Defects** | Review findings (`BLOCKER` / `MAJOR` / `MINOR`), QA reports, and bug tickets where an unvalidated input or failure mode lacked a task check | `IP11` |
