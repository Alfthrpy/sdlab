---
source: brooker-telling-stories-littles-law
read_by: agent
date: 2026-11-17
sections_read: ["Intro", "Feedback", "Arrival Processes and Spiky Behavior", "Telling Stories", "footer"]
---

# Notes: Telling Stories About Little's Law (Marc Brooker)

> Notes are in English and in your own words. Whole page read via WebFetch and from raw HTML text (`curl`) on 2026-11-17. The page shows no date (registry date comes from the URL). Footer: Creative Commons Attribution 4.0 International; opinions are the author's own.

## Key points

- (Intro) Little's law: mean concurrency L equals mean arrival rate (lambda) times mean time W each request spends in the system. Its value is that capacity, hard to observe, can be reasoned about from request rate and latency, which are easy to measure.
- (Intro) Concurrency is a good capacity measure because it counts consumption of numerically limited resources; the page lists threads, memory, connections and file handles. Connections are named only in passing; there is no connection-pool worked example.
- (Feedback) The law needs long-term averages and treats lambda and W as independent. In real systems W rises with concurrency (contention), and lambda may fall, stay flat or rise with latency (clients that retry on timeout raise lambda when W rises). The result is plateaus and cliffs.
- (Arrival Processes) Means hide high-percentile behavior and non-stationary traffic (daily cycles, cron spikes), so estimates are less precise.
- (Telling Stories) A flash-sale example: latency rises from lock contention on the database, timeouts cause retries, retries raise load.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| L = lambda x W | Intro | The relation to use for "connections in use = queries per second x seconds per query" |
| Concurrency measures use of limited resources incl. connections | Intro | One sentence; supports applying the law to a connection pool |

## Relevant to concepts

- `connection-pooling` objective 2 (query-load part): PARTLY. Gives the arrival rate x time-in-system relation and says it applies to connections as a limited resource. The step "pool size = peak queries per second x average query seconds (plus headroom)" is a direct application by the lesson author, not stated on the page. Pair with `little-2011-littles-law-50th` (section 4.1 on servers) if a primary source is wanted.
- `connection-pooling` objective 3: the feedback section explains why a slow database makes a pool run out (W up, retries push lambda up).
- `littles-law` (Unit 1): primary use.

## Warnings

- Mean-based; peak and tail demand need headroom, which the page does not quantify.
- The law counts requests in the whole system; for a pool, W is the time a connection is held (checkout to return), not the end-to-end request time. The page does not discuss this distinction.
