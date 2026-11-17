---
source: pg-docs-connect-estab
read_by: agent
date: 2026-11-17
sections_read: ["51.2 How Connections Are Established (whole page, about 300 words)"]
---

# Notes: PostgreSQL 18 Documentation, 51.2. How Connections Are Established

> Notes are in English and in your own words. Opened with WebFetch and confirmed on the raw page with `curl` on 2026-11-17. Page title "PostgreSQL: Documentation: 18: 51.2. How Connections Are Established"; footer "Copyright (c) 1996-2026 The PostgreSQL Global Development Group". No per-page date; the site banner of that day announces 18.7.

## Key points

- (51.2, first paragraph) PostgreSQL uses a "process per user" model: every client connection is served by exactly one dedicated backend process.
- (51.2) Because the number of connections is not known in advance, a supervisor process called the postmaster listens on the TCP/IP port and starts (spawns) a new backend each time a connection request arrives. So a new connection means a new OS process on the server.
- (51.2) Backends and other server processes coordinate through semaphores and shared memory.
- (51.2) After the connection exists, the client sends query text, and the backend parses, plans and runs it; the client does no parsing.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| One backend process per client connection, started by the postmaster | 51.2 | The official statement of the process-per-connection model |

## Relevant to concepts

- `connection-pooling` objective 1 (why a new connection per request wastes resources): PARTLY. It supports the server-side half: a new connection means the postmaster spawns a new process. It gives no timing, memory figures, authentication or TLS details (the page says nothing about them). Combine with `brandur-postgres-connections-2018` (fork, about 5 MB) and `freund-connection-scalability-2020` (TLS, latency, Postgres cost ordering).
- `single-machine-limits`: background for connection count as a process-level limit (with `pg-docs-kernel-resources` 18.4.3).

## Warnings

- Does not describe authentication or the exact fork step; do not cite for those.
- Describes the community PostgreSQL server only; MySQL uses a thread per connection, which is not covered here.
- Versioned `/docs/current/` URL; cite as "PostgreSQL 18".
