---
source: google-sre-book-monitoring-ch6
read_by: agent
date: 2026-11-17
sections_read: ["Definitions", "Why Monitor?", "Setting Reasonable Expectations for Monitoring", "Symptoms Versus Causes", "Black-Box Versus White-Box", "The Four Golden Signals", "Worrying About Your Tail", "Choosing an Appropriate Resolution for Measurements", "As Simple as Possible, No Simpler", "Tying These Principles Together", "Monitoring for the Long Term (Bigtable, Gmail, The Long Run)", "Conclusion"]
---

# Notes: Site Reliability Engineering, Chapter 6: Monitoring Distributed Systems (Rob Ewaschuk; ed. Betsy Beyer)

> Notes are in English and in your own words. Chapter has no section numbers; locations are section headings. Read with WebFetch, and key wording and numbers (golden signals, 100 ms / 1% / 5 s example, 99.9% / 9 hours, absence of "RED" and "duration") were checked in the raw page text via curl. Footer: "Copyright 2017 Google, Inc. Published by O'Reilly Media, Inc. Licensed under CC BY-NC-ND 4.0".

## Key points

- (Definitions) The chapter first admits there is no standard vocabulary and fixes its own. Monitoring = collecting, processing, aggregating and showing real-time quantitative data (counts, error counts, processing times, server lifetimes). White-box monitoring = based on metrics exposed by the system's internals, and the chapter lists logs, profiling interfaces, and HTTP handlers that emit internal stats as examples. Black-box = testing externally visible behavior as a user would see it. Dashboard = a prebuilt view of the key metrics of a service. Alert = a notification to a human as a ticket, email, or page. Push = any change to the running software or its configuration.
- (Why Monitor?) Purposes: long-term trends, comparing over time or between experiment groups, alerting, dashboards for basic questions, and retrospective debugging ("latency jumped, what else changed around then?").
- (Why Monitor?, Tying These Principles Together) Pages cost human attention. A noisy alert trains people to ignore pages. The chapter's test for an alert: it should signal something urgent, actionable, needing human judgment, and not already covered by another page.
- (Symptoms Versus Causes) Monitoring should answer "what is broken" (the symptom) and "why" (the cause, possibly an intermediate one). Table 6-1 pairs examples such as HTTP 500s with database servers refusing connections, and slow responses with overloaded CPUs. The chapter calls this one of the most important distinctions for good monitoring.
- (Black-Box Versus White-Box) Black-box is symptom-oriented: it shows a problem that is happening now, so it is a good basis for paging, but it cannot warn about problems that have not happened yet. White-box inspects internals such as logs and HTTP endpoints, so it can reveal imminent problems and failures hidden by retries, and is needed for debugging. Which one is the "symptom" depends on the layer: slow database reads are a symptom for the database team and a cause for the web frontend team.
- (The Four Golden Signals) "If you can measure only four things for a user-facing system, measure these": latency, traffic, errors, saturation.
  - Latency: time to serve a request; keep successful and failed requests separate, because a fast error can make averages look good, and a slow error is worse than a fast one.
  - Traffic: demand on the system, in a high-level, system-specific unit (HTTP requests per second for a web service; sessions or network I/O for audio streaming; transactions and reads per second for a key-value store).
  - Errors: the rate of requests that fail, explicitly (HTTP 500), implicitly (HTTP 200 with wrong content), or by policy (slower than a promised response time). A load balancer sees complete failures; only end-to-end tests catch wrong content.
  - Saturation: how "full" the service is, focused on the most constrained resource (memory for a memory-bound system, I/O for an I/O-bound one). Many systems degrade before reaching 100% use, so a utilization target is needed. A 99th-percentile latency over a short window (about a minute) can be an early saturation signal. Saturation also covers predictions, for example a disk that will fill in some hours.
  - Measuring all four and paging when one is bad (or, for saturation, nearly bad) gives "decent" coverage.
