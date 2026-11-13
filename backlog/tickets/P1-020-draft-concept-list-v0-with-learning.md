---
id: P1-020
title: "Draft concept list v0 with learning objectives"
milestone: M2
type: curriculum
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-019]
estimate: 2
outputs:
  - curriculum/concepts.yaml
---

## Context

Draft ~46 concepts for the 7 units (0–6). Each concept in Units 1–6 gets a `trigger` (ADR 0004 Amendment 1). Use the `curriculum-designer` subagent.

## Tasks

1. Derive concepts from the unit table and coverage.
2. Check coverage against Tier 6 sources (only to make sure no common topic is missed).
3. Write 1–4 learning objectives per concept (Indonesian, starting with 'Bisa ...').

## Done criteria

- [x] 40–50 concepts across 7 units (0–6)
- [x] Every concept in Units 1–6 has a `trigger`
- [x] Every concept has testable learning objectives
- [x] `content-reviewer` passes
- [x] `python scripts/validate.py` passes

## Notes

2026-11-13: `curriculum/concepts.yaml` v0 has 50 concepts (U0 8, U1 6, U2 9, U3 8, U4 5, U5 6, U6 8). `content-reviewer` ran twice: pass 1 found 5 accuracy issues (Lamport vs vector clocks, quorum vs linearizability, outbox, read-your-writes, CAP framing), weak triggers, and 3 missing topics (added `stateless-services-sessions`, `dns-networking-basics`, `distributed-transactions`); pass 2 passed with minor fixes, applied. Reverse proxy is merged into `load-balancer-reverse-proxy`; adaptive concurrency is out. Deferred topics (object storage, search, WebSocket push, autoscaling, multi-region, service discovery) are a comment at the top of the file. The list is at the 50 cap: any addition needs a swap. No sources or prerequisites yet (P1-023, P1-021).

For P1-021 (from the second review): put `transactions-acid` and `isolation-levels` early in Unit 3 as prerequisites; `time-and-clocks` before `consistency-models`; `cap-pacelc` after `consistency-models`; `idempotency` before `retry-backoff-jitter` and `delivery-semantics`; `distributed-transactions` after idempotency, delivery-semantics, outbox-cdc, consensus. Possible splits if the cap allows: quorums out of `consistency-models`, failover out of `replication-lag-failover`, 2PC vs saga. Keep `back-of-envelope-estimation` (estimate) distinct from `capacity-headroom` (measured), and `connection-pooling` (empirical) from `littles-law` (formal). Owner should read the triggers of `data-models`, `index-structures`, `consistent-hashing`.
