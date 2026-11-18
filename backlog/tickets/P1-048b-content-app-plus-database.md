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

- [x] All files in `content/concepts/app-plus-database/` complete and pass the validator
- [x] `content-reviewer` passes (first pass: fail with 4 major; second pass: pass with minor fixes; M1-M9 fixed, not re-reviewed per the reviewer)
- [x] Concept status is `review` in concepts.yaml
- [x] `python scripts/validate.py` passes

## Notes

Output: `content/concepts/app-plus-database/` (`lesson.md` 587 words by the validator's method, `questions.yaml` 9 questions, `misconceptions.md` 5; no lab, `formats` is lesson + quiz). Validator 0 errors, no warnings for these files.

**Flow:** content-writer (draft) -> content-reviewer (FAIL, 4 major + 11 minor) -> content-writer (all 15 fixed) -> content-reviewer second pass (pass with minor fixes, M1-M9) -> content-writer (M1-M9 fixed). Same writer and reviewer agents were resumed each time.

**Major findings worth reusing in later concepts:** (1) a twelve-factor PaaS claim ("restart wipes local files") taught as a general fact, while the lesson's own SQLite paragraph contradicted it; (2) one engine's limits (SQLite single writer) reused as general reasons to leave one-app-one-db; (3) a MCQ whose correct option followed a non sequitur and whose distractors were strawmen; (4) a prompt phrase ("di luar hitungan itu") that leaked the answer.

**Source gaps:**
- No source gives how many RPS one PostgreSQL/MySQL server handles. The lesson and q06 use a labeled hypothetical (300 RPS) and tell the reader to measure their own. Opened P1-085.
- `robustperception-peak-to-mean-ratio` is still registry `candidate` and is cited in the lesson, q01, q02, q04, q05 and `average-is-enough`. The owner must approve it before this concept can be `published`.
- The peak-to-mean ratio of 3 for single-time-zone users is an assumption, not sourced (the lesson says so).
- `system-design-primer` remains in the concept's `sources` list but is no longer used in the lesson (the per-month conversion was cut to fit the word limit). It is a mapped-but-unused pointer; remove it from concepts.yaml or restore the conversion later.
- The Redis-keeps-carts-across-a-deploy claim rests on twelve-factor's remark about session datastores; the source does not discuss Redis restarts.
