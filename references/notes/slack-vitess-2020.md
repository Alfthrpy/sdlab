---
source: slack-vitess-2020
read_by: agent
date: 2026-11-15
sections_read: ["Whole article (raw HTML converted to text)"]
---

# Notes: Scaling Datastores at Slack with Vitess (2020)

> Notes are in English and in your own words.

## Key points

- (The beginning) Slack stored data in MySQL shards keyed by workspace id: each shard held thousands of workspaces, a separate metadata cluster mapped workspace id to shard, and a "kitchen sink" cluster held data not tied to a workspace. The application (the monolith) did all the routing itself.
- (The beginning, Advantages) Each shard was a pair of MySQL hosts in different data centers replicating to each other asynchronously, and either host could take reads and writes (a multi-primary pair). Benefit named: a failed host could be retried on its partner with no visible customer impact. Other benefits: simple mental model (one workspace, one database), easy debugging, easy to add shards for new customers.
- (Disadvantages) The trigger list, each item a reason to leave the scheme: the largest customers reached the biggest available host; hot shards next to underused ones, with over-provisioning because moving workspaces was hard; a shard outage took down every workspace on it; new products (Enterprise Grid, Slack Connect) broke the one-workspace-per-shard assumption; and the multi-primary setup was non-standard, needing custom tools, with no usable replicas to read from.
- (What to do?) The team weighed evolving the in-application sharding against replacing it. They wanted to keep MySQL and relational behaviour, which ruled out moving to a NoSQL or NewSQL store. Building a new shard key into the application was prototyped but found tangled with how data was stored, and would not have fixed operations.
- (What to do?, Why Vitess?) Stated goal (not confirmed as done in the article): shard message data by channel id instead of workspace id, so one very large customer is spread over many shards. Vitess supplies sharding, failover, backups and topology tracking underneath MySQL.
- (Why Vitess?) Migration style: start with one small feature end to end, build backfill plus application double-writes plus double-reads that diff the old and new results, then move table by table (the post says moving whole shards came later). Slack also fixed gaps in Vitess upstream.
- (Has Vitess been a success?) By publication about 99 percent of query load ran on Vitess; keyspaces scale on different dimensions (users, teams, channels). In March 2020 query rates rose about 50 percent in a week and a busy keyspace was split horizontally with Vitess's resharding workflow.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 2.3M queries per second at peak (2M reads, 300K writes), median 2 ms, p99 11 ms | Intro | Slack, December 2020 |
| Migration started 2017, about 99 percent of load on Vitess three years in | Intro, Why Vitess? | |
| Query rates up about 50 percent in one week in March 2020 | Has Vitess been a success? | Resharded one busy keyspace |

## Relevant to concepts

- `sharding`: a second real shard-key story (tenant key to a finer key) and why tenant-per-shard breaks for very large tenants.
- `hot-partitions`: concrete hot-spot symptoms from a tenant-based key.
- `multi-leader-replication`: the original active-active pair per shard, with its operational downsides (use as a small production example, not as a design guide; the post does not discuss conflict handling).
- `migration`: backfill, double-write, double-read diff.

## Warnings

- A success story from the team that made the choice; the Disadvantages section of the old design is the most useful part, the Vitess section is mostly advocacy.
- The post does not explain how write conflicts were handled in the original multi-primary pairs, and says nothing on cross-shard transactions.
- Numbers are 2020 and Slack-specific.
