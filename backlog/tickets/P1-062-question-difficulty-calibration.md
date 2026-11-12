---
id: P1-062
title: "Question difficulty calibration"
milestone: M5
type: review
owner: agent
review: agent
status: todo
priority: low
depends_on: [P1-040, P1-041, P1-042]
estimate: 1
outputs:
  - content/concepts/
---

## Context

The difficulty distribution must be balanced and questions must not leak.

## Tasks

1. Compute the difficulty distribution per concept and unit.
2. Run the anti-leak heuristics; fix flagged questions.

## Done criteria

- [ ] Difficulty distribution recorded
- [ ] No anti-leak warnings left
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
