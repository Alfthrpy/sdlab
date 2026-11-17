---
id: P1-048c
title: "Content: indexes-query-basics"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/indexes-query-basics/
---

## Context

Content production for the Unit 0 concept `indexes-query-basics` (Index dan dasar optimasi query). Part of epic P1-048. Prerequisites: app-plus-database. Formats per concepts.yaml: ['lesson', 'quiz', 'lab'].

## Tasks

1. Run the `content-writer` subagent for `indexes-query-basics`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
3. Set the concept status to `review` in `curriculum/concepts.yaml`.
4. Record time and obstacles in Notes.

## Done criteria

- [ ] All files in `content/concepts/indexes-query-basics/` complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Concept status is `review` in concepts.yaml
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
