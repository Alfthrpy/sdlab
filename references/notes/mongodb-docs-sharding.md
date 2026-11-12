---
source: mongodb-docs-sharding
read_by: agent
date: 2026-11-12
sections_read: ["Sharding Introduction and Architecture (single page)"]
---

# Notes: MongoDB Database Manual, Sharding Introduction and Architecture

> Notes are in English and in your own words. Page read as Database Manual 9.0.

## Key points

- Sharding spreads one collection over several machines. The page motivates it by the ceiling of vertical scaling: CPU exhausted by query rate, or a working set larger than RAM that pushes work to disk. It also admits sharding brings more operational complexity.
- A cluster has three roles: shards (each is itself a replica set), a router process clients talk to, and config servers holding the metadata map (also a replica set). So sharding in this system sits on top of replication.
- The shard key decides where each document lives. It can be changed later by resharding (from version 5.0), but picking well still matters.
- Ranged sharding keeps neighbouring key values together: range queries touch few shards, but a bad key makes uneven load. Hashed sharding spreads keys evenly, including steadily increasing keys, but range queries must ask every shard.
- Data is cut into chunks (inclusive lower, exclusive upper bound). A background balancer moves chunks between shards to even things out; a shard takes part in one migration at a time, and cleanup of the moved range afterwards is slow and heavy.
- Monotonically increasing keys such as timestamps send new writes to a single chunk and shard, the classic hot spot; hashing mitigates it.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Resharding available since 5.0 | Shard keys section | Version-specific |

## Relevant to concepts

- `sharding-basics` and its trigger: vertical scaling limits come first, replica-set-per-shard architecture.
- `shard-key-choice`: ranged vs hashed table.
- `rebalancing`: chunk migration via balancer.
- `hot-spots`: monotonic keys.

## Warnings

- Vendor documentation; version-specific details (8.0 config shard, 8.3 mongos rule) change quickly and should not be taught.
- The page does not use the phrase "hot spot"; that framing is inferred from the monotonic-key discussion.
