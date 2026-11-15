---
source: myrocks-vldb20
read_by: agent
date: 2026-11-15
sections_read: ["Abstract", "1 Introduction", "2.1 UDB Architecture", "2.2 UDB Storage", "2.4 RocksDB: Optimized for Flash", "4 Production migration (opening, skimmed)", "5.1 MyRocks vs InnoDB efficiency in UDB"]
---

# Notes: MyRocks: LSM-Tree Database Storage Engine Serving Facebook's Social Graph (VLDB 2020)

> Notes are in English and in your own words. Read from the PDF text extraction. Sections 3 (performance work), 4 (testing and migration tooling), 5.2 and 6 (lessons) were not read in depth.

## Key points

- (1) Facebook's main user database (UDB) ran MySQL with InnoDB, a B+tree engine. The two bottlenecks they wanted to fix on flash storage were space use and write amplification; moving to flash had moved the bottleneck from IOPS to capacity.
- (2.1) UDB is a very widely sharded MySQL fleet, with one database copy per region, asynchronous replication across regions, and a small log-keeping tier that receives each instance's binary log by semi-synchronous replication inside a region (a way to keep short commit latency without three full copies). A cache tier (TAO) takes most reads.
- (2.2) Why InnoDB hurt: a small change to a row still rewrites a whole 8 KB page when it is flushed, and InnoDB's double-write buffer (protection against torn pages) writes it twice; the cache tier meant the working set was not in DRAM, so dirty pages were flushed often and bursts stalled flash writes. Index fragmentation wasted about 25-30 percent of each block, and compression was limited because pages had to be updatable in place.
- (2.4.2) Why an LSM tree fits: updates are batched in memory and written sequentially, pages written out contain mostly new data, and the bulk of data sits compacted in the last level; dead data stays low through compaction tuning (they cite about 10 percent). Per-row transaction metadata also shrinks because sequence numbers are zeroed during compaction.
- (1, 2.2) Costs they list for the LSM engine: slower range queries, higher CPU for key comparisons, bloom filters that need memory, deletes handled by markers (tombstones) that can slow rows updated and deleted often, and compactions that can stall under burst writes.
- (2.1, 4) Migration was done by adding MyRocks replicas to existing replica sets (replication is independent of the storage engine), validating with replayed production queries and full data comparison, then promoting a MyRocks primary; migration finished August 2017. Bulk loading skipped compaction work to speed data copy.
- (5.1) Results for the same data: instances 62.3 percent smaller than compressed InnoDB (37.7 percent of the size), bytes written to flash down 75 percent, CPU time slightly lower (about 40 percent lower for replication-only write load, mostly because secondary index maintenance needs no random reads). The authors admit part of the CPU gain came from compression choice and a binary tuned for MyRocks, and that InnoDB could have come close with the same options.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Instance size 62.3 percent smaller than compressed InnoDB; bytes written to flash down 75 percent | 1, 5.1 | Facebook UDB, random-write heavy workload behind a cache tier |
| InnoDB block space wasted by fragmentation about 25-30 percent | 2.2 | |
| InnoDB rewrites a full 8 KB page for a one-row change; plus double-write | 2.2 | Default page size in the paper's setup is 16 KB, tables mostly use 8 KB compressed blocks |
| UDB migration from InnoDB to MyRocks completed August 2017 | 1, 4 | |

## Relevant to concepts

- `lsm-vs-btree` (Unit 3 storage engines): production evidence for when write amplification and space, not reads, are the bottleneck.
- `write-amplification`: concrete mechanisms (page rewrite, double-write, fragmentation) on the B-tree side.
- `storage-engine-migration`: replica-by-replica engine swap with shadow traffic and data comparison.

## Warnings

- One company, one workload (social graph, flash, TAO cache in front, very write-heavy randomness). The gains do not transfer to read-heavy or range-scan-heavy workloads; the authors say as much about range queries.
- "Write amplification" here is a mix of measured flash bytes and design reasoning; the paper reports a bytes-written drop, not a clean WA ratio for each engine.
- The license is CC BY-NC-ND: paraphrase only, no adapted text.
