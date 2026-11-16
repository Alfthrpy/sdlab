---
source: figma-sharding-postgres-2024
read_by: agent
date: 2026-11-16
sections_read: ["whole article as returned by the fetch tool (summary, truncated before the footer)"]
---

# Notes: How Figma's Databases Team Lived to Tell the Scale (2024)

> Notes are in English and in your own words. Read through a fetch tool that summarizes; verify details at verification time.

## Key points

- (Background) Growth path: caching, read replicas, vertical partitioning (separate tables into separate databases), then horizontal sharding when single tables became too big for vacuum and IOPS limits.
- (Options) Evaluated NewSQL and Vitess systems and a NoSQL move; rejected because of migration risk, the loss of in-house Postgres expertise and little time left; they built sharding on top of their existing Postgres.
- (Costs of sharding) Some queries become inefficient, Postgres cannot enforce foreign keys or unique indexes across shards, schema changes need coordination, and a transaction across shards can partially commit.
- (Shard key) They use several keys (user, file, org) and hash them to avoid hot spots from sequential IDs, accepting weaker range scans. Tables sharing a key are grouped so joins and transactions still work within that key.
- (Rollout) Logical sharding first (routing as if sharded, rollback by configuration), physical data split last. A proxy service parses and routes queries; queries without a shard key fan out to all shards.
- (Outcome) First sharded table went live in September 2023 with about ten seconds of partial availability on primaries; remaining work included cross-shard atomic transactions and global unique IDs.

## Relevant to concepts

- `partitioning-sharding`: trigger (single-table limits after other scaling steps), shard key and hot-spot trade-off, cross-shard query cost, when sharding was delayed.

## Warnings

- Company-specific design; says nothing about general consistent hashing. Footer not seen.
