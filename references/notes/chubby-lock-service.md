---
source: chubby-lock-service
read_by: agent
date: 2026-11-12
sections_read: ["Abstract", "1 Introduction", "2.1 Rationale", "2.4 Locks and sequencers", "2.8 Sessions and KeepAlives", "2.9 Fail-overs", "4 Use and surprises", "4.6 Lessons learned"]
---

# Notes: The Chubby lock service for loosely-coupled distributed systems

> Notes are in English and in your own words. Read via text extraction of the PDF. The PDF prints no venue or date; OSDI '06 (8 November 2006) is confirmed from the USENIX OSDI '06 technical sessions page.

## Key points

- (Abstract, 1) Chubby offers a file-system-like interface with advisory locks, built for availability and reliability rather than speed. GFS uses it to appoint a master; Bigtable uses it to elect a master, discover tablet servers, and store small metadata.
- (1) Before Chubby, Google services used ad hoc election, or needed operator intervention when correctness mattered. Primary election is a consensus problem, which Chubby solves once for everyone.
- (2.1) Design choice: coarse-grained locks held for hours or days (for example to elect a primary), not fine-grained locks held for seconds. Coarse locks put little load on the lock service and survive its failover. Clients that need fine-grained locks build them on top.
- (2.4) Because the lock is advisory and clients can be delayed, Chubby gives a "sequencer" (lock name, mode, generation) that a client sends to the protected server, which can check it; this is the same idea as a fencing token.
- (2.8) A session is kept alive by periodic KeepAlive handshakes and gives the client a lease. If contact is lost, the client has a grace period; the library signals "jeopardy", then "safe" or "expired" so the app can pause rather than act on a lock it may have lost.
- (2.9) When a master fails, the session lease timer pauses until a new master is elected; a client whose local lease estimate runs out enters a grace period during which it blocks API calls and gets a jeopardy event, and if a new master answers in time the failover is only a delay. The new master starts with a conservative estimate of the old leases.
- (4, 4.6) Later sections discuss real-world surprises and lessons; only 4.6 was read for takeaways, and these notes record none of its details.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Several instances handle tens of thousands of clients each | Abstract | As reported at publication |

## Relevant to concepts

- `lease-based-leadership`, `distributed-locks`: sessions, leases, sequencers.
- `consensus`: Chubby cells replicate with Paxos (not read closely).

## Warnings

- Not available outside Google; it is a model that ZooKeeper and etcd imitate.
- The paper was written long ago; numbers on usage are historical.
