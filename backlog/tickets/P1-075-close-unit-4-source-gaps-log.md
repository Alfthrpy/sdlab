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

All new entries are `candidate` with `verified_on` empty (set by the verifier, per research-protocol.md).

- A9: added `kreps-the-log-2013`. Working URL: https://www.linkedin.com/blog/engineering/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying (old engineering.linkedin.com URL: 404). Kafka design docs: https://kafka.apache.org/44/design/design/ could NOT be fetched this session (WebFetch and curl both failed), so `kafka-docs-design` topics were left unchanged; its existing note already says Log Compaction is covered and retention is only mentioned in passing. Proposed action: the verifier re-opens it and confirms; Kreps' essay covers retention (inside Log Compaction section) meanwhile.
- A10: added `rabbitmq-docs-queue-length-limit` (bounded queue, reject-publish, publisher nack) and `rabbitmq-docs-flow-control` (broker throttles publishers). gRPC flow control page was opened but not registered: it covers streaming RPCs only and says nothing on bounded queues. Gap left: no vendor-neutral source on 429/503 propagation across several service hops; `sre-book-handling-overload-ch21` and `envoy-docs-circuit-breaking` (already registered) partly cover it.
- B7: added `aws-sqs-fifo-delivery-logic` (per message group ordering). Kafka ordering/KIP-98 not opened (kafka.apache.org unreachable), so no Kafka-specific ordering source; proposed action: retry KIP-98 later.
- B8: added `aws-sqs-cloudwatch-metrics` (queue age and depth). Gap left: no consumer-lag alerting practice source for Kafka (Burrow/lag alerting); not searched in depth.
- Reading notes: aws-sqs-fifo-delivery-logic, aws-sqs-cloudwatch-metrics, rabbitmq-docs-queue-length-limit, kreps-the-log-2013 (the last from a fetch-tool summary only).

Verification (source-verifier): all 5 entries reopened; pass. Two reading-note fixes: inference sentences in the SQS metrics note are now labelled; the Kreps "Part Four" bullet is marked UNCONFIRMED. Entries stay `candidate`, `verified_on` empty.

Kafka retry (not registered; for a follow-up): `kafka.apache.org` was unreachable. The Kafka 4.4 design page was readable via `https://raw.githubusercontent.com/apache/kafka-site/asf-site/44/design/design/index.html` (likely canonical URL `https://kafka.apache.org/44/design/design/`, not opened). It has a Log Compaction section; retention appears only in passing (so register `kafka-docs-design` for compaction, not retention; retention config probably lives on the Configuration page, unverified). It describes the idempotent producer but not ordering. KIP-98 (`https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging`, last updated 2026-03-04 by Matthias J. Sax) states per-partition sequence numbers and, with idempotence, per-partition ordering without duplicates; it is a wiki page (weaker than Tier 2 docs).

Gaps left (proposed actions): Kafka ordering source (register KIP-98 in a follow-up once reopened by a researcher); Kafka consumer-lag alerting (Burrow or an SRE article, not searched in depth, so B8 rests on SQS only); cross-hop 429/503 propagation (no vendor-neutral primary; decide if `sre-book-handling-overload-ch21` and `envoy-docs-circuit-breaking` suffice); the Kafka design page's retention coverage. Licence doubts: SQS footers unseen (all-rights-reserved by protocol default).
