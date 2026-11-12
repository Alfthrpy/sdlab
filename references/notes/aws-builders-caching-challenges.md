---
source: aws-builders-caching-challenges
read_by: agent
date: 2026-11-12
sections_read: ["The ecstasy and the agony of caches", "When we use caching", "Local caches", "External caches", "Inline vs. side caches", "Cache expiration", "Other considerations", "Amazon best practices and considerations"]
---

# Notes: Caching challenges and strategies (Amazon Builders' Library)

> Notes are in English and in your own words. Section names are the headings shown on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (The ecstasy and the agony of caches) A cache gives a big early win but the service slowly starts to depend on it; losing the cache or a traffic shift can then cause an outage.
- (When we use caching) Use it when a dependency is slow or throttles under load, results are reused across requests, and clients tolerate slightly stale data.
- (Local caches) In-process caches are the quickest to add but each server holds different data and new servers start cold.
- (External caches) A shared cache fleet keeps data consistent across servers and shields the dependency, at the cost of extra operations and its own failure modes.
- (Inline vs. side caches) Inline caches are transparent to callers but tie cache availability to the dependency; side caches are managed in application code.
- (Cache expiration) Size, TTL and eviction should come from measuring real traffic; soft and hard TTLs can keep serving older data while a dependency struggles.
- (Other considerations) Have a plan for downstream errors: either serve the last good cached value, or cache the error itself with its own, different expiry. Either way the cache should hold something for error cases (negative caching), because otherwise a briefly unavailable resource keeps drawing upstream requests and can deepen an outage; the authors say they saw failures rise when negative responses were not cached. Also consider cache poisoning and timing side channels; prevent thundering herds with request coalescing (one pending upstream request per uncached item).
- (Amazon best practices) Justify the cache, operate it like a real service, tune it empirically, keep the system able to survive without it.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published 2019-12-05 (author Jas Chhabra) | page header | Footer copyright 2026 AWS |

## Relevant to concepts

- `cache`: trigger (slow or throttled dependency, reused results) and the "when not to" side (cache becomes a hard dependency).
- Later (Unit 6): metastable failure after cache loss.

## Warnings

- No concrete numbers are given for TTL or size; those must come from the learner's own measurements.
- Write patterns (write-through and so on) are not the focus; see `azure-cache-aside-pattern`.
