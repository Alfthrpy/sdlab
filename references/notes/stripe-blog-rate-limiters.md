---
source: stripe-blog-rate-limiters
read_by: agent
date: 2026-11-16
sections_read: ["whole post, via fetch summary; verifier should reopen"]
---

# Notes: Scaling your API with rate limiters (Stripe)

> Notes are in English and in your own words.

## Key points

- (Overview) Stripe runs four kinds of control in production, ordered by importance: a per-user request rate limiter, a per-user concurrent request limiter, a fleet usage load shedder that reserves capacity for critical traffic, and a worker utilization load shedder that drops low-priority traffic first when workers are busy.
- (Request rate limiter) Token bucket per user, state kept in Redis; the post says to start with this one.
- (Concurrency limiter) Caps in-flight requests per user; helps protect expensive endpoints.
- (Placement) Limiters run as middleware in the API stack, in front of the business logic.
- (Failure mode) Limiter code should fail open: a bug or a Redis outage must not take the API down.
- (Responses) 429 for a limited client; 503 for load shedding by the server.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Four limiter types in production | Overview | Names vary slightly; check wording on the page before quoting |

## Relevant to concepts

- `rate-limiting`: where a limiter sits, why fail-open, difference between limiting a client and shedding load.

## Warnings

- 2017 post; this note came from a model-written fetch summary, so the verifier should reopen it before any detail is used in a lesson.
