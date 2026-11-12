---
id: P1-031
title: "Style guide and anti-leak rules for questions"
milestone: M3
type: content
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-024]
estimate: 1
outputs:
  - docs/conventions/writing-style.md
---

## Context

Real complaints about similar apps: question titles leak the answer and content feels AI-made.

## Tasks

1. Finalize the style guide with good/bad examples for lessons and questions.
2. Add automatically checkable anti-leak heuristics (e.g. correct option is the longest in > 40% of a concept's questions) to the validator as warnings.

## Done criteria

- [ ] Final guide with ≥ 5 good/bad examples
- [ ] Anti-leak heuristics are in the validator
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
