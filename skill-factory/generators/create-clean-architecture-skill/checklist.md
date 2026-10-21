# Pre-handover checklist

Run through every item. Fix failures before reporting.

## Process
- [ ] The user explicitly confirmed the folder tree (both trees for fullstack) before any project file was written
- [ ] Context Card fields are all filled; inferred values were confirmed
- [ ] Related skills/docs (P1) and existing gates (P2) were looked for and recorded
- [ ] Sources used are cited in `01-folder-structure.md` (each branch)

## Layout
- [ ] Flat layout for single-stack projects; branched `shared/ + be/ + fe/` for fullstack
- [ ] Fullstack: each `be/0X` / `fe/0X` covers only its branch; cross-branch rules live in `shared/`
- [ ] Fullstack: `SKILL.md` routes `be_dir` → `be/`, `fe_dir` → `fe/`, with one gate per branch
- [ ] Files generated match each branch's level (`lite`/`standard`/`full`)

## Content
- [ ] Every folder in each `01` tree has an entry in the matching `02`
- [ ] All examples use real project names/paths and the stack's real syntax; shape-only snippets say so
- [ ] Dependency direction is identical across `SKILL.md`, `02`, and `05` (per branch)
- [ ] Each `04` smell table points to real paths; thresholds match the owner (clean-code skill or confirmed defaults)
- [ ] Every rule in `backend-rules.md` / `frontend-rules.md` is expressed or marked "not adopted"
- [ ] Existing gates are referenced in `05` and in the SKILL checklist

## Existing project / Update mode
- [ ] Locked architecture documented as-is; drift reported; only open decisions asked (P4)
- [ ] Project-specific rules kept as their own files, not weakened (P5)
- [ ] Volatile facts and known debt only in `incremental-adoption.md`
- [ ] Coverage table old rule → new file built; no rule dropped
- [ ] Uncommitted changes in modified/deleted files were carried over (P3)
- [ ] Inbound links updated or old names kept, as agreed; 0 broken links:
  `grep -rnoE "clean-architecture/(references|scripts|assets)/[A-Za-z0-9_./-]+" --include='*.md' . | grep -v node_modules`

## Hygiene
- [ ] No `{{` placeholders and no `<!-- GEN:` comments remain:
  `grep -rn -e '{{' -e '<!-- GEN:' .agents/skills/clean-architecture/`
- [ ] Every generated file ends with a `custom:start/end` block
- [ ] Each file is under ~200 lines
- [ ] All generated text is in English (quoted section names of other skills excepted)

## Wiring
- [ ] `CLAUDE.md` (and `AGENTS.md` if present) points to `.agents/skills/clean-architecture/`
- [ ] The user was asked about the `.claude/skills/` symlink, scaffolding, lint suggestions, and saving a new preset (when applicable)
- [ ] No project code was moved and no packages were installed without the user's request
