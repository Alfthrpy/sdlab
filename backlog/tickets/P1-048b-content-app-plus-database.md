---
id: P1-048b
title: "Content: app-plus-database"
milestone: M4
type: content
owner: agent
review: agent
status: review
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
2. Run the `cold-reader` subagent on the lesson core; rewrite until its verdict is `clear` (writing-style.md, "Cold-read gate"). Write for the two layers: core for newcomers, `## Lebih dalam` for practitioners.
3. Run `content-reviewer` (a different subagent); fix its findings; second pass if the first has major findings.
4. Set the concept status to `review` in `curriculum/concepts.yaml`.
5. Record time and obstacles in Notes.

## Done criteria

- [x] All files in `content/concepts/app-plus-database/` complete and pass the validator
- [x] `cold-reader` verdict `clear` and `content-reviewer` passes (see Notes; the lesson was rewritten once under P1-086)
- [x] Concept status is `review` in concepts.yaml
- [x] `python scripts/validate.py` passes

## Notes

Output: `content/concepts/app-plus-database/`: `lesson.md` core 441 words (validator method) plus `## Lebih dalam` (about 220 words), `questions.yaml` 10 questions, `misconceptions.md` 5. No lab (`formats`: lesson, quiz). Validator 0 errors, no warnings for these files.

**History (two rounds).**
1. First draft (587-word single layer): content-reviewer FAIL (4 major), fixed, then pass with minor fixes. Accurate, but the owner found it hard to read even for them.
2. Diagnosis (see P1-086): two ideas in one lesson, caveat chains added per reviewer finding (17 words/sentence vs 12.5), no story spine, about 10 new terms, no readability gate. A cold-reader baseline on the old lesson: `needs work`, 3 lost points (dense Stack Overflow paragraph, unexplained "measure capacity yourself", CSV example under "cache").
3. Rewrite under the new convention (P1-086): one shop story in two stages, 6 italic terms, Stack Overflow / SQLite / VPS / Redis moved to `## Lebih dalam`. Cold-reader: `needs work (borderline)` with 2 lost points, fixed; second read `clear`. content-reviewer: pass with minor fixes, no major; the lesson fixes were applied directly and the question/misconception fixes by the writer (q03 reframed, q10 added for `one-db-is-toy`, option shapes equalised). The fixes after the second review were not re-reviewed.

**Source gaps and caveats.**
- No source gives the RPS of one PostgreSQL/MySQL server. The 300 RPS is a labeled hypothetical, and the core explains how to measure it on a copy of the system. That method is plain reasoning with no source. P1-085 is open for a source.
- `robustperception-peak-to-mean-ratio` is a registry `candidate`; the owner must approve it before this concept can be `published`.
- The ratio 3 for a single time zone is the lesson's starting assumption, not a sourced figure.
- `system-design-primer` stays in the concept's `sources` list but is not used in the lesson.
- q02 and q05 give ratios (1.7, 2.4) in their prompts that the core does not teach as figures; they stay answerable from the prompt.

**Reusable lessons.** Reviewer-driven fixes accumulate hedges: put source nuance in `## Lebih dalam` instead of the core. A cold read on the draft finds the confusing paragraph quickly and cheaply (about 15 s, 15k tokens). Questions that rely on a sourced detail should rely on the core, so the deep layer can be skipped.
