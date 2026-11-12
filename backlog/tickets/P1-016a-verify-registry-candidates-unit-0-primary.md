---
id: P1-016a
title: "Verify registry candidates: Unit 0 (primary unit)"
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

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 0 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

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

(Filled in during the work.)

Done 2026-11-12: all 25 entries with primary unit 0 reopened (WebFetch) and given `verified_on`. Metadata matched the registry; no corrections to authors/dates/versions were needed. Changes: 8 `unknown` licenses resolved to `all-rights-reserved` (pages state no license; see the amended protocol rule 4), `NO-DATE:` explanations added for undated docs, OpenTelemetry got `NO-AUTHOR:` and an `attribution` line (CC BY 4.0 re-confirmed from the opentelemetry.io repo README). Simulated approval of all 25 passes the validator. Open choices for G0: pgbouncer/prometheus/hikaricp docs repos show ISC/Apache-2.0 but do not say they cover the docs text, so the conservative reading was kept. source-verifier (11 entries reopened, incl. Tier 1) found stale or contradictory notes on hikaricp, pgbouncer, gregg-use-method, opentelemetry; fixed (no metadata or license values changed).
