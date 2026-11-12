---
source: dynamo-sosp07
read_by: agent
date: 2026-11-12
sections_read: ["Abstract", "1 Introduction", "4.2 Partitioning Algorithm", "4.3 Replication (skimmed)", "6.1-6.2 (N,R,W) experience", "6.2 partitioning strategies (skimmed)"]
---

# Notes: Dynamo: Amazon's Highly Available Key-value Store (SOSP 2007)

> Notes are in English and in your own words. Read via text extraction of the PDF; section numbers follow the paper's headings. Sections on vector clocks, hinted handoff and Merkle trees (4.4-4.7) were only seen as headings.

## Key points

- (Abstract, 1) The design deliberately gives up consistency under some failures to keep writes always available; conflicts are resolved with versioning and help from the application. The motivating example is a shopping cart that must always accept additions.
- (4.2) Partitioning uses consistent hashing: the hash output space is a ring, each node sits at a point, and a key belongs to the first node clockwise. A node joining or leaving affects only its neighbours.
- (4.2) Plain consistent hashing has two flaws: random node positions give uneven load, and it ignores differences in machine power. The fix is virtual nodes: each physical node takes many positions ("tokens"), which spreads a failed node's load over many others.
- (4.3, 6) Each key is stored on N replicas; a read waits for R and a write waits for W responses. Raising W shrinks the window where data may be lost but makes writes fail more often when nodes are down. The common configuration was (3,2,2).
- (6.2) Later experience led to a different partitioning strategy with equal-sized fixed partitions, because random token ranges made bootstrap slow (up to about a day in busy periods), forced Merkle tree recalculation, and made snapshots hard.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Common (N,R,W) = (3,2,2) | 6.1 | Quorum overlap when R + W > N |
| Bootstrap sometimes took almost a day during busy season | 6.2 | Motivates fixed-size partitions |

## Relevant to concepts

- `consistent-hashing`: ring, virtual nodes, minimal data movement.
- `leaderless-replication`: N/R/W quorum and tunable consistency.
- `rebalancing`: why fixed partitions beat random token ranges.

## Warnings

- 2007 system, since superseded in practice by DynamoDB (a different service). Do not present the paper's design as how DynamoDB works today.
- Copyright ACM 2007; the free PDF is hosted by an author's site. Rewrite only.
