---
source: aws-builders-insurmountable-queue-backlogs
read_by: agent
date: 2026-11-12
sections_read: ["Introduction", "The duplicitous nature of queues", "Queue-based systems", "Failures in asynchronous systems", "Measuring availability and latency", "Backlogs", "Amazon's approach", "Conclusion"]
---

# Notes: Avoiding insurmountable queue backlogs (Amazon Builders' Library)

> Notes are in English and in your own words. Section names as reported by the fetch tool.

## Key points

- (Introduction) A queue only matters when it is long; the article is about keeping backlogs from becoming unrecoverable.
- (Duplicitous nature of queues) Queues add durability and retry ability, but also latency, and they can make recovery from an outage slower.
- (Failures in asynchronous systems) After an outage the backlog must be drained on top of new traffic, so recovery can take as long as the outage or longer. A synchronous system just rejects requests and recovers faster.
- (Measuring availability and latency) Track the age of messages when taken from the queue; separate first attempts from retries so a few slow or offline clients do not hide a real problem.
- (Backlogs) In a shared system one tenant's burst delays everyone. Rate limits at the front door are not enough because already-queued work bypasses them.
- (Amazon's approach) Tools listed: separate queues per customer or workload (shuffle-sharding to reduce cost), spillover or sidelining of stale or excess messages, dropping old messages when a later sync makes them useless, per-workload concurrency limits, backpressure that rejects upstream, plus delay queues, in-flight limits, dead-letter queues and message heartbeats.
- (Conclusion) Plan for the backlog case from the start.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published 2019-12-05 | page header | Author shown only as "David" |

## Relevant to concepts

- `backpressure`: when and how to push back instead of queueing forever.
- `consumer-lag`: message age as the key health signal.
- `ladder trigger`: a queue helps with spikes but turns an outage into a backlog; know when to shed load instead.

## Warnings

- Written from AWS multi-tenant scale; small systems need only the ideas (bounded queue, age metric, drop stale work).
