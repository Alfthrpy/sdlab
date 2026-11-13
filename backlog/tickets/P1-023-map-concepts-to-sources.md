---
id: P1-023
title: "Map concepts to sources"
milestone: M2
type: curriculum
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-021]
estimate: 1
outputs:
  - curriculum/concepts.yaml
---

## Context

Every concept needs ≥ 2 approved sources as input for content-writer.

## Tasks

1. Fill `sources` per concept, preferring a Tier 1–2 + free-source combination.
2. Concepts lacking sources → create extra research tickets.

## Done criteria

- [x] Every concept has ≥ 2 approved sources (see Notes: 8 are thin)
- [x] `python scripts/validate.py` passes

## Notes

- All 50 concepts now have `sources` (2-5 each), using only `approved`, non-Tier-6 registry entries. `ddia-2e` is unused (paywalled, chapters unverified).
- Several concepts meet the count but not the quality bar. The reviewer (`content-reviewer`) flagged them; they are tracked in gap tickets and the concept should not go to content-writer until they are closed:
  - P1-078: `rate-limiting`, `dns-networking-basics` (TCP/TLS), `distributed-transactions` (no saga/2PC source).
  - P1-079 (new): `back-of-envelope-estimation`, `transactions-acid`, `cache-stampede-hot-keys`, `stateless-services-sessions`, `capacity-headroom`, `app-plus-database`.
  - Existing: P1-072 (Unit 0), P1-073 (`cdn`), P1-074 (`replication`, `replication-lag-failover`, `isolation-levels`), P1-075 (`event-log-streaming`, `backpressure-consumer-lag`), P1-076 (`consistency-models`, `time-and-clocks`, `observability`).
- Review fixes: dropped `sre-book-handling-overload-ch21` from `back-of-envelope-estimation` and `jepsen-consistency-models` from `transactions-acid` (landing page); added `vogels-eventually-consistent-2008` to `replication-lag-failover` and `rfc-9111-http-caching` to `caching-basics`; corrected the MDN claim in P1-078.
- Not applied: `ietf-idempotency-key-header-draft` for `idempotency` (moving URL, P1-077), `dynamo-sosp07` for vector clocks (sections unread, P1-076).
- The `mdn-http-overview` registry note overstates that it excludes TCP/TLS; reword it at the next re-verification.
