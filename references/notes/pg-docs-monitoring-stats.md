---
source: pg-docs-monitoring-stats
read_by: agent
date: 2026-11-17
sections_read: ["27.2 intro", "27.2.1 Statistics Collection Configuration", "27.2.2 Viewing Statistics (incl. Table 27.1)", "27.2.3 pg_stat_activity (Table 27.3, note on wait_event and state, Table 27.4 wait event types)", "27.2.13 pg_stat_io (closing paragraph only)", "27.2.17 pg_stat_database (start of Table 27.27)"]
---

# Notes: PostgreSQL 18 Documentation, 27.2. The Cumulative Statistics System (incl. pg_stat_activity)

> Notes are in English and in your own words. Read from the raw page downloaded with curl and converted to text, since the page is long (about 100k characters). Only the sections listed above were read closely; the detailed wait-event tables (27.5-27.13), the replication, WAL, SLRU and per-table views (27.2.4-27.2.12, 27.2.14-27.2.16, 27.2.18-27.2.26) were skimmed by title only. When I opened the page the banner mentioned PostgreSQL 18.7, while the registry says 18.6 (see Warnings).

## Key points

- (27.2 intro) PostgreSQL has two separate facilities: the cumulative statistics system (accumulated counts of table and index accesses, row counts, vacuum/analyze activity, optional per-function call counts and time) and a "dynamic" view of what is going on right now (which commands other processes are running, which connections exist). The second is independent of the first.
- (27.2.1) Collecting statistics costs some query overhead, so each kind can be switched on or off by settings (`track_activities`, `track_counts`, `track_functions`, `track_io_timing`, and a few others). Only superusers may change them per session, so ordinary users cannot hide their activity.
- (27.2.1) Statistics live in shared memory. They are written to disk on a clean shutdown and survive a restart; after a crash or an immediate shutdown (and after restoring from a base backup or point-in-time recovery), all counters reset to zero.
- (27.2.2) Cumulative numbers lag behind reality: a process flushes them only when going idle and at most about once per second, so a running query does not appear in totals yet. The current-query information (`track_activities`) is always up to date.
- (27.2.2) Within one transaction, the statistics you read are cached, so repeated reads in the same transaction show the same numbers. This is deliberate, to allow correlating results; `stats_fetch_consistency` changes the behavior.
- (27.2.2) Ordinary users only see full details of their own sessions; superusers and members of `pg_read_all_stats` see all sessions.
- (27.2.3) `pg_stat_activity` returns one row per server process (client connections and background processes), with columns such as database, user, application name, client address, `backend_start`, `xact_start`, `query_start`, `state_change`, `state`, `wait_event_type`, `wait_event`, and the query text. `backend_type` tells client backends apart from background processes, which matters when counting connections.
- (27.2.3) `state` values: active (running a query), idle (waiting for the client's next command), idle in transaction (inside a transaction but not running a query), idle in transaction (aborted), starting, fastpath function call, disabled.
- (27.2.3, note) `state` and `wait_event` are independent: a backend can be "active" and also waiting (blocked) on something, which signals that the query is held up inside the system. The columns are not read atomically, so small inconsistencies can appear.
- (27.2.3) The query text is truncated at 1024 bytes by default (`track_activity_query_size`). Query identifiers are empty unless `compute_query_id` or an extension turns them on.
- (27.2.3, Table 27.4) Wait event types group the reasons a backend waits: Activity (idle internal loop), BufferPin, Client (waiting on the application socket), Extension, IO, IPC, Lock (heavyweight locks on tables and similar), LWLock (internal lightweight locks), Timeout.
- (27.2.17) `pg_stat_database` has one row per database. `numbackends` is the number of backends currently connected; it is the only column in that view that shows the current state, while all others are accumulated since the last reset. Other accumulated columns include commit and rollback counts, block reads and cache hits, temporary file counts and bytes, and deadlocks.
- (27.2.13, closing paragraph) The PostgreSQL I/O statistics cannot tell whether a read came from disk or from the operating system's page cache, so the docs advise using them together with OS utilities for a full picture of I/O performance.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Statistics flush at most once per `PGSTAT_MIN_INTERVAL` (1 second unless changed at build time) | 27.2.2 | Cumulative counters lag; "current query" does not |
| Query text in `pg_stat_activity` is truncated at 1024 bytes by default | 27.2.3 (`query` column) | Parameter `track_activity_query_size` |
| `numbackends` in `pg_stat_database` is the only live column; the rest are cumulative since reset | 27.2.17 | Use deltas between two samples to get rates |
| Counters reset after a crash, immediate shutdown, base-backup start, or PITR; kept after a clean shutdown | 27.2.1 | Beware when graphing counters across a crash |
| `pg_stat_activity` has one row per server process, not only per client connection | 27.2.3 | Filter on `backend_type = 'client backend'` to count client connections (the column and value are documented there) |

## Relevant to concepts

- `basic-monitoring` objective 1 (distinguish the use of log, metric, health check): weak fit. This page shows what the database itself can tell you about its state (a "white-box" metric source). It does not compare logs, metrics, and health checks. Use it only as an example of the kind of internal metrics a database exposes, for instance connection state counts from `pg_stat_activity`.
- `basic-monitoring` objective 2 (minimum metrics, rate/errors/duration): weak fit. The accumulated counters (commits, rollbacks, deadlocks, blocks read) can be turned into rates by sampling twice, but the page does not discuss which metrics are minimal. Do not cite it for the minimum metric set.
- `basic-monitoring` objective 3 (health check alive vs dependency): not supported directly. Indirectly, the fact that a database may be reachable but all its connections `idle in transaction` or blocked on a `Lock` wait is a good example of "process alive but not healthy", which can be built from the `state` and `wait_event` columns.
- `single-machine-limits` objective 1 (identify which of CPU, memory, disk, or connections is the bottleneck): not mapped there in the curriculum, but the page is the practical tool for the "number of connections" and "waiting on lock or I/O" side (state counts, wait_event_type = IO or Lock, `numbackends`). The page does not state a maximum connection count or what a connection costs; for that see `pg-docs-kernel-resources` and `pg-wiki-number-of-connections`.

## Warnings

- Registry says "PostgreSQL 18 (18.6)" and was verified 2026-11-12; the page banner now announces 18.7 released on 12 November 2026 and the "Home" breadcrumb says 18.7. The monitoring-stats text I read matches a current 18 manual, but the exact minor version recorded in the registry may be stale; I did not change it (report only).
- Version-specific: view and column names (for example `pg_stat_checkpointer`, `pg_stat_io`, `track_cost_delay_timing`) differ between PostgreSQL versions; older versions have different names.
- PostgreSQL only; MySQL and others have different views.
- This is a reference manual page, not a tutorial. It does not say what values are "bad", has no thresholds, and does not explain monitoring strategy.
- Counters are cumulative: one number alone says little; you need two samples to compute a rate.
- The page is long; sections 27.2.4-27.2.12, 27.2.14-27.2.16, 27.2.18-27.2.26 and the wait event tables 27.5-27.13 were not read in detail.
