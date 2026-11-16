---
source: berenson-critique-ansi-isolation-1995
read_by: agent
date: 2026-11-16
sections_read: ["Abstract", "1 Introduction", "2.1-2.3 Isolation Definitions", "3 Analyzing ANSI SQL Isolation Levels", "4.1 Cursor Stability", "4.2 Snapshot Isolation", "4.3 Other Multi-Version Systems", "5 Summary and Conclusions (partly; the last paragraph and Figure 2 text were garbled by extraction)"]
---

# Notes: A Critique of ANSI SQL Isolation Levels (MSR-TR-95-51, June 1995)

> Notes are in English and in your own words. Read from the PDF text (13 pages). Not read: the reference list. Section numbers follow the PDF headings (the introduction's roadmap says the summary is Section 6, but the heading in the text is 5). Figure 2 (the level hierarchy diagram) and Tables 1-3 were readable only as flattened text, so table cell layout was reconstructed from context.

## What I could and could not read

- Could read: all prose, the history notation, the remarks, Tables 1-3 (as flattened text), the histories H1-H5.
- Could not read cleanly: the figure showing the hierarchy of levels (only labels came through), and the end of the conclusion (cut by two-column extraction). Section 2.1 and parts of section 4.2 had column interleaving; I re-read them in order.
- The PDF refers to a longer version [OOBBGM] for formal proofs (not opened).

## Key points

- (Sec. 1) The ANSI SQL-92 levels are defined by three forbidden phenomena (dirty read, non-repeatable read, phantom). The paper's thesis is that this phenomenon-based definition is ambiguous and does not match how locking databases behave or what products offer.
- (Sec. 2.2) Each phenomenon can be read narrowly (a concrete bad outcome, e.g. the writer actually aborts) or broadly (the risky pattern, whether or not it ends badly). The paper writes both forms (A1-A3 strict, P1-P3 broad).
- (Sec. 2.2, Table 1) With the standard's table, a level that forbids the three phenomena is called "anomaly serializable". The standard's separate sentence in 4.28 still requires truly serializable execution, so forbidding the three phenomena alone does not imply serializability.
- (Sec. 3, H1, H2, H3) Three bank-style histories (a transfer being read mid-way; reading x then y after a concurrent change; counting active employees after an insert) are non-serializable yet not excluded by the strict readings. The authors conclude the broad readings are what the standard must have meant.
- (Sec. 3, P0) The standard does not forbid dirty writes (two uncommitted transactions overwriting the same item). Dirty writes can break a constraint between two items and make rollback by restoring old values ambiguous, so the paper recommends forbidding them at every level (Remark 3).
- (Sec. 3, Table 3, Remark 6) With P0-P3 added, the phenomenon-based levels become equal to the locking levels of Table 2 (long write locks; long item read locks for repeatable read; long predicate read locks for serializable). The phenomena are in effect locking behaviour in disguise.
- (Sec. 2.3) The paper notes the term "repeatable read" is misleading: ANSI's version still allows phantoms, and earlier industry usage (Date, DB2) used it to mean full serializability.
- (Sec. 4.1) Lost update (P4): both transactions read, one writes and commits, the other writes from its stale read. It can occur at Read Committed. Cursor Stability (hold a lock on the row the cursor is on) prevents the cursor version of it and sits between Read Committed and Repeatable Read.
- (Sec. 4.2) Snapshot Isolation: reads come from a snapshot at transaction start; commit succeeds only if no concurrent committed transaction wrote the same item ("first committer wins"), which prevents lost updates. It prevents dirty reads, fuzzy reads and strict phantoms, but is not serializable.
- (Sec. 4.2, H5) Write skew: two transactions read overlapping data, each writes a different item, and a constraint across the items (a balance sum staying positive) is violated. A related example with a predicate (task-hours sum limit) shows that insertion of different rows still slips through.
- (Sec. 4.2, A5A) Read skew: a transaction reads one item, another transaction updates two related items and commits, then the first reads the second item and sees an inconsistent pair.
- (Sec. 4.2, Remarks 8-10) Snapshot Isolation is stronger than Read Committed, incomparable with Repeatable Read (each permits an anomaly the other forbids: write skew for SI, phantoms for locking RR).
- (Sec. 4.2) Practical remarks: read-only transactions never block; long update transactions that compete with short ones tend to abort under first-committer-wins.
- (Sec. 4.3) Oracle-style "read consistency" gives each statement the latest committed data at its start, so it is stronger than Read Committed (cursor lost updates) but still allows non-repeatable reads, general lost updates and read skew.
- (Sec. 5) Conclusion: ANSI definitions are ambiguous and incomplete; the paper recommends adding P0 and using the broad readings; it also recommends finding another name for "repeatable read".

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Venue and date: SIGMOD 1995, pp. 1-10, San Jose, June 1995 | cover and running footer | The PDF is the technical-report layout (MSR-TR-95-51) |
| Four anomalies with exact history notation: P0, P1, P2, P3, P4, A5A, A5B | Secs. 2-4 | Use for precise definitions of dirty write, dirty read, fuzzy read, phantom, lost update, read skew, write skew |
| Write skew example constraint: x + y must stay positive, start 50/50, each writes -40 to its own item | Sec. 4.2, H5 | Good seed for a lab |
| Lost update example: x=100, one adds 20, the other adds 30, result 130 | Sec. 4.1, H4 | Shows the +20 vanishing |

## Relevant to concepts

- `isolation-levels`: the anomaly vocabulary (dirty write/read, non-repeatable read, phantom, lost update, read skew, write skew) and why a level name does not tell you which anomalies you are protected from.
- `transactions-acid`: the "I" in ACID is not a single guarantee.

## Warnings

- Dated 1995 (single-version locking and early snapshot systems); modern engines differ (PostgreSQL's Repeatable Read is snapshot isolation and also blocks phantoms; Serializable there is SSI, which postdates this paper). Use pg-docs-transaction-iso and hermitage-isolation-tests for current engine behaviour.
- The paper uses "Read Skew" and "Write Skew" in a narrower sense than some later literature (Adya, Bailis et al.); see jepsen-consistency-models and hermitage-isolation-tests for the later G-single/G2 names.
- Table 1 shows "Possible/Not Possible", and the strict-vs-broad distinction is easy to misquote: the ANSI standard, as written, is the weaker one.
