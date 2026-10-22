# Checklist — database-migrations

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule M1–M14 is adopted, adapted, or "not adopted" with a reason; M1, M2, M3, M5, M9, M10 are adopted
- [ ] Runner facts come from reading its code/scripts; commands have cwd; their limits are stated
- [ ] Forbidden delivery commands (reset/sync/seed/bootstrap) are named explicitly
- [ ] Targets, selectors and who may apply are listed; read-only sources marked as not targets
- [ ] Engine lock notes and patterns match the real engine/version
- [ ] Disposable-DB verification recipe is concrete (clean install, upgrade with data, rerun)
- [ ] States use the workspace's names if it has them; handoff packet has no secret values
- [ ] Skill is flat and scoped to the backend directory
