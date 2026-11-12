---
source: pg-docs-using-explain
read_by: agent
date: 2026-11-12
sections_read: ["14.1.1 EXPLAIN Basics", "14.1.2 EXPLAIN ANALYZE", "14.1.3 Caveats"]
---

# Notes: PostgreSQL 18 Documentation, 14.1. Using EXPLAIN

> Notes are in English and in your own words.

## Key points

- (14.1.1) A plan is a tree. Leaves read tables (sequential, index, or bitmap scan); upper nodes join, sort, or aggregate.
- (14.1.1) Each node shows an estimated startup cost, total cost, row count and row width. Costs are in arbitrary planner units, not milliseconds, and a parent's cost includes its children.
- (14.1.1) The planner picks between a full scan and an index scan based on how selective the condition is; a bitmap scan sits in between.
- (14.1.1) The `enable_*` settings let you discourage a plan type to compare alternatives; they do not forbid it.
- (14.1.2) EXPLAIN ANALYZE runs the query and adds real row counts and times. Comparing estimated and actual rows is the quickest way to spot bad statistics. Times are per loop, so multiply by the loop count.
- (14.1.2) The BUFFERS output shows how many blocks came from cache vs. disk.
- (14.1.2) Because ANALYZE really executes the statement, wrap INSERT/UPDATE/DELETE tests in a transaction that you roll back.
- (14.1.3) Tiny tables give misleading plans: a sequential scan can win simply because the table is one page.
- (14.1.3) Timing overhead and omitted network time mean the measured time is not exactly what a client sees.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| EXPLAIN ANALYZE executes the statement | 14.1.2 | Warn learners before they run it on writes |
| Estimated cost units are arbitrary | 14.1.1 | Do not present them as ms |

## Relevant to concepts

- `query-plans-and-explain`: reading a plan and noticing seq scan vs. index scan.
- `indexes-basics`: shows when an index is and is not used.

## Warnings

- Example output in the page comes from a development build and a particular sample schema; numbers will differ on a learner's machine.
- The page goes deep into joins and subplans; Unit 0 should use only scans, sort, and estimated-vs-actual.
