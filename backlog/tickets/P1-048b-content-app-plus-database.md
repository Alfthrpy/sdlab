---
id: P1-048b
title: "Content: app-plus-database"
milestone: M4
type: content
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/app-plus-database/
---

## Context

Content production for the Unit 0 concept `app-plus-database` (Satu aplikasi dan satu database). Part of epic P1-048. Prerequisites: request-lifecycle. Formats per concepts.yaml: ['lesson', 'quiz'].

## Tasks

1. Run the `content-writer` subagent for `app-plus-database`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
3. Set the concept status to `review` in `curriculum/concepts.yaml`.
4. Record time and obstacles in Notes.

## Done criteria

- [ ] All files in `content/concepts/app-plus-database/` complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Concept status is `review` in concepts.yaml
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
