---
source: aws-sqs-cloudwatch-metrics
read_by: agent
date: 2026-11-16
sections_read: ["Amazon SQS metrics table", "Dead-letter queues and CloudWatch metrics", "Fair queues and CloudWatch metrics", "Monitoring tips"]
---

# Notes: Available CloudWatch metrics for Amazon SQS

> Notes are in English and in your own words. The fetch tool returned the page text; section names are as shown.

## Key points

- (Metrics table) Queue age (ApproximateAgeOfOldestMessage) measures how long the oldest unprocessed message has waited; queue depth (ApproximateNumberOfMessagesVisible) measures backlog size. (inference, not on the page:) age shows the delay the user feels; depth alone can mislead when message sizes or rates vary.
- (Metrics table) Age can look healthy while work is stuck: poison messages received repeatedly in a standard queue are pushed back and excluded from the age figure, and a message moved to a DLQ restarts its age. So pair the age alarm with a DLQ depth alarm. (Pairing an age alarm with a DLQ depth alarm is an inference, not stated on the page.)
- (Metrics table) In FIFO queues a failing message blocks its group and keeps aging, so age rises for the blocked group.
- (Metrics table) In-flight count (not visible) shows messages being processed or stuck consumers; it can briefly report nonzero on an empty queue, so alarm on several consecutive points.
- (Monitoring tips) Alarm on visible-message count to catch backlog growth; for a DLQ, use the visible count.
- (Note at top) Values are approximate because of the distributed design.

## Relevant to concepts

- `backpressure-consumer-lag`: diagnosing a growing queue from age and depth; choosing between more consumers and throttling producers.
- `message-queue`: DLQ and visibility timeout side effects on metrics.

## Warnings

- Gives metric definitions, not thresholds or an alerting method.
- Page footer and date not seen; license assumed all-rights-reserved.
