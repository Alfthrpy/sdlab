---
id: P1-078
title: "Close source gaps: rate limiting, TCP/TLS and DNS basics, saga and 2PC, and other thin concepts"
milestone: M2
type: research
owner: agent
review: agent
status: in-progress
priority: medium
depends_on: []
estimate: 1
outputs:
  - references/registry.yaml
---

## Context

Found in P1-023 (map concepts to sources). Three concepts reach the ≥ 2 approved sources minimum only with weak or indirect coverage:

- `rate-limiting` (Unit 2): mapped to `sre-book-handling-overload-ch21` and `aws-builders-load-shedding`, which cover overload and shedding but not limiter algorithms (token bucket, leaky bucket, fixed/sliding window).
- `dns-networking-basics` (Unit 2): TCP handshake and TLS are not covered by any approved source (only DNS and HTTP).
- `distributed-transactions` (Unit 5): mapped to `spanner-osdi12` and `ddia-2e` (paywalled); no free source for saga or two-phase commit. `ddia-2e`'s `free_companion` only covers Unit 1 topics, so nothing free exists for Unit 5 transactions.

Further thin coverage found by the P1-023 review (not tracked in P1-072/074/075/076):

- `dns-networking-basics`: also DNS resolution stages and TTL at beginner level (only a Tier 1 SRE chapter exists), plus keep-alive.
- `back-of-envelope-estimation`: no Tier 1-2 source; the Dean slides are image-only with no license (`highscalability-back-of-envelope-2011` and `latency-numbers-gist` are still candidates).
- `stateless-services-sessions`: nothing on signed-cookie vs shared-store vs sticky sessions.
- `transactions-acid`: nothing free on atomicity and durability (WAL); only `ddia-2e` (paywalled) was added.
- `capacity-headroom`: nothing on computing headroom from a load test.
- `observability`: the high-dimensional events argument is weakly covered (tracing and SLO alerting belong to P1-076).

## Tasks

1. Rate limiting: find one free, authoritative source on limiter algorithms and where to place a limiter.
2. TCP/TLS: find one free source for the TCP handshake and TLS basics at beginner level (MDN, Cloudflare Learning, or an RFC overview).
3. Saga / 2PC: find one free source each for the saga pattern and two-phase commit (for example the Azure Architecture Center saga pattern, or the original saga paper).
4. Also look for the thin-coverage items listed in the Context, in the order given.
5. Register each as `candidate` with license and `verified_on`; the owner approves later. If nothing suitable exists, record it as a gap in `references/coverage.md`.

## Done criteria

- [ ] One candidate source per gap above, or a documented gap
- [ ] After approval, add the ids to `sources` of the matching concepts in `curriculum/concepts.yaml`
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
