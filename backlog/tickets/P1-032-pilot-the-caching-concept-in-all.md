---
id: P1-032
title: "Pilot the 'caching' concept in all formats"
milestone: M3
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-030, P1-031]
estimate: 2
outputs:
  - content/concepts/caching-basics/
---

## Context

A pilot to test templates and the production flow before mass production. The concept id follows `curriculum/concepts.yaml`.

## Tasks

1. Do it with the `content-writer` subagent: misconceptions, lesson, 8–10 questions, lab.yaml (draft spec).
2. Review with `content-reviewer`, fix.
3. Record time and production obstacles in the Notes (input for M4 estimates).

## Done criteria

- [ ] All concept files are complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Time & production obstacles recorded
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
