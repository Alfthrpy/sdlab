---
source: rabbitmq-docs-maxlength
read_by: agent
date: 2026-11-15
sections_read: ["Overview", "Default Max Queue Length Limit Behaviour", "Queue Overflow Behaviour", "Define Max Queue Length Using a Policy", "Define Max Queue Length Using x-arguments During Declaration", "Inspecting Queue Length Limits"]
---

# Notes: Queue Length Limit (RabbitMQ docs, 4.4)

> Notes are in English and in your own words. The fetch tool summarized the page, so details of wording should be rechecked before any quote.

## Key points

- (Overview) A queue can be bounded by number of messages, by total size of message bodies in bytes, or by both; whichever limit is hit first applies. Only bodies count, not headers or overhead.
- (Overview, policy and x-arguments sections) Limits are set by policy (recommended) or when the queue is declared; if both are present the lower value wins. Operators can also set them through operator policies.
- (Default behaviour) Only ready messages count in classic queues. Messages already delivered to a consumer but not yet acknowledged do not count, so a bound does not limit unacknowledged work. Quorum queues also count delayed messages and messages waiting for dead-lettering, so they hit the bound sooner.
- (Queue Overflow Behaviour) Three choices when full: drop-head (default; discards or dead-letters the oldest messages), reject-publish (refuses the newest incoming messages), reject-publish-dlx (refuses and dead-letters them).
- (Queue Overflow Behaviour) With publisher confirms on, a refused message makes the broker send the publisher a negative acknowledgement. So reject-publish is the mechanism that turns a full queue into a signal the producer can see (backpressure); drop-head instead sheds the oldest work silently (load shedding of stale data).
- (Queue Overflow Behaviour) If one message is routed to several queues and one is full, the publisher still gets the negative ack, but queues with room still keep the message.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default overflow behaviour is drop-head | Default behaviour / Overflow | Oldest message goes first |
| Three overflow values: drop-head, reject-publish, reject-publish-dlx | Queue Overflow Behaviour | |

## Relevant to concepts

- `backpressure-consumer-lag`: a bounded queue, and the choice between telling the producer to stop (reject-publish) and dropping old messages (drop-head).
- `message-queue`: bound size plus dead-letter exchange as a safety net.
- `load-shedding` (Unit 1/6): drop-head as a form of shedding stale work.

## Warnings

- Vendor-specific behaviour (RabbitMQ). Kafka and SQS do not bound queues this way: Kafka bounds by retention and consumers pull, SQS standard queues have no hard backlog limit (see aws-sqs-cloudwatch-metrics).
- The page describes the broker only; it says nothing about what the producer service should do after a negative ack (retry with backoff, shed, or fail the user request).
- Copyright Broadcom, no open license; rewrite only.
