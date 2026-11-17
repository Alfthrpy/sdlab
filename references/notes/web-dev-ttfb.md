---
source: web-dev-ttfb
read_by: agent
date: 2026-11-17
sections_read: ["What is TTFB?", "TTFB and Early Hints", "What is a good TTFB score?", "How to measure TTFB"]
---

# Notes: Time to First Byte (TTFB) (web.dev, Barry Pollard and Jeremy Wagner)

> Notes are in English and in your own words. Page read via WebFetch and re-checked against the raw HTML (curl): authors, dates, the phase list, the thresholds and the license footer. Published 2021-10-26, last updated 2025-11-18 (page body); footer says last updated 2025-11-28.

## Key points

- (intro note) TTFB is a basic measure of how fast a connection is set up and how quickly the web server answers. For a page (HTML document) request it comes before every other loading metric the user perceives.
- (What is TTFB?) TTFB is the time from the start of navigation until the first byte of the response arrives. The page shows a diagram of the request phases, with TTFB covering everything between the navigation start and the response start.
- (What is TTFB?) TTFB is stated to be the sum of these phases, in this order: redirect time, service worker startup (only if one is used), DNS lookup, connection and TLS negotiation, and then "request" up to the arrival of the first response byte. The last phase is the part where the server does its work (reading the request, running the app, querying the database) before replying; the page names "backend" latency as a reason TTFB is high but does not break the last phase down further.
- (What is TTFB?) Two levers are named for a lower TTFB: shorter connection setup time, and a faster backend.
- (TTFB and Early Hints) What counts as the "first byte" varies: a 103 Early Hints response or early flushed headers count as first bytes. So TTFB values from different platforms are not always comparable. Chrome changed what it reports in version 115 and reverted in 133 (detail, not needed for Unit 0).
- (What is a good TTFB score?) Rough guide: 0.8 seconds or less is good, over 1.8 seconds is poor. This is explicitly not a Core Web Vitals threshold and is not a hard target. A server-rendered site can tolerate a higher TTFB than a single-page app, because an SPA needs the markup before it can start drawing.
- (How to measure TTFB) Field: Chrome User Experience Report and the `web-vitals` library. Lab: Chrome DevTools network panel, WebPageTest. In code: a `PerformanceObserver` on `navigation` entries reads `responseStart`; per-resource entries need care (cached or reused-connection entries have `responseStart` 0, and cross-origin requests need a `Timing-Allow-Origin` header).
- (How to measure TTFB) The phase diagram labels the browser timing fields for each phase (redirect, DNS lookup, connect and secure connect, request and response start); for the full field list see `mdn-navigation-resource-timings`.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| TTFB = redirect + service worker startup (if any) + DNS lookup + connection and TLS negotiation + request up to the first response byte | What is TTFB? | The phase list is the useful part for `request-lifecycle` obj 1; the phases are the page's, in order |
| Good TTFB 0.8 s or less; poor above 1.8 s | What is a good TTFB score? | "Rough guide", not a Core Web Vitals threshold; measured at the 75th percentile of users per the page's advice |
| Ways to reduce TTFB: less connection setup latency, less backend latency | What is TTFB? | |

## Relevant to concepts

- `request-lifecycle` (unit 0), objective 1 (draw the stages of a request from browser to database and back): partly supported. It lists the client-side phases before the server works (DNS, connect, TLS) and puts the server's work in one box ("request ... until first byte"). It does not show the proxy, app or database inside that box; take those from `nginx-reverse-proxy-admin-guide`, `pg-docs-query-path` and Craver.
- `request-lifecycle`, objective 2 (given time per stage, find the likely slowest): partly supported. It treats a request's time as a sum of phases, which is the premise of the exercise, and gives the 0.8 s / 1.8 s reference for the total before the first byte. It gives no typical value for each phase, so scenario numbers must be the author's own (or be anchored on Craver's server-side figures).
- `latency-throughput` (unit 1): minor, a worked decomposition of latency into phases.

## Warnings

- It is a front-end performance guide for page loads, so it measures from the browser. Server-to-database time is hidden inside the last phase.
- Early Hints and Chrome's change in how `responseStart` is reported make TTFB comparisons between tools subtle. Not needed for beginners.
- The thresholds are guidance for web pages, not an SLO for an API.
