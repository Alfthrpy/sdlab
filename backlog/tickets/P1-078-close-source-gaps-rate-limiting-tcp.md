---
id: P1-078
title: "Close source gaps: rate limiting, TCP/TLS and DNS basics, saga and 2PC, and other thin concepts"
milestone: M2
type: research
owner: agent
review: agent
status: done
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

- [x] One candidate source per gap above, or a documented gap
- [x] `python scripts/validate.py` passes

## Notes

Research pass 2026-11-16. All entries are `candidate`, `verified_on` empty (verifier sets it). curriculum/concepts.yaml not edited; the owner approves first.

1. rate-limiting: `redis-tutorial-rate-limiters-five-algorithms` (algorithms, 429 + Retry-After), `stripe-blog-rate-limiters` (placement, fail open, load shedders), `rfc-6585-additional-http-status-codes` (429 spec). Covered.
2. dns-networking-basics: `mdn-tcp-handshake-glossary`, `mdn-transport-layer-security`, `mdn-http-connection-management-1x` (keep-alive), `aws-route53-how-dns-routes-traffic` (resolution stages, caching). Partial gap: TTL is only covered briefly (MDN TTL glossary page is one paragraph, not registered). Cloudflare Learning returned HTTP 403. Proposed action: add an RFC 1035/2181 TTL section or a resolver doc if the owner wants more.
3. distributed-transactions: `azure-saga-pattern`, `pg-docs-prepare-transaction`. Gap: no free source on the 2PC coordinator protocol and its blocking problem. Proposed action: open the Garcia-Molina/Salem saga paper and a university text on 2PC.
4. back-of-envelope-estimation: `sre-workbook-non-abstract-design-ch12` (Tier 1, CC BY-NC-ND). Only a large-scale ads example; a beginner-sized worked example (QPS = daily requests / 86,400, storage, bandwidth) from a Tier 1-2 source is still missing. The existing tier 6 candidates were not re-opened.
5. stateless-services-sessions: `django-docs-sessions`, `owasp-session-management-cheat-sheet`. Gap: sticky sessions (load balancer affinity); the AWS ALB page fetch returned nothing usable. Proposed action: open NGINX or HAProxy or Envoy session persistence docs.
6. transactions-acid: `pg-docs-wal-intro` (durability, redo). Gap: atomicity (undo) is not explained there.
7. capacity-headroom: `sre-book-appendix-b-best-practices` (N+2, load-test ratios), `aws-wa-rel07-bp04-load-test`. Gap: no source gives a formula or a utilization target (such as 70-80%) for computing headroom from a load test. Proposed action: owner decides whether to rewrite the trigger or find a Brooker/Gregg style post.
8. observability: `honeycomb-structured-events-basis-observability` (wide events argument; vendor view; date is the page's Updated date).

Unverified: license footers not visible in fetches for the Redis tutorial, AWS docs (Route 53, REL07-BP04), Django docs (all recorded as all-rights-reserved); licenses for MDN, Microsoft Learn were taken from the MDN attribution page and the architecture-center repo LICENSE, not the article page footers. Missing dates: AWS, Django, OWASP, PostgreSQL pages (versioned or undated). Fetch results are model summaries, so exact titles and dates need the verifier's re-check (especially Stripe date and Honeycomb date).

Verification (source-verifier): pass. 9 of 16 reopened in full (the riskiest), the other 7 quick-fetched; all URLs resolve. One edit: the Honeycomb title was set to the page's exact string. Entries stay `candidate`.

Gaps left (proposed actions): DNS TTL (RFC 2181/1035 or a resolver doc); 2PC coordinator protocol and blocking (the Garcia-Molina/Salem saga paper and a university text were not opened); a beginner-sized estimation example; sticky sessions (NGINX/HAProxy/Envoy docs); atomicity/undo; a headroom formula or utilization target (the concept trigger quotes 70-80%, which no source supports, so the owner may rewrite the trigger); high-cardinality observability docs. Licence doubts: Django docs (BSD may cover the docs), Redis, OWASP footer, MDN CC-BY-SA-2.5 (rests on the MDN attribution page).

The criterion "after approval, add the ids to `sources` in `concepts.yaml`" was removed from this ticket and moved to P1-079 (needs the owner to approve the candidates first).
