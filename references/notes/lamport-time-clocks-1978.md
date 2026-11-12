---
source: lamport-time-clocks-1978
read_by: agent
date: 2026-11-12
sections_read: ["Introduction", "The Partial Ordering", "Logical Clocks", "Ordering the Events Totally (skimmed)", "Physical Clocks (skimmed)"]
---

# Notes: Time, Clocks, and the Ordering of Events in a Distributed System

> Notes are in English and in your own words. Read via text extraction of the PDF (CACM, July 1978, pp. 558-565). Section names are as printed; the physical clock proofs were only skimmed.

## Key points

- (Intro) A system is "distributed" when message delay is not negligible compared with the time between events inside one process. In such a system it is sometimes impossible to say which of two events came first.
- (Partial ordering) "Happened before" is defined from three things: order inside one process, a send before its receive, and chaining of these. Events not connected this way are concurrent.
- (Logical clocks) Each process keeps a counter, bumps it between its own events, stamps messages with it, and on receive moves its counter past the incoming stamp. Then if a happened before b, a's stamp is smaller. The reverse does not hold: a smaller stamp does not prove causality.
- (Total ordering) Break ties with process ids to get one order of all events that respects causality. The paper uses this to build a mutual exclusion scheme, which is the basis for replicated state machines.
- (Physical clocks) Real clocks drift; the paper bounds how far synchronized clocks can differ given drift rate and message delay uncertainty, and shows logical ordering can still anomalously disagree with real-time order seen by users.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Copyright 1978 ACM; CACM July 1978 | page footer | Rewrite only |

## Relevant to concepts

- `logical-clocks`, `happened-before`: origin of Lamport clocks.
- `vector-clocks`: motivated by the one-way implication above (vector clocks are not in this paper).
- `replicated-state-machine`: total order of commands.

## Warnings

- 1978 notation (processes, "events"); learners need a modern worked example.
- No vector clocks or hybrid clocks here; use the Dynamo and HLC entries.
