---
id: P1-082
title: "ADR 0007: beta-first, Unit 0 first, G2 deferred"
milestone: M3
type: decision
owner: agent
review: human
status: review
priority: medium
depends_on: []
estimate: 1
outputs:
  - docs/decisions/0007-beta-first-unit-0-first.md
---

## Context

The owner read the P1-032 pilot lesson, was fine with it, and decided to skip the 5-user test for now, ship Unit 0 first, and build far enough that a quiz and lab run end to end with the owner as beta tester. This ticket records that decision and adjusts the backlog.

## Tasks

1. Write ADR 0007.
2. Defer G2 (P1-034, status `blocked`), point P1-035 at P1-032, raise P1-048 (Unit 0 epic) to high priority.
3. Ask the owner for the stack and first-slice scope that Phase 2/3 planning needs.

## Done criteria

- [x] ADR 0007 written and the affected tickets adjusted
- [ ] Owner reviews the ADR (status `review`)
- [ ] `python scripts/validate.py` passes

## Notes

Next, not part of this ticket: a Phase 2/3 plan (stack, repo layout, the first slice: Unit 0 quiz plus one lab) once the owner answers; then P1-033 (lab spec) fitted to what the simulator will do, P1-035, and P1-048 (Unit 0 production).
