---
source: debezium-outbox-pattern-2019
read_by: agent
date: 2026-11-12
sections_read: ["The Issue of Dual Writes", "The Outbox Pattern", "An Implementation Based on Change Data Capture", "The Outbox Table", "Duplicate Detection in the Consuming Service", "Summary"]
---

# Notes: Reliable Microservices Data Exchange With the Outbox Pattern (Debezium, 2019)

> Notes are in English and in your own words. Section names as reported by the fetch tool.

## Key points

- (The Issue of Dual Writes) Writing to the database and publishing to a broker are two separate systems with no shared transaction, so one can succeed and the other fail, leaving them inconsistent.
- (The Outbox Pattern) Store the event in an outbox table in the same local transaction as the business change; a separate process forwards it to the broker. The service itself sees its own writes immediately; other services see them eventually.
- (CDC implementation) Instead of polling, read the database transaction log and publish inserts from the outbox table. Low overhead, near-real-time. The example inserts then deletes the row, so the table stays small while the log keeps the record.
- (CDC implementation) The aggregate ID is used as the message key so that events for one entity stay ordered within a partition.
- (The Outbox Table) Columns: event id, aggregate type, aggregate id, event type, JSON payload. The event schema is part of the service's public API.
- (Duplicate Detection) Delivery is at-least-once. Each event has a unique ID; the consumer records processed IDs in its own database within the same transaction as its work and skips repeats.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published 2019-02-19, author Gunnar Morling | page header | Site content CC BY 3.0 per page |

## Relevant to concepts

- `outbox-pattern`: dual-write problem, transactional outbox, CDC relay.
- `idempotent-consumer`: dedup table in the same transaction.
- `ladder trigger`: needed once one action must change your database and also notify another system reliably.

## Warnings

- Debezium and Kafka specific; the idea also works with a polling relay (see microservices-io-transactional-outbox).
- Written in 2019; tool versions have moved on (see debezium-docs-outbox-event-router).
