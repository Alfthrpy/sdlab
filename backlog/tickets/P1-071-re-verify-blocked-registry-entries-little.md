---
id: P1-071
title: "Re-verify blocked registry entries (Little 2011, Codd 1970, Tail at Scale DOI)"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: medium
depends_on: []
estimate: 1
outputs: []
---

## Context

Left over from P1-016b and P1-016d: three entries could not be re-verified because the publisher blocks automated fetches or the source is unreadable.

## Tasks

1. `little-2011-littles-law-50th`: INFORMS returns HTTP 403; confirm metadata by another route (Crossref, the author's copy, a different network) and set `verified_on`.
2. `codd-relational-model-1970`: the UPenn PDF is a scan with no text; find a readable canonical URL (CACM or another stable copy), recheck metadata, set `verified_on`.
3. Tail at Scale (Dean and Barroso): the DOI is unconfirmed because ACM returns 403; confirm it via Crossref or another source.

## Done criteria

- [x] All three entries have `verified_on` and confirmed metadata
- [x] `python scripts/validate.py` passes

## Notes

2026-11-13: All three entries confirmed via Crossref, DOIs added for Codd and Tail at Scale, `verified_on` set. `source-verifier` passed after one note fix. See `sessions/2026-11-13-P1-071.md`.
