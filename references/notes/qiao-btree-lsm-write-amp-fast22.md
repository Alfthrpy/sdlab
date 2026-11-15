---
source: qiao-btree-lsm-write-amp-fast22
read_by: agent
date: 2026-11-15
sections_read: ["Abstract", "1 Introduction", "2.1-2.4", "4 Evaluation (results text for the baseline comparison, skimmed)"]
---

# Notes: Closing the B+-tree vs. LSM-tree Write Amplification Gap (Qiao et al., FAST '22)

> Notes are in English and in your own words. Peer-reviewed FAST '22 version (it supersedes the arXiv preprint v1). The design sections (3: page shadowing, localized modification logging, sparse redo logging) were skimmed, not studied.

## Key points

- (Abstract, 1) The common belief is that an LSM-tree beats a B+-tree on space use and write amplification. The paper argues this changes on storage that compresses data transparently in hardware, because then a B+-tree can write mostly-empty blocks without paying the physical space.
- (2.4) Definition used: write amplification is physical bytes written to the media divided by user bytes written. For a B+-tree it is the sum of three parts: log writes (redo/undo), page writes (flushing dirty pages), and extra writes needed to make a page write atomic.
- (2.4) Atomicity detail: devices only guarantee atomic writes of a 4 KB block, so a larger B+-tree page needs protection against torn writes. Updating in place needs a journal or a double-write step (about twice the write volume), while copy-on-write avoids that but needs mapping bookkeeping, which also adds writes.
- (2.1, 2.3) Page compression in B+-trees is limited because each compressed page must still occupy whole 4 KB blocks (a 16 KB page that compresses to 5 KB still uses 8 KB), and under random writes B+-tree pages are typically only 50-80 percent full; the LSM tree is more compact on both counts.
- (1, 4) Baseline shows the usual gap: with the setup used, RocksDB (LSM) had roughly 4 to 7 times lower write amplification than WiredTiger (B+-tree) at 8 KB pages, depending on the workload. With 128-byte records and random writes, the paper reports 14 for RocksDB and 64 for WiredTiger at 8 KB pages, against 8 for their redesigned B+-tree.
- (4) With a 500 GB data set, 15 GB cache and 32-byte records, RocksDB is 38, WiredTiger 268 at 8 KB pages and 530 at 16 KB, and the redesigned tree 28 at 8 KB and 36 at 16 KB. Plain B+-tree write amplification grows roughly in proportion to page size divided by record size; LSM write amplification grows as the data set (number of levels) grows, while the B+-tree's depends little on data set size.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| RocksDB WA 38 vs WiredTiger 268 (8 KB pages) and 530 (16 KB), 32-byte records, 500 GB, 15 GB cache | 4, results discussion | Authors' test on a compressing drive; not a general constant |
| RocksDB 14, WiredTiger 64, redesigned B+-tree 8 at 128-byte records, random writes, 8 KB pages | 1 | Same caveat |
| Journaling in-place page updates costs about 2x write volume | 2.4 | Double-write buffer (MySQL) is the example the paper names |
| B+-tree pages typically 50-80 percent full under random writes | 1, 2.1 | Cites standard B-tree theory |

## Relevant to concepts

- `write-amplification`: a clear decomposition (log, page, atomicity extras) and the page-size-over-record-size intuition for B+-trees.
- `lsm-vs-btree`: shows the conventional gap and why it depends on hardware and workload.

## Warnings

- The USENIX page and PDF state no license (only that USENIX papers are open access), so the registry records all-rights-reserved and rewrite-only. The earlier arXiv preprint had conflicting license text; do not cite it.
- The headline result depends on drives with built-in transparent compression, and the authors include staff of a company selling such drives. Treat it as a design argument, not evidence that B+-trees match LSM trees on ordinary SSDs.
- The baseline numbers use small records and data sets much larger than the cache, which are the settings where the B+-tree's whole-page rewrite hurts most; other workloads may show a smaller gap (not tested in the parts read).
- Use `myrocks-vldb20` for a production comparison and `oneil-lsm-tree` for the original motivation.
