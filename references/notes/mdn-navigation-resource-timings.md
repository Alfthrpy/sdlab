---
source: mdn-navigation-resource-timings
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "Navigation timing (timestamp list and diagram)", "Calculating timings (code example)", "Resource timing", "page footer"]
---

# Notes: Navigation and resource timings (MDN Web Docs)

> Notes are in English and in your own words. Page read via WebFetch and checked against the raw HTML (curl): property names, the example formulas and "last modified Sep 2, 2026". Footer says portions are copyright 1998-2026 mozilla.org contributors, content under a Creative Commons license (same MDN licensing as the other MDN entries).

## Key points

- (Introduction) Navigation timing records timestamps for loading the main document; resource timing does the same for each asset the document requests (images, scripts, and so on). The old `performance.timing` interface is deprecated but still works; the modern route is `PerformanceNavigationTiming` through the Performance Entry API.
- (Navigation timing) The page lists the timestamps in the order they happen, with a diagram: navigation start; unload of the previous page; redirects; fetch start; DNS lookup start and end; TCP connect start and end; start of the secure (TLS) connection; request start; response start (first byte) and response end (last byte); then browser-side DOM processing and the load event.
- (Navigation timing) Several values read 0 or undefined in some cases (no previous page, no redirect, a non-HTTPS page has no secure-connection timestamp), so a calculation must handle that.
- (Calculating timings) The page gives subtraction formulas for common phases: DNS time is the lookup end minus start; TCP time is connect end minus connect start; TLS time is request start minus secure-connection start; time to first byte is response start minus navigation start; full page load is load event start minus navigation start. The same code appears with old-style property names.
- (Resource timing) Each sub-resource (image, script) has its own timeline in the same style, including a diagram of its timestamps.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Request phases in order: redirect, DNS lookup, TCP connect, TLS (secure connection), request sent, response start, response end | Navigation timing | These are the stages a browser can time before the server's first byte; good basis for a stage diagram and for "which stage was slow" exercises |
| DNS = domainLookupEnd - domainLookupStart; TCP = connectEnd - connectStart; TLS = requestStart - secureConnectionStart; TTFB = responseStart - navigationStart | Calculating timings | Written with legacy `performance.timing` names; the modern `PerformanceNavigationTiming` has the same fields relative to start |
| `secureConnectionStart` is 0 for non-HTTPS pages and undefined when unavailable | Navigation timing | |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1: partly supported. It is the most concrete list of the browser-visible stages (DNS, TCP, TLS, request, response). It does not cover what happens after the request reaches the server.
- `request-lifecycle`, objective 2: partly supported. It shows how each stage's duration is obtained in practice from timestamps, so a learner can read a timing table. It gives no typical durations.
- `basic-monitoring` (unit 0): minor, the idea that duration can be recorded per phase.

## Warnings

- Browser-side view only (client measurements). It does not show proxy, application or database time.
- Some of the page uses deprecated property names; teach the stage order and the subtraction idea, not the API names.
- Cross-origin resources can hide detail unless the server allows it (see `web-dev-ttfb`); not needed for Unit 0.
