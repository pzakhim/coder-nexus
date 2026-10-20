# AGENTS.md — AIFactory-Coder

Instructions for agents working in this **Hub repository**. Treat current code, tests, and the [plugin manifest](plugins/core/bundle_manifest.json) as implementation evidence.

## 1. Responsibility and boundaries

- **Coder Nexus / AIFactory-Coder (Hub):** Python MCP server in `src/coder_nexus/`, read-only Huly adapter, Clean Architecture references and validators, the `core-usage` skill that routes agents to the iMESPro packages (`app_core`, `app_util`, `app_ui_kit`), plugin sources split into stack-neutral `plugins/core/`, shared `plugins/layers/`, stack packs in `plugins/packs/<stack>/` (composed by `coder_nexus.plugin_build`; see the [installation guide](docs/guides/installation.md#how-a-projection-is-built)) and the legacy `plugins/coder-nexus-be/`, shared handshake contracts in `plugins/shared_contracts/`, and an initial VS Code plugin-sync extension. Use `uv` for Python commands.
- **Antigravity Flutter Client (separate workspace):** owns its `.env`, resolved package dependencies, approved feature documents under `docs/features/<module>/<feature>/vN/`, implementation under `lib/`, tests, and revision-bound evidence. The iMESPro packages live next to the Client (`../app-core`, `../app-util`, `../app-ui-kit`); `coder-nexus setup flutter --check` proves they are resolved.
- **Huly:** a source of real task details and acceptance criteria. Hub Huly operations are read-only. A real user request can also supply requirements when no Huly task exists.

Do not describe the agent profiles as an autonomous code generator. They are host-executed instructions with explicit approvals and verification gates. Do not claim Figma live extraction, full Flutter logic coverage, or feature E2E acceptance without evidence.

## 2. Read before changing code

1. Read [README.md](README.md) and [docs/guides](docs/guides/) for current capability and acceptance status.
2. Inspect actual source, tests, plugin agent/skill contracts, and the target Client when a change crosses the Hub–Client boundary. Do not treat template imports, paths, or old examples as verified Client APIs.
3. Check `git status` and preserve unrelated or pre-existing user changes. Keep Markdown links clickable and repository-relative where possible.

## 3. Implementation rules

- Follow the **Ponytail** approach: solve the current problem with the smallest clear change; avoid unused layers, speculative abstractions, and duplicated Kit widgets.
- Manage Python with `uv`. Keep MCP lookups and validators free of Client writes. Catalog search/spec lookup must remain read-only.
- For Flutter work, use the `core-usage` skill: pass `coder-nexus setup flutter --check`, read `../app-*/guidance/GUIDE.md`, then decide per need. Reuse a core API or `app_ui_kit` widget when its GUIDE "Use when" fits, even if styling differs from a supplied design; ask when several fit. Otherwise write the simplest Client code under `lib/modules/<feature>/` (shared folder only when two or more modules need it) and record a Core gap in `design.md`. A failed setup gate is a blocker.
- Keep Domain independent of Flutter and Data implementations; use the real Client's Data, Presentation, routing, state, and DI conventions. Add only the layers required by the approved behavior.
- For feature work, honor the three actual user approval gates for requirements, design, and plan. Code Writer implements one ready phase; Reviewer inspects the same revision; Test Runner supplies independent evidence. Neither a validator result nor an agent may self-approve a gate. `NOT_RUN`, `BLOCKED`, and `UNVERIFIED` are not `PASS`.
- Report exact checks and their limits.

## 4. Ask before changing

- Dependencies in `pyproject.toml`.
- Public schemas, signatures, or behavior of the existing MCP tools, including the original five core tools.
- The Component Registry schema.

## 5. Prohibited actions

- Do not store Huly, Figma, or developer credentials in this repository or Git. Credential persistence belongs to the Client workspace `.env` and must remain untracked.
- Do not implement Huly create, update, or delete operations.
- Do not fabricate business records, mock design/task data, or hardcoded fallback data to make a missing source look successful. Fail explicitly when required evidence is unavailable.
- Do not edit, copy, or rewrite `app_core` / `app_util` / `app_ui_kit` code into the Client, invent a package API, or mark an unrun analyzer, test, build, or visual check as passed.

## 6. Current verification boundary

The Hub currently exposes **8 MCP tools** (the `flutter_ui_kit` catalog tools were removed on 2026-10-13) and the plugin bundles **6 agent profiles** (5 delivery roles plus Docs Writer) and **20 public skills**. The Hub suite passed **188/188 tests** on 2026-10-17. The example Client resolved a pinned Kit package, passed analysis and an import probe, and passed its two existing Flutter tests on 2026-10-07. A real approved feature replay through specification, code, review, runtime visual inspection, and acceptance testing has **not** run. Keep that distinction in code review and documentation.

## 7. Release and tagging protocol

Automated testing, `.vsix` packaging, Open VSX publication (`IMP-AIFactory.coder-nexus`), and GitHub Release generation are managed by [`.github/workflows/release.yml`](.github/workflows/release.yml).

- **Single Source of Truth (SSOT):** The version is synchronized between [`plugins/core/bundle_manifest.json`](plugins/core/bundle_manifest.json) (`plugin_version`) and [`package.json`](package.json) (`version`) via [`scripts/sync_version.py`](scripts/sync_version.py). Tests dynamically assert compatibility across manifest and package metadata; never re-introduce hardcoded version strings into test suites.
- **Decide what a push includes:** On every push request, inspect `git status --short --branch`, the current branch and upstream, the working diff, and commits ahead of the target remote branch. Stage only files belonging to the requested work with `git add -- <paths>`; inspect `git diff --cached` and `git diff --cached --check` before committing. Preserve unrelated modified and untracked files, credentials, generated files, and other agents' work. Do not push unrelated existing commits without the user's authorization. Push the current task branch to its intended remote branch; never assume it is `main`. Do not use `git add .`, `git push --all`, or `git push --tags`.
- **Decide whether to tag:** A routine push sends the scoped commit(s) without a version tag. Create a release tag when the user requests a release/version or a verified extension/plugin milestone is ready to publish. A documentation or CI-only fix after an existing release does not retroactively change that tag. Do not move or reuse a published tag. If the scope or release readiness is uncertain, finish the reviewable changes and ask before publishing a release.
- **For a release:**
  1. Check the latest local and remote tags (`git tag --sort=-v:refname` and `git ls-remote --tags origin`) and choose the next semver version based on the change. Confirm the target tag does not exist on either side.
  2. Run `python3 scripts/sync_version.py <new_version>` (release notes are generated on the GitHub Release), and refresh only the authorized Client workspace projection. Do not install globally when the user requested workspace-only installation.
  3. Run `uv run pytest -q` and any checks required by the change. Stage only release files and requested work, inspect the staged diff, then commit. Create an **annotated** tag on that exact verified commit with `git tag -a vX.Y.Z -m "Coder Nexus vX.Y.Z"`.
  4. Push the intended branch and **that exact tag** together, for example `git push --atomic origin HEAD:refs/heads/<branch> refs/tags/vX.Y.Z`. Do not push unrelated local tags. If the remote rejects the push, resolve the rejection and revalidate; do not force-push or retag a published version.
  5. Check the tag-triggered [release workflow](.github/workflows/release.yml), the Open VSX version, and the GitHub Release with its `.vsix` asset. A pushed tag or packaged local VSIX alone does not prove publication. If a later step fails after Open VSX succeeded, repair and retry that release; do not create a new version merely to bypass a duplicate publication error.
