---
source: qiao-btree-lsm-write-amp-2021
read_by: agent
date: 2026-11-16
sections_read: ["Abstract", "1 Introduction", "2.1-2.3 (background and motivating comparison, Table 1, Figures 3-4)"]
---

# Notes: Closing the B-tree vs. LSM-tree Write Amplification Gap (arXiv v1, 2021)

> Notes are in English and in your own words. Read from PDF text; sections after the motivating comparison (design of the three B-tree techniques and their evaluation) were not read in detail.

## Key points

- (Abstract, Sec. 1) The common belief is that an LSM-tree beats a B-tree on space efficiency and write amplification. The paper argues this changes when the drive compresses data transparently in hardware, because the B-tree can then leave pages sparse without paying for the empty space physically.
- (Sec. 1) Write amplification here is measured at the flash media (after in-drive compression), not at the logical block interface.
- (Sec. 1) Three B-tree techniques are proposed: deterministic page shadowing (atomic page updates without double writes), localized page modification logging (log only the changed part of a page), and sparse redo logging (avoid rewriting partly filled log blocks).
- (Sec. 2.3, Table 1, Fig. 4) Baseline on the same drive: RocksDB (LSM) uses less logical space than WiredTiger (B-tree) but after compression WiredTiger uses less physical space; RocksDB has about 4 times lower write amplification than WiredTiger across client thread counts.
- (Sec. 1) Headline result: with random 128-byte record writes, write amplification is about 14 for RocksDB, 64 for WiredTiger (8 KB pages) and 8 for their modified B-tree; reported throughput of 85K, 71K and 28K TPS respectively.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| RocksDB 14, WiredTiger 64, modified B-tree 8 write amplification | Sec. 1 | 128 B random writes, 8 KB page, one commercial compressing drive |
| RocksDB about 4x less write amplification than WiredTiger | Sec. 2.3, Fig. 4 | Baseline before the new techniques |
| Logical 218 GB vs 280 GB; physical 129 GB vs 104 GB (RocksDB vs WiredTiger) | Table 1 | Shows space-amplification ranking flips after compression |

## Relevant to concepts

- `index-structures`: measured evidence for the B-tree vs LSM write-amplification trade-off, plus a caveat that the gap depends on the storage hardware.

## Warnings

- Preprint with placeholders (PVLDB 14(1) 2020, no DOI); final version not found. License conflict (arXiv link says CC BY 4.0, PDF says CC BY-NC-ND 4.0).
- Hardware-specific; do not claim "B-trees have equal write amplification as LSM" in general. For the general worst-case model use tikv-docs-btree-vs-lsm; for the original idea oneil-lsm-tree.
