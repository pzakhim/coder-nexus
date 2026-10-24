# Common checklist (all generators)

- [ ] Nothing written into `.agents/plugins/coder-nexus/` or extension-regenerated role files (Step 0)
- [ ] The user confirmed the gate item before any workspace file was written
- [ ] Context Card complete; inferred values confirmed; related skills/docs/gates recorded (P1–P2)
- [ ] Layout matches the workspace (flat / branched)
- [ ] No `{{` and no `<!-- GEN:` left: `rg -n -e '\{\{' -e '<!-- GEN:' .agents/skills/<skill>/`
- [ ] English only (quoted section names of other skills excepted); each file < ~200 lines; custom block at the end
- [ ] Project-specific rules kept; volatile facts only in incremental-adoption (P5)
- [ ] Uncommitted changes carried over; inbound links updated or kept as agreed; 0 broken links (P3)
- [ ] All **Mandatory** content present; deviations from the suggested shape listed with reasons
- [ ] Rules explain their why; hard "never/always" only for absolute rules; `SKILL.md` lean with pointers into `references/`
- [ ] Trial run done (or skipped by the user, recorded): with-skill plans follow the skill and beat the baseline ([trial-run.md](trial-run.md))
- [ ] Description names the workspace, lists concrete situations and team trigger words, and triggered on the trial prompts
- [ ] `CLAUDE.md` / `AGENTS.md` point at the skill
- [ ] Provenance recorded in `~/.claude/skill-factory-registry/<workspace-slug>.json`; nothing written into the workspace about it
- [ ] No project code moved, no packages installed, nothing committed without the user's request
