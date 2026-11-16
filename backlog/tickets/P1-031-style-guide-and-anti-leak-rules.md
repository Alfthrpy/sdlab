---
id: P1-031
title: "Style guide and anti-leak rules for questions"
milestone: M3
type: content
owner: agent
review: agent
status: done
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

- [x] Final guide with ≥ 5 good/bad examples
- [x] Anti-leak heuristics are in the validator
- [x] `python scripts/validate.py` passes

## Notes

- `docs/conventions/writing-style.md` is final: 11 good/bad examples (5 for lessons, 6 for questions), a difficulty-mix note, and an "Automatic checks" table that matches the code.
- Validator warnings (`scripts/validate.py`, constants at the top): correct option longest (> 40% of mcq), answer position (> 50%, 5+ mcq), prompt echo (> 50%), absolute words only in wrong options, escape-hatch options ("semua jawaban benar", "A dan B benar"), explanation over 3 sentences, one difficulty only (4+ questions), lesson openers ("Pada lesson ini ..."), filler phrases and emoji. All only warn.
- Tests: 100 pass (`tests/test_content.py`, 25 new). The branch is stacked on t/P1-030-final-content-schema (PR #42): the heuristics live in `check_questions`, which P1-030 introduced.
- Review (content-reviewer, independent): pass with fixes, applied: crash on non-list `options`; example 6 broke the guide's own rules (rewritten, options now similar in length); noisy heuristics tuned (`semua`/`seluruh` no longer an absolute word, check marks are not emoji, abbreviations do not end sentences, stopwords ignored in echo, position check needs 5 mcq, quoted or coded filler ignored, headings skipped before the opener); doc/table mismatches and stale lines in `content-schema.md` fixed; `content-writer` and `content-reviewer` instructions mention the warnings.
- Known limits: the heuristics are lexical (no stemming): Indonesian affixes ("database"/"databasenya") and English/Indonesian pairs are not matched. Meaning-based leaks and implausible distractors stay with the reviewer. Thresholds are guesses; revisit them after the P1-032 pilot shows real warning rates.
