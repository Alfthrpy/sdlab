---
source: pg-docs-prepare-transaction
read_by: agent
date: 2026-11-16
sections_read: ["PREPARE TRANSACTION (description, notes)"]
---

# Notes: PREPARE TRANSACTION (PostgreSQL 18)

> Notes are in English and in your own words.

## Key points

- (Description) PREPARE TRANSACTION ends the session's involvement and saves the transaction's state on disk, so it can still commit after a crash. Any session can then finish it with COMMIT PREPARED or ROLLBACK PREPARED, identified by a string id.
- (Description) The docs explain that this exists for an external transaction manager that coordinates a global transaction across several resources: phase one prepares every resource, phase two commits or rolls back all of them. Unless you write such a manager you should not use it.
- (Notes) A prepared transaction still holds its locks and blocks VACUUM cleanup; leaving it prepared for long can threaten transaction ID wraparound. Keep them short.
- (Notes) Setting `max_prepared_transactions` to zero prevents forgotten prepared transactions; `pg_prepared_xacts` lists current ones.
- (Notes) Some features (temporary tables, WITH HOLD cursors, LISTEN/NOTIFY) block preparation.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| transaction id must be shorter than 200 bytes | Description | Minor detail |

## Relevant to concepts

- `distributed-transactions`: the participant side of 2PC and its operational cost (locks held while waiting for the coordinator).

## Warnings

- Covers only the participant; the coordinator protocol and its blocking problem when the coordinator dies are not on this page.
