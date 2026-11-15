---
source: burrow-kafka-consumer-monitoring-2015
read_by: agent
date: 2026-11-15
sections_read: ["Why Are Kafka Consumers Hard to Monitor?", "Introducing Burrow", "Next Steps", "Burrow Code and Documentation"]
---

# Notes: Burrow: Kafka Consumer Monitoring Reinvented (Palino, LinkedIn, 2015)

> Notes are in English and in your own words. The fetch tool summarized the page; the GitHub README of linkedin/Burrow was also opened (Apache-2.0, description "Kafka Consumer Lag Checking", no archived banner, wiki holds configuration docs).

## Key points

- (Why Are Kafka Consumers Hard to Monitor?) Consumer lag is the key health number, but it is hard to alert on: the MaxLag sensor only shows the worst partition and is meaningless once a consumer disappears; spot-checking a few topics misses problems elsewhere; lag is per partition, so wildcard consumers produce huge numbers of series and aggregation hides slow topics.
- (Why ...) Fixed thresholds misfire. Lag rises during harmless traffic spikes. Because offsets are committed periodically, lag has a sawtooth shape, so thresholds must be set high and then detect real trouble late on quiet topics. A single lag value also cannot tell a dead consumer, a reporting glitch and a healthy consumer catching up apart.
- (Introducing Burrow) A central service, independent of consumers, reads the Kafka topic where offsets are committed plus broker state, and evaluates every consumer group and partition. It judges a sliding window of 10 offset commits (about 10 minutes at LinkedIn) and asks: is the consumer committing at all, are committed offsets moving forward, is lag growing, is growing lag steady or fluctuating.
- (Introducing Burrow) Partition results roll up to one status per consumer: OK (working), warning (working but falling behind), error (stopped or stalled). No configured thresholds. Status is available over HTTP and can be pushed by email or HTTP; LinkedIn states alerts come within about 10 minutes of a problem.
- (Next Steps) Only covers consumers that commit offsets to Kafka (not ZooKeeper at the time); wider coverage was planned.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Sliding window of 10 offset commits, about 10 minutes at LinkedIn | Introducing Burrow | Depends on commit interval |
| Published June 12, 2015, by Todd Palino | page header | |

## Relevant to concepts

- `backpressure-consumer-lag`: why a trend in lag (growing, steady, stalled) is a better alarm than a fixed number; lag versus a dead consumer; per-partition view.

## Warnings

- 2015, Kafka 0.8.2 era; today most teams use the `kafka-consumer-groups` CLI (see kafka-docs-basic-operations), Prometheus exporters, or Burrow itself. The modern Burrow wiki was not read.
- Lag measures offsets, not time. For a time-based signal see the message-age idea in aws-builders-insurmountable-queue-backlogs and aws-sqs-cloudwatch-metrics.
- Article is an announcement of LinkedIn's own tool; the evidence is LinkedIn's experience, not a benchmark. No article license stated.
