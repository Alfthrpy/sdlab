---
source: pg-docs-log-shipping-standby
read_by: agent
date: 2026-11-12
sections_read: ["26.2 Log-Shipping Standby Servers (26.2.1-26.2.9)"]
---

# Notes: PostgreSQL 18 Documentation, 26.2. Log-Shipping Standby Servers

> Notes are in English and in your own words.

## Key points

- (26.2) A standby is a server that continuously replays the write-ahead log produced by the primary. Log shipping is asynchronous, so a catastrophic primary failure can lose the last transactions that were not yet shipped.
- (26.2.2) A standby is promoted to primary with an explicit command; it then stops following the old primary.
- (26.2.5) With streaming, the standby receives log records as they are produced; the page says lag is typically under a second, versus waiting for whole log files.
- (26.2.5.2) Lag is measured by comparing log positions: the primary's current position versus what the standby has received and replayed. A gap between received and replayed means the standby cannot apply changes as fast as they arrive.
- (26.2.6) A replication slot makes the primary keep log (and avoid removing rows) the standby still needs, even while it is disconnected. The cost: a dead standby can fill the primary's disk, so cap retention.
- (26.2.7) Standbys can feed other standbys (cascading); this is always asynchronous.
- (26.2.8) Synchronous replication makes commit wait for a standby. Levels differ in how far the standby must get (written to disk, written to OS, or applied and visible). Priority (FIRST n) and quorum (ANY n) lists of standbys are supported.
- (26.2.8.3) Waiting for a standby holds locks longer and needs network bandwidth above the log generation rate, so apply it selectively.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Streaming lag is typically under 1 second | 26.2.5 | "Typically", not a guarantee |
| Sync levels: remote_write, on, remote_apply | 26.2.8.1 | Pair with high-availability chapter intro: sync can cut performance by more than half over slow networks |

## Relevant to concepts

- `leader-follower-replication`: primary/standby model, promotion.
- `replication-lag`: how to measure it, why async can lose data.
- `read-replicas` (trigger): offloading reads to standbys; the read-query side is in 26.4, not read here.
- `sync-vs-async-replication`: the commit-wait levels.

## Warnings

- Failover procedure (26.3) and hot-standby query conflicts (26.4) were not read; do not cite this note for them.
- Physical (byte-level) replication: primary and standby must match major version and architecture. Logical replication is a different chapter.
