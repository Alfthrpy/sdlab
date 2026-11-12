---
source: pg-docs-backup-restore
read_by: agent
date: 2026-11-12
sections_read: ["25 (chapter outline)", "25.1 SQL Dump", "25.3 Continuous Archiving and PITR (section list and 25.3.1 config-file remark re-checked 2026-11-12)"]
---

# Notes: PostgreSQL 18 Documentation, Chapter 25. Backup and Restore

> Notes are in English and in your own words. Locations are section numbers in the PostgreSQL 18 docs.

## Key points

- (25, intro) There are three distinct approaches: a logical SQL dump, a copy of the data directory files, and continuous archiving of the write-ahead log (WAL) on top of a base backup.
- (25.1) A dump is a script that rebuilds the database as it was when the dump started. It reads from a consistent snapshot and does not stop normal reads and writes.
- (25.1) A dump is portable across PostgreSQL versions and machine architectures; a file-level copy is tied to one server version.
- (25.1.1) Restore into an empty database created from the pristine template, and make sure the roles the dump refers to already exist. Plain restores continue after errors unless told to stop, so a partial restore can go unnoticed.
- (25.1) Run ANALYZE after a restore so the planner has statistics again.
- (25.1.2) A single-database dump leaves out roles and tablespaces; the cluster-wide dump tool includes them.
- (25.1.3) Large databases: compress, split, use the custom or directory format, and dump or restore in parallel.
- (25.3) Continuous archiving = base backup + every WAL segment written after it. Replaying WAL up to a chosen moment gives point-in-time recovery (PITR), for example "just before the bad DELETE".
- (25.3.1) The archive command must succeed only if the file is really stored, and must not overwrite an existing archived file. If archiving falls behind, WAL piles up on the data disk and can fill it.
- (25.3.1) Only completed WAL segments are archived, so a time-based forced switch bounds how much recent data could be missing from the archive.
- (25.3.5) Recovery order: stop the server, keep a copy of what is there, restore the base backup, point the server at the archive, signal recovery, start, then check the data. If the result is wrong, retry with a different target.
- (25.3.1) Config files (postgresql.conf, pg_hba.conf, pg_ident.conf) are not restored by WAL archiving because they are edited by hand, so keep them in a location covered by the normal file backup. (25.3.8 Caveats is a separate section and was not checked for the tablespace remark.)
- (25.3.3) Incremental base backups exist, but restoring needs the whole chain; the server does not stop you from deleting a backup a later one depends on.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| WAL segments are 16 MB by default and archived only when complete | 25.3.1 | Explains why a forced switch interval is used |
| A full disk caused by unarchived WAL ends in a PANIC shutdown, but no committed transaction is lost | 25.3.1 | Good "what happens if archiving breaks" fact |
| Logical dumps cannot be used as the base for WAL replay | 25.3 | Dump and PITR are separate strategies |

## Relevant to concepts

- `backups-and-recovery-basics`: logical dump vs. physical base backup + WAL, and what PITR buys you.
- `restore-testing`: the recovery procedure is a checklist a learner can rehearse.
- `limits-of-one-machine`: backups on the same disk as the data do not survive disk loss (inference; the docs do not say this directly).

## Warnings

- Written for PostgreSQL 18; commands and some option names differ in older versions (incremental backup is new in 17+).
- The chapter covers mechanics only: nothing on how often to back up, where to store copies, or how to rehearse restores. That needs another source (gap).
