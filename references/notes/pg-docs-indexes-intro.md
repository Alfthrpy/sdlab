---
source: pg-docs-indexes-intro
read_by: agent
date: 2026-11-12
sections_read: ["11.1 Introduction"]
---

# Notes: PostgreSQL 18 Documentation, 11.1. Indexes: Introduction

> Notes are in English and in your own words.

## Key points

- (11.1) Without an index, a lookup by value reads every row; an index lets the database reach the matching rows by following a small search structure.
- (11.1) After creation the database maintains the index itself and decides per query whether using it is cheaper than a full scan.
- (11.1) Running ANALYZE regularly keeps the planner's statistics useful for that decision.
- (11.1) Indexes can also help UPDATE and DELETE with conditions, and joins on indexed columns.
- (11.1) A condition benefits only if it has the shape "indexed column, operator the index supports, a value that does not change during the query".
- (11.1) Building an index normally blocks writes to the table (reads still work). A concurrent build avoids that at some cost.
- (11.1) Every index slows writes and takes space; unused indexes should be removed.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Normal CREATE INDEX blocks writes, allows reads | 11.1 | Relevant to "adding an index on a live app" |

## Relevant to concepts

- `indexes-basics`: what an index is, when it is used, and what it costs.
- `query-plans-and-explain`: pairs with pg-docs-using-explain.

## Warnings

- Intro page only; index types and multicolumn rules are in later sections of chapter 11 that were not read.
- PostgreSQL-specific wording (HOT updates etc.); MySQL has its own behavior (see mysql-84-optimization-indexes).
