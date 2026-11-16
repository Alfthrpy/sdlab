---
source: redis-tutorial-rate-limiters-five-algorithms
read_by: agent
date: 2026-11-16
sections_read: ["whole page: algorithm comparison, why Lua scripts, five algorithm sections, when to use which, HTTP response codes and headers"]
---

# Notes: Build 5 Rate Limiters with Redis

> Notes are in English and in your own words. Code on the page is TypeScript/Lua; do not copy it.

## Key points

- (Algorithm comparison) Five limiters are compared: fixed window, sliding window log, sliding window counter, token bucket, leaky bucket. The table rates memory per client, accuracy, and burst behavior.
- (Fixed window) One counter per time slot; cheap, but a client can place a burst at the end of one window and another at the start of the next, so up to about twice the limit passes in a short span.
- (Sliding window log) Keeps one timestamp per request, so it is exact but memory grows with the request count per client.
- (Sliding window counter) Blends the previous and current window counts by how far into the current window you are; near-exact, two counters per client. The page's default pick for general APIs.
- (Token bucket) Tokens refill at a steady rate up to a cap; each request spends one; allows bursts up to the cap while holding an average rate.
- (Leaky bucket) Two uses: as a meter that rejects immediately (policing) or as a queue that delays (shaping). The page says token and leaky bucket are duals of each other.
- (Why Lua scripts) Read-decide-write is a race when many requests run at once; the limiter state must change atomically, and a shared store is what makes the limit hold across several app servers.
- (HTTP response codes and headers) Return 429 when limited and include Retry-After in seconds; X-RateLimit-* headers are only a convention with no single standard.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Fixed window can allow about 2x the limit across a window boundary | Algorithm comparison table; section 1 trade-offs | Example in the text: 10 requests at second 9 and 10 more at second 11 for a 10-per-10-seconds limit |

## Relevant to concepts

- `rate-limiting`: algorithm choice, boundary-burst problem, 429 + Retry-After.

## Warnings

- Vendor tutorial; the "best default" recommendation is the author's view. Placement (gateway vs service) is barely covered; use `stripe-blog-rate-limiters` for that.
- License footer was not visible in the fetch.
