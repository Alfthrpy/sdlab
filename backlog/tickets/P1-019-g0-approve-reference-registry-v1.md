---
id: P1-019
title: "G0 — Approve Reference Registry v1"
milestone: M1
type: review
owner: human
review: human
status: done
priority: high
depends_on: [P1-016, P1-017, P1-018]
estimate: 1
outputs:
  - references/registry.yaml
---

## Context

Gate G0. The agent has prepared the registry, coverage, and gap list. The owner decides whether it is enough to start the curriculum.

## Tasks

1. Read `references/coverage.md` (a ready-to-decide summary is prepared by the agent in the Notes section).
2. Decide: approve, or ask for more research on specific gaps.
3. After approval, the agent changes the status of the chosen sources to `approved`. The validator requires `verified_on` (and `attribution` for adapt-with-attribution sources) on each of them.

## Done criteria

- [x] Owner decision recorded
- [x] Every unit has ≥ 1 approved Tier 1–2 source and ≥ 1 approved Tier 3–4

## Notes

2026-11-13: Owner approved registry v1 after reading the coverage summary and delegated the gap list to the agent. Gap dispositions are in `references/coverage.md`; follow-up research is P1-072..P1-077, which run in parallel with M2 and do not block G0.

Agent approved 146 sources (all non-Tier-6 candidates that pass the validator's `approved` rules). Left as `candidate`, because authors and/or published date are missing and are not to be invented: `raft-github-io`, `jepsen-linearizable`, `etcd-docs-why`, `etcd-docs-api-guarantees`, `zookeeper-docs-overview`, `zookeeper-docs-recipes`, `k8s-docs-leases`, `redis-docs-distributed-locks`, `kulkarni-hybrid-logical-clocks`, `ntp-org-how-ntp-works`, `mongodb-docs-causal-consistency`, `envoy-docs-circuit-breaking`, `k8s-docs-deployments`. Tier 6 (map-only) stays `candidate` by design.

Approved free sources per unit (Tier 1-2 / Tier 3-4): U0 24/1, U1 13/4, U2 23/7, U3 17/7, U4 22/1, U5 7/11, U6 20/18. Note: Unit 5 Tier 1-2 dropped from 17 to 7 because the 10 candidates that lack author/date metadata (etcd, ZooKeeper, k8s, Redis, Raft site, etc.) stay candidate.
