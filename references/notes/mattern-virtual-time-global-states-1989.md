---
source: mattern-virtual-time-global-states-1989
read_by: agent
date: 2026-11-16
sections_read: ["1 Introduction", "6-7 Virtual time and Vector time (read)", "8 Structure of vector time (definition 4 read, rest skimmed)", "10 Application of vector time"]
---

# Notes: Virtual Time and Global States of Distributed Systems

> Notes are in English and in your own words. Read via pdftotext of a university-hosted copy; symbols were garbled, so rules are described in words. Sections 2-5 (event structures, consistent cuts, global states), 9 (Minkowski space-time) and 11 onward were only skimmed or not read.

## Key points

- (1) With no shared memory and unpredictable message delays, no process sees the whole system; the paper studies simulating global time and global state to make algorithms simpler.
- (7) Vector time: each process keeps a vector with one slot per process; it advances its own slot at each event, attaches the vector to outgoing messages, and on receive takes the componentwise maximum of its vector and the message's vector (then ticks). A process always knows its own slot best, so every other process's view of it is at most the real value.
- (7, 8) Vectors can be compared: one is "less" if every slot is less or equal and they are not identical; two vectors where neither is less are concurrent. This gives an exact match with causality, unlike scalar Lamport clocks where a smaller stamp does not prove cause.
- (10) Use: finding possible race conditions in traces (two events with incomparable vectors are concurrent), debugging, and measuring potential parallelism. The paper says Fidge independently proposed the same idea.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Copyright 1989 Elsevier Science Publishers B.V., edited version, reproduced with author's permission | first-page footnote | Workshop was October 1988 |

## Relevant to concepts

- `time-and-clocks`: logical time beyond Lamport scalars; vector clocks detect concurrency.
- `consistency-models`: causal consistency needs a way to tell causal from concurrent writes (pair with `jepsen-causal`, `dynamo-sosp07`).

## Warnings

- Vector size grows with the number of processes; this paper does not discuss pruning or dotted version vectors (see `riak-docs-causal-context`).
- Fidge 1988 not opened; do not cite it.
