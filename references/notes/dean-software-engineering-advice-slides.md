---
source: dean-software-engineering-advice-slides
read_by: agent
date: 2026-11-12
sections_read: ["slides 1-16: title through 'Back of the Envelope Calculations'"]
---

# Notes: Software Engineering Advice from Building Large-Scale Distributed Systems (Jeff Dean)

> Notes are in English and in your own words. Slides are image-only; read visually, slide numbers counted from the title slide. No date on the deck.

## Key points

- (slide 12 "Designing Efficient Systems") Being able to estimate how a design will perform without building it is named as a core design skill.
- (slide 13 "Numbers Everyone Should Know") A single table of latencies spanning cache, memory, network, and disk shows the orders-of-magnitude gaps that make estimates possible.
- (slides 14-16 "Back of the Envelope Calculations") Worked example: building an image-results page of 30 thumbnails by reading serially versus in parallel; the estimate shows parallel reads cut time by more than an order of magnitude, and the author adds that variance pushes the real figure higher. Estimation is used to pick which design variants (caching, precomputed thumbnails) deserve effort.
- (slide 4 "The Joys of Real Hardware") In a new cluster's first year, many machine, rack, and network failures are expected, so failure is routine at scale.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Round trip within one datacenter about 500,000 ns (0.5 ms) | slide 13 | Old hardware era; use as order of magnitude only |
| Disk seek about 10 ms; read 1 MB from memory about 250 us | slide 13 | Same caveat |
| Serial design 560 ms vs parallel design 18 ms (author says really 30-60 ms) | slides 14-15 | Assumes 10 ms seek, 30 MB/s disk |

## Relevant to concepts

- back-of-envelope estimation: method (list operations, multiply by latency, compare designs).
- latency numbers: why network and disk dominate in-memory work.

## Warnings

- Undated and old; modern hardware differs (SSDs, faster networks). Do not teach the values as current.
- Posting rights of the hosted copy are unverified; link only.
