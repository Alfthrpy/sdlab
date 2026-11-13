---
id: P1-017
title: "Map sources to topics and list gaps"
milestone: M1
type: research
owner: agent
review: agent
status: done
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

- [x] `references/coverage.md` contains the matrix and the gap list
- [x] Every gap has a proposed action
- [x] `python scripts/validate.py` passes

## Notes

2026-11-13: `references/coverage.md` written (matrix, G0 per-unit check, gap list with actions). All units meet the PLAN G0 criterion; Units 0 and 4 only narrowly. `source-verifier` failed the first pass; fixes applied, no second pass. No follow-up tickets created yet, see the Summary for G0 in the file. See `sessions/2026-11-13-P1-017.md`.
