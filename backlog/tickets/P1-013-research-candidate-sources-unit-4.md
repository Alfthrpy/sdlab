---
id: P1-013
title: "Research candidate sources — Unit 4"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-010, P1-068]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Context

Fill the Reference Registry for Unit 4: Async & streams (queues, logs, delivery semantics, outbox, backpressure). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
4. Write reading notes for the 3–5 most important sources.
5. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [x] ≥ 15 candidates for this unit, all opened in the session
- [x] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [x] Reading notes for the 3–5 main sources
- [x] `source-verifier` says pass
- [x] `python scripts/validate.py` passes

## Notes

Result: 20 new candidates (unit 4), unit 4 added to `aws-builders-load-shedding`, `sre-book-handling-overload-ch21`, `aws-builders-idempotent-apis`; 5 reading notes. `source-verifier`: pass; minor fixes applied (Kafka paper venue provenance, RabbitMQ topics).

Gaps and weak spots:
- **Tier 1:** `ddia-2e` is still unverified (paywalled; streaming chapter TOC not checked).
- **Kreps, "The Log" (LinkedIn, 2013):** URL could not be opened (404/400), so it is not registered. Needs a manual check for a working URL.
- **Consumer lag as an operational practice:** only Kafka CLI output; look for Burrow, Confluent monitoring docs, or queue-age alerting.
- **Google Cloud Pub/Sub, SQS FIFO / message groups, Kafka KIP-98, RabbitMQ pub/sub tutorial:** not opened.
- **Ordering guarantees (per-partition vs total):** no dedicated free primary source.
- **Backpressure:** `reactive-manifesto` is vocabulary only and should not count toward coverage; Node.js streams is in-process only.
- **Weak metadata:** `kafka-netdb-2011` is a course-hosted copy with no DOI; Debezium site license is CC BY 3.0 (not in the schema enum, so `unknown` blocks approval until P1-070-style handling); `microservices-io-*` have no dates and a practitioner author; Azure and SQS pages show no license text; Kafka docs pinned to /44/.
- `verified_on` is unset on all entries (P1-016 does that).

Trigger hints found: slow work in the request path (RabbitMQ, SQS) leads to a work queue; traffic spikes on a downstream service lead to queue-based load leveling (not when a synchronous reply is needed); many independent consumers lead to pub/sub; replay or rewind needs a log (offsets per group); one action that must change the DB and notify another system leads to the outbox/CDC; retries and at-least-once delivery mean idempotent consumers; producer rate above consumer rate means unbounded queue growth, so apply backpressure or shed load.
