---
source: kreps-the-log-2013
read_by: agent
date: 2026-11-15
sections_read: ["Part One (What Is a Log?, Logs in databases, Logs in distributed systems, Changelog 101)", "Part Two (Log-structured data flow, Building a Scalable Log)", "Part Three (Data flow graphs, Stateful Real-Time Processing, Log Compaction)", "Part Four (The place of the log in system architecture)"]
---

# Notes: The Log: What every software engineer should know about real-time data's unifying abstraction (Kreps, 2013)

> Notes are in English and in your own words. Read as text converted from the page HTML; section names are the page's own headings.

## Key points

- (Part One, What Is a Log?) A log is an append-only sequence of records in time order; each entry gets a sequential number, and that number works as a timestamp that does not depend on any physical clock. It is closer to a table or file sorted by time than to application text logging.
- (Part One, Logs in databases) Databases first used the log to keep tables and indexes consistent after crashes, then to ship changes to replicas. The same abstraction can feed other subscribers, not just replicas.
- (Part One, Logs in distributed systems) State machine replication: deterministic processes that start equal and see the same inputs in the same order end equal. So the hard part of keeping replicas in sync reduces to producing one agreed ordered log. A replica's progress can be described by one number, the last log position it applied. Contrast of active-active (log the requests) and primary-backup (log the leader's results) is shown with an add/multiply example where order changes the outcome.
- (Part One, Changelog 101) Tables and change logs are two views of one thing: replay the log to get the table; record table updates to get a changelog.
- (Part Two, Log-structured data flow) A central log lets each downstream system (cache, search, warehouse) consume at its own pace; the log is a buffer that decouples producers from consumers, so a subscriber can be down and catch up later. This cuts the number of point-to-point pipelines.
- (Part Two, Building a Scalable Log) To scale, the log is cut into partitions. Each partition is totally ordered, but there is no global order across partitions. The writer chooses the partition, usually by key such as user id. The author calls the missing global order a limitation that mattered little in practice, because many independent processes write anyway. Guarantee stated: appends from one sender to one partition arrive in the order sent. Partitions are replicated with one leader each. Other scaling tricks: batching and avoiding copies.
- (Part Three, Data flow graphs) Between processing stages the log acts as a large buffer: if a producer is faster than the consumer the stage must block, buffer or drop, and blocking can stall the whole graph, so a persistent log lets the slow stage lag without hurting the fast one.
- (Part Three, Log Compaction) Keeping everything forever costs space and makes replay slower. Two cleanup modes: for event data keep a window by time or size (usually a few days); for keyed data compaction removes records that have a newer record with the same key, so the log still rebuilds the latest state of every key but not every past state.
- (Part Four, place of the log) A system can be split into a log (ordering, replication, restore) and serving nodes (indexes, queries); a restoring node can replay the log, or load a snapshot and replay the tail.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| LinkedIn wrote over 60 billion unique messages a day through Kafka (several hundred billion counting cross-data-center mirroring) | Part Two, Building a Scalable Log | 2013 figure |
| Published December 16, 2013 | page header | |

## Relevant to concepts

- `event-log-streaming`: what a log is, partition ordering guarantee and its limit (no global order), retention window versus compaction, replay.
- `backpressure-consumer-lag`: the log as buffer that lets consumers run at their own pace (Part Two, Part Three).
- `delivery-semantics`: only indirectly (ordering); the essay does not discuss delivery guarantees.

## Warnings

- 2013 essay by the Kafka creator: it is an argument for the log abstraction, not current Kafka documentation. Check kafka-docs-design for current behaviour and config names.
- The URL on engineering.linkedin.com returns 404; use the www.linkedin.com/blog/engineering path recorded in the registry.
- No license stated on the page (footer is LinkedIn copyright), so rewrite only and keep quotes to one short sentence.
