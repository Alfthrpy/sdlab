---
source: little-2011-littles-law-50th
read_by: agent
date: 2026-11-12
sections_read: ["1. Introduction", "2. Queuing Processes Over a Finite Time Period (2.1, 2.3)", "4. Importance to Practice (4.1 Computer Architecture, opening)"]
---

# Notes: Little's Law as Viewed on Its 50th Anniversary

> Notes are in English and in your own words. Read directly from the PDF text (not a summary); only the parts listed were read closely.

## Key points

- (1. Introduction) The law relates three averages of a queuing system: the number of items inside (L), their arrival rate, and the average time each spends inside (W). L equals arrival rate times W. "Items" can be customers, aircraft, or instructions.
- (1. Introduction) The "system" includes both waiting and being served, and it can be any boundary one draws.
- (2) The usual proofs assume the process runs forever; practitioners observe a finite window, and over a finite window the relation is exact numerically when the system is empty at both ends (2.1).
- (2.1.1) Worked example: a supermarket day. Average time in store, arrival rate, and average number inside are tied together; if two are measured the third follows.
- (2.3) The most useful practical point: knowing any two of the three gives the third, which helps when one is hard to measure.
- (4.1) For servers, W is response time and L is requests in process; if the arrival rate is set by users, lowering W lowers the number of requests in flight.
- (4.1) The model ignores most details and has to be combined with other models for design decisions.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Operations Research 59(3), 536-549, May-June 2011; copyright INFORMS | PDF header | Source is a course-hosted copy |
| Original proof: Little 1961, Oper. Res. 9(3), 383-387 | Abstract | Not opened here |

## Relevant to concepts

- `littles-law`: the statement, the "any two give the third" use, and the finite-window caveat.
- `capacity-estimation`: concurrency (requests in flight) = rate x latency; ties to threads and connections in Unit 0.

## Warnings

- Academic tone; the section on theory (3) was not read.
- The paper's example of queue-related overhead (4.1.1) was only skimmed; do not cite for that without reading it.
- Real services violate the "independent averages" assumption when latency rises with load; see `brooker-telling-stories-littles-law`.
