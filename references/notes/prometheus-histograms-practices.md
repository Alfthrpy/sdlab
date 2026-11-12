---
source: prometheus-histograms-practices
read_by: agent
date: 2026-11-12
sections_read: ["Quantiles", "Bucketing", "Errors of quantile estimation"]
---

# Notes: Histograms and summaries (Prometheus best practices)

> Notes are in English and in your own words. Section names are headings on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (Quantiles) Two ways to get percentiles: a summary computes them inside the application; a histogram only exports bucket counts and the server computes the quantile at query time with `histogram_quantile()`.
- (Bucketing) Classic histograms use boundaries fixed in advance and every bucket is an extra time series; native histograms pick buckets on an exponential scale so you set a resolution instead.
- (Bucketing) The page's framing: a histogram is basically a set of bucketed counters.
- (Errors of quantile estimation) Quantiles are estimates. A summary bounds the error on the percentile axis; a histogram bounds it on the value axis (width of the bucket the percentile falls into).
- (Inference, not stated on the page) Practical consequence for learners: choose bucket boundaries around the SLO threshold, otherwise the reported p99 can be far off.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| No date or version on the page; footer credits Prometheus Authors 2014-2026 | page footer | Docs license unclear (license: unknown in registry) |

## Relevant to concepts

- `percentiles`: how p50/p95/p99 are computed from real metrics.
- `sli-slo`: a latency SLI needs a bucket boundary at the threshold.

## Warnings

- Prometheus-specific; the concepts apply to any histogram-based monitor.
