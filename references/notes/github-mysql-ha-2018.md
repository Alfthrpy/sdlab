---
source: github-mysql-ha-2018
read_by: agent
date: 2026-11-15
sections_read: ["Whole article (raw HTML converted to text)"]
---

# Notes: MySQL High Availability at GitHub (Shlomi Noach, 2018)

> Notes are in English and in your own words.

## Key points

- (Objectives, intro) A cluster is one writable primary with asynchronous replicas. With no primary no write can be saved, so the design goal is to shorten the time with no writer and to make the switch lose as little as possible.
- (Moving away from VIP and DNS) The old design advertised the primary through a virtual IP plus DNS. Problems named: the old primary has to cooperate in releasing the address, so two hosts can believe they own it; DNS answers are cached by clients so a change spreads slowly, especially across data centers; failover also needed manual restart of helper tools (lag heartbeats, Pseudo-GTID).
- (GitHub's HA solution) New flow: apps connect to a stable writer name that reaches a proxy tier; orchestrator detects the failure and promotes a replica; the new primary's identity is written to Consul; each proxy picks it up from Consul and reloads its backend list. Clients never rediscover the primary themselves.
- (orchestrator/raft failure detection) Failure is judged from several signals together (the primary's own view and its replicas' view), which the author says gave no false-positive failovers. Orchestrator runs as a raft group across data centers where no single site is a majority, so a site that is cut off cannot elect itself leader; the decision falls to the majority outside the isolated site.
- (Quicker advertisement) If a suitable promotion candidate exists, orchestrator makes it writable and advertises it first, and repairs the rest of the replication tree afterwards, because the tree repair takes several more seconds.
- (Semi-synchronous replication) Commit waits for at least one replica to have the change, so a primary crash usually loses nothing. Cost: if no replica answers, writes stall; a 500 ms timeout lets the primary fall back to asynchronous mode. They enable it on same-data-center replicas and expect, but do not enforce, lossless failover; they do not expect lossless on a whole-data-center failure because that would be too expensive.
- (Semi-synchronous replication) Side effect used on purpose: marking designated replicas as semi-sync makes them the usual promotion winners, which makes the quick advertisement path more likely.
- (Heartbeat injection) Replication lag and throttling are measured with heartbeat rows written by a service that runs on every server all the time: it writes only on whichever server is currently writable, so no manual start or stop is needed during failover.
- (Limitations and drawbacks) The proxy hides which application is connected from the primary. A primary in an isolated data center can still receive writes from apps in that data center, leaving divergent data after the network heals; they were working on fencing the isolated primary and say fully avoiding split-brain is very costly.
- (The results) Outage per failover: 10-13 s in most cases, up to 20 s less often, up to 25 s in extreme cases; failovers typically lossless; detection reliable.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Total outage 10-13 s typical, up to 20 s, up to 25 s in extreme cases | The results | GitHub's own fleet and tooling in 2018 |
| Semi-sync fallback timeout 500 ms | Semi-synchronous replication | Their chosen value, not a default |
| Orchestrator nodes spread so that no single data center is a quorum | orchestrator/raft failure detection | Design choice to survive site isolation |

## Relevant to concepts

- `failover`: detect, choose a candidate, promote, advertise; why the advertise step (discovery) matters as much as the promotion.
- `replication-lag`: lag measured by heartbeat rows; semi-sync as the trade of write latency and availability for lower data loss.
- `split-brain`: the unhandled isolated-data-center case, and why fencing is needed.
- Pairs with the incident that followed four months later (`github-oct21-2018-postmortem`).

## Warnings

- MySQL- and GitHub-specific (orchestrator, Consul, GLB/HAProxy, pt-heartbeat). Teach the pattern, not the stack.
- The author reports no false positives and lossless failovers as typical; that is an operator's claim from their own fleet, and the Oct 2018 incident shows an automated failover that was correct by its rules but harmful in outcome.
