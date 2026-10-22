# Checklist — quality-environment

Run this and `~/.claude/skill-factory/core/checklist-common.md`.

- [ ] Every rule E1–E14 is adopted, adapted, or "not adopted" with a reason; E2, E5, E7, E9, E12, E13 are adopted
- [ ] Services, ports, start commands (cwd), health checks and start order are real; make targets were read before listing
- [ ] Probe-first and "stop only what you started" are explicit; stop-everything targets flagged
- [ ] Forbidden data commands named; isolation strategy and seed are local/disposable only
- [ ] Accounts per role and environment listed by name; credentials only referenced
- [ ] Each external provider has sandbox, stub or BLOCKED; stub labelling stated
- [ ] Revision alignment and local migration steps present
- [ ] Environment record format present; no secret values anywhere
