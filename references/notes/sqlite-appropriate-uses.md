---
source: sqlite-appropriate-uses
read_by: agent
date: 2026-11-17
sections_read: ["Intro", "1. Situations Where SQLite Works Well (all subsections)", "2. Situations Where A Client/Server RDBMS May Work Better", "3. Checklist For Choosing The Right Database Engine"]
---

# Notes: Appropriate Uses For SQLite

> Notes are in English and in your own words. Whole page read via WebFetch and checked against the raw HTML with curl; the page says "last updated 2025-05-31 13:08:22Z". The page itself shows no license; the public-domain statement is on sqlite.org/copyright.html (checked by an earlier session, not re-opened here).

## Key points

- (Intro) SQLite is positioned as local storage inside one application, not as a shared enterprise data repository. The page's own framing is that it competes with plain file I/O (`fopen()`), not with client/server databases like PostgreSQL or MySQL.
- (1, Websites) SQLite is claimed to suit most low-to-medium traffic websites. The page gives a rule of thumb of fewer than 100K hits/day as a conservative figure, and says it has been demonstrated at about ten times that.
- (1, Websites) Worked example: the SQLite site itself, in 2015, took roughly 400K-500K HTTP requests per day, 15-20% of them dynamic and touching the database, about 200 SQL statements per dynamic page, on a VM shared with 23 others, with load average mostly under 0.1.
- (1, Server-side database) Some designers use SQLite behind an application server; the server serializes requests and can use one database file per user/subdomain to get concurrency.
- (2, Client/Server Applications) If many client programs on different machines send SQL to the same database over a network, use a client/server engine. Network filesystems add latency and have buggy file locking in many implementations, which can lead to corruption. Rule of thumb: avoid direct, simultaneous access from many computers over a network (an application server in between is fine).
- (2, High-volume Websites) If the site is write-intensive, or so busy that it needs several servers, move to a client/server database.
- (2, Very large datasets) The size limit is 281 TB (2^48 bytes), but a single file and filesystem limits make the terabyte range a signal to look at client/server.
- (2, High Concurrency) Unlimited concurrent readers, but exactly one writer at any instant. Writers queue, and in most cases a write lock lasts only a few dozen milliseconds.
- (3, Checklist) Decision order: data separated from the app by a network -> client/server; many concurrent writers that cannot take turns -> client/server; data heading toward terabytes -> client/server; otherwise SQLite. The reasoning given for the first rule: keep the high-bandwidth engine-to-disk path local and let only the low-bandwidth app-to-engine path cross the network. "Application" here means the code issuing SQL, so an app server on the same machine as the file still qualifies.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| "Fewer than 100K hits/day" is a conservative SQLite-OK estimate (about 1.2 hits/s on average; my arithmetic) | 1, Websites | Page says it is not a hard bound and that 10x has been shown. A "hit" is not defined (HTTP request vs page) |
| sqlite.org: ~400K-500K requests/day, 15-20% dynamic, ~200 SQL statements per dynamic page, load average < 0.1, shared VM | 1, Websites | As of 2015, per the page. One site's workload, mostly read |
| One writer at a time, unlimited readers; write locks typically a few dozen ms | 2, High Concurrency; 3 checklist | Basis for estimating writes/s a single file can take; the page gives no writes/s number |
| Max database size 281 TB (2^48 bytes) | 2, Very large datasets | Practical advice is to reconsider near 1 TB (3, Big data) |
| "Less than a terabyte" and low writer concurrency -> SQLite almost always better | 3, Otherwise | |

## Relevant to concepts

- `app-plus-database` (unit 0), objective 1 (calculate from user count and requests/s that one app plus one database is enough): partly supported. It supplies two reference points (100K hits/day rule of thumb; the sqlite.org example) and the qualitative limits (write-heavy, multi-server, terabytes). It does not teach how to turn users into requests per second or give a peak factor, and its numbers are for SQLite, not for a PostgreSQL/MySQL server. Pair with aws-startups-scaling-part1-primer and craver-stack-overflow-architecture-2016 for larger examples.
- `app-plus-database`, objective 2 (distinguish state in the database from state lost on app restart): only weakly. The page's embedded-file model is a good contrast (data in a file survives restarts), but it does not discuss in-process state at all. Use twelve-factor-app for this objective.
- `single-machine-limits` (not mapped to this source): the one-writer limit is a concrete example of a single-resource limit, but the page does not teach identifying bottlenecks.

## Warnings

- SQLite is a different engine from the PostgreSQL/MySQL the course uses elsewhere. The "one writer" rule describes SQLite's file locking; do not apply it to PostgreSQL/MySQL, which allow concurrent writers.
- The website figures are from 2015 (the page text says so) and describe a mostly read-only site; the page itself was last updated 2025 but the number was not refreshed. The 100K hits/day figure is the SQLite authors' own conservative guess, not a benchmark, and "hit" is undefined.
- The page mentions that it works over network filesystems but warns against it; do not describe SQLite as "unsafe" in general, only in the multi-machine direct-access case.
- Concurrency details (WAL mode, `busy_timeout`) are not on this page.
