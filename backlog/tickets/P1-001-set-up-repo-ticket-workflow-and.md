---
id: P1-001
title: "Set up repo, ticket workflow, and agent support files"
milestone: M0
type: infra
owner: agent
review: none
status: done
priority: high
depends_on: []
estimate: 1
outputs:
  - AGENTS.md
  - docs/
  - backlog/
  - templates/
  - scripts/
  - .claude/
  - .github/
---

## Context

Foundation for Phase 1 work: repo structure, ticket system, agent rules, templates, and automated validation.

## Tasks

1. Create the repo structure and the workflow document.
2. Write AGENTS.md, subagents, and slash commands.
3. Write the Phase 1 plan and the initial backlog.
4. Create the validate/board/new_ticket scripts and CI.
5. Seed the registry from the initial research.

## Done criteria

- [x] Repo structure matches the README
- [x] Initial backlog is complete with owner/review/dependencies
- [x] CI runs validate.py
- [x] `python scripts/validate.py` passes

## Notes

Created in the planning session of 2026-11-12 at the owner's request. Later structural changes are made as new tickets.
