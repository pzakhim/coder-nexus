# Working with an existing project (P1–P5)

Read this in Step 1 for any project that already has code, and always in Update mode.

## P1 — Read related skills and docs first

Before proposing anything, look for what the project already decided:

```bash
ls .agents/skills .claude/skills 2>/dev/null
rg -l -i "clean.?code|architecture|folder.?structure|boundar" CLAUDE.md AGENTS.md docs .agents .claude 2>/dev/null
```

- A `clean-code` skill (or similar) usually owns **naming and size thresholds**. Use its numbers in `04` and link to it instead of the defaults; state who owns what.
- Architecture/structure docs (e.g. `docs/standards/*`) are sources: link them, do not contradict them silently.
- Record in the Context Card: related skills found, thresholds found, docs found.

## P2 — Reuse existing gates

Find the checks that already enforce architecture:

- Architecture tests (`tests/architecture`, `*boundar*`, `test_*import*`), import-linter / dependency-cruiser / ESLint boundary configs, CI steps, check scripts inside skills.
- Put them into `05-dependency-rules.md` (what each checks, how to run it) and into the SKILL checklist.
- Do **not** suggest a new lint tool when a gate already covers the rule; suggest one only for rules no gate covers.

## P3 — Protect inbound links and uncommitted work (Update mode)

Before renaming, moving or deleting any file of the existing skill:

1. List inbound links from the rest of the repo:
   ```bash
   rg -n -o "<skill-dir>/(references|scripts|assets)/[A-Za-z0-9_./-]+" -g "*.md" -g "*.py" -g "*.sh" . | rg -v node_modules | rg -v '^./<skill-dir>/'
   ```
2. Show the user the list and ask: update those links, or keep the old file names.
3. Check `git status` for uncommitted changes in the skill and in files you would touch. Read the **working copy** (not `HEAD`), and before deleting a modified file confirm every change in `git diff HEAD -- <file>` is carried into the new files.
4. When updating links, change only the link targets/labels; never reformat the user's files.
5. Use `git mv` for files that only move, so history is kept.

## P4 — Locked architecture: document, do not re-design

If the architecture is already enforced by tests/scripts or clearly established:

- Step 3 does **not** offer 2–3 competing trees. Instead present:
  - the **current tree** as the target (with real module/feature names),
  - **drift** between the old docs and the real code (wrong example names, missing modules, folders outside the whitelist),
  - **open decisions** only where the rules are silent (e.g. how to split an over-long repository).
- Research is limited to 2 confirming sources.
- Drift becomes either a doc fix (docs were wrong) or known debt (code is wrong); ask the user which when unclear.

## P5 — Keep project-specific rules

The existing skill often holds rules the generic frame does not have (e.g. a no-wrapper rule, a root-file rule, scope matrices, plan formats).

- Keep each one as its own reference file (`shared/` if it applies to BE and FE), translated if needed but **not weakened or merged away**.
- Volatile facts (migration status, counts to update, known debt) go into `shared/incremental-adoption.md` (or `incremental-adoption.md` in the flat layout), never into timeless rule files.
- Before handing over, build a coverage table **old rule → new file** and check that no rule was dropped. Show it to the user if anything moved substantially.
