---
source: brandur-postgres-connections-2018
read_by: agent
date: 2026-11-17
sections_read: ["intro and error example", "The practical limits of concurrency", "Techniques for efficient connection use: Connection pools", "PgBouncer & inter-node pooling", "Connections as a resource", "footnotes"]
---

# Notes: How to Manage Connections Efficiently in Postgres, or Any Database (brandur)

> Notes are in English and in your own words. Read in full via WebFetch and from the raw HTML text (`curl`) on 2026-11-17. Author shown as "brandur" (no full name on the page); published Oct 15, 2018, San Francisco. The page states no license; the about page states none either.

## Key points

- (intro) The typical first production surprise: after traffic grows, app logs fill with a FATAL error saying the remaining connection slots are reserved for non-replication superusers. It means the database connection limit was hit.
- (intro) `max_connections` defaults to 100; the article says managed cloud databases cap it carefully, with the largest at about 500 and small ones at 20 or 25 (as of 2018, vendor limits have changed).
- (The practical limits of concurrency) Postgres has a postmaster that forks a child backend per connection; each backend starts around 5 MB and can grow with what it touches. The author says memory is the most direct but least important limit; shared structures that track every process and transaction are a more important bottleneck. A benchmark in the article shows throughput degrading as active connections grow (the author says it only demonstrates that degradation exists).
- (Connection pools) A pool is a cache of connections, usually local to one process. Its main benefit is performance: opening a database connection carries inherent overhead on both client and server, so reuse avoids paying it every time. Pool max size also makes per-node connection use predictable. Built into Go database/sql, JDBC, Active Record. Forking app servers (Unicorn) get one pool per process.
- ("Minimum viable checkouts") Release the connection while slow external calls are in flight (do not hold a transaction across them) so the pool is used efficiently.
- (PgBouncer & inter-node pooling) With N app nodes and at most M connections per node, N x M may deliberately exceed `max_connections` to cover uneven load, but nodes do not coordinate, so a busy cluster can still hit the limit. A shared PgBouncer in transaction mode lets N x M exceed the limit and still approach full use of connections; requests may still wait for a free connection.
- (Connections as a resource) Developers should know connections per node, total across the cluster (per-node number times nodes), and how that total relates to `max_connections`; deploys are a common trigger because a graceful restart starts new workers before old ones stop, so count connections during deploys too.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| max_connections default 100 | intro | Matches pg-docs-connections |
| Backend process starts around 5 MB | The practical limits of concurrency | Author's figure, with footnote; older than Freund's measured "below 2 MiB with huge pages" |
| Cluster total = connections per node x nodes, compare to max_connections | Connections as a resource | The only sourced statement of the "divide the DB limit across instances" arithmetic found in this group |
| Error text: remaining connection slots are reserved for non-replication superuser connections | intro | Exact wording confirmed on the raw page |

## Relevant to concepts

- `connection-pooling` objective 1: SUPPORTS (fork per connection, about 5 MB, overhead in client and server). No numbers for TCP/TLS/auth.
- `connection-pooling` objective 2: PARTLY. Supports the "split the DB limit across instances" input (N x M versus max_connections, deploy overlap). Gives no formula for the pool size itself and says nothing of Little's law.
- `connection-pooling` objective 3: PARTLY. Gives one exhaustion symptom (the FATAL error when the DB limit is hit) and one waiting symptom (requests delayed waiting for a pooler connection). It does not cover an in-app pool timeout.

## Warnings

- 2018 article; cloud limits and Postgres internals have changed (snapshot scalability improved in PG 14, see Freund). Treat 5 MB as an order of magnitude.
- All-rights-reserved (no license stated); rewrite only.
- Author is a single practitioner; the article is opinionated but references real operation.
