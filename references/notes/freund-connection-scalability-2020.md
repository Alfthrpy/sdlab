---
source: freund-connection-scalability-2020
read_by: agent
date: 2026-11-17
sections_read: ["Why connection scalability in Postgres is important", "Memory usage: Constant connection overhead", "Snapshot scalability", "Connection model & context switches"]
---

# Notes: Analyzing the Limits of Connection Scalability in Postgres (Andres Freund)

> Notes are in English and in your own words. Read via WebFetch and from the raw HTML text (`curl`) on 2026-11-17, whole page. Written by Andres Freund (Postgres committer), October 8, 2020, on the Citus Data blog (originally on the Azure Database for PostgreSQL blog). Footer: "(c) 2026 Citus Data, a Microsoft Company. All rights reserved."

## Key points

- (Why connection scalability is important) One sentence names the cost of establishing a new database connection as TLS, latency and Postgres costs, in that order. This is why apps keep pools of connections big enough to absorb small spikes. No numbers are given for it.
- (same section) Connections are often idle most of the time because of network latency and app processing time. In a pgbench test with 1 ms network delay and 1 ms processing delay, throughput peaked near 3000 connections versus about 48 without delays; a real 10GbE link moved the peak to about 500.
- (Constant connection overhead) Postgres uses a process per connection: the supervisor process creates a dedicated process for each new connection. Memory per connection is hard to measure; with huge_pages the author found it below 2 MiB in many workloads.
- (Snapshot scalability) Many established connections, even idle, slow down active ones in the versions tested (PG 12): one active connection ran at 33,457 TPS with 0 idle and 14,496 with 10,000 idle (table in footnote).
- (Connection model) Process-per-connection costs context switches; a thread model would not fix that by itself.
- (Pooling remark) Poolers such as PgBouncer reduce server connections only in transaction or statement mode, which loses features like prepared statements and temp tables.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Cost order of a new connection: TLS, latency, Postgres | Why connection scalability is important | One sentence; no measurements |
| Memory overhead below 2 MiB per connection with huge_pages | Constant connection overhead | Workstation test, version 13-era; contrasts with older 5 MB figure |
| 1 active connection: 33,457 TPS at 0 idle, 14,496 TPS at 10,000 idle (PG 12) | footnote 7 table | Fixed in PG 14 per the author's follow-up (not read) |

## Relevant to concepts

- `connection-pooling` objective 1: PARTLY. Names the three cost components of opening a connection and confirms the process-per-connection model, but gives no timings. Good for the order TLS then network latency then server cost.
- `connection-pooling` objective 2: weak (pools must absorb small spikes; many idle connections still cost).
- `single-machine-limits`: connection count as a bottleneck.

## Warnings

- 2020, PG 12/13-era numbers; PG 14 improved snapshot scalability. Do not present TPS figures as current.
- All-rights-reserved (no open license); rewrite only.
- Written by a Microsoft-employed committer about Postgres; vendor-neutral in tone but not a neutral standards document.
