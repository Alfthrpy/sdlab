---
source: hikaricp-wiki-dropwizard-metrics
read_by: agent
date: 2026-11-17
sections_read: ["whole page (short)"]
---

# Notes: Dropwizard Metrics (HikariCP wiki)

> Notes are in English and in your own words. Read via WebFetch and confirmed on the raw wiki markdown with `curl` on 2026-11-17. The page header shows the last edit by Brett Wooldridge on Aug 17, 2015 (4 revisions). No license is stated on the page.

## Key points

- Metrics are enabled by giving the pool a Dropwizard `MetricRegistry`; names are prefixed with the pool name, so set a pool name for consistent names.
- `pool.Wait`: a timer of how long callers wait inside `getConnection()` (including waits that end in a timeout). Direct measure of "time spent waiting for a connection".
- `pool.Usage`: histogram of how long each connection is held before being returned. Long usage with many waiters points at slow queries or leaks rather than too small a pool.
- `pool.PendingConnections`: gauge of threads currently waiting for a connection. Together with `ActiveConnections`, `IdleConnections`, `TotalConnections` it describes pool state; gauges refresh at most once per second.
- A related wiki page ("MBean (JMX) Monitoring and Management", opened, last edit Aug 22, 2018) exposes the same four counts through JMX under the name ThreadsAwaitingConnection, and warns they are snapshots that may not add up and are for monitoring only.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Gauges refreshed on demand at 1 second resolution | each gauge entry | Do not read them as exact |
| Metrics: Wait, Usage, TotalConnections, IdleConnections, ActiveConnections, PendingConnections | whole page | TimeoutRate is not on this page |

## Relevant to concepts

- `connection-pooling` objective 3 (diagnose exhaustion): SUPPORTS the "what to measure" part: waiting threads (Pending), time waiting (Wait), time holding (Usage), active vs total. Gives the diagnosis split: high Wait with high Usage = connections held too long; high Wait with low Usage = pool too small for the arrival rate.  (The last sentence is a reading of the metrics by the notes author, not a claim of the page.)

## Warnings

- Java and Dropwizard specific; old page (2015) for HikariCP 2.2.0+.
- Wiki text with no stated license: treated as all-rights-reserved; rewrite only.
