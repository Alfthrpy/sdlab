---
source: aws-sqs-fifo-delivery-logic
read_by: agent
date: 2026-11-16
sections_read: ["Sending messages", "Receiving messages", "Retrying multiple times", "Additional notes on FIFO behavior", "Examples"]
---

# Notes: FIFO queue delivery logic in Amazon SQS

> Notes are in English and in your own words. The fetch tool returned the page text; section names are as shown.

## Key points

- (Sending messages) Ordering is defined per message group ID, not for the whole queue. Inside one group, order is strict; across groups there is no promise.
- (Sending messages) For one total order over everything, give all messages the same group ID. The price is that only one consumer can make progress at a time.
- (Receiving messages) Once messages of a group are handed to a consumer, the rest of that group is withheld until those are deleted or the visibility timeout expires. A stuck message therefore stalls its whole group.
- (Additional notes) To get parallelism, use many group IDs for independent workflows (per user, per order, and so on).
- (Retrying) Producer retries with the same deduplication ID do not create duplicates or break order, within the deduplication window.

## Relevant to concepts

- `event-log-streaming`: same trade-off as Kafka partitions (order per key/group, parallelism across groups); useful as a second example next to partitions.
- `message-queue`: ties ordering to visibility timeout behavior.

## Warnings

- SQS-specific; group ID plays the role of a partition key but is not the same mechanism.
- Page footer and date not seen; license assumed all-rights-reserved.
