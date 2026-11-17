---
source: mysql-84-backup-recovery
read_by: agent
date: 2026-11-17
sections_read: ["Chapter 9 landing page (intro and Additional Resources)", "9.1 Backup and Recovery Types", "9.2 Database Backup Methods", "9.3 Example Backup and Recovery Strategy (intro)", "9.3.1 Establishing a Backup Policy", "9.3.2 Using Backups for Recovery", "9.3.3 Backup Strategy Summary", "9.5.1 Point-in-Time Recovery Using Binary Log"]
---

# Notes: MySQL 8.4 Reference Manual, Chapter 9 Backup and Recovery

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location.
> All pages above were read on 2026-11-17 via `curl` on the raw HTML (WebFetch summaries were not relied on). Not read: 9.4 (mysqldump in detail), 9.5.2 (event positions), 9.6 (MyISAM maintenance), MySQL Enterprise Backup chapter. The registry entry says only the landing page was opened; this note covers more subpages than the registry text mentions (the registry was not changed). Page footer: (c) 2026 Oracle; the version selector shows 8.4, 8.0 and 9.7 (marked current).

## Key points

- (Ch. 9 intro) Backups are needed for crashes, hardware failure and people deleting data by mistake; they are also the safety step before an upgrade, and a way to move an installation or seed a replica. Chapter scope: backup types, methods, recovery including point-in-time recovery, scheduling/compression/encryption, table maintenance.
- (9.1, Physical vs logical) Physical backup = raw copy of data files; faster and more compact, suited to big databases that must be restored quickly, but portable only between machines with similar hardware. Logical backup = SQL statements or delimited text produced by querying the server; slower and larger, but works for any storage engine, is machine-independent, and can be done at server, database or table granularity.
- (9.1, Online vs offline) Online (hot) backups run while the server serves clients and need correct locking for consistency; offline (cold) backups need the server stopped, so they are often taken from a replica. Restoring is more disruptive than backing up because clients must be kept away from data being rewritten.
- (9.1, Full vs incremental; Full vs point-in-time recovery) A full backup is all data at one moment. An incremental backup is the changes between two moments, available in MySQL through the binary log. Point-in-time recovery means: restore the full backup first, then replay binary-log changes up to the chosen moment.
- (9.1, Backup scheduling...) MySQL itself does not schedule, compress or encrypt backups; that is done with external tools.
- (9.2) Overview of methods: Enterprise Backup (physical, hot for InnoDB), mysqldump (logical, all engines; for InnoDB can be non-locking with --single-transaction), copying table files (not valid for InnoDB), delimited-text export (data only, no structure), incremental backups via the binary log (enabled by default in 8.4; rotate with FLUSH LOGS then copy the finished logs), backups taken from a replica to reduce impact on the source, and file system snapshots.
- (9.2, Using replicas) Taking the backup from a replica is a way to reduce load on the primary. A replica is a separate server that receives the primary's changes; the page treats it as a place to take backups from, not as a replacement for backups.
- (9.3.1) A worked example policy: full dump with mysqldump (all databases, --single-transaction, flush logs, record binary-log position) on Sunday at 1 p.m. when load is low; then an incremental backup each day at 1 p.m. by rotating the binary log and copying the closed log to a safe place.
- (9.3.1) Trade-off stated for full vs incremental: full backups are big and slow because every run copies unchanged data again; incrementals are small and quick but make recovery more work (reload full, then apply each incremental).
- (9.3.1) Binary logs take disk space and need purging, but purging while replicas have not consumed them is dangerous.
- (9.3.2) Recovery walk-through: crash on Wednesday 8 a.m.; restore Sunday's full dump, replay binary logs 7 and 8 (changes up to Tuesday 1 p.m.). Changes after Tuesday 1 p.m. are lost unless the binary logs were stored on a different physical device than the data files, in which case the newest log can be replayed too and nothing is lost up to the crash.
- (9.3, intro) With InnoDB, an OS crash or power failure is handled by the engine's own crash recovery from its log, with no backup needed. A file system crash or hardware failure that leaves the data unreadable is the case where backups are mandatory, so the policy must exist beforehand.
- (9.3.3) Summary rules: keep binary logging on, make periodic online full backups, make periodic incremental backups by flushing logs.
- (9.5.1) Point-in-time recovery needs binary logging enabled; commands to list logs and find the current one (SHOW BINARY LOGS, SHOW BINARY LOG STATUS); mysqlbinlog converts events to text that the mysql client can apply, optionally limited by time or position; apply multiple logs through one connection.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Binary logging is on by default in MySQL 8.4 | 9.2 (incremental backups), 9.3.3, 9.5.1 | Version-specific; do not generalize to older versions |
| Example schedule: full backup Sunday 1 p.m., incremental each day at 1 p.m., crash Wednesday 8 a.m. | 9.3.1 and 9.3.2 | Useful for a "what is lost" exercise; with logs on the same disk, loss window = Tuesday 1 p.m. to Wednesday 8 a.m. (the page implies it, we state it) |
| Copying table files does not work for InnoDB | 9.2, Making Backups by Copying Table Files | Applies to the file-copy method, not to physical backup tools |
| mysqldump --single-transaction gives an online InnoDB backup without table locks, via consistent read | 9.2 and 9.3.1 | Requires all tables to be transactional; non-transactional tables need no changes during the dump |
| Brief global read lock at the start of the dump to get the binary log position, then lock-free | 9.3.1 | May stall if long updates are running |

