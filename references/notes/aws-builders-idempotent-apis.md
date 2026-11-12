---
source: aws-builders-idempotent-apis
read_by: agent
date: 2026-11-12
sections_read: ["Introduction", "Retrying and side effects", "Reducing client complexity", "Retries and semantic equivalence", "Late arriving requests", "Same client request ID, different intent", "Conclusion"]
---

# Notes: Making retries safe with idempotent APIs (Amazon Builders' Library)

> Notes are in English and in your own words. Section names are the headings shown on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (Introduction) Retrying fixes transient failures but can duplicate effects when the operation is not safe to repeat.
- (Retrying and side effects) When a response is lost, the client cannot tell whether the first attempt worked, so a blind retry might create a second resource.
- (Reducing client complexity) AWS prefers a client-supplied unique request identifier over guessing duplicates from the request parameters; this keeps client logic simple.
- (Retries and semantic equivalence) A repeated request gets a response with the same meaning as the first (not necessarily byte-identical), which lets SDKs and the CLI retry automatically.
- (Late arriving requests) The service stores idempotency records for a limited time so that delayed retries are still answered consistently.
- (Same client request ID, different intent) Reusing an ID with different parameters is treated as a mistake and rejected with a validation error.
- (Conclusion) Idempotency adds complexity and is not worth it for every service.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Footer copyright 2026 AWS, all rights reserved | page footer | Rewrite only; no publication date on the page |

## Relevant to concepts

- `idempotency`: the pattern (request ID plus stored record plus conflict rule).
- `retries` (Unit 6 link): why retries need idempotency; see `aws-builders-timeouts-retries`.

## Warnings

- Service-side details such as how the record store is built and its expiry are only described at a high level here; pair with `stripe-docs-idempotent-requests` for concrete numbers.
