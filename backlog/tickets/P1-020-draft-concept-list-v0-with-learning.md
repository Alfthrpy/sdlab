---
id: P1-020
title: "Draft concept list v0 with learning objectives"
milestone: M2
type: curriculum
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-019]
estimate: 2
outputs:
  - curriculum/concepts.yaml
---

## Context

Draft ~46 concepts for the 7 units (0–6). Each concept in Units 1–6 gets a `trigger` (ADR 0004 Amendment 1). Use the `curriculum-designer` subagent.

## Tasks

1. Derive concepts from the unit table and coverage.
2. Check coverage against Tier 6 sources (only to make sure no common topic is missed).
3. Write 1–4 learning objectives per concept (Indonesian, starting with 'Bisa ...').

## Done criteria

- [ ] 40–50 concepts across 7 units (0–6)
- [ ] Every concept in Units 1–6 has a `trigger`
- [ ] Every concept has testable learning objectives
- [ ] `content-reviewer` passes
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
