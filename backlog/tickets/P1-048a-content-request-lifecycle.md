---
id: P1-048a
title: "Content: request-lifecycle"
milestone: M4
type: content
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-083]
estimate: 1
outputs:
  - content/concepts/request-lifecycle/
---

## Context

Content production for the Unit 0 concept `request-lifecycle` (Perjalanan satu request di satu mesin). Part of epic P1-048. Prerequisites: none. Formats per concepts.yaml: ['lesson', 'quiz'].

## Tasks

1. Run the `content-writer` subagent for `request-lifecycle`: lesson, questions, misconceptions (and lab.yaml only if `formats` lists a lab).
2. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
3. Set the concept status to `review` in `curriculum/concepts.yaml`.
4. Record time and obstacles in Notes.

## Done criteria

- [x] All files in `content/concepts/request-lifecycle/` complete and pass the validator
- [x] `content-reviewer` passes (pass with minor fixes; all 11 findings fixed; the fixes were not re-reviewed, per the reviewer's note that no second pass was needed)
- [x] Concept status is `review` in concepts.yaml
- [x] `python scripts/validate.py` passes

## Notes

Output: `content/concepts/request-lifecycle/` (`lesson.md` 505 words by the validator's method, `questions.yaml` 8 questions, `misconceptions.md` 5; no lab, as `formats` lists only lesson and quiz). Validator 0 errors, no warnings for these files.

**Flow:** content-writer (draft) -> content-reviewer (pass with minor fixes, 11 findings) -> content-writer (fixes, same agent resumed) -> my own validator check. Three subagent runs; wall clock about 15 minutes.

**Source gap (not a ticket yet):** objective 2 (find the slowest stage from per-stage timings) has no source with typical per-stage timings. `web-dev-ttfb` gives the premise (TTFB is a sum of phases) and Craver gives real cumulative totals; the worked example (900 ms: DNS 50, connection+TLS 200, proxy 10, app 80, database 560) and the numbers in q04-q06 are the author's hypothetical figures and carry no marker. If a reviewer wants a source for them, open a source ticket.

**Review findings worth reusing in later concepts:** (1) in mcq, the correct option was the odd one out in form (the only one without the shared "Cek X dulu, karena" opening); (2) a threshold from a source was applied to the wrong quantity (TTFB vs page load); (3) a worked example total fell inside the lesson's own "no need to hunt" zone; (4) a distractor that is true in the real data; (5) objective tags drifting from what a question tests.
