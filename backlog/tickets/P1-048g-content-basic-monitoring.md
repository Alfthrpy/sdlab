---
id: P1-048g
title: "Content: basic-monitoring"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/basic-monitoring/
---

## Context

Content production for the Unit 0 concept `basic-monitoring` (Monitoring dasar - log, metrik, dan health check). Part of epic P1-048. Prerequisites: request-lifecycle. Formats per concepts.yaml: ['lesson', 'quiz'].

## Tasks

1. Run the `content-writer` subagent for `basic-monitoring`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run the `cold-reader` subagent on the lesson core; rewrite until its verdict is `clear` (writing-style.md, "Cold-read gate"). Write for the two layers: core for newcomers, `## Lebih dalam` for practitioners.
3. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
4. Set the concept status to `review` in `curriculum/concepts.yaml`.
5. Record time and obstacles in Notes.

## Done criteria

- [ ] All files in `content/concepts/basic-monitoring/` complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Concept status is `review` in concepts.yaml
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
