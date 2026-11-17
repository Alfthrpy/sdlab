---
source: pg-docs-connections
read_by: agent
date: 2026-11-17
sections_read: ["19.3.1 Connection Settings: max_connections, reserved_connections, superuser_reserved_connections entries", "page header and footer"]
---

# Notes: PostgreSQL 18 Documentation, 19.3. Connections and Authentication (max_connections)

> Notes are in English and in your own words. Page opened on 2026-11-17 (fetch plus raw HTML via `curl`). Only the three connection-slot parameters were read in detail; the rest of 19.3 (listen_addresses, TCP settings, authentication, SSL) was skimmed, not used.

## Key points

- (19.3.1, max_connections) It is the cap on simultaneous client connections to the server. The documented default is typically 100, but initdb may choose a lower value if the kernel settings cannot support it.
- (19.3.1, max_connections) It can be changed only at server start (restart needed), so it is not something to tune casually during an incident.
- (19.3.1, max_connections) The server sizes some of its resources directly from this value, including shared memory, so raising it increases allocation even if the extra connections are never used.
- (19.3.1, max_connections) On a standby server it must be equal to or higher than the primary's value, or queries are not allowed on the standby.
- (19.3.1, superuser_reserved_connections) A number of slots (default 3) are kept for superusers. When active connections reach max_connections minus this number, only superusers can connect, which gives an emergency way in.
- (19.3.1, reserved_connections) A second, optional reserve (default 0) for roles with the pg_use_reserved_connections privilege. Slots are used in layers: ordinary users are refused first, then reserved-role users, and finally only superusers get in.
- (19.3.1) Both reserve settings must be smaller than max_connections minus the other reserve, and both are start-time only.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| max_connections default is typically 100 (may be lower depending on kernel limits found by initdb) | 19.3.1, max_connections | "Typically" matters: do not state it as a fixed constant |
| superuser_reserved_connections default is 3 | 19.3.1, superuser_reserved_connections | Superusers can still connect when ordinary slots are full |
| reserved_connections default is 0 | 19.3.1, reserved_connections | Documented in the version 18 page; other versions were not checked |
| max_connections, reserved_connections, superuser_reserved_connections all require a server restart | 19.3.1 | Each entry says it can only be set at server start |
| Standby must have max_connections >= primary | 19.3.1, max_connections | Relevant when a replica is added later (Unit 2) |

## Relevant to concepts

- `connection-pooling` obj. 2 (compute a sensible pool size from cores, query load and DB connection limit, then validate by measurement): provides only the "DB connection limit" input, i.e. the hard ceiling (max_connections minus reserved slots, default 100) that the sum of all pool sizes across app instances must stay under. It gives NO formula or rule of thumb for choosing the size; that is in pg-wiki-number-of-connections. No measurement guidance either.
- `connection-pooling` obj. 1 (why a new connection per request wastes resources): only background. The page does not describe per-connection setup cost; it merely shows connections are a limited, pre-sized resource.
- `connection-pooling` obj. 3 (diagnose a starved pool): NOT supported by this page. It does not say what error clients see when the limit is reached.
- `single-machine-limits` (connection count as a bottleneck; objectives 1 and 2): useful as the concrete limit to monitor against, but the page itself gives no metrics or USE-style guidance.

## Warnings

- This is the PostgreSQL 18 page (the `/docs/current/` URL changes meaning when a new major version ships). On the page, the version is shown only as "Current (18)"; the registry entry says 18.6, which is not visible on the page (the site banner announced 18.7 on 12 November 2026), so cite it as "PostgreSQL 18" without a minor version.
- Defaults are for PostgreSQL only. A MySQL equivalent is not covered here and its values must not be inferred from this page.
- It says nothing about how many connections are sensible; a high max_connections is not a recommendation. The "more connections is worse past the knee" argument is on the PostgreSQL wiki page, not here.
- The page describes the community PostgreSQL server only; it says nothing about managed services, whose limits must be checked in their own documentation.
- The page does not mention the word "pool" at all, even though the registry topics include connection-pooling; the pooling link is made by the lesson, not by this source.
- The page does not mention that each connection is a separate server process, so do not cite it for that claim.
