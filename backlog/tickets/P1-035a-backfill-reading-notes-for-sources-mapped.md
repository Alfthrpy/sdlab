---
id: P1-035a
title: "Backfill reading notes for sources mapped to Unit 0 concepts"
milestone: M4
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: [P1-035]
estimate: 1
outputs: []
---

## Context

Found in the P1-032 pilot (P1-035 review): 3 of the 4 `caching-basics` sources had no reading notes, so the writer fetched the pages itself, the biggest time cost of the pilot. P1-035 now requires notes for every source mapped to a concept, but only going forward. Unit 0 ships first (ADR 0007), so its sources come first: 20 of the 28 sources mapped to Unit 0 concepts have no `references/notes/<id>.md` yet. Do this before the Unit 0 concept tickets (P1-048a onward) so writers do not refetch.

## Tasks

1. List the sources mapped to Unit 0 concepts in `curriculum/concepts.yaml` that have no `references/notes/<id>.md` (20 at the time of writing).
2. For each, open the page and write reading notes per `templates/source-notes.md` (English, own words, section references), including the facts and numbers the Unit 0 objectives need, and any outdated parts.
3. Check each Unit 0 objective against its notes: if a source does not support what an objective asks, record the gap in the Notes and create a ticket (as P1-081 did for write-back).
4. Do not change registry entries other than what verification requires.

## Done criteria

- [ ] Every source mapped to a Unit 0 concept has reading notes
- [ ] Every Unit 0 objective is checked against the notes; gaps have tickets
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
