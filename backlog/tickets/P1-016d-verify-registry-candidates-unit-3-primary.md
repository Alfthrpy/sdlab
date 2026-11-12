---
id: P1-016d
title: "Verify registry candidates: Unit 3 (primary unit)"
milestone: M1
type: research
owner: agent
review: agent
status: review
priority: high
depends_on: []
estimate: 1
outputs: []
---

## Context

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 3 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

## Tasks

Follow P1-016 Tasks 1–5 for each entry in scope, SEED and Tier 1–3 first:

1. Reopen the URL; confirm it is the intended page.
2. Complete `authors`, `published`, `edition`, canonical URL, `license` from the page; resolve every `license: unknown` or explain it in `notes`.
3. Check for a newer edition/version; mark outdated entries `deprecated`.
4. Record `free_companion` for paywalled sources.
5. Set `verified_on`; write `attribution` for `adapt-with-attribution` entries; remove resolved `SEED` markers.
6. Do not set `status: approved` (that is G0, P1-019); only make entries approvable.

## Done criteria

- [ ] Every in-scope entry reopened this session and has `verified_on` (Codd 1970 excepted, see Notes)
- [x] No empty `authors`/`published` without a `NO-AUTHOR`/`NO-DATE` explanation
- [x] No `license: unknown` without an explanation; no `SEED` notes left
- [ ] `source-verifier` passes (sample)
- [x] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)

2026-11-12: 23 entries with primary unit 3 reopened; 22 have `verified_on`. `codd-relational-model-1970` does not: its PDF on the UPenn course site is now a scanned image with no readable text, so its CACM metadata was not rechecked (it stays a candidate with a NOT RE-VERIFIED note; replace with a readable canonical URL). Licenses: 11 `unknown` resolved. Apache-2.0: CouchDB docs (src/docs/LICENSE in apache/couchdb). CC-BY-NC-SA-4.0: Neo4j getting-started (repo LICENSE.txt). all-rights-reserved: MongoDB (repo README says CC BY-NC-SA 3.0, not in enum, NonCommercial), DynamoDB docs x2, Bigtable, Berenson critique, O'Neil LSM, Karger, Jepsen. Cassandra docs (Apache-2.0 footer) got an attribution line. PDFs read by text extraction (pdftotext): Dynamo (Copyright 2007 ACM), LSM-tree, Karger; none shows a license. Jepsen SEED resolved.
Reviewer pass done 2026-11-12 (PASS): cosmetic note wording fixes only.
