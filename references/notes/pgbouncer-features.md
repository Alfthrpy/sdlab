---
source: pgbouncer-features
read_by: agent
date: 2026-11-17
sections_read: ["Features (whole page): pooling modes, resource/operational properties, SQL feature map for pooling modes with footnotes"]
---

# Notes: PgBouncer features

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location.
> The page is short; it was read in full via WebFetch and confirmed on the raw page with `curl` on 2026-11-17. Footer: "Website (c) 2026 PgBouncer Authors". The news list on the site shows PgBouncer 1.26.1 as the latest release (site-wide, not part of this page's content).

## Key points

- (Features, top list) PgBouncer offers three ways of "rotating" server connections, described as increasing levels of aggressiveness.
- (Session pooling) A server connection is tied to a client for as long as the client stays connected, and goes back to the pool only when the client disconnects. It is the gentlest mode and supports all PostgreSQL features.
- (Transaction pooling) A server connection is assigned to a client only while a transaction runs, and is returned to the pool as soon as PgBouncer sees the transaction end. The page says this breaks some session-level features by design, so the application must cooperate by not using them.
- (Statement pooling) Like transaction pooling, but multi-statement transactions are disallowed, which forces autocommit behavior on the client; the page says it is mostly aimed at PL/Proxy.
- (Features, bullet list) Low memory use (the default is 2 kB per connection, because PgBouncer does not need to see whole packets at once); not tied to a single backend server (target databases may be on different hosts); most settings can be reconfigured online; online restart/upgrade is possible without dropping client connections.
- ("SQL feature map for pooling modes") Table of PostgreSQL features against session and transaction mode. In transaction mode, these are marked "Never": SET/RESET, LISTEN, WITH HOLD cursors, PREPARE/DEALLOCATE (SQL level), PRESERVE/DELETE ROWS temp tables, LOAD, and session-level advisory locks. These work: startup parameters (a fixed list of six that PgBouncer tracks), NOTIFY, WITHOUT HOLD cursors, ON COMMIT DROP temp tables, cached plan reset, and protocol-level prepared statements (see footnote 2 below).
- (Footnote 2) Protocol-level prepared statements work in transaction mode only if max_prepared_statements is set to a non-zero value.
- (Footnote 1) The tracked startup parameters are client_encoding, DateStyle, IntervalStyle, Timezone, standard_conforming_strings and application_name; others need track_extra_parameters or ignore_startup_parameters.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default memory per connection is 2 kB | Features, bullet list | Shows why an external pooler can hold many client connections cheaply; this is a default, not a guarantee |
| Three pooling modes: session, transaction, statement | Features, top | Order from most compatible to most aggressive |
| Transaction mode: SET/RESET, LISTEN, WITH HOLD cursors, PREPARE/DEALLOCATE, session advisory locks, LOAD are "Never" | SQL feature map table | Exact table values confirmed on the raw page; useful for a "what breaks" lesson |
| Prepared statements at protocol level in transaction mode need max_prepared_statements non-zero | Table footnote 2 | Setting name confirmed on the raw page |

## Relevant to concepts

- `connection-pooling` objective 1 (explain why a new connection per request wastes resources): only indirectly supported. The page shows the other side (a pooler reuses a small set of server connections and clients are cheap, 2 kB each) but does not say what a new connection costs on the database side. Needs another source (pg-docs-connections, pg-wiki-number-of-connections).
- `connection-pooling` objective 2 (compute pool size, then validate by measurement): NOT supported. The page has no sizing guidance and no pool size settings (it does not mention default_pool_size, max_client_conn, etc.). It only supports a conceptual choice between modes.
- `connection-pooling` objective 3 (diagnose an exhausted pool, requests waiting for a connection): NOT supported. No monitoring commands (SHOW POOLS and similar), no wait/timeout settings, no symptoms. The usage and configuration pages of PgBouncer (listed in the site menu: Usage, Configuration, FAQ) were not opened and would be the place to look.
- `connection-pooling` (conceptual coverage): good for the lesson point that a pooler in front of the database can hold a pool shared by many clients, and that transaction-level reuse has compatibility costs. Suitable as the "external pooler" option next to an in-app pool (HikariCP).

## Warnings

- NO-DATE and NO-AUTHOR; all-rights-reserved (see registry). Rewrite only; the feature table must be rebuilt in our own wording and layout.
- The page is a feature overview, not an operations guide. Registry already flags it as possibly more advanced than Unit 0; a beginner lesson should use at most the three modes and one or two broken-features examples.
- "Never" in the table is about transaction pooling as documented on this page at the time of reading; the footnote about max_prepared_statements suggests behavior is version- and setting-dependent. The page does not state which PgBouncer version the table applies to.
- It is PostgreSQL-only. MySQL has no equivalent mapped source.
