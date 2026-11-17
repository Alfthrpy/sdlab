---
source: pg-wiki-number-of-connections
read_by: agent
date: 2026-11-17
sections_read: ["Summary", "The Need for an External Pool", "Reasons for Performance Reduction Past the Knee", "How to Find the Optimal Database Connection Pool Size", "page footer (last-edit date)"]
---

# Notes: Number Of Database Connections (PostgreSQL Wiki)

> Notes are in English and in your own words. Whole page read on 2026-11-17 (fetch of the live wiki page, text extracted from raw HTML via `curl`; the page is short, about 1,300 words). Page shows no author; footer says it was last edited on 14 March 2014 and states no license.

## Key points

- (Summary) A database has finite resources. Adding connections raises throughput until the resources are saturated; after that more connections add contention and throughput falls.
- (Summary) The recommended strategy is to cap the number of connections that have an active transaction near what the hardware can really use, and to queue anything extra instead of starting it. A queued transaction often finishes sooner overall than one started immediately under saturation.
- (Summary) Illustration given: the same 10,000 transactions usually finish faster when run 5, 10, or 20 at a time than 500 at a time. The right number depends on the workload and must be found by tuning.
- (The Need for an External Pool) Throughput versus connection count has a "knee": it climbs, hits saturation, then declines. Work for version 9.2 moved the knee right and softened the decline, but the effect is inherent without admission control or pooling.
- (The Need for an External Pool) PostgreSQL deliberately has no built-in pooler. Reasons listed: a pooler on a separate machine often performs better; no single pooling design fits all needs; client-side software can pool with more functionality; some frameworks (Java EE, JPA, Hibernate) always pool already.
- (The Need for an External Pool) Persistent connections (e.g. from mod_php) are not pooling and still need a real pool.
- (Reasons for Performance Reduction) Independent causes of the drop past the knee: disk contention (random access thrashing, especially on spinning disks); RAM use (work_mem can be allocated per query node per connection, risking cache eviction or swapping); lock contention (spinlocks and lightweight locks eating CPU); context switches; CPU cache-line contention; and general scaling cost, since some structures sized by max_connections grow as O(N^2) or O(N log N).
- (How to Find the Optimal Pool Size) Rule of thumb that "held up across benchmarks": active connections near (core_count * 2) + effective_spindle_count. Core count excludes hyperthreading threads. Effective spindle count is 0 when the active data set is fully cached and approaches the real number of disks as cache hit rate falls.
- (How to Find the Optimal Pool Size) Use the formula only as a starting point; adjust in small steps on the production system to find the real sweet spot for the hardware and workload.
- (How to Find the Optimal Pool Size) The figure counts connections actively doing work; mostly-idle monitoring or admin connections are ignored.
- (How to Find the Optimal Pool Size) Keep max_connections a bit above the pool size so direct maintenance and monitoring connections always have free slots.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Pool size starting point: (core_count * 2) + effective_spindle_count | How to Find the Optimal Database Connection Pool Size | Core count excludes hyperthreads; effective spindles = 0 if fully cached |
| Example: 10,000 transactions finish faster at 5, 10, or 20 concurrent than at 500 | Summary | Qualitative illustration, no measured numbers or hardware given |
| Some max_connections-sized structures scale O(N^2) or O(N log N) | Reasons for Performance Reduction, "General scaling" | Explains why very large max_connections is costly even when idle |
| Page last edited 14 March 2014 | page footer | Also the page's only date |
| Keep max_connections slightly larger than pool size for maintenance slots | How to Find the Optimal Database Connection Pool Size, last paragraph | Ties pool size to the server limit (see pg-docs-connections) |

## Relevant to concepts

- `connection-pooling` obj. 2 (compute a sensible pool size from cores, query load and the database connection limit, then validate by measurement): this is the source in this group that gives the formula and the rule of thumb. It supports the cores part directly via (cores * 2) + effective spindles, the DB-limit part via the "keep max_connections above the pool" advice, and the validation part via "adjust incrementally on production". It does NOT give a query-load-based method (no arrival-rate or query-duration calculation, no Little's law), so the "query load" input has to come from another source or from the lesson's own reasoning. pg-docs-connections supplies only the limit, not a sizing method.
- `connection-pooling` obj. 1 (why opening a new connection on every request wastes resources): only indirectly supported. The page explains why too many concurrent connections hurt (contention, memory, scaling cost), not the per-connection setup cost of connect, authenticate, and fork a backend. Another source is needed for setup cost.
- `connection-pooling` obj. 3 (diagnose pool exhaustion, requests waiting for a connection): NOT directly supported. The page says to queue extra work at the pool but does not describe symptoms or metrics of a starved pool; use hikaricp-about-pool-sizing and pgbouncer-features for that.
- `single-machine-limits` (connection count as a bottleneck): the "knee" and the list of contention causes give background on why connection count becomes a limit before CPU is full.

## Warnings

- Old page (2014). It says explicitly that benchmarks for version 9.2 suggest the formula may need adjustment, and that nobody had analyzed it for SSDs. Treat it as a starting heuristic, not a law. The "effective spindle count" term is awkward for SSD or cloud storage; say so when teaching it.
- No author and no stated license; treated as all-rights-reserved (rewrite only). The claims are unreferenced assertions by wiki editors, not measurements shown on the page.
- The formula sizes the number of connections actively executing, not the number of application threads or clients; do not confuse it with max_connections.
- The formula assumes the database is the CPU/disk-bound resource on its own machine; a pool shared by several app instances must divide the total across instances (the page does not cover this).
