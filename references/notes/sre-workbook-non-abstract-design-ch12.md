---
source: sre-workbook-non-abstract-design-ch12
read_by: agent
date: 2026-11-16
sections_read: ["whole chapter via fetch summary; verifier should reopen"]
---

# Notes: Non-Abstract Large System Design (SRE Workbook ch. 12)

> Notes are in English and in your own words.

## Key points

- (Worked example) The chapter sizes a click-tracking and query-logging design from stated assumptions: start with queries per second and click rate, then derive log volume per day, memory and disk needs, number of tasks and machines, and network bandwidth.
- (Method) Round numbers up, state assumptions, double the load when replicating across locations, and check the result against what one machine can hold (RAM, disk IOPS, bandwidth share).
- (Method) Estimate per-operation latency of the coordination layer to bound operations per second per process.
- (Headroom) Run more processes than the minimum so a backlog after downtime or a spike can be absorbed.
- (Design checks) Evaluate the design by asking what happens when components fail and whether SLOs still hold.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| About 500,000 queries/s and 10,000 clicks/s as the baseline | worked example | Specific to the case; teach as method |
| About 86.4 TB/day of logs from 2 KB entries, rounded to 100 TB | worked example | Shows the round-up habit |

## Relevant to concepts

- `back-of-envelope-estimation`: a Tier 1 worked estimate with units and rounding.
- `capacity-headroom`: only the "run more than the minimum" idea; no load-test method.

## Warnings

- Not interview-style and heavy on a large-scale ads case; beginners may need a simpler example. Hardware assumptions are old. Note was written from a model-written fetch summary; reopen before citing numbers.
