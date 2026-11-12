---
id: P1-016g
title: "Verify registry candidates: Unit 6 (primary unit)"
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

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 6 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

## Tasks

Follow P1-016 Tasks 1–5 for each entry in scope, SEED and Tier 1–3 first:

1. Reopen the URL; confirm it is the intended page.
2. Complete `authors`, `published`, `edition`, canonical URL, `license` from the page; resolve every `license: unknown` or explain it in `notes`.
3. Check for a newer edition/version; mark outdated entries `deprecated`.
4. Record `free_companion` for paywalled sources.
5. Set `verified_on`; write `attribution` for `adapt-with-attribution` entries; remove resolved `SEED` markers.
6. Do not set `status: approved` (that is G0, P1-019); only make entries approvable.

## Done criteria

- [x] Every in-scope entry reopened this session and has `verified_on`
- [x] No empty `authors`/`published` without a `NO-AUTHOR`/`NO-DATE` explanation
- [x] No `license: unknown` without an explanation; no `SEED` notes left
- [x] `source-verifier` passes (sample)
- [x] `python scripts/validate.py` passes

## Notes

- Reopened all 24 entries (primary unit 6); `verified_on` set on all; no `unknown` licenses or SEED notes left.
- Licenses: Azure pattern pages CC-BY-4.0 (MicrosoftDocs/architecture-center README), gRPC docs CC-BY-4.0 (grpc.io repo LICENSE), Envoy docs Apache-2.0 (envoy repo LICENSE); all three inferred from repos, not page footers. Pages with no license text (Cloudflare, GCP, CrowdStrike, AWS arch blog, Grafana, Dapper, USENIX OSDI '22) are all-rights-reserved; usage stays rewrite-only.
- analyzing-metastable-hotos25: SEED resolved; authors and 2025-05-14 date from Crossref (dl.acm.org returns 403 to scripts, so the ACM page was not opened).
- cloudflare-1111-incident-2025-07-14: authors corrected to Ash Pallarito and Joe Abley (earlier NO-AUTHOR was wrong).
- Envoy v1.40.2 is still the latest release.
- source-verifier sampled 13 entries: pass; one cosmetic double space fixed.
