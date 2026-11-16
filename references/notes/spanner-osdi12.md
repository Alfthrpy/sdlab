---
source: spanner-osdi12
read_by: agent
date: 2026-11-16
sections_read: ["Abstract", "1 Introduction (skimmed)", "3 TrueTime", "4 Concurrency Control (4.1.1-4.1.4, 4.2.1-4.2.3)", "5.1 microbenchmarks (commit wait figure)", "5.3 TrueTime", "7 Future Work (TrueTime paragraph)", "8 Conclusions"]
---

# Notes: Spanner: Google's Globally-Distributed Database

> Notes are in English and in your own words. Read via pdftotext of the USENIX OSDI '12 PDF (pages 251-264 of the proceedings). Not read in detail: 2 Implementation (2.1-2.3 skimmed only), 5.2 availability, 5.4 F1, 6 related work, Appendix A (lease disjointness, only its start). Two-column extraction scrambled some symbols (epsilon, subscripts), so formulas below are described in words.

## Key points

- (3) TrueTime exposes time as an interval instead of one number. `TT.now()` returns an earliest and latest bound that is guaranteed to contain the real time of the call; `TT.after(t)` and `TT.before(t)` say whether t has definitely passed or definitely not arrived. The half-width of the interval is the uncertainty (epsilon).
- (3) Two kinds of time references are used on purpose, GPS receivers and atomic clocks, because they fail in unrelated ways (GPS: antenna, interference, spoofing, leap-second bugs; atomic clocks: slow drift). Each datacenter has several time-master machines; every machine runs a daemon that polls multiple masters, throws out outliers with a variant of Marzullo's algorithm, and evicts itself if its local clock drifts beyond the worst-case bound.
- (3) Between polls the daemon's advertised uncertainty grows linearly at an assumed worst-case drift rate, giving a sawtooth; the paper reports it varying roughly 1 to 7 ms with the average around 4 ms, a 30 s poll interval and 200 microseconds per second assumed drift.
- (4.1.2) Spanner keeps three invariants: timestamps within a Paxos group increase monotonically (even across leaders), leaders' lease intervals are disjoint, and external consistency (if T2 starts after T1 commits, T2's timestamp is larger).
- (4.1.2) External consistency comes from two rules. Start: the coordinator picks a commit timestamp no smaller than the latest bound of `TT.now()` taken after the commit request arrived. Commit wait: nothing the transaction wrote becomes visible until `TT.after(commit timestamp)` is true. The short proof chains these two facts with the causal assumption.
- (4.2.1) In a read-write transaction, writes are buffered at the client, reads take locks at leaders (wound-wait for deadlocks), the client drives two-phase commit, participants log prepare records through Paxos, and the coordinator chooses a timestamp at least as large as every prepare timestamp. It then waits out the commit wait before applying and releasing locks. The expected wait is at least twice the average uncertainty, and it overlaps with Paxos replication.
- (4.1.3, 4.1.4, 4.2.2) Read-only transactions and snapshot reads run lock-free at a timestamp. A replica can serve a read at t only if t is not beyond its "safe time"; prepared-but-uncommitted transactions hold safe time back. For multi-group reads Spanner simply uses the latest bound of `TT.now()`, which may have to wait.
- (4.2.3) Atomic schema changes work by assigning the change a timestamp in the future; operations with later timestamps block behind it, earlier ones proceed. The paper says this would be meaningless without TrueTime.
- (5.1) In the one-replica microbenchmark, commit wait costs about 5 ms and Paxos about 9 ms.
- (5.3) The authors argue clock errors beyond the assumed drift bound are rare compared with other hardware faults (bad CPUs were about 6 times more likely than bad clocks). Uncertainty percentiles are mostly small but have tail spikes from network congestion or time-master maintenance; those spikes directly raise commit latency.
- (7, 8) They expect to push uncertainty below 1 ms, and conclude that systems should stop relying on loosely synchronized clocks with weak time APIs.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Typical uncertainty about 1-7 ms, average about 4 ms | Sec. 3 | Production figures at paper time (2012) |
| Poll interval 30 s, assumed drift 200 microseconds/s | Sec. 3 | Parameters, not guarantees for other systems |
| Expected commit wait at least 2x average uncertainty | Sec. 4.2.1 | Overlaps with Paxos latency |
| Commit wait about 5 ms, Paxos about 9 ms (1 replica) | Sec. 5.1 | Microbenchmark |
| Default leader lease 10 seconds | Sec. 4.1.1 | Leases bound leader overlap |

## Relevant to concepts

- `time-and-clocks`: why physical clocks need explicit uncertainty; contrast with NTP and HLC.
- `consistency-models`: external consistency is the strict-serializability-like guarantee; see `jepsen-linearizable` and `jepsen-serializable` for definitions.
- `distributed-transactions`: 2PC over Paxos groups, prepare timestamps, commit wait.
- `locks-leases-fencing`: timed leader leases and the disjointness invariant.

## Warnings

- TrueTime needs GPS and atomic-clock hardware; the paper says its details are left to another paper. Do not teach it as something a normal team can replicate.
- 2012 numbers; later Google material may differ and was not read.
- The paper states Spanner chooses consistency over availability, but only as a design statement, not a formal CAP analysis.
- Appendix A and 5.4 F1 were not read in depth.
