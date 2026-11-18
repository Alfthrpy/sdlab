---
id: P1-048
title: "EPIC Production Unit 0"
milestone: M4
type: content
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-035, P1-035a, P1-083]
estimate: 1
outputs: []
---

## Context

Content production for Unit 0: Single-server backend (request lifecycle, one app plus one database, indexes, connection pooling, backups, simple deploys, basic monitoring, limits of one machine). Added by ADR 0004 Amendment 1. This is an epic: split it before working on it.

## Tasks

1. First session: create one sub-ticket per concept of this unit (`python scripts/new_ticket.py ... --depends P1-048`), ids `P1-048a`, `P1-048b`, etc. Set the epic to `in-progress`.
2. Each sub-ticket: content-writer → content-reviewer → fixes → PR.
3. After all sub-tickets are done: mark 2 random concepts for human spot-check in P1-063.

## Done criteria

- [ ] All concepts of this unit have status `review` or `published` in concepts.yaml
- [ ] All sub-tickets done
- [ ] `python scripts/validate.py` passes

## Notes

Session 1 (2026-11-17): split into 8 sub-tickets, one per concept, P1-048a..h in the order of `curriculum/concepts.yaml` (a request-lifecycle, b app-plus-database, c indexes-query-basics, d connection-pooling, e backup-recovery, f simple-deploys, g basic-monitoring, h single-machine-limits). Order respects prerequisites; g only needs a, h needs g and d.

Sub-tickets use `depends_on: [P1-083]`, not `[P1-048]` as the Tasks line suggested: the epic closes only after its sub-tickets, so depending on it would keep them out of the ready list forever. Prerequisite order is not enforced through depends_on, so concepts can be written in parallel (lessons only reference prerequisite concepts by id).

Step 3 (mark 2 random concepts for P1-063) happens after all sub-tickets are done.
