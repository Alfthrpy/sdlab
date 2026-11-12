---
source: kleppmann-distributed-locking-2016
read_by: agent
date: 2026-11-12
sections_read: ["What are you using that lock for?", "Protecting a resource with a lock", "Making the lock safe with fencing", "Using time to solve consensus", "Breaking Redlock with bad timings", "The synchrony assumptions of Redlock", "Conclusion"]
---

# Notes: How to do distributed locking

> Notes are in English and in your own words. Full page read. Footer license: CC BY 3.0 Unported (not in the schema enum, so registry license is unknown; rewrite only).

## Key points

- Two reasons to want a lock: efficiency (avoid doing work twice; an occasional double run is harmless) and correctness (two holders would corrupt data). The right tool depends on which one you need.
- A lock with a timeout (a lease) stops a crashed holder from blocking everyone forever. But a live holder can pause (GC, page fault, delayed packet), wake up after its lease expired, and still write.
- Fix: the lock service returns a number that grows with every grant (a fencing token); the client sends it with every write; the storage side remembers the highest token it saw and rejects older ones. The resource itself must do the check.
- Redlock (majority of independent Redis nodes) has no natural fencing token, and its safety assumes bounded pauses, delays and clock drift. Wall-clock jumps can expire a lock early.
- Safe algorithms should keep safety without timing assumptions (as consensus systems such as Raft, Paxos, Zab do) and only lose availability when timing is bad. For correctness-critical locks he recommends a consensus-backed service such as ZooKeeper plus fencing tokens; a single Redis is fine for efficiency-only locks.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Post dated 8 February 2016; update note: Redlock's author posted a rebuttal on 9 February 2016 and Kleppmann kept his conclusions | page header and update note | Redis docs link to it as the main critique of Redlock |

## Relevant to concepts

- `distributed-locks`: lease plus fencing token pattern; efficiency vs correctness locks.
- `leases`: why TTL alone is not safety.
- `clocks-and-time`: why wall-clock expiry is a risk.
- Trigger hint: a DB row lock or advisory lock in one database is enough while all writers use that same database; move to a consensus-backed lock only when several systems must agree and the protected resource cannot check a token.

## Warnings

- One side of a debate; the Redlock author's rebuttal was not opened here (the page itself points to it in its 9 Feb 2016 update note). Present both.
- Blog post, not peer reviewed. Use it for the argument, and the Chubby paper (sequencers) for the same idea in a production system.