- (Worrying About Your Tail) Averages hide problems: an average latency of 100 ms at 1,000 requests per second can coexist with 1% of requests taking 5 seconds. If a page depends on several backends, one backend's 99th percentile can become the frontend's median. The recommended remedy is a histogram of requests per latency bucket with buckets growing roughly exponentially (factor of about 3).
- (Choosing an Appropriate Resolution) Pick measurement frequency per goal: for a service with a 99.9% yearly availability target, checking for a 200 response more than once or twice a minute is overkill, and checking disk fullness more often than every 1-2 minutes too. To see brief CPU spikes cheaply, sample on the server each second into 5%-wide buckets and have the external system aggregate once a minute.
- (As Simple as Possible, No Simpler) Monitoring grows fragile if unbounded. Keep the alert rules that catch most real incidents simple; remove collection and alert rules that are rarely used; remove signals that appear on no dashboard and trigger no alert. Do not merge monitoring with profiling, debugging, load testing, log analysis, or traffic inspection; keep them separate with simple interfaces between them.
- (Tying These Principles Together, Conclusion) Page mainly on symptoms; use cause-based signals mainly to help debug; reserve cause-based pages for definite, imminent problems. Email alerts have limited value and become noise, so use dashboards (perhaps backed by logs for history) for lesser problems.
- (Monitoring for the Long Term) Two case studies, Bigtable (alerts based on a mean latency hid a bad tail and over-paged) and Gmail (alerts per descheduled task were unmanageable). These are about alert fatigue and are written for a very large organization.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| The "four golden signals of monitoring" are latency, traffic, errors, saturation | The Four Golden Signals | Exact words of this source. The chapter text does NOT contain the words "RED" or "duration"; it uses "latency" for time and "traffic" for demand, and "rate" appears only inside the definition of errors ("the rate of requests that fail"). "Rate" is therefore not a signal name here |
| Average 100 ms at 1,000 requests/s while 1% of requests take 5 seconds | Worrying About Your Tail | Good illustration for why to measure percentiles; needs the percentile lesson in Unit 1 |
| Histogram buckets spaced by factors of roughly 3 (0-10 ms, 10-30, 30-100, 100-300 ms ...) | Worrying About Your Tail | Example only |
| 99.9% yearly uptime = about 9 hours of downtime per year; probe for a 200 at most once or twice a minute at that target | Choosing an Appropriate Resolution | The 9-hour figure is the chapter's rounded number |
| A 10-12 person Google SRE team typically has one or two people mainly maintaining monitoring | Setting Reasonable Expectations | Context for scale: this is not a beginner's setup |
| CPU sampling example: record every second, 5% buckets, aggregate every minute | Choosing an Appropriate Resolution | |
| Copyright 2017 Google, published by O'Reilly, CC BY-NC-ND 4.0 | page footer | Matches the registry (rewrite-only) |

## Relevant to concepts

- `basic-monitoring` objective 1 (distinguish the use of log, metric, and health check for the same problem): partly supported. The chapter separates white-box monitoring (internal metrics and logs) from black-box (external probing, e.g. probing for a 200 response), and symptom from cause, and it mentions logs as a basis for historical analysis. It does not define "health check" as a term and does not compare logs and metrics side by side; the closest match to a health check is the black-box probe. Combine with `prometheus-instrumentation-practices` (log lines vs counters), `aws-builders-implementing-health-checks` and `owasp-logging-cheat-sheet`.
- `basic-monitoring` objective 2 (choose the minimum metrics: rate, errors, duration): supported, but the words differ. Source of the wording: this chapter says "four golden signals": latency, traffic, errors, saturation. The set "rate, errors, duration" is not in this chapter; the nearest names are traffic (rate), errors (errors), latency (duration). The saturation signal has no counterpart in the three-signal set. Prometheus's instrumentation page (separate note) says "number of queries, errors, latency" for online-serving systems. The registry maps `grafana-red-method` to another concept; the "RED" wording must be taken from that source, which this ticket did not open. A lesson that uses the RED words must state which source gave which wording.
- `basic-monitoring` objective 3 (health check that answers only "process is alive" vs one that checks dependencies): not supported by this chapter. It has no health-check discussion; the only related idea is that HTTP 500s caused by lost database connections show up as symptoms (Table 6-1). Use `aws-builders-implementing-health-checks`.
- `single-machine-limits` / `capacity-headroom` (mapped elsewhere, not this ticket): the saturation signal and the "utilization target, since many systems degrade before 100%" point are consistent with the USE method in gregg-use-method.
- Unit 1 (registry `units: [0, 1, 6]`): tail latency, alert design, and SLO-based paging are also in this chapter.

## Warnings

- The text is written for Google-scale SRE teams. For Unit 0, the registry notes recommend using only symptoms vs causes and the four signals; the tail-latency, resolution, long-term and case-study sections are for later units.
- The chapter mixes two levels of reader: operators of fleets and individual engineers. Statements such as "page a human" do not apply to a solo developer without on-call; the lesson must adapt this (alert to a chat or email, check dashboards daily).
- The page shows copyright 2017; tool references are generic (the chapter text I read names no specific monitoring product).
- Saturation here is defined broadly ("how full the service is") while USE defines it narrowly (queued extra work); do not equate the two without noting the difference.
- "Errors" in this source include implicit failures (HTTP 200 with wrong content) and policy failures (too slow), which a simple load-balancer error counter would not show.
