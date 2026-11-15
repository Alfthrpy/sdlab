---
source: figma-horizontal-sharding-2024
read_by: agent
date: 2026-11-15
sections_read: ["Background", "Scaffolding for scale", "Exploring our options", "The path to horizontal sharding", "Our unique approach (skimmed)", "Our sharding implementation (logical solution, query engine, topology, physical sharding operation)", "We've come a long way"]
---

# Notes: How Figma's Databases Team Lived to Tell the Scale (2024)

> Notes are in English and in your own words. Read from the raw HTML of the page converted to text; the fetched text matched the section headings of the page.

## Key points

- (Background) In 2020 Figma ran one Postgres database on the largest instance AWS offered, and by the time of writing the database stack had grown about 100 times.
- (Background) Trigger signals: some tables held several terabytes and billions of rows, vacuum work began to hurt reliability (vacuum prevents transaction ID exhaustion), and the busiest write tables were approaching the IOPS ceiling of the largest instance.
- (Background) Before sharding they split groups of related tables into separate databases (vertical partitioning). This bought time but cannot split one table, so it hits a wall; they measured CPU, IO, table size and rows written per database to predict how much runway each had.
- (Scaffolding for scale) Stated goals included: little developer impact, transparent future scale-out, no huge backfills, incremental rollout, no one-way migrations (keep rollback after a physical split), and strong consistency without relying on double-writes.
- (Exploring our options) They evaluated CockroachDB, TiDB, Spanner and Vitess and NoSQL stores and rejected them: each meant a complex migration to a second kind of database, loss of in-house RDS Postgres expertise, or rewriting a relational application. Building a limited sharding layer on top of existing Postgres was judged cheaper because they could support a much smaller feature set than a general database.
- (The path to horizontal sharding) They treated horizontal sharding as an order of magnitude more complex than earlier steps: some queries become inefficient or impossible, application code must supply the shard key for routing, schema changes must be coordinated across shards, and foreign keys and globally unique indexes can no longer be enforced by Postgres. Queries without a shard key need scatter-gather, which they restrict because too many of them hurt scalability. They chose not to support atomic cross-shard transactions, on the basis that failures could be worked around in the application. The first target was one simple, very busy table.
- (Our unique approach) Related tables that share one shard key are sharded together as a "colo". Logical sharding (in the application and proxy layer) is separated from physical sharding (moving data); they copy the full data set to the new databases and then only serve the owned slice, instead of filtered replication. They kept the ability to roll back after a physical split.
- (Our sharding implementation) Shard keys were chosen per table group (user id, file id, organization id). Because their IDs were auto-increment or time-prefixed, routing uses a hash of the shard key to avoid putting most data on one shard; the cost is that range scans over the key become inefficient.
- (The logical solution) Logical shards are Postgres views filtered by hash range over the still-unsharded table, so reads and writes can be routed as if sharded before any data moves; a proxy service parses queries, finds the shard key, and rewrites the query for the right physical database. Queries without a shard key become scatter-gather and are restricted to a supported subset.
- (We've come a long way) First sharded table shipped in September 2023; the failover cost about ten seconds of partial availability on primaries and none on replicas, with no later latency or availability regressions. Open problems named: globally unique IDs, cross-shard transactions, automated resharding.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Database stack grew about 100x since 2020; started from one instance on the largest AWS size | Background | Figma-specific |
| First horizontally sharded table in production September 2023; ~10 s partial availability on primaries during failover | We've come a long way | |

## Relevant to concepts

- `sharding`: the staged ladder (replicas and pooling, then vertical split, then horizontal sharding) and the signals that justify each step.
- `shard-key`: hashing a key to avoid hot shards and giving up range scans; co-locating tables on the same key.
- `migration`: separating the logical switch from the physical move to make each step reversible.

## Warnings

- Company blog by the team that built it; written as a project retrospective, not a neutral comparison with managed alternatives (it does discuss options considered).
- The page has no license or copyright statement; treat as all rights reserved and paraphrase.
- Numbers are Figma's. Only the first sharded table was live at publication, so long-term outcomes are not covered.
