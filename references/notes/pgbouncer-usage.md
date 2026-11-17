---
source: pgbouncer-usage
read_by: agent
date: 2026-11-17
sections_read: ["SHOW CLIENTS", "SHOW POOLS", "SHOW STATS (wait-time columns)", "page footer"]
---

# Notes: PgBouncer command-line usage (admin console SHOW commands)

> Notes are in English and in your own words. Opened with WebFetch and confirmed on the raw page with `curl` on 2026-11-17. Page title is "PgBouncer command-line usage"; the footer says "Website (c) 2026 PgBouncer Authors", with no license statement and no page date.

## Key points

- (SHOW POOLS) One row per (database, user) pair. `cl_active` counts clients that are linked to a server connection or idle with nothing queued. `cl_waiting` counts clients that have sent a query but have no server connection yet. This is the direct "requests are waiting for a connection" counter.
- (SHOW POOLS) `sv_active` are server connections linked to a client; `sv_idle` are server connections free for immediate use. A pool whose `sv_idle` is 0 while `cl_waiting` is above 0 is the exhausted-pool picture.
- (SHOW POOLS, `maxwait`) Age in seconds of the oldest queued client. The page says that if this keeps growing, the servers are not handling requests fast enough, because either the server is overloaded or the pool size is too small. `maxwait_us` is the microsecond part.
- (SHOW CLIENTS) Each client has a `state` (active, idle, waiting, plus cancel-request variants) and `wait` / `wait_us` showing how long it has been waiting at the moment.
- (SHOW STATS) `total_wait_time` and `avg_wait_time` (microseconds) record how long clients waited to be assigned a server. They allow a trend view instead of a single snapshot.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| `cl_waiting` = clients with a query but no server connection | SHOW POOLS | Exact column names confirmed on the raw page |
| `maxwait` growing means servers too slow or pool_size too small | SHOW POOLS | Two-cause diagnosis stated by the page itself |
| Wait time is exposed as total_wait_time / avg_wait_time in SHOW STATS | SHOW STATS | Units are microseconds |

## Relevant to concepts

- `connection-pooling` objective 3 (diagnose an exhausted pool): SUPPORTS well for the external-pooler case. It gives the observable signals (cl_waiting, maxwait, wait time) and the two candidate causes (slow queries or undersized pool). It does not give an incident procedure; the lesson must add the reasoning (look at sv_active vs pool size, then at query duration).
- `connection-pooling` objective 2: only indirectly (the maxwait remark ties pool_size to symptoms).

## Warnings

- PgBouncer-only vocabulary; an in-app pool (HikariCP, ActiveRecord) uses different names for the same ideas.
- No license stated; treat as all-rights-reserved (rewrite only). Do not copy the column descriptions word for word.
- The page documents no error counters or error messages, so it cannot support "what error does the client see".
