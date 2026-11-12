---
source: pg-docs-transaction-iso
read_by: agent
date: 2026-11-12
sections_read: ["13.2 Transaction Isolation (13.2.1-13.2.3)"]
---

# Notes: PostgreSQL 18 Documentation, 13.2. Transaction Isolation

> Notes are in English and in your own words.

## Key points

- (13.2, Table 13.1) The SQL standard defines isolation levels by which anomalies they forbid: dirty read, nonrepeatable read, phantom read, serialization anomaly. PostgreSQL accepts four level names but really implements three; asking for Read Uncommitted gives Read Committed.
- (13.2) The standard only sets minimum guarantees, so an implementation may be stricter: PostgreSQL's Repeatable Read also blocks phantoms.
- (13.2.1) Read Committed is the default. Each statement gets its own fresh snapshot, so two SELECTs in one transaction can disagree.
- (13.2.1) For writes under Read Committed, a statement that hits a row being changed by another transaction waits, then re-checks the row against its condition once the other one commits. This can give surprising results within a single statement (the page's DELETE-vs-increment example).
- (13.2.2) Repeatable Read takes one snapshot at the first real statement and keeps it. If a concurrent transaction already changed a row you try to modify, you get an error and must retry. This level is snapshot isolation; it still allows write skew-style anomalies.
- (13.2.3) Serializable adds dependency tracking on top of snapshot isolation (SSI). It does not block; it aborts one transaction when a dangerous read/write pattern appears.
- (13.2.3) Failures at Repeatable Read and Serializable carry SQLSTATE 40001. The application must roll back and rerun the whole transaction, and must not trust data read in a transaction that was aborted.
- (13.2.3) Tips to keep Serializable cheap: mark read-only work as READ ONLY, keep transactions short, limit connections, avoid idle-in-transaction sessions.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default level is Read Committed | 13.2.1 | PostgreSQL-specific; other engines may differ (not checked) |
| Failure code for serialization problems is 40001 | 13.2.2 / 13.2.3 | Retry loop lesson |

## Relevant to concepts

- `isolation-levels`: the four-level table and the PostgreSQL deviations.
- `mvcc-snapshots`: statement-level vs transaction-level snapshot.
- `transaction-retry`: why app code needs a retry loop for 40001.

## Warnings

- Describes PostgreSQL behavior only; do not present it as what "the SQL standard says" for all databases. Pair with berenson-critique-ansi-isolation-1995 (abstract only so far) and jepsen-consistency-models for a vendor-neutral view.
- The MVCC mechanism itself (tuple versions, vacuum) is not explained on this page.
