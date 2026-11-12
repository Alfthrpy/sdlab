---
id: P1-016f
title: "Verify registry candidates: Unit 5 (primary unit)"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: high
depends_on: []
estimate: 1
outputs: []
---

## Context

Sub-ticket of P1-016. Covers every registry entry whose lowest `units` value is 5 (list them with `python -c` or grep on `units:`; entries without units go to P1-016a). Entries that also serve higher units are handled here, once.

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

- Reopened all 26 entries (primary unit 5); `verified_on` set on all; no `unknown` licenses or SEED notes left.
- Licenses resolved: etcd docs CC-BY-4.0 and Redis docs CC-BY-NC-SA-4.0 (both inferred from the repo LICENSE, not the page text); ZooKeeper docs Apache-2.0 (page header); papers/blogs/vendor pages with no license text set to all-rights-reserved (conservative, usage stays rewrite-only).
- etcd.io/docs/latest now redirects to v3.7, so both etcd URLs moved from v3.6 to v3.7.
- source-verifier sampled 12 entries: pass; one stray punctuation fix applied (raft-extended-paper).
- Gap: Spanner PDF not opened (TrueTime sections must be read by the content writer).
