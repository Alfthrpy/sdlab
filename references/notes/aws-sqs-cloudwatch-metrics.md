---
source: aws-sqs-cloudwatch-metrics
read_by: agent
date: 2026-11-15
sections_read: ["Amazon SQS metrics (table)", "Dead-letter queues and CloudWatch metrics", "Fair queues and CloudWatch metrics", "Dimensions", "Monitoring tips"]
---

# Notes: Available CloudWatch metrics for Amazon SQS

> Notes are in English and in your own words.

## Key points

- (Amazon SQS metrics) ApproximateAgeOfOldestMessage is the age in seconds of the oldest message that is still waiting; it is reported only while the queue holds at least one active message. It is the queue-age signal: it rises when consumers fall behind or a message cannot be processed.
- (Table, key notes on age) In standard queues a message that has been received three or more times without delete is moved to the back and left out of the metric, so poison messages do not inflate age. When a message is moved to a dead-letter queue its age restarts there. In FIFO queues messages are not reordered, so a failing message blocks its group, so the oldest message stays old.
- (Table) ApproximateNumberOfMessagesVisible is the backlog waiting for a consumer; a consistently high value suggests too few consumers or stuck processing. ApproximateNumberOfMessagesNotVisible counts messages in flight (received, not yet deleted); high values point to slow or stuck consumers. A short blip can be a server problem, so alarm on several consecutive data points.
- (Table) For FIFO, ApproximateNumberOfGroupsWithInflightMessages shows how many groups are being worked on at once; a big backlog with a low value suggests more consumers or more active groups.
- (Table, footnote) Sent, received and deleted counters include retries and duplicates, so they are activity measures and not exact counts of unique messages.
- (Fair queues) With fair queues, "quiet group" variants of the same metrics, including age of the oldest message in quiet groups, exclude noisy tenants so you can see whether other tenants are affected.
- (Dead-letter queues) For a DLQ, watch the visible-messages metric, because automatic redrive is not counted in the sent metric.
- (Monitoring tips) The page's own advice is short: alarm on visible messages to spot backlog growth; it does not recommend a threshold for message age.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Age metric unit is seconds | metric table | |
| Standard queue: message received 3 or more times without delete is moved to the back and left out of the age metric | metric table, key notes | Applies even when a redrive policy exists |

## Relevant to concepts

- `backpressure-consumer-lag`: queue age and backlog as health signals; difference between depth (count) and age; in-flight count as a hint of stuck consumers.
- `message-queue`: DLQ monitoring.

## Warnings

- Counts are approximate (distributed system); the page says so.
- SQS-specific. Kafka uses offset lag instead (see burrow-kafka-consumer-monitoring-2015 and kafka-docs-basic-operations).
- No date or license text in the fetched content; treated as all-rights-reserved. Metric list changes over time; recheck before citing exact names.
