---
id: P1-078
title: "Close source gaps for rate limiting, DNS/TCP/TLS, and distributed transactions"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: medium
depends_on: []
estimate: 1
outputs: []
---

## Context

Found in P1-023 (concept-to-source mapping). Three concepts have fewer than two sources that genuinely cover them, so they were mapped with the closest approved sources and are still thin:

- `rate-limiting` (Unit 2): only `sre-book-handling-overload-ch21` (per-customer limits) and `aws-builders-load-shedding`; no source explains rate-limiter algorithms (token bucket, sliding window) or per-client limits for API providers.
- `dns-networking-basics` (Unit 2): DNS is covered by `sre-book-load-balancing-frontend-ch19` and `system-design-primer`; `mdn-http-overview` covers TCP round trips and persistent connections only at sentence level, mentions TLS in passing, and has nothing on DNS; no registered source explains the TCP or TLS handshake (its registry note overstates the exclusion and should be reworded when sources are re-verified).
- `distributed-transactions` (Unit 5): no registered source covers saga or two-phase commit. It is mapped to `spanner-osdi12` (abstract page only was read) and `microservices-io-transactional-outbox` (related, but not about sagas).

## Tasks

1. Rate limiting: find one or two free sources on rate-limiter algorithms and per-client limits (vendor-neutral or an operator's engineering post).
2. DNS/TCP/TLS: find one free, beginner-level source each for the TCP handshake and connection reuse, and for the TLS handshake (RFC, MDN, or an operator guide).
3. Distributed transactions: find free sources for saga and for two-phase commit (original saga paper, a pattern catalogue, or a database docs page); read `spanner-osdi12` beyond the abstract page if it stays in the mapping.
4. Register new sources as `candidate` with `verified_on`; note anything not found as a gap. Do not edit `curriculum/concepts.yaml`; the owner of P1-023 follow-up (or a later ticket) updates the mapping once the sources are approved.

## Done criteria

- [ ] Every task above is done or recorded as a gap with a proposed action
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