## Relevant to concepts

- `backup-recovery` objective 1 (distinguish backups from replicas/mirrors by the kind of damage each protects against): partly supported. 9.2 "Making Backups Using Replicas" and the chapter intro mention replicas as a place to take backups from, but the pages do not explicitly say that a replica copies mistakes (a deleted table, a bad UPDATE) to itself. 9.3.2 supports the opposite side: point-in-time recovery from backup plus logs is what recovers from a user error. The explicit "replica does not protect against deletion" statement must come from another source (atlassian-pir-april-2022 for the architecture contrast, pg-docs-log-shipping-standby or google-sre-book-data-integrity-ch26).
- `backup-recovery` objective 2 (choose backup frequency from RPO and RTO): NOT well supported. The words RPO and RTO do not appear on the pages read. 9.3.1/9.3.2 give a concrete weekly-full plus daily-incremental schedule and show what is lost when the logs are on the same disk as the data, which lets a learner reason about data-loss window, and 9.3.1 states the full-vs-incremental trade-off (size/time vs restore effort). It does not show how to derive a schedule from a target loss or recovery time, nor does it give restore duration numbers. Pair with atlassian-pir-april-2022 (definitions and the RPO/RTO result) and the SRE book source.
- `backup-recovery` objective 3 (explain why a never-restored backup is not yet safe): NOT supported on the pages read. 9.3.2 shows the restore procedure but does not recommend test restores. The chapter's other pages (9.4.x mysqldump reload, 9.5.2) were not read and may touch it, but nothing indicates a testing recommendation.
- `backup-recovery` (general): good for the vocabulary: logical vs physical, full vs incremental, online vs offline, point-in-time recovery, and for a concrete MySQL example next to the PostgreSQL source (pg-docs-backup-restore).

## Warnings

- NO-DATE, NO-AUTHOR and all-rights-reserved (see registry): rewrite only; do not copy the example commands and log listings beyond short command names.
- MySQL 8.4 specifics: the page uses option names such as --source-data and --delete-source-logs; other MySQL versions may name these differently (not checked here), so do not mix versions in a lesson. MySQL Enterprise Backup is a commercial product, so the "physical backup tool" described is not available in the free Community Edition; the free alternatives on the page are mysqldump (logical) and file-system-level copies/snapshots.
- The InnoDB statement "crash recovery needs no backup" covers OS crash and power loss only (9.3 intro); it must not be stretched to disk loss or user error.
- 9.3.2 notes that no data is lost only if the binary logs live on a separate device; the example would otherwise lose changes since the last incremental. This is the easy-to-miss point for RPO discussion.
- 9.3.3 contains a small typo in the original ("tun" for "run"); the page is as published.
- Subpage 9.4 (mysqldump options) and 9.6 were not opened; keep claims limited to the sections listed in `sections_read`.
