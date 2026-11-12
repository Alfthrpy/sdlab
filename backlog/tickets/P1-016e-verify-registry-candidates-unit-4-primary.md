---
id: P1-016e
title: "Verify registry candidates: Unit 4 (primary unit)"
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

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 4 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

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

2026-11-12: all 20 entries with primary unit 4 reopened, all with `verified_on`; metadata matched. Licenses: 7 `unknown` resolved. all-rights-reserved: AWS SQS docs x3 (no license in fetched text), Reactive Manifesto (may be copied only in its entirety, so no adaptation). CC-BY-3.0: Debezium outbox-event-router docs (own footer shows none; the Debezium blog footer on the same site says 'The website and documentation are licensed under CC BY 3.0'). CC-BY-4.0: Azure queue-based load leveling, competing consumers, publisher-subscriber (inferred from the public MicrosoftDocs/architecture-center README, same as cache-aside; page footers show nothing; usage stays rewrite-only). Kafka NetDB paper read with pdftotext ('NetDB'11 ... Copyright 2011 ACM'). NO-AUTHOR/NO-DATE notes added for undated docs.
