---
source: qiao-btree-lsm-write-amp-2021
read_by: agent
date: 2026-11-15
sections_read: ["Abstract", "1 Introduction", "2.1-2.2", "3 B-tree write amplification model (opening)", "Evaluation results text for the baseline comparison (skimmed)"]
---

# Notes: Closing the B-tree vs. LSM-tree Write Amplification Gap (Qiao et al., arXiv 2021)

> Notes are in English and in your own words. Preprint v1; design sections (page shadowing, localized modification logging, sparse redo logging) were skimmed, not studied.

## Key points

- (Abstract, 1) The common belief is that an LSM-tree beats a B-tree on space use and write amplification. The paper argues this changes on storage that compresses data transparently in hardware, because then a B-tree can write mostly-empty blocks without paying the physical space.
- (3) Definition used: write amplification is physical bytes written to the media divided by user bytes written. For a B-tree it is the sum of three parts: log writes (redo/undo), page writes (flushing dirty pages), and extra writes needed to make a page write atomic.
- (3) Atomicity detail: devices only guarantee atomic writes of a 4 KB block, so a larger B-tree page needs protection against torn writes. Updating in place needs a journal or a double-write step (about twice the write volume), while copy-on-write avoids that but needs mapping bookkeeping, which also adds writes.
- (2.1) Page compression in B-trees is limited because each compressed page must still occupy whole 4 KB blocks (a 16 KB page that compresses to 5 KB still uses 8 KB), and under random writes B-tree pages are typically only 50-80 percent full; the LSM tree is more compact on both counts.
- (1, evaluation) Baseline shows the usual gap: with the setup used, RocksDB (LSM) had about 4 times lower write amplification than WiredTiger (B-tree). With 128-byte records and random writes, the paper reports about 14 for RocksDB and 64 for WiredTiger at 8 KB pages, against 8 for their redesigned B-tree.
- (Evaluation, 500 GB data set, 15 GB cache, 32-byte records, 4 client threads) RocksDB about 38, WiredTiger 268 at 8 KB pages and larger at 16 KB, redesigned B-tree 28 at 8 KB. Plain B-tree write amplification grows roughly in proportion to page size divided by record size; LSM write amplification grows as the data set (number of levels) grows, while the B-tree's depends little on data set size.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| RocksDB WA about 38 vs WiredTiger 268 (8 KB pages), 32-byte records, 500 GB, 15 GB cache | Evaluation, results discussion | Authors' test on a compressing drive; not a general constant |
| Journaling in-place page updates costs about 2x write volume | 3 | Double-write buffer (MySQL) or full-page writes (PostgreSQL) are examples the paper names |
| B-tree pages typically 50-80 percent full under random writes | 2.1 | Cites standard B-tree theory |

## Relevant to concepts

- `write-amplification`: a clear decomposition (log, page, atomicity extras) and the page-size-over-record-size intuition for B-trees.
- `lsm-vs-btree`: shows the conventional gap and why it depends on hardware and workload.

## Warnings

- Preprint, with placeholder DOI and artifact text in the PDF; the arXiv abstract page lists CC BY 4.0 while the PDF states CC BY-NC-ND 4.0 (strictest recorded in the registry).
- The headline result depends on drives with built-in transparent compression, and the authors work for a company selling such drives. Treat it as a design argument, not evidence that B-trees match LSM trees on ordinary SSDs.
- The baseline numbers use small records and data sets much larger than the cache, which are the settings where the B-tree's whole-page rewrite hurts most; other workloads may show a smaller gap (not tested in the parts read).
- Use `myrocks-vldb20` for a production comparison and `oneil-lsm-tree` for the original motivation.
