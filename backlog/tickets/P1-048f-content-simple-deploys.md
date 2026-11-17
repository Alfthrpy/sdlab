---
id: P1-048f
title: "Content: simple-deploys"
milestone: M4
type: content
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/simple-deploys/
---

## Context

Content production for the Unit 0 concept `simple-deploys` (Deploy sederhana di satu server). Part of epic P1-048. Prerequisites: app-plus-database. Formats per concepts.yaml: ['lesson', 'quiz'].

## Tasks

1. Run the `content-writer` subagent for `simple-deploys`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
3. Set the concept status to `review` in `curriculum/concepts.yaml`.
4. Record time and obstacles in Notes.

## Done criteria

- [ ] All files in `content/concepts/simple-deploys/` complete and pass the validator
- [ ] `content-reviewer` passes
- [ ] Concept status is `review` in concepts.yaml
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
