---
id: P1-016
title: "Verify license, version, and metadata of all candidates"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-011, P1-012, P1-013, P1-014, P1-015]
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

(Filled in during the work.)
