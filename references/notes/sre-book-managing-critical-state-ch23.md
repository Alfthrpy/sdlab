---
source: sre-book-managing-critical-state-ch23
read_by: agent
date: 2026-11-12
sections_read: ["CAP Theorem", "Motivating the Use of Consensus: Distributed Systems Coordination Failure", "How Distributed Consensus Works", "Distributed Consensus Performance"]
---

# Notes: SRE Book, Chapter 23: Managing Critical State

> Notes are in English and in your own words. Chapter written by Laura Nolan; Tim Harvey is the editor (not an author). Published year 2017 is the chapter footer copyright year; the google-sre-book registry entry records 2016 for the book.

## Key points

- (Motivating the Use of Consensus) Leader identity, group membership, lock ownership and queue message state are "critical state". Ad hoc mechanisms (heartbeats, gossip) tend to fail in subtle ways; a proven consensus protocol is the safer choice.
- (CAP Theorem) Partitions cannot be ruled out, so a system either serves possibly inconsistent data or pauses some requests. For data such as money, correctness is not traded for speed.
- (Case Studies 1-3) Three Google case studies where timeouts plus heartbeats caused two active primaries or no primary: replicated file servers with STONITH, a database failover that paged a human, and a search cluster where each side of a partition elected its own leader.
- (How Distributed Consensus Works) Proposals are numbered; a value is chosen once a majority accept; any two majorities overlap; acceptors must persist promises. Multi-Paxos keeps a stable leader so most decisions take one round trip. Dueling proposers can livelock; randomized backoff helps. Raft, Zab, Mencius follow similar ideas.
- (System Architecture Patterns) Teams normally consume consensus through Chubby, ZooKeeper, Consul or etcd instead of implementing it.
- (Performance) Cost is dominated by network round trips and disk writes; batching and pipelining help; replica count and placement trade fault tolerance against latency and cost.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Licensed CC BY-NC-ND 4.0, copyright 2017 Google | chapter footer | Rewrite only; no derivatives |
| Datacenter round trip about a millisecond; across continents tens of ms | Distributed Consensus Performance | Order of magnitude per the chapter |

## Relevant to concepts

- `consensus`, `leader-election`, `quorum`, `split-brain`: the free, practitioner-level entry point.
- `cap-pacelc`: a short operator framing of CAP.
- Trigger hint: you need consensus when more than one machine must agree on a single fact (who is leader) and a wrong answer corrupts data; for one database with one primary, the database's own failover tooling hides this.

## Warnings

- Google-scale framing; examples should be rewritten for small teams.
- Chapter is from 2017; mentions of tools (Consul, etcd) reflect that time.
