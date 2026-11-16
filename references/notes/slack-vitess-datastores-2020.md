---
source: slack-vitess-datastores-2020
read_by: agent
date: 2026-11-16
sections_read: ["whole article as returned by the fetch tool (summary)"]
---

# Notes: Scaling Datastores at Slack with Vitess (2020)

> Notes are in English and in your own words. Read through a fetch tool that summarizes; verify details at verification time.

## Key points

- (Problem) Data was sharded by workspace ID on MySQL pairs. Very large customers outgrew the biggest machine, hot shards left much of the fleet idle, one shard outage hit every workspace on it, and application code assumed the physical layout.
- (Choice) Slack chose Vitess over adding more sharding logic in the app, and stated a goal of sharding message data by channel instead of workspace so one large customer's load spreads across shards (the page does not confirm this as the final production key).
- (Migration) Migration began in 2017 with backfill, double writes and double-read comparison; at publication Vitess served about 99% of query load.
- (Scale) Peak about 2.3M queries per second (about 2M reads, 300K writes), median 2 ms, p99 11 ms. Query rates rose 50% in one week in March 2020, and splitting a busy keyspace was the tool they relied on to scale.
- (Gap in the article) Little detail about cross-shard queries or how keys were chosen.

## Relevant to concepts

- `partitioning-sharding`: a bad shard key (tenant ID with uneven tenants) causes hot partitions; changing the key is painful.

## Warnings

- Marketing-leaning tone for Vitess; numbers are from 2020.
