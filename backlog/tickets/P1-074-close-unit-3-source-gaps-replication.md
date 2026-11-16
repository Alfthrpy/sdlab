---
id: P1-074
title: "Close Unit 3 source gaps: replication, isolation, sharding and LSM depth"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: medium
depends_on: []
estimate: 2
outputs: []
---

## Context

Gap items A7, A8, B5 in `references/coverage.md`. `ddia-2e` is paywalled, so Unit 3 concepts lean on few free sources.

## Tasks

1. A7: find an operator source on failover and replication lag, and a free multi-leader source.
2. A8: find one free explainer on isolation levels and anomalies; re-read `berenson-critique-ansi-isolation-1995` in full.
3. B5: find a production sharding case beyond Notion and a modern write-amplification (LSM vs B-tree) source.
4. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [x] Every task above is done or recorded as a gap with a proposed action
- [x] `python scripts/validate.py` passes

## Notes

Research run 2026-11-16. All new entries are `candidate` with `verified_on` empty (verifier sets it, per research-protocol.md).

- A7 failover and lag: added `github-mysql-ha-2018` (Tier 2) and `github-oct21-2018-postmortem` (Tier 4). Multi-leader: added `dynamodb-docs-global-tables` (Tier 2, product docs, footer not seen). Gap remains: no free conceptual multi-leader source with a clear license (ddia.vonng.com translation was seen only in a search snippet and not opened; not registered). Proposed action: ask the owner whether a short multi-leader explainer should be written from couchdb-docs-replication-intro plus dynamodb-docs-global-tables, or find a CRDT/conflict paper (e.g. a Kleppmann paper) in a later ticket. Builders' Library has no replication article found in this session.
- A8: added `hermitage-isolation-tests` (Tier 5, CC BY 4.0) and `mysql-84-innodb-isolation-levels` (Tier 2). Berenson re-read in full from the PDF text; notes at `references/notes/berenson-critique-ansi-isolation-1995.md`; the registry entry notes were updated (venue SIGMOD 95 seen on the PDF cover).
- B5: added `figma-sharding-postgres-2024` and `slack-vitess-datastores-2020` (sharding cases), `tikv-docs-btree-vs-lsm` (Tier 2) and `qiao-btree-lsm-write-amp-2021` (Tier 3, license conflict recorded). Gap: Instagram sharding post could not be fetched (tool error); not registered. Gap: InnoDB MVCC internals (read views, undo log) still not covered. Gap: no GitHub/Vitess sharding case opened.
- Reading notes written for the Tier 2-3 sources listed above (web notes derive from fetch-tool summaries; marked in each note).

Verification (source-verifier): all 9 entries reopened; pass. Fixes: three overstated claims in the Slack reading notes were softened; the GitHub postmortem note now says "954 writes in the affected window" (the page does not say "unreplicated"). Entries stay `candidate` with empty `verified_on`.

Gaps left (proposed actions): free conceptual multi-leader source (only CouchDB intro, DynamoDB global tables, Dynamo paper; propose a CRDT/conflict-resolution paper or write the lesson from existing sources); Instagram sharding post (fetch failed); GitHub/Vitess sharding case (not searched); MySQL InnoDB MVCC internals (propose the MySQL 8.4 InnoDB multi-versioning page); Builders' Library replication article (none found); per-topic `free_companion` entries on `ddia-2e` (not done: out of scope for new entries). Licence doubts: Figma, DynamoDB footers unseen; TiKV docs content licence not found (software is Apache-2.0); Qiao paper arXiv says CC BY 4.0 but the PDF says CC BY-NC-ND 4.0 (strictest recorded); Hermitage has no LICENSE file (README says CC BY 4.0). Berenson was read in full as extracted text; the reference list, Figure 2, the last conclusion paragraph and the flattened Tables 1-3 were not reliably readable.
