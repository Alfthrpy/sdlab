---
source: heroku-concurrency-database-connections
read_by: agent
date: 2026-11-17
sections_read: ["Connection pool", "Maximum database connections", "Calculating required connections", "Number of active connections", "Bad connections", "Limit connections with PgBouncer"]
---

# Notes: Concurrency and Database Connections in Ruby with ActiveRecord (Heroku Dev Center)

> Notes are in English and in your own words. Read via WebFetch and from the raw page text (`curl`) on 2026-11-17. The page says "Last updated October 08, 2025" and names no author. Footer: "(c) 2026 Salesforce, Inc. All rights reserved."

## Key points

- (Connection pool) With a multi-threaded or multi-process server, each thread or process needs its own database connection. ActiveRecord keeps a pool per process; the default maximum is 5. Connections are created lazily, only when a thread first needs one.
- (Connection pool) If every connection in the pool is in use, the requesting thread blocks. If none frees up in time, an error is raised. The example message reads: could not obtain a database connection within 5 seconds, the max pool size is currently 5, consider increasing it. This is the in-app pool exhaustion symptom.
- (Maximum database connections) Managed databases have per-plan connection limits (20 on the Essential tier). When the limit is reached, new connections are refused, causing timeouts and likely exceptions. When scaling out, count connections per dyno: with 5 per dyno you can scale to only four dynos on a 20-connection database.
- (Calculating required connections) Derive the number from the web server settings: processes (Unicorn) or threads (Puma, 16 by default) per dyno times dynos. Example: 3 connections per dyno, 6 dynos, 18 of 20 connections used. Tune thread counts by load testing in a production-like environment.
- (Number of active connections) Count them in the database with a query on `pg_stat_activity`; because connections are lazy, hit the app repeatedly (or measure in production) before trusting the count.
- (Bad connections) Hung connections can make a process hold up to its full pool; the page suggests a small pool (1 or 2) and a reaper, and says the reaper is not a permanent fix.
- (Limit connections with PgBouncer) When the limit is near, put PgBouncer in front; transaction pooling disables named prepared statements, session advisory locks and LISTEN/NOTIFY.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default ActiveRecord pool size 5 | Connection pool | Rails-specific |
| Entry-tier Heroku Postgres limited to 20 connections | Maximum database connections | Current as of the page date; plans change |
| 6 dynos x 3 connections = 18 of 20 | Calculating required connections | Worked example for the "share the limit across instances" arithmetic |
| Pool timeout error text (could not obtain a database connection within 5 seconds ...) | Connection pool | Exact wording confirmed on the raw page |

## Relevant to concepts

- `connection-pooling` objective 2: SUPPORTS the "divide the DB connection limit across app instances" input, with a worked example and the load-test advice. Does NOT give the arrival-rate x query-duration calculation.
- `connection-pooling` objective 3: SUPPORTS the symptom (threads block, then a timeout error naming the pool size) and the two usual fixes (adjust pool size to concurrency while staying under the DB limit; hung connections). Weak on root-cause diagnosis (slow queries, leaks).
- `connection-pooling` objective 1: only that connections are a limited resource; no setup-cost data.

## Warnings

- Ruby/Rails/Heroku-specific; the principle is general but numbers (pool 5, limit 20) are platform defaults.
- All-rights-reserved (Salesforce); rewrite only.
- The page advises tiny pools (1 or 2) for forking servers to avoid zombie connections; that is a platform-specific tradeoff, not a general sizing rule.
