---
source: aws-builders-timeouts-retries
read_by: agent
date: 2026-11-12
sections_read: ["Failures happen", "Timeouts", "Retries and backoff", "Jitter", "Conclusion"]
---

# Notes: Timeouts, retries, and backoff with jitter (Amazon Builders' Library)

> Notes are in English and in your own words. Section names are as reported by the fetch tool (the page was read through a summarizing fetch, not line by line).

## Key points

- (Failures happen) Small, constant failure rates are normal; the goal is to keep them from growing into outages. Timeouts, retries, and backoff are the basic tools.
- (Timeouts) Every remote call needs a timeout, for the connection and for the request. Too long wastes resources while waiting; too short causes extra retries. A usual starting point is a high percentile of the dependency's measured latency, adjusted for network distance.
- (Timeouts) Default socket timeouts can skip phases such as DNS lookup or the TLS handshake. A case in the article: a low timeout failed on fresh connections after deployments; the fix was opening connections at startup.
- (Retries and backoff) Retries help with rare, transient faults but add load during overload. Exponential backoff with a cap spaces them out; limit the number of attempts.
- (Retries and backoff) Retrying at every layer of a deep call chain multiplies load on the failing dependency. Prefer retrying at one layer for cheap operations.
- (Retries and backoff) A local token bucket works as a retry budget: retries are free while tokens last, then limited to a fixed rate. The AWS SDK added this in 2016.
- (Retries and backoff) Circuit breakers stop calls after an error threshold, but the article warns they are harder to test and can slow recovery.
- (Retries and backoff) Retry only idempotent operations, and do not retry client errors.
- (Jitter) Random delay spreads retries and also periodic jobs and timers so clients do not hit a service at the same moment. For scheduled work, a stable per-host offset is easier to debug than pure randomness.
- (Conclusion) Retry only when the dependency looks healthy, and stop when retries no longer improve availability.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published and last modified 2019-12-05 | page header | Author shown as "Marc" only |
| Token-bucket retry behavior added to the AWS SDK in 2016 | Retries and backoff | Article's own statement |

## Relevant to concepts

- `timeout`: how to choose a value and what the default does not cover.
- `retry-backoff-jitter`: backoff plus jitter plus a cap on attempts.
- `retry-budget`: token bucket idea for limiting retries.
- `circuit-breaker`: the article's balanced view (useful but harder to test).
- ladder trigger: appears once a request touches more than one remote dependency.

## Warnings

- AWS-scale framing; beginners need the ideas, not the SDK details.
- The article does not give a formula for choosing the percentile; do not invent one in lessons.
- Author name on the page is incomplete; the registry leaves `authors` empty (NO-AUTHOR) instead of recording a bare first name.
