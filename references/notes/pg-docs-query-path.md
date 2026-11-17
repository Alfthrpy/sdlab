---
source: pg-docs-query-path
read_by: agent
date: 2026-11-17
sections_read: ["51.1. The Path of a Query (whole page)"]
---

# Notes: PostgreSQL 18 Documentation, 51.1. The Path of a Query

> Notes are in English and in your own words. The page is one short section (about 400 words) of Chapter 51, "Overview of PostgreSQL Internals". Read via WebFetch and checked against the raw HTML (curl); footer "Copyright (c) 1996-2026 The PostgreSQL Global Development Group"; the site banner at read time listed 18.7 as the current minor release. The page has no date.

## Key points

- (whole page) A query goes through a fixed sequence inside the database server, once an application has a connection to it: the application sends the query text and waits for results.
- (parser stage) The parser checks syntax and builds an internal tree of the query.
- (rewrite system) The tree is rewritten using rules stored in the system catalogs. Views are the main example: a query on a view becomes a query on the base tables behind it.
- (planner/optimizer) The planner enumerates the ways to get the same result (the page's example: scan the whole table, or use an index when one exists), estimates the cost of each, picks the cheapest, and turns it into a complete plan.
- (executor) The executor walks the plan and fetches rows, using the storage system to read tables, and does sorts, joins and filtering; it then hands the rows back.
- (whole page) The page does not give any timings. It gives the order of stages only.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Stages inside the DB: connection, parser, rewrite system, planner/optimizer, executor | 51.1 | Five items in the page's own order (connection first) |
| The planner chooses between a sequential scan and an index scan by estimated cost | 51.1 | Links the database stage to `indexes-query-basics` |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1: partly supported, and it fills the "database stage" box that the MDN and nginx sources leave empty. For a Unit 0 lesson the stage can be drawn as one box with a short list inside (parse, plan, execute, return rows).
- `request-lifecycle`, objective 2: no timing data; but it names where time can go inside the database stage (planning vs reading rows), useful as a hint when a scenario says "the query takes 400 ms".
- `indexes-query-basics` (unit 0): a one-sentence bridge to why EXPLAIN shows a plan.

## Warnings

- Internals overview for the server process, not for tuning. Nothing about network or connection cost, and nothing about the time share of each stage.
- PostgreSQL-specific (MySQL has similar stages but is not described here).
- This is the page for PostgreSQL 18 ("current" URL); it can change to a newer version without notice.
