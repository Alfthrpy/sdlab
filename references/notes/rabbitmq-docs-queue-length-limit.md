---
source: rabbitmq-docs-queue-length-limit
read_by: agent
date: 2026-11-16
sections_read: ["Overview", "Queue Overflow Behaviour", "Define Max Queue Length Using a Policy"]
---

# Notes: Queue Length Limit (RabbitMQ 4.4 docs)

> Notes are in English and in your own words. The fetch tool summarized this page; re-read before relying on option names.

## Key points

- (Overview) A queue can be capped by count, by bytes, or both; policy is the recommended way, and the smaller value wins if both policy and declaration set one.
- (Overview) Unacknowledged messages do not count for classic queues, so the cap bounds the waiting backlog, not work in progress.
- (Queue Overflow Behaviour) Default on overflow: drop the oldest messages (or dead-letter them). That means a full queue silently loses old work.
- (Queue Overflow Behaviour) The alternative, reject-publish, refuses the new message; with publisher confirms the producer gets a nack and can slow down, retry later, or shed. This is the "bounded queue pushes back on the producer" pattern.
- (Queue Overflow Behaviour) With a message routed to several queues, one rejecting queue nacks the publisher while the others still keep it.

## Relevant to concepts

- `backpressure-consumer-lag`: bounded queue plus rejection signal as a concrete backpressure mechanism; contrast with load shedding.
- `message-queue`: dead-lettering of overflow.

## Warnings

- Vendor-specific; the default (drop-head) is the opposite of what many learners expect from a "bound".
- No date on the page; version 4.4 per the version selector.
