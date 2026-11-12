---
id: P1-004
title: "Mirror backlog to GitHub Projects (optional)"
milestone: M0
type: infra
owner: agent
review: human
status: todo
priority: low
depends_on: [P1-001]
estimate: 1
outputs:
  - .github/workflows/sync-issues.yml
  - scripts/sync_issues.py
---

## Context

Tickets live in files (ADR 0001). If the owner wants a kanban view and notifications, build a one-way sync from files to GitHub Issues/Projects.

## Tasks

1. Confirm with the owner whether this is needed; if not, close the ticket as won't-do.
2. Build a one-way sync script (files are the source of truth) using GITHUB_TOKEN in Actions.
3. Labels: milestone, owner, type, status.

## Done criteria

- [ ] Owner has decided whether it is needed
- [ ] If needed: Issues sync on push to main, with no duplicates
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
