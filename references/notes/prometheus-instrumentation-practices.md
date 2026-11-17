---
source: prometheus-instrumentation-practices
read_by: agent
date: 2026-11-17
sections_read: ["How to instrument", "The three types of services (online-serving, offline processing, batch jobs)", "Subsystems (libraries, logging, failures, threadpools, caches, collectors)", "Things to watch out for (labels, counter vs gauge, timestamps, inner loops, missing metrics)"]
---

# Notes: Instrumentation (Prometheus best practices)

> Notes are in English and in your own words. The page is short (about 12k characters) and was read in full from the raw page via curl; section headings are used as locations. The page has no author, version, or date; the footer shows only "© Prometheus Authors 2014-2026" and the Apache 2 note for components.

## Key points

- (How to instrument) Advice is to instrument everything: each library, subsystem, and service should expose a few metrics for a rough health picture. Define a metric in the same file in which it is used, so that going from an alert to the dashboard to the code is easy.
- (The three types of services) Services are grouped as online-serving (someone waits for an answer), offline processing (nobody waits, work often batched, several stages), and batch jobs (do not run continuously, so hard to scrape). Each type has a different set of key metrics.
- (Online-serving systems) The key metrics are the number of queries performed, the number of errors, and latency; the number of requests in progress is also useful. Measure on both the client and the server side, because differences between the two views are informative. Be consistent about counting a query at its start or end; the end is recommended since it lines up with the error and latency stats.
- (Offline processing) Per stage, track items in, items in progress, last processed time, and items out; a heartbeat item passed through the whole pipeline helps detect a stall.
- (Batch jobs) The key metric is the last time the job succeeded, plus stage durations and total runtime. These are pushed (PushGateway) because the job is short-lived. Very frequent jobs (say, more often than every 15 minutes) should become daemons.
- (Libraries) A library that talks to something outside the process (network, disk, IPC) should count queries, errors, and latency at minimum, with labels when it serves different targets (for example, a connection pool distinguishes databases).
- (Logging) For each logging statement, there should also be a counter incremented at that point. A log line tells what happened once; the counter tells how often and since when. It is also useful to export total counts of info/warning/error lines and compare them across releases.
- (Failures) Count each failure as well, and keep a total-attempts metric so the failure ratio can be computed.
- (Threadpools) Key metrics: queued requests, threads in use, total threads, tasks processed, task duration, queue wait time.
- (Caches) Key metrics: total lookups, hits, latency, plus the query count, errors, and latency of the backend behind the cache.
- (Use labels) Prefer one metric with a label (for example `http_responses_total` with a `code` label) over several separate metrics with the value in the name.
- (Do not overuse labels) Each label combination is another time series with memory/CPU/disk cost. Guideline: keep label cardinality below 10 for most metrics; investigate other solutions if one is above 100 or can grow there. Start with no labels and add when a real use appears.
- (Counter vs. gauge) If a value can go down, it is a gauge; counters only go up (or reset on restart). A raw counter is rarely useful, so take its per-second `rate()`. Never `rate()` a gauge.
- (Timestamps, not time since) Export the Unix time of an event and compute "time since" in the query.
- (Inner loops) Instrumentation cost is usually small compared with the benefits; for code called more than about 100,000 times per second per process, limit metric updates and labels. A Java counter increment is quoted at 12-17 ns.
- (Avoid missing metrics) Export a default of 0 for series you know might exist, so queries do not break when the first event has not occurred.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Online-serving key metrics: queries (count), errors, latency; in-progress requests also useful | Online-serving systems | Exact wording of this source. It does NOT use the names "RED", "rate" or "duration" for this set; "rate()" appears only as the function applied to counters (Counter vs. gauge) |
| One counter per logging line; also track total info/warn/error line counts | Logging | Direct support for explaining the difference between a log (what happened) and a metric (how often) |
| Counter cardinality guidance: keep below 10, investigate above 100 | Do not overuse labels | Guideline, not a hard rule |
| A Java counter increment costs 12-17 ns; care is only needed above about 100,000 calls/s per process | Inner loops | |
| node_exporter example: about 10,000 nodes x tens of filesystem series = roughly 100,000 series, fine; adding per-user quotas for 10,000 users would reach tens of millions, too many | Do not overuse labels | Shows label cost |
| Batch jobs run more often than every 15 minutes should become daemons | Batch jobs | |

## Relevant to concepts

- `basic-monitoring` objective 1 (distinguish log, metric, health check for the same problem): supports the log-vs-metric half well. The Logging section says each log statement should have a matching counter and gives the reason (frequency and duration vs single occurrence). The page does not mention health checks, so the third term must come from `aws-builders-implementing-health-checks`.
- `basic-monitoring` objective 2 (choose the minimum metrics: rate, errors, duration): supports it for online-serving services: queries, errors, latency (plus in-progress). The wording of this source is "number of performed queries, errors, and latency", not "rate / errors / duration". To get a rate, the page says to apply `rate()` to a counter. There is no mention of saturation as a golden signal on this page, although the threadpool metrics (queued requests, threads in use) are saturation-type signals. Compare with `google-sre-book-monitoring-ch6`, which uses "latency, traffic, errors, saturation".
- `basic-monitoring` objective 3 (health check "alive" vs "dependencies ok"): not supported; no health-check content on this page.
- Possible use in `single-machine-limits`: the threadpool and cache metrics are examples of software-resource saturation, but the page is not mapped there.

## Warnings

- The page is tool-specific ("opinionated guidelines" for Prometheus): the terms counter, gauge, label, `rate()`, PushGateway, scrape only make sense in that ecosystem. Use the generic idea (count requests, errors, latency) in Unit 0 and keep the Prometheus vocabulary minimal.
- No publication date, version, or named author; license is recorded conservatively as all-rights-reserved (see registry).
- Guidance on batch jobs, offline pipelines, PushGateway, and cardinality is beyond Unit 0 needs; do not pull all of it into a beginner lesson.
- "Latency" is the same quantity others call "duration" (RED), but this page itself says latency.
