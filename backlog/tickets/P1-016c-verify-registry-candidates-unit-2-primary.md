---
id: P1-016c
title: "Verify registry candidates: Unit 2 (primary unit)"
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

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 2 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

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
- [ ] `source-verifier` passes (sample)
- [x] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)

2026-11-12: all 24 entries with primary unit 2 reopened; all have `verified_on`; metadata matched the registry (titles, authors, dates). Licenses: 10 `unknown` resolved. all-rights-reserved: Stripe docs, IETF draft and RFC 9110/9111 (IETF Trust 'all rights reserved' boilerplate), Cloudflare docs and blog (no footer), Envoy docs (Apache-2.0 repo does not state it covers docs), USENIX papers (open access to read, no license named). CC-BY-4.0: gRPC docs (repo LICENSE linked from footer), Azure cache-aside (inferred from the public MicrosoftDocs/architecture-center README; page itself shows no footer; usage stays rewrite-only). Attribution lines added for the two adapt-with-attribution entries (Microsoft REST API guidelines, Google AIP). Open: Microsoft api-guidelines CC BY 4.0 comes from a README badge; the scope over text and license.txt contents were not read.
Reviewer pass done 2026-11-12 (PASS): cosmetic note fixes only. Follow-up: azure-queue-based-load-leveling, azure-competing-consumers, azure-publisher-subscriber (Unit 4) and azure-circuit-breaker-pattern, azure-retry-pattern (Unit 6) should get the same MicrosoftDocs/architecture-center README check in P1-016e/g.
