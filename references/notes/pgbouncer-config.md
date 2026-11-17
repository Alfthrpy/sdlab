---
source: pgbouncer-config
read_by: agent
date: 2026-11-17
sections_read: ["pool_mode", "max_client_conn", "default_pool_size", "min_pool_size", "reserve_pool_size / reserve_pool_timeout", "max_db_connections", "query_wait_timeout", "page footer"]
---

# Notes: PgBouncer config

> Notes are in English and in your own words. Opened with WebFetch and confirmed on the raw page with `curl` on 2026-11-17. Page title "PgBouncer config"; footer "Website (c) 2026 PgBouncer Authors"; no license statement, no page date.

## Key points

- (pool_mode) Says when a server connection goes back to the pool: after the client disconnects (session, the default), after the transaction (transaction), or after each statement (statement).
- (default_pool_size) Maximum number of server connections per (user, database) pair; default 20. It can be overridden per database or user. Because it is per pair, the real total on the database can be larger than one pool.
- (max_client_conn) Maximum number of client connections PgBouncer accepts; default 100. The page warns that file-descriptor limits may need raising and gives the theoretical maximum of descriptors as max_client_conn plus pool size times databases (times users).
- (max_db_connections / max_user_connections) Caps on server connections per database or user across pools; default 0 (unlimited). The page notes that closing a client in one pool does not instantly free a slot for another pool; the slot frees when the idle server connection closes.
- (max_db_client_connections) The gap between this and max_db_connections can be thought of as the length of the queue of clients waiting for a server connection.
- (query_wait_timeout) Maximum time a query may wait to get a server connection; after that the client is disconnected. Default 120 seconds. 0 disables it and clients then queue without limit. The page says the purpose is to stop an unresponsive server from tying up connections.
- (reserve_pool_size / reserve_pool_timeout) Optional extra connections used if a client has waited longer than the timeout (default 5 s); reserve size default 0 (off).
- (min_pool_size) Keeps a minimum number of server connections open; default 0.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| default_pool_size = 20 | default_pool_size | Per user/database pair |
| max_client_conn = 100 | max_client_conn | Client side, not server side |
| query_wait_timeout = 120 s; 0 means unlimited queueing | query_wait_timeout | Defines how long an exhausted pool keeps clients waiting |
| reserve_pool_timeout = 5 s, reserve_pool_size = 0 | reserve_pool_* | Reserve is off by default |
| pool_mode default = session | pool_mode | |

## Relevant to concepts

- `connection-pooling` objective 3 (diagnose exhaustion): SUPPORTS the "what happens to waiting requests" half: they queue, and after query_wait_timeout the client is dropped; with 0 they wait forever. Pair with `pgbouncer-usage` for the observable counters.
- `connection-pooling` objective 2 (size a pool, share a DB limit): PARTLY. It shows the knobs (default_pool_size per pair, max_db_connections, max_client_conn) and that client count and server count are separate numbers. It gives no sizing method and does not say how to divide max_connections across instances.

## Warnings

- Defaults are for the version current on 2026-11-17 (site news shows 1.26.1); the page does not state which version its defaults apply to.
- No license stated; rewrite only.
- Mostly operations material; for a Unit 0 lesson use at most pool size, client limit and query_wait_timeout.
