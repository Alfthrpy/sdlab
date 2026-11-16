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

- [x] Every concept has ≥ 2 approved sources
- [x] `python scripts/validate.py` passes

## Notes

- All 50 concepts have `sources` with 2–5 approved registry ids (Tier 1–2 plus free sources preferred; Tier 3 papers only where they are the primary source).
- Thin coverage is recorded in P1-078 (rate limiting, TCP/TLS, saga/2PC). `distributed-transactions` uses `ddia-2e` (paywalled; its free companions only cover Unit 1, so there is no free Unit 5 source).
- Units 0, 3 and 4 gaps from P1-072/074/075 are not yet closed; concepts there meet the minimum but may gain sources later.
- Candidate sources (raft-github-io, etcd, zookeeper docs, jepsen-linearizable, HLC, NTP) were not used because they are not approved.

- Review (content-reviewer): pass with minor fixes. Applied: added `brooker-telling-stories-littles-law` (latency-throughput), `ddia-2e` (transactions-acid), `stripe-blog-idempotency` (idempotency); replaced `cassandra-docs-dynamo` with `pg-docs-high-availability` in `replication` (leaderless is contrast, not primary).
- Concepts with no or weak Tier 1-2 coverage: `back-of-envelope-estimation` (none), `distributed-transactions` (only paywalled `ddia-2e`), `latency-throughput`, `rate-limiting`, `dns-networking-basics`, `stateless-services-sessions`. All tracked in P1-078. `request-lifecycle` (app-to-database stage) belongs to P1-072; `transactions-acid` isolation parts to P1-074.
- Treat these concepts as blocked for content-writer until P1-078 (or P1-072/074) lands.
