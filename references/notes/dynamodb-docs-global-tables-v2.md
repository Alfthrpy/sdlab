---
source: dynamodb-docs-global-tables-v2
read_by: agent
date: 2026-11-15
sections_read: ["Concepts", "Versions", "Availability", "Consistency modes (MREC, MRSC)", "Choosing a consistency mode", "Monitoring global tables", "Transactions", "Streams (skimmed)"]
---

# Notes: How DynamoDB global tables work (Version 2019.11.21)

> Notes are in English and in your own words. Companion page read for conflict-avoidance advice: the legacy 2017.11.29 "Global tables: How it works".

## Key points

- (Concepts) A global table is a set of replica tables, one per Region, with the same key schema and the same items. A write to any replica is copied to all the others, so every Region accepts writes: this is multi-leader (multi-active) replication.
- (Consistency modes, MREC) Default mode is multi-Region eventual consistency: copies travel asynchronously, usually in about a second or less. If two Regions change the same item at nearly the same time, the version with the later internal timestamp wins, per item ("last writer wins"), and all replicas converge to it. The losing change is simply overwritten.
- (MREC) Strongly consistent reads are only strong with respect to the Region that served them: they can be stale if the item was last written in another Region. Conditional writes are checked against the local copy.
- (Consistency modes, MRSC) Strong-consistency mode copies each write synchronously to at least one other Region before reporting success, requires exactly three Regions (or two plus a witness), and rejects a write that collides with an in-flight write to the same item elsewhere (the client must retry). The price is higher write latency.
- (Choosing a consistency mode) The page frames the decision as: lower write latency and tolerance for a recovery point greater than zero (MREC) versus global read consistency and a recovery point of zero (MRSC). In MREC the recovery point objective equals the replication delay.
- (Monitoring) For MREC there is a replication-latency metric per source and destination Region pair; a rising value means updates are not propagating in time, and the page suggests temporarily moving traffic to another Region.
- (Transactions) Transactions are atomic only in the Region where they run; other Regions may briefly show part of a transaction.
- (Legacy page, Common tasks) Ways to avoid conflicts that the legacy page lists: allow writes in only one Region (for example by permissions), route each user to one Region, and prefer absolute updates ("set to 25") over relative ones ("add 1").

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| MREC replication typically within about a second or less | Consistency modes, MREC | AWS's statement, depends on Regions and load |
| MRSC needs exactly three Regions (or two plus a witness) | Consistency modes, MRSC | |
| Global tables SLA 99.999 percent vs 99.99 percent single-Region | Availability | Vendor SLA figure |

## Relevant to concepts

- `multi-leader-replication`: a concrete product where all replicas accept writes, how conflicts are resolved (timestamps), what is lost (the overwritten write), and how to design around conflicts.
- `replication-lag`: lag as a first-class metric that doubles as the data-loss window on failover.
- `conflict-resolution`: contrast last-writer-wins with reject-and-retry (MRSC) and with application-level merge (CouchDB, `couchdb-docs-replication-intro`).

## Warnings

- Vendor feature documentation, not a neutral treatment of multi-leader replication. Last-writer-wins can silently discard a valid write; the legacy 2017.11.29 global tables page (not this one) says "best effort" for choosing the last writer, and this page does not describe clock behaviour in detail.
- Conflict-avoidance advice is on the legacy page, not on this one; confirm it still applies before quoting.
