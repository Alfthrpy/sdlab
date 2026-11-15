---
source: berenson-critique-ansi-isolation-1995
read_by: agent
date: 2026-11-15
sections_read: ["Abstract", "1 Introduction", "2.1-2.3", "3", "4.1", "4.2", "4.3", "5 Summary and Conclusions", "Tables 1-4, Figure 2 (text extraction of the PDF)"]
---

# Notes: A Critique of ANSI SQL Isolation Levels (Berenson et al., SIGMOD 1995, MSR-TR-95-51)

> Notes are in English and in your own words. Read in full from the Microsoft Research PDF (text extraction; Figure 2 is a diagram and was read only through its caption and labels). The "longer version" the paper cites (O'Neil et al.) was not read.

## Key points

- (1, 2.2) The ANSI SQL-92 isolation levels are defined by three forbidden "phenomena": dirty read, non-repeatable (fuzzy) read, phantom. The paper's thesis is that this wording is ambiguous and incomplete, and that it does not match how locking databases actually behave.
- (2.2) Each phenomenon can be read narrowly (only when an anomaly actually happens, such as the writer later aborting) or broadly (any interleaving that could lead to one). The paper calls the narrow readings A1-A3 and the broad ones P1-P3 and argues in (3) that only the broad readings were intended, with worked histories H1-H3 (a bank transfer seen half-done, an inconsistent total, an employee count that disagrees with the list).
- (2.2, Table 1) The ANSI table makes it look as if forbidding the three phenomena equals serializable. The standard has a separate sentence demanding "fully serializable" execution, which the table hides. The paper calls the table-only version "anomaly serializable".
- (3) A fourth phenomenon is missing from the ANSI list: dirty write (P0), where two uncommitted transactions overwrite the same item. Without forbidding it, constraints between two items can break and rollback by restoring old values stops working. The paper recommends forbidding P0 at every level (Remark 3, Table 3).
- (2.3, Table 2) Locking definitions: levels differ by what is locked (single items or predicates), in which mode (read or write) and for how long (short or held to commit). Read Uncommitted keeps long write locks only; Read Committed adds short read locks; Locking Repeatable Read holds item read locks but only short predicate locks; Serializable holds everything to commit.
- (2.3, 3) With P0-P3 forbidden in the broad sense, the phenomenon-based definition equals the locking one (Remark 6): the phenomena are "locking behaviour in disguise" for single-version systems.
- (2.3) The term "Repeatable Read" is called an unfortunate choice twice over: under the ANSI definition reads are not repeatable (phantoms can still change a re-read result), and earlier products (Date, DB2) used the same words to mean full serializability.
- (4.1) Lost update (P4): a transaction overwrites a value after another transaction changed it, based on a stale read, so the other update vanishes. Read Committed does not stop it, Repeatable Read does. Cursor Stability sits between the two: it holds a lock on the row under a cursor, which prevents lost updates for cursor-based read-modify-write only.
- (4.2) Snapshot Isolation: each transaction reads from a snapshot taken at its start and never blocks on reads; at commit the first committer wins and a later writer of the same item aborts. It prevents dirty reads, lost updates, read skew, and the ANSI-defined phantom. It is therefore stronger than Read Committed in some ways.
- (4.2) Snapshot Isolation is still not serializable. Write skew (A5B): two transactions read overlapping data, each writes a different item, both commit, and a constraint across the items breaks (the paper's example is two accounts whose combined balance must stay non-negative; a second example sums task hours via a predicate). Read skew (A5A) is the mirror problem under weaker levels.
- (4.2, Remarks 9-10) Snapshot Isolation and ANSI Repeatable Read are incomparable: each allows an anomaly the other forbids (write skew versus phantom). Since Snapshot Isolation never shows the ANSI phantom, it satisfies the three-phenomenon "serializable" table without being serializable.
- (4.2) The paper expects Snapshot Isolation to suit mostly-read-only workloads and short updates, and to suit long update transactions badly because they are likely to lose the first-committer race and abort.
- (4.3) Other multi-version designs exist: Oracle-style "read consistency" gives each statement a fresh snapshot and uses first-writer-wins locking, so it allows lost updates and read skew that Snapshot Isolation does not.
- (5, Figure 2, Table 4) Summary ordering of levels by what they allow: Read Uncommitted < Read Committed < Cursor Stability < Repeatable Read < Serializable, with Snapshot Isolation sitting above Read Committed but incomparable with Repeatable Read. The paper's advice: fix the ANSI definitions (add P0, use the broad P1-P3), and find a new name for "Repeatable Read".

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published as Proc. ACM SIGMOD 95, pp. 1-10, San Jose, June 1995 | page footers | The PDF is the Microsoft Research copy, MSR-TR-95-51 |
| Phenomena P0 dirty write, P1 dirty read, P2 fuzzy read, P3 phantom, P4 lost update, A5A read skew, A5B write skew | 3, 4.1, 4.2 | Names and definitions used by later literature (Adya, Hermitage) |
| Snapshot Isolation permits write skew (A5B) but not lost update, dirty read or the ANSI phantom | 4.2, Table 4 | Useful to explain why "repeatable read" differs between databases |
| Locking Repeatable Read keeps long item read locks but only short predicate read locks | 2.3, Table 2 | Why phantoms survive at that level |

## Relevant to concepts

- `isolation-levels` (Unit 3): why named levels do not mean the same thing across databases; the phenomena as vocabulary.
- `snapshot-isolation` / `mvcc`: how snapshot reads and first-committer-wins work, and what they still allow.
- `write-skew` and `lost-update`: the minimal examples and which levels block them.

## Warnings

- 1995 text, written before modern implementations. PostgreSQL's Serializable (SSI) and today's MVCC engines postdate it; check each database's manual (`pg-docs-transaction-iso`) and the Hermitage results (`hermitage-isolation-tests`) before saying what a level does in a given product.
- The paper's formal notation (w1[x], r2[x]) is dense. For learners, use the paper's anomalies and examples, not its notation.
- It is a critique of the SQL standard as of SQL-92; later standard text changed the wording.
- It is a 10-page conference paper; its proofs and the multi-version formalism are in a longer companion report that was not read.
