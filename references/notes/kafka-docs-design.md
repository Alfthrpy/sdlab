---
source: kafka-docs-design
read_by: agent
date: 2026-11-12
sections_read: ["Message Delivery Semantics", "Using Transactions", "Consumer Position", "Push vs Pull", "Consumer Groups", "Log Compaction", "Retention"]
---

# Notes: Design (Apache Kafka documentation, 4.4.X)

> Notes are in English and in your own words. The fetch tool summarized the page, so section names are as reported; re-read exact wording before quoting.

## Key points

- (Message Delivery Semantics) Three levels: at-most-once (may lose, never repeats), at-least-once (never loses, may repeat), exactly-once (each message effectively handled once). Kafka's default behavior is at-least-once.
- (Message Delivery Semantics) An idempotent producer (since 0.11) lets the broker drop duplicate retries using producer ID plus sequence number, so a producer retry does not duplicate a record in a partition.
- (Using Transactions) A producer can write to several partitions atomically; read-committed consumers see only committed data. Consumer offsets can be committed in the same transaction as the output, so output and progress succeed or fail together. This needs auto-commit off.
- (Consumer Position) Each partition is read by one consumer in a group at a time, so progress is one number (offset) per partition. This makes acknowledgement state tiny, and allows rewinding to re-read after a bug fix.
- (Push vs Pull) Consumers pull; therefore a slow consumer simply reads less often and is not flooded. Long polling avoids busy waiting. This is the pull-based form of backpressure.
- (Consumer Groups) Partitions of a topic are split among group members; static membership avoids rebalances on routine restarts.
- (Log Compaction) Compaction keeps at least the newest record per key; a null value is a delete marker (tombstone); offsets and order are preserved. Enabled with cleanup.policy=compact.
- (Retention) Reading does not delete data; data is kept for a time or size limit, which is cheap because disk access is sequential.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Idempotent producer exists since Kafka 0.11.0.0 | Message Delivery Semantics | Version history; docs are 4.4.X |
| Static membership needs Kafka 2.3 or later | Consumer Groups | |

## Relevant to concepts

- `delivery-semantics`: the three levels and how Kafka reaches exactly-once within its own boundary.
- `log-abstraction`: offsets, retention, compaction, consumer groups.
- `backpressure`: pull model and consumer pace.
- `ladder trigger` (queue to log): a queue deletes on ack; a log keeps data so many independent readers and replays become possible.

## Warnings

- Exactly-once here covers read-process-write inside Kafka only; external side effects are not covered (see confluent-exactly-once-2017).
- Config names and defaults change between releases; the page is version-pinned to 4.4.X.
