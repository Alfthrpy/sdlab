---
source: pg-docs-wal-intro
read_by: agent
date: 2026-11-16
sections_read: ["28.3 Write-Ahead Logging (WAL)"]
---

# Notes: Write-Ahead Logging (PostgreSQL 18)

> Notes are in English and in your own words.

## Key points

- (28.3) Core rule: a change to a table or index file may be written only after the WAL record describing it is safely on disk.
- (28.3) Durability at commit: commit needs only the sequential WAL flush, not a flush of every changed data page, which is much cheaper. One flush can cover several concurrent commits (group commit).
- (28.3) Crash recovery: pages not yet written can be rebuilt by replaying WAL (redo, roll-forward).
- (28.3) Archived WAL plus a base backup allows point-in-time recovery; the backup need not be an instant snapshot because replay repairs inconsistencies.
- (28.3) A journaling file system is not required for data safety because WAL does the recovery.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| none needed | | |

## Relevant to concepts

- `transactions-acid`: durability mechanism (D), why commit is fast.
- `backup-restore` style topics: PITR via archived WAL.

## Warnings

- Atomicity (undoing uncommitted work) is not explained here; the page is about redo and durability. Checkpoints are in other sections of the chapter, not read.
