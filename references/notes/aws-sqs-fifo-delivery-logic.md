---
source: aws-sqs-fifo-delivery-logic
read_by: agent
date: 2026-11-15
sections_read: ["Sending messages", "Receiving messages", "Retrying multiple times", "Additional notes on FIFO behavior", "Examples for better understanding"]
---

# Notes: FIFO queue delivery logic in Amazon SQS

> Notes are in English and in your own words. Related pages opened the same day: sqs-fifo-queues.html (overview), using-messagegroupid-property.html, interleaving-multiple-ordered-message-groups.html, avoid-backlog-with-the-same-message-group-id.html, standard-queues.html.

## Key points

- (Sending messages, Message group ID) Order in a FIFO queue is defined per message group ID. Every message must carry one; sending without it fails. Several producers using the same group ID are ordered by arrival at the queue; to keep strict order per producer, give each producer its own group ID.
- (Sending messages, Per-group ordering) Within a group everything is sent and received in strict order. Between groups there is no order guarantee, groups may overtake each other.
- (Receiving messages) One receive call can return up to 10 messages, preferably from the same group, still in order. After a group's messages have been received, no more messages of that group are returned until they are deleted or become visible again after the visibility timeout. Consumers cannot ask for a specific group.
- (Additional notes) Parallelism comes from having many groups: different consumers work on different groups at the same time. One group ID for the whole queue gives total order but no parallelism (one message in flight at a time).
- (Retrying multiple times) Producer retries with the same deduplication ID do not create duplicates or break order, as long as one attempt was acknowledged within the deduplication interval. Receive retries with the same attempt ID also keep order.
- (Interleaving page) While a message of a group is invisible (being processed), nobody else gets that group's later messages; this is why one stuck message holds back its whole group.
- (Backlog page) FIFO queues look at roughly the first 120,000 messages to find available groups, so a large backlog in one group can delay groups whose messages were sent later; a dead-letter queue after repeated failures is the suggested relief.
- (standard-queues page) Standard queues only try to keep the send order and may deliver out of order and more than once.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Up to 10 messages per receive call | Receiving messages | MaxNumberOfMessages |
| About 120,000 in-flight messages limit, and the scan of the first 120,000 messages | Backlog page | Quotas change; recheck |
| Deduplication interval is 5 minutes | referenced in other SQS pages, not read on this page | Do not cite from this page |

## Relevant to concepts

- `event-log-streaming`: contrast of per-partition ordering (Kafka) with per-group ordering (SQS FIFO); both give order inside a key and none across keys.
- `message-queue`: ordering costs parallelism; head-of-line blocking per group.
- `delivery-semantics`: deduplication ID as the producer-side idempotency tool.

## Warnings

- No date and no license text in the fetched content; treated as all-rights-reserved.
- The page defines ordering for SQS only; it does not discuss ordering with a dead-letter queue (aws-sqs-dead-letter-queues advises against DLQs on FIFO queues when order matters).
- High-throughput FIFO mode and throughput quotas were not read.
