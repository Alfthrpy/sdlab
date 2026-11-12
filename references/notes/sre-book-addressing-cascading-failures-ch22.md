---
source: sre-book-addressing-cascading-failures-ch22
read_by: agent
date: 2026-11-12
sections_read: ["Causes of cascading failures and designing to avoid them", "Preventing server overload", "Slow startup and cold caching", "Load shedding and graceful degradation", "Retries", "Latency and Deadlines (Picking a deadline, Missing deadlines, Deadline propagation, Cancellation propagation, Bimodal latency)", "Testing for cascading failures", "Immediate steps to address cascading failures", "Closing remarks"]
---

# Notes: SRE Book, Chapter 22 - Addressing Cascading Failures

> Notes are in English and in your own words. Chapter license is CC BY-NC-ND 4.0, so rewrite only.

## Key points

- (Causes) A cascading failure feeds itself: one failing part raises the failure chance of the others. One overloaded replica pushes its peers toward the same fate.
- (Server overload) Overload is the most common trigger. When a cluster fails, its traffic shifts to others and can fail them within minutes, even across regions.
- (Resource exhaustion) CPU, memory, threads, and file descriptors affect each other. More in-flight requests use more memory, more GC uses CPU, and lower cache hit rates push load to backends.
- (Unavailability) Crashing servers push load onto survivors and cause crash loops. Recovery may need load far below the level that caused the failure.
- (Load shedding, degradation) Reject excess work early and cheaply; degrade responses (cheaper ranking, smaller data) instead of failing. These paths are rarely used, so they need monitoring and regular tests.
- (Retries) Naive retries multiply load. Mitigations: randomized exponential backoff, per-request retry limits, server-wide retry budgets, retry at one layer, separate retriable from permanent errors.
- (Latency and Deadlines) Set deadlines, pass the remaining time down the call chain, and cancel downstream work no longer needed.
- (Testing) Load test until failure and watch recovery; test clients' retry behavior; verify non-critical backends cannot take down critical paths.
- (Immediate steps) Add capacity, pause health checks that cause restart churn, restart wedged servers, drop traffic, degrade, remove batch or harmful queries.
- (Closing) Features meant to raise reliability (retries, caching, failover) can themselves enlarge a failure.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Chapter by Mike Ulrich, copyright 2017 Google, CC BY-NC-ND 4.0 | page header/footer | The page names no editor (author only) |

## Relevant to concepts

- `cascading-failure`: causes and the overload feedback loop.
- `load-shedding`, `graceful-degradation`.
- `retry-budget`, `deadline-propagation`.
- ladder trigger: appears when one service sits behind many callers and a slow replica starts dragging others down.

## Warnings

- Written for Google-scale services with their own RPC stack; use the ideas, not the specifics.
- No numbers worth citing were extracted; quote none.
