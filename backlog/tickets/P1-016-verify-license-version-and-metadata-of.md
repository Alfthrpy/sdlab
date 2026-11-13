---
id: P1-016
title: "Verify license, version, and metadata of all candidates"
milestone: M1
type: research
owner: agent
review: agent
status: in-progress
priority: high
depends_on: [P1-011, P1-012, P1-013, P1-014, P1-015, P1-069, P1-016a, P1-016b, P1-016c, P1-016d, P1-016e, P1-016f, P1-016g]
estimate: 2
outputs:
  - references/registry.yaml
---

## Context

Includes the 11 SEED entries from the initial research, some of whose metadata came from search results.

## Tasks

1. Reopen every entry (priority: SEED and Tier 1–3).
2. Complete `authors`, `published`, `edition`, canonical URL, and `license` from the source page.
3. Check the latest edition/version; mark outdated ones `deprecated`.
4. For `paywalled` sources, record a free companion source (`free_companion`).
5. Set `verified_on` on every entry you reopen, and write `attribution` for every `adapt-with-attribution` source.

## Done criteria

- [ ] No entry has empty `published` or `authors` unless truly unavailable (explained in notes)
- [ ] No `license: unknown` without an explanation
- [ ] All 'SEED' notes are removed or resolved
- [ ] Every entry intended for approval has `verified_on` (and `attribution` where required)
- [ ] `source-verifier` passes
- [ ] `python scripts/validate.py` passes

## Notes

Split on 2026-11-12 into P1-016a–g (one per primary unit 0–6, 20–26 entries each) because 163 candidate entries do not fit one session. This ticket closes when all seven are done and a final `python scripts/validate.py` plus a sample `source-verifier` pass confirm the done criteria across the whole registry.
