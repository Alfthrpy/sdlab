---
id: P1-017
title: "Map sources to topics and list gaps"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-016]
estimate: 1
outputs:
  - references/coverage.md
---

## Context

Input for the G0 decision: is every unit covered by adequate sources.

## Tasks

1. Build a sub-topic × source matrix (tier, free/paid).
2. Mark gaps: sub-topics without Tier 1–2 or without a free source.
3. Propose how to close each gap (more research, official docs, or dropping the sub-topic).

## Done criteria

- [ ] `references/coverage.md` contains the matrix and the gap list
- [ ] Every gap has a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
