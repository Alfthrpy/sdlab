---
source: raft-extended-paper
read_by: agent
date: 2026-11-12
sections_read: ["Abstract", "1 Introduction", "5.1 Raft basics", "5.2 Leader election", "5.4 Safety (skimmed)", "5.6 Timing and availability", "6 Cluster membership changes (skimmed)"]
---

# Notes: In Search of an Understandable Consensus Algorithm (Extended Version)

> Notes are in English and in your own words. Read via text extraction of the PDF; section numbers follow the paper. Section 8 (client interaction), 7 (log compaction), proofs and the evaluation were not read closely; 5.4 and 6 were skimmed.

## Key points

- (Abstract, 1) Raft is a consensus algorithm for a replicated log, claimed to be equivalent to multi-Paxos in result and efficiency, but split into separate parts (leader election, log replication, safety) to be easier to understand. The authors back the "understandable" claim with a user study of 43 students.
- (1) Raft uses a strong leader: log entries flow only from the leader to followers, so followers never push entries upward. This simplifies reasoning about the log.
- (1, 5.2) Leaders are chosen with randomized election timers on top of heartbeats, so that split votes are rare and resolve quickly.
- (5.1) Time is cut into numbered terms; a server that sees a higher term steps down. A cluster needs a majority of servers to make progress (for example 3 of 5), which is why odd-sized clusters are common.
- (5.4) Safety rule: a candidate cannot win unless its log is at least as up to date as a majority of voters', so a committed entry is never lost by a new leader.
- (5.6) Safety never depends on timing, but availability does. The paper states the needed relation as broadcast time much smaller than election timeout, much smaller than mean time between failures. It gives rough magnitudes (broadcast 0.5-20 ms, election timeout 10-500 ms depending on storage).
- (6) Membership changes go through a two-phase "joint consensus" so that two disjoint majorities can never exist during a switch.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Broadcast time may be 0.5 ms to 20 ms; election timeout likely 10 ms to 500 ms | 5.6 | Depends on storage latency; paper's own estimate |
| User study: 43 students, 33 answered Raft questions better than Paxos questions | Abstract | Small study at two universities |
| Extended version published May 20, 2014 | first page | Conference version: USENIX ATC 2014 (per raft.github.io) |

## Relevant to concepts

- `consensus`: what a replicated log with a majority quorum gives you.
- `leader-election`: terms, randomized timeouts, why a leader can be briefly absent.
- `quorum`: majority overlap as the safety argument.
- `flp-intuition`: Raft stays safe in asynchrony and gives up liveness when timing is bad, the practical response to FLP.

## Warnings

- The paper is about a replicated log, not about locks. Do not present Raft as a lock service; locks and leases are built on top (see etcd, ZooKeeper, Chubby entries).
- Typical timeout numbers are 2014-era estimates; tuning guidance in real systems differs.
