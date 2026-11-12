---
id: P1-043
title: "EPIC Production Unit 3"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-035]
estimate: 6
outputs:
  - content/concepts/
---

## Context

Content production for Unit 3: Data (data models, indexes, replication, partitioning, transactions & isolation). This is an epic: split it before working on it.

## Tasks

1. First session: create one sub-ticket per concept of this unit (`python scripts/new_ticket.py ... --depends P1-043`), ids `P1-043a`, `P1-043b`, etc. Set the epic to `in-progress`.
2. Each sub-ticket: content-writer → content-reviewer → fixes → PR.
3. After all sub-tickets are done: mark 2 random concepts for human spot-check in P1-063.

## Done criteria

- [ ] All concepts of this unit have status `review` or `published` in concepts.yaml
- [ ] All sub-tickets done
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
