---
name: docs
description: Write and verify reader-facing Client documentation from implemented source and approved work-item scope.
---

# Client documentation

Read the approved `.superpowers/work-items/<slug>/vN/brief.md`, optional design/plan, actual Client source, tests and relevant evidence. Write only assigned reader-facing Markdown paths. Describe the real flow, inputs/outputs, state, errors, routing, UI Kit use and setup (stack conventions: `{{slot:architecture-design}}`) only where relevant to the reader's task. Link to source-relative docs where practical; do not present planned work as shipped.

For a `documentation` work item, Docs Writer can deliver directly from the approved brief. For code work, write after implementation is available and before final review. Check every command/example against real configuration, inspect links and diagrams, and give Code Reviewer the source paths supporting each material claim. Return `BLOCKED` when source and approved contract disagree. Do not edit runtime code, tests or approved specs/plans.
