---
source: tikv-docs-btree-vs-lsm
read_by: agent
date: 2026-11-16
sections_read: ["whole page as returned by the fetch tool (summary)"]
---

# Notes: TiKV docs, B-Tree vs LSM-Tree

> Notes are in English and in your own words. Read through a fetch tool that summarizes; check formulas against the page at verification.

## Key points

- (Metrics) Defines write amplification (bytes written to storage divided by bytes written to the database), read amplification (disk reads per query) and space amplification (bytes on disk divided by bytes in the database).
- (Trade-off) A structure can be good at only two of the three.
- (B+ tree) Worst-case write amplification is about the page size B, since one small change rewrites a whole page; read cost equals tree depth.
- (Level-based LSM) Levels grow by factor k; an item is rewritten about k/2 times per level, giving write amplification around k times the number of levels; reads must check each level, so reads cost more.
- (Conclusion) LSM writes better, B-tree reads better; TiKV chose LSM because caching can fix reads more easily than writes.

## Relevant to concepts

- `index-structures`: simple vocabulary and a formula-level comparison for the B-tree vs LSM-tree question.

## Warnings

- Worst-case analysis only, no measurements; the page does not analyze space amplification. Use qiao-btree-lsm-write-amp-2021 for measured values.
