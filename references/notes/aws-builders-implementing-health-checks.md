---
source: aws-builders-implementing-health-checks
read_by: agent
date: 2026-11-12
sections_read: ["whole article, as summarized by the fetch tool"]
---

# Notes: Implementing health checks (Amazon Builders' Library)

> Notes are in English and in your own words. The fetch returned a summary, not full text; section names below are approximate.

## Key points

- Three kinds of check: liveness (is the process there and answering), local (can this server use its own disk and does the app really respond), and dependency (can it reach what it needs).
- Liveness checks need no application code; they are what a load balancer or external monitor typically does.
- A dependency check fails when the dependency is down, which can make a healthy server look broken.
- Pitfalls: a broken server that fails fast can attract more traffic; a check that depends on another service makes that service a hard dependency; an overloaded server too slow to answer pings gets removed and shifts load onto the rest.
- Automation that removes servers on failed checks needs safeguards (fail open, thresholds, rate limits, humans for uncertain cases).

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published 2019-12-05 | page header | Author shown only as "David" |

## Relevant to concepts

- `health-checks`: liveness vs. local vs. dependency, for Unit 0 a simple endpoint plus a database ping.
- Later (Unit 2): load balancing and automatic removal.

## Warnings

- Aimed at large fleets; most pitfalls need multiple servers and belong in Unit 2+.
- Not re-read in full; verify section names before citing.
