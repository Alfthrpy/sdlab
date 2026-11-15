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

Eight new `candidate` entries in `references/registry.yaml` plus a re-read of Berenson, all opened on 2026-11-15 and reopened by `source-verifier` (first verdict: FAIL, fixable; all required fixes applied, see below). Reading notes are in `references/notes/`.

| Gap | Result | Entry |
| --- | --- | --- |
| A7 failover and replication lag | **Closed.** GitHub's MySQL HA design (orchestrator, Consul, semi-sync, heartbeat lag) plus its Oct 21 2018 postmortem (automated cross-region failover with async replication led to divergent writes; Tier 4, also the first data-incident case for Unit 3). GitHub-specific: teach the pattern, not the tooling. No Builders' Library article was found. | `github-mysql-ha-2018` (T2), `github-oct21-2018-postmortem` (T4) |
| A7 free multi-leader source | **Partly closed.** Vendor docs (DynamoDB global tables: last-writer-wins, or synchronous reject-and-retry) and Slack's multi-primary shard pairs. Still no neutral source on conflict detection, CRDTs or topologies. Proposal: **accept**, pair with `couchdb-docs-replication-intro`; or open a small follow-up for an open multi-leader or CRDT source. | `dynamodb-docs-global-tables-v2` (T2, no license stated), `slack-vitess-2020` |
| A8 isolation explainer | **Partly closed.** Hermitage is a precise table of real behaviour per database plus runnable tests, not a beginner narrative (its README says so). No gentle free explainer was found. Proposal: **accept** and pair with the PostgreSQL transaction-isolation docs already in the registry, or open a follow-up. | `hermitage-isolation-tests` (T5, CC BY 4.0 from the README only) |
| A8 Berenson re-read | **Closed.** Full text read (13-page PDF). DOI added after the verifier checked Crossref and I re-checked it: `10.1145/223784.223785` (SIGMOD '95 proceedings); the SIGMOD Record DOI `10.1145/568271.223785` is in `notes`. | `berenson-critique-ansi-isolation-1995` (changed) |
| B5 sharding beyond Notion | **Closed** with two cases: Slack (Vitess, double-write migration; the channel-id key is only a stated goal) and Figma (triggers, hashed key, logical views before the physical split, rollback kept). Instagram's post was unreachable (503 / reset), so it is not registered. | `slack-vitess-2020` (T2), `figma-horizontal-sharding-2024` (T2) |
| B5 LSM vs B-tree | **Closed.** Production case (Facebook MyRocks: instances 62.3% smaller, bytes written down 75%) and a counterpoint (FAST '22 paper on closing the write-amplification gap, needs compressing drives, vendor-affiliated authors). | `myrocks-vldb20` (T3, CC BY-NC-ND 4.0), `qiao-btree-lsm-write-amp-fast22` (T3) |

- Verifier fixes applied: GitHub notes said the postmortem came "three years" after the HA post (it was four months); Slack wording ("at least two instances per shard"; channel-id sharding is a stated goal, not confirmed); DynamoDB "best effort" belongs to the legacy page, and "no license stated" is now explicit; Berenson DOI recorded and `verified_on` updated.
- Qiao: the verifier found the paper was published at FAST '22. I opened the USENIX page and PDF myself, switched the entry to that version (id renamed from `-2021` to `-fast22`, nothing referenced the old id), corrected section numbers (write amplification is 2.4, evaluation is 4) and the "about 4 times" figure (4 to 7 times). The FAST version states no license, so it is all-rights-reserved. These last fixes were not sent back through `source-verifier`.
- Not registered, with reason: GitHub "Partitioning GitHub's relational databases" (2021, vertical and functional partitioning; add only if a lesson on vertical partitioning needs it); TiKV "B-Tree vs LSM-Tree" (docs repo license not confirmed); the ACM page for Berenson (403).
- Licenses still unconfirmed: AWS Site Terms were not opened (DynamoDB entry is the default, all-rights-reserved); Hermitage license rests on the README line alone. A human may want to confirm both before the entries are approved.
- Not done: no entry is `approved`; `references/coverage.md` and `curriculum/concepts.yaml` were not changed (as in P1-072); `ddia-2e` per-topic `free_companion` entries were outside the tasks. Owner: confirm the accept proposals for A7 (multi-leader) and A8 (beginner explainer).
- `validate.py`: 0 errors, 31 warnings (missing DOIs and editions, all existing kinds).
