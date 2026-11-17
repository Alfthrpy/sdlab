---
id: P1-035a
title: "Backfill reading notes for sources mapped to Unit 0 concepts"
milestone: M4
type: research
owner: agent
review: agent
status: done
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

- [x] Every source mapped to a Unit 0 concept has reading notes
- [x] Every Unit 0 objective is checked against the notes; gaps have tickets
- [x] `python scripts/validate.py` passes

## Notes

**Result.** All 28 sources mapped to Unit 0 concepts now have `references/notes/<id>.md` (20 new, 8 existing). The 20 new notes were written by four `researcher` runs (5 sources each, 2026-11-17), each source opened with WebFetch and the raw page re-checked with `curl` for numbers, formulas and directive names. Validator 0 errors; 160 tests pass.

**Verification.** `source-verifier` (independent) reopened 6 of the 20 notes (those with exact numbers: atlassian-pir-april-2022, craver-stack-overflow-architecture-2016, gregg-use-method, hikaricp-about-pool-sizing, pg-wiki-number-of-connections, systemd-service-man): no wrong number found; four wording fixes applied (an overstated claim in gregg-use-method, the Atlassian byline location, a softening word in craver, a near-quoted fragment in systemd). The other 14 notes were not independently reopened; the `mysql-84-backup-recovery` subpages could not be fetched with curl (403), so its subpage content was checked only through the writer's fetch. Registry corrections confirmed by the verifier and applied: `version` "18.6" removed from `pg-docs-connections` and `pg-docs-monitoring-stats` (not visible on the pages), the AWS primer footer now confirmed (all rights reserved), and the notes of `twelve-factor-app` and `mysql-84-backup-recovery` updated to what was read.

**Objective check (task 3).** Gaps are listed in ticket P1-083 (high priority; now a dependency of P1-048): `connection-pooling` obj 1-3, `request-lifecycle` obj 1-2, `app-plus-database` obj 1, `basic-monitoring` obj 2 (the sources say "golden signals" and "queries, errors, latency", not RED/rate/duration), `single-machine-limits` obj 3 (no current machine size ceiling), plus three partly supported objectives to decide. Checked against the pre-existing notes and found supported, so not gaps: `indexes-query-basics` obj 1 (EXPLAIN: `pg-docs-using-explain`), `backup-recovery` obj 3 and part of obj 2 (Atlassian, SRE ch. 26), `basic-monitoring` obj 3 (AWS health checks), `single-machine-limits` obj 1 (kernel resources and Gregg).

**Cosmetic, not fixed:** the pre-existing notes (for example `pg-docs-using-explain`, `pg-docs-backup-restore`) name old concept ids in "Relevant to concepts" (`query-plans-and-explain`, `backups-and-recovery-basics`); the P1-083 or Unit 0 sub-tickets can refresh them when they are re-read. The `systemd-service-man` note does not cover `RestartSteps=`, `RestartMaxDelaySec=` and `RestartRandomizedDelaySec=`.

**Process note.** Reading notes cost about 5 minutes of wall clock per batch with four parallel runs; the objective-gap analysis and verification were the longer part. Use the same four-way split when a later unit starts its notes pass.

