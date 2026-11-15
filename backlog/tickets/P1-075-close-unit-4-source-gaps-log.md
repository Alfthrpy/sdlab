---
id: P1-075
title: "Close Unit 4 source gaps: log streaming, backpressure, ordering, consumer lag"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: medium
depends_on: []
estimate: 2
outputs: []
---

## Context

Gap items A9, A10, B7, B8 in `references/coverage.md`. `reactive-manifesto` must not be counted as backpressure coverage.

## Tasks

1. A9: find a working URL for Kreps "The Log" and check whether the Kafka design docs cover retention and compaction.
2. A10: find one source on bounded queues and flow control between services.
3. B7: find a free primary source on ordering guarantees (per partition vs total).
4. B8: find a queue-age or consumer-lag monitoring source.
5. Register new sources as `candidate` with `verified_on`; note anything not found as a gap.

## Done criteria

- [x] Every task above is done or recorded as a gap with a proposed action
- [x] `python scripts/validate.py` passes

## Notes

Seven new `candidate` entries in `references/registry.yaml` (all Tier 2), plus an extended note on `kafka-docs-design`. All opened on 2026-11-15 and reopened by `source-verifier` (verdict: conditional pass; all fixes applied). Reading notes are in `references/notes/`. `reactive-manifesto` is not counted anywhere.

| Gap | Result | Entry |
| --- | --- | --- |
| A9a Kafka design page: retention and compaction | **Closed, with a limit.** Compaction has its own section (basics, guarantees, details, cleaner config; `delete.retention.ms` default 24 h; compaction never reorders). Time or size retention is only mentioned in passing, with no config names. | `kafka-docs-design` (notes extended) |
| A9b working URL for "The Log" | **Closed.** The old `engineering.linkedin.com` URL is 404; the working one is on `linkedin.com/blog/engineering/...`. Author and date (2013-12-16) match; full text read. No license stated, so all-rights-reserved. The Wayback copy could not be opened, so no `archive_url`. | `kreps-the-log-2013` (T2) |
| A10 bounded queues and flow control between services | **Closed.** RabbitMQ queue length limits with `reject-publish` and publisher nacks (the clearest producer pushback), RabbitMQ flow control (short page, no credit mechanics), gRPC flow control for streaming RPCs. | `rabbitmq-docs-maxlength`, `rabbitmq-docs-flow-control`, `grpc-docs-flow-control` (T2) |
| B7 ordering, per partition vs total | **Closed, with a caveat.** SQS FIFO orders per message group id (one group id gives total order, no parallelism). Together with Kreps and the Kafka design page, which say partitions are totally ordered with no global order, both sides are covered. Kafka producer-side ordering under retries is not covered; KIP-98 is on a wiki and mostly about exactly-once, so it was not registered. | `aws-sqs-fifo-delivery-logic` (T2) |
| B8 queue age and consumer lag | **Closed.** SQS `ApproximateAgeOfOldestMessage` with its poison-message and DLQ caveats; Burrow's window-of-offset-commits approach instead of fixed lag thresholds (the article's setting is LinkedIn's, 2015, Kafka-committed offsets only). | `aws-sqs-cloudwatch-metrics`, `burrow-kafka-consumer-monitoring-2015` (T2) |

- Verifier fixes applied: the two new RabbitMQ entries were wrongly recorded as "no open license". I opened the `rabbitmq-website` README myself: it licenses the docs Apache-2.0 OR MPL-2.0 (blog excluded), while the page footer says all rights reserved. They are now `Apache-2.0` with `rewrite-only` and the conflict stated in `notes`. Also fixed: Kreps word count (about 12,000, not 8,000), two inferences stated as page claims (SQS FIFO "keeps the age growing", gRPC "buffering without limit"), and `accessed` on `kafka-docs-design`.
- Proposed follow-ups, not done: (1) the existing `rabbitmq-tutorial-work-queues` and `rabbitmq-docs-confirms` entries are still all-rights-reserved; they may fall under the same README license, but I did not check which repo holds the tutorial pages. (2) Register the Kafka topic-config page (`retention.ms`, `retention.bytes`) if a lesson needs exact retention settings. (3) KIP-98 or the Kafka producer docs if a lesson needs ordering under retries. (4) The Burrow GitHub README and wiki (Apache-2.0) were opened or skipped but not registered.
- Reading limits: the RabbitMQ pages were read through a fetch summary only (the site blocks curl), the gRPC and Burrow pages were checked against raw HTML by the verifier. Recheck exact wording and config names before quoting. AWS Site Terms and LinkedIn's copyright policy were not opened, so those licenses are the default, all-rights-reserved.
- Not done: no entry is `approved`; `coverage.md` and `concepts.yaml` are unchanged, so the Unit 4 concepts do not yet cite the new ids. Owner: confirm that the new ids are mapped to `event-log-streaming`, `backpressure-consumer-lag`, `message-queue` and `delivery-semantics` after approval.
- `validate.py`: 0 errors, 31 warnings (existing kinds).
