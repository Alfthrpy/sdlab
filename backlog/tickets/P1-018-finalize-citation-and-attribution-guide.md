---
id: P1-018
title: "Finalize citation and attribution guide"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: medium
depends_on: [P1-010]
estimate: 1
outputs:
  - docs/conventions/citation-guide.md
  - scripts/validate.py
---

## Context

The v0 guide exists. Finalize it and make sure the validator enforces it in content.

## Tasks

1. Test the guide on one sample lesson (may be a dummy).
2. Add validator checks: `[^id]` markers exist in `sources` and the registry; `published` content must not cite `candidate`; attribution is required when using an `adapt-with-attribution` source.
3. Clarify the direct-quote rule with examples.

## Done criteria

- [x] Guide is final
- [x] Validator enforces the citation rules
- [x] `python scripts/validate.py` passes

## Notes

- Validator (`check_content`): added `[^id]`-in-registry check, `loc` required for book/paper sources, attribution line required for `adapt-with-attribution` sources (error), published questions may only cite approved non-map-only sources, direct-quote limit (one per source per lesson, under 15 words; heuristic: quoted spans of 4+ words followed by a marker, code blocks skipped).
- Guide is final: enforcement table, quote rules with examples, sample lesson that `tests/test_content.py` runs through the validator.
- `tests/test_content.py`: 15 new fixture tests (35 total pass).
- content-reviewer: pass with minor fixes; applied (sample lesson test, missing tests, narrower quote rule, heuristic wording, schema cross-link).
- Known limits: attribution check only looks for "diadaptasi"; quotes without markers, quotes in questions.yaml, and single-quote styles are left to the reviewer.
