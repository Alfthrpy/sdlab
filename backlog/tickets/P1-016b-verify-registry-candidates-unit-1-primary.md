---
id: P1-016b
title: "Verify registry candidates: Unit 1 (primary unit)"
milestone: M1
type: research
owner: agent
review: agent
status: in-progress
priority: high
depends_on: []
estimate: 1
outputs: []
---

## Context

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 1 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

## Tasks

Follow P1-016 Tasks 1–5 for each entry in scope, SEED and Tier 1–3 first:

1. Reopen the URL; confirm it is the intended page.
2. Complete `authors`, `published`, `edition`, canonical URL, `license` from the page; resolve every `license: unknown` or explain it in `notes`.
3. Check for a newer edition/version; mark outdated entries `deprecated`.
4. Record `free_companion` for paywalled sources.
5. Set `verified_on`; write `attribution` for `adapt-with-attribution` entries; remove resolved `SEED` markers.
6. Do not set `status: approved` (that is G0, P1-019); only make entries approvable.

## Done criteria

- [ ] Every in-scope entry reopened this session and has `verified_on`
- [x] No empty `authors`/`published` without a `NO-AUTHOR`/`NO-DATE` explanation
- [x] No `license: unknown` without an explanation; no `SEED` notes left
- [ ] `source-verifier` passes (sample)
- [x] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)

2026-11-12: 21 entries with primary unit 1 reopened. 20 have `verified_on`; `little-2011-littles-law-50th` does NOT (INFORMS page returns HTTP 403 to automated fetches; DOI resolves to INFORMS, metadata from the earlier PDF header stays unrechecked, so that criterion stays open for it). Changes: all 5 SEED notes resolved (DDIA 2e date set to 2026-03 from the authors' own page, since the O'Reilly page returns 403; SRE book editors added and 2nd-edition existence noted; System Design Primer license CC BY 4.0 confirmed from LICENSE.txt, repo maintained, attribution added; Tier 6 pages got NO-AUTHOR/NO-DATE). `free_companion` set for the two paywalled entries (DDIA, Alex Xu). Licenses: 5 unknown -> all-rights-reserved (no license stated), grpc docs -> CC-BY-4.0 (repo LICENSE linked from footer); attribution lines added for 2 Brooker posts. Open gaps: Tail at Scale DOI still unconfirmed (ACM 403); Dean slides are an image-only PDF so nothing beyond existence/absence of license could be checked.
