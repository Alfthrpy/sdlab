---
source: sre-book-slo-ch4
read_by: agent
date: 2026-11-12
sections_read: ["Service Level Terminology", "Indicators in Practice", "Objectives in Practice", "Agreements in Practice"]
---

# Notes: Site Reliability Engineering, Chapter 4: Service Level Objectives

> Notes are in English and in your own words. Section names are the headings on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (Service Level Terminology) Three layers: an SLI is a measured quantity (latency, error rate, throughput), an SLO is a target for that quantity, and an SLA is a contract with consequences if the target is missed.
- (Indicators in Practice, What Do You and Your Users Care About) Choose a handful of indicators that reflect what users feel; tracking every available metric dilutes attention.
- (Indicators in Practice, Collecting Indicators) Server-side measurement is the default, but client-side measurement is needed when server data would miss what users experience.
- (Indicators in Practice, Aggregation) Averages hide slow requests, so latency is better summarized with percentiles that show the shape of the distribution.
- (Objectives in Practice, Defining Objectives) An SLO says how it is measured and over what conditions, and it leaves room for some failures (an error budget) rather than demanding 100%.
- (Objectives in Practice, Choosing Targets) Targets come from what the product needs, not from what the system happens to do today; keep few, simple, and revisable.
- (Objectives in Practice, Control Measures) SLOs close a loop: measure, compare, decide, act.
- (Objectives in Practice, SLOs Set Expectations) Publishing a target creates user dependence on it; keep an internal margin tighter than the public number.
- (Agreements in Practice) SLA penalties are a business and legal matter; promise conservatively.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Copyright 2017, CC BY-NC-ND 4.0 | page footer | Rewrite and link only; no derivative text |

## Relevant to concepts

- `sli-slo`: the vocabulary and the loop.
- `percentiles`: motivation for percentiles over averages (the chapter's argument, not the math).
- `is-this-stage-enough` (Unit 1 trigger): an SLO breached or budget used up is a concrete trigger to move to the next stage.

## Warnings

- Written from Google's scale; the worked examples are large services. Small-service examples must be created independently.
- Percentile mechanics (how to compute them) are not here; see `prometheus-histograms-practices`.
