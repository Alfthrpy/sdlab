---
id: P1-079
title: "Add approved P1-072/P1-078 sources to concepts"
milestone: M2
type: curriculum
owner: agent
review: agent
status: done
priority: medium
depends_on: []
estimate: 1
outputs:
  - curriculum/concepts.yaml
---

## Context

P1-072 and P1-078 registered `candidate` sources for thin concepts. Only `approved` sources may be cited, and the owner approves them. Do this ticket after that approval. It needs the owner to approve (or reject) the candidates first, so do not start it before then.

## Tasks

1. List which P1-072 and P1-078 candidates are now `approved`.
2. Add each to `sources` of the concepts named in the P1-072 and P1-078 ticket Notes (backup-recovery, simple-deploys, basic-monitoring, app-plus-database, single-machine-limits; rate-limiting, dns-networking-basics, distributed-transactions, back-of-envelope-estimation, stateless-services-sessions, transactions-acid, capacity-headroom, observability).
3. Update `references/coverage.md` gap rows to match, and re-run the graph and validator.

## Done criteria

- [x] Every approved candidate is mapped to its concept(s)
- [x] Gaps still open (A1, TTL, 2PC, sticky sessions, headroom formula, beginner estimation) are listed in the ticket Notes
- [x] `python scripts/validate.py` passes

## Notes

- Scope grew beyond the title: all approved sources from P1-072, 074, 075, 076 and 078 (and older Unit 5-6 candidates) were mapped into `curriculum/concepts.yaml`; `references/coverage.md` has a new status table.
- Review (content-reviewer): pass with fixes, applied: `jepsen-serializable` moved from `consistency-models` to `isolation-levels`; `mongodb-docs-causal-consistency` added to `replication-lag-failover`; `envoy-docs-circuit-breaking` moved from `circuit-breaker` to `load-shedding` (static limits, not the state machine); `riak-docs-causal-context` mapped to `time-and-clocks` (best beginner vector-clock explainer); `zookeeper-docs-overview` and `etcd-docs-why` moved from `consensus` to `locks-leases-fencing` (consensus objectives are Raft-only).
- Approved but deliberately not mapped to any concept (outside the stated objectives; kept for later): `kulkarni-hybrid-logical-clocks` (HLC is in no objective), `dissecting-zab-yahoo-2010`, `sre-book-practical-alerting-ch10` (Borgmon-specific), `sre-book-release-engineering-ch8` (build pipelines more than rollout), the four Tier 6 `map-only` entries, and `dynamodb-docs-secondary-indexes`. The older Tier 4 incident entries belong to the incident layer, not concept `sources` (owner to confirm).
- Lesson-writing cautions: attribute the Honeycomb argument to the vendor view; frame `github-mysql-ha-2018` as contrast (automated failover) for the manual-failover objective; `consensus` has no source for the 2f+1 arithmetic beyond the Raft paper.

Open gaps (copied from the research tickets): A1 request lifecycle end to end (accept: MDN plus own diagram); DNS TTL beginner source; 2PC coordinator and blocking (only `ddia-2e` and `spanner-osdi12`); sticky sessions; atomicity/undo; headroom formula (the `capacity-headroom` trigger quotes 70-80% with no source: owner decision); beginner-sized estimation example; conceptual multi-leader source; InnoDB MVCC internals; Instagram and GitHub/Vitess sharding cases; Kafka ordering (KIP-98), Kafka consumer-lag alerting and Kafka retention coverage (`kafka.apache.org` unreachable); cross-hop 429/503 propagation; Fidge 1988 and the Zab DSN 2011 paper; a split-brain incident (accept for v1); `ddia-2e` per-topic `free_companion`; B11 `tail-at-scale-cacm13` full read (owner).

Thin coverage noticed by the reviewer but not tracked before: `consistency-models` quorum (R+W>N) rests on `dynamo-sosp07` only; `littles-law` (2 sources), `request-lifecycle` (2), and `cache-stampede-hot-keys`, `cdn`, `outbox-cdc`, `timeouts`, `load-shedding` (3 each) are thin but meet the minimum.
