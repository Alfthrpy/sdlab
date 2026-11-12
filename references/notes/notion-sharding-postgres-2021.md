---
source: notion-sharding-postgres-2021
read_by: agent
date: 2026-11-12
sections_read: ["Whole article"]
---

# Notes: Herding elephants: Lessons learned from sharding Postgres at Notion (2021)

> Notes are in English and in your own words.

## Key points

- Trigger: the single Postgres monolith hit trouble that was not simply "too much traffic". Vacuum kept stalling, which left dead rows uncleaned and raised the risk of transaction ID wraparound (which would stop writes). CPU spikes were also waking on-call engineers and some schema migrations were becoming unsafe.
- Choice: sharding in the application rather than adopting an off-the-shelf sharding layer, to keep control over data placement.
- Shard key: the workspace ID, because each block belongs to one workspace and most queries stay inside one workspace, avoiding cross-shard joins. Tables reachable by foreign key from the block table were sharded together.
- Layout: many small logical shards (each a schema with its own copy of the tables) mapped onto fewer physical databases. The logical count was chosen with many divisors so shards can be redistributed evenly when hosts are added.
- Migration pattern: double-write new changes, backfill old data without overwriting newer versions, verify (sampling plus comparison reads), then cut over with a short window; a reverse path was prepared for rollback.
- Logical replication was rejected as the double-write method because it struggled to keep up with the write volume of the busiest tables during the initial snapshot step.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 480 logical shards on 32 physical databases (15 per DB) | Partitioning scheme section | Notion-specific |
| Cutover maintenance window about 5 minutes | Migration section | Notion-specific |
| Limits mentioned: 500 GB per table, 10 TB per physical DB | Planning section | Their operational targets, not universal |

## Relevant to concepts

- `sharding-trigger`: a real example of why a team shards after exhausting simpler options.
- `logical-vs-physical-shards`: a way to make rebalancing cheaper.
- `shard-key-choice`: pick the key that matches the dominant query scope.
- `online-migration`: double-write and backfill pattern.

## Warnings

- One company's case; the numbers are context, not rules. Published October 2021.
- The article is about Postgres operational limits (vacuum, wraparound), so avoid teaching those as general sharding triggers without noting they are engine-specific.
