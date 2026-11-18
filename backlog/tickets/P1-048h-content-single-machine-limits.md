---
id: P1-048h
title: "Content: single-machine-limits"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/single-machine-limits/
---

## Context

Content production for the Unit 0 concept `single-machine-limits` (Batas satu mesin dan cara mengenalinya). Part of epic P1-048. Prerequisites: basic-monitoring, connection-pooling. Formats per concepts.yaml: ['lesson', 'quiz', 'lab'].

## Tasks

1. Run the `content-writer` subagent for `single-machine-limits`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
3. Set the concept status to `review` in `curriculum/concepts.yaml`.
4. Record time and obstacles in Notes.

## Done criteria

- [ ] All files in `content/concepts/single-machine-limits/` complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Concept status is `review` in concepts.yaml
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
