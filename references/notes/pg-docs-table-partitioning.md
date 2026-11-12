---
source: pg-docs-table-partitioning
read_by: agent
date: 2026-11-12
sections_read: ["5.12.1 Overview", "5.12.2 Declarative Partitioning", "5.12.4 Partition Pruning", "5.12.6 Best Practices"]
---

# Notes: PostgreSQL 18 Documentation, 5.12. Table Partitioning

> Notes are in English and in your own words.

## Key points

- (5.12.1) Partitioning splits one logical table into physical pieces inside one server. Three built-in methods: range (non-overlapping key ranges), list (explicit value sets), hash (modulus and remainder).
- (5.12.1) Stated benefits: hot rows concentrated in few partitions keep index pages in memory; bulk delete becomes dropping or detaching a partition; cold data can sit on cheaper storage.
- (5.12.1) Trigger hint: the page says the gain usually justifies the work only when the table would be very large, with a rule of thumb that the table exceeds server memory.
- (5.12.2.1) Rows inserted outside every partition's bounds fail, so partitions must be created ahead of time (important for time-based ranges).
- (5.12.2.3) Unique and primary key constraints must include the partition key columns.
- (5.12.4) Pruning lets the planner skip partitions the WHERE clause rules out; it works from partition bounds, not from indexes.
- (5.12.6) Choosing the key: use columns that appear in WHERE clauses; count matters, since too few partitions leave big indexes and too many cost planning time and memory. Re-partitioning large data later is slow.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| "Table larger than server memory" as a rule of thumb for partitioning | 5.12.1 | A rule of thumb from the docs, not a measured law |
| Planner copes with up to a few thousand partitions if pruning leaves few | 5.12.6 | OLTP vs warehouse differ |

## Relevant to concepts

- `partitioning-vs-sharding`: same ideas (range/hash, key choice) on one machine; sharding adds the network and cross-node queries.
- `range-vs-hash-partitioning`: the three methods.
- `hot-spots`: time-range keys concentrate recent writes in one partition.

## Warnings

- This is single-server partitioning, not distributed sharding. Do not use it to explain rebalancing across nodes.
- Inheritance-based partitioning (5.12.3) is legacy; ignore it for teaching.
