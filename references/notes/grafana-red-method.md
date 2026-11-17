---
source: grafana-red-method
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "The USE Method", "The RED Method", "The Four Golden Signals", "Two Sides of the Same Coin", "page footer"]
---

# Notes: The RED Method: How to Instrument Your Services (Grafana Labs blog, Julie Dam, 2018-08-03)

> Notes are in English and in your own words. Whole page read via WebFetch and re-checked against the raw HTML with curl (the wording of the three RED metric names and the footer were taken from the raw text). The page is a 4-minute read, a write-up of a talk, with no code.

## Key points

- (Introduction) The post recaps a talk Tom Wilkie gave at GrafanaCon EU in March 2018. The byline is Julie Dam; the ideas are Wilkie's, who says he created RED in 2015 for monitoring microservices.
- (The USE Method) Before RED, the talk recaps USE (popularized by Brendan Gregg) as a checklist applied to every resource: utilization (share of time busy), saturation (work waiting, often a queue length), errors (count of error events). Wilkie calls it useful for finding what you do not know, but abstract: applying it to memory is awkward (do caches count as used? what is a memory error?).
- (The RED Method) Wilkie created RED after a new colleague asked about his monitoring philosophy. His reasoning: USE fits hardware, network and disks, but does not really fit services, so a service-oriented method was needed. RED means three numbers per service:
  - Rate: the number of requests per second.
  - Errors: the number of those requests that are failing.
  - Duration: the amount of time those requests take.
  The page's bullet list introduces them with "for every resource, monitor", which is a slip of wording: the context is clearly "every service".
- (The RED Method) The speaker's advice: everyone should know the request rate, the error rate, and some distribution of latency for each service, modeled the same way for every service. Consistency across services is said to let a team scale its operations and put people on call for code they did not write.
- (The RED Method) RED is described as a proxy for how happy customers are: high error rate means users see failed page loads, high duration means a slow site. The page says these are good metrics for alerts and for measuring an SLA.
- (The Four Golden Signals) The page maps Google's golden signals (latency, traffic, errors, saturation) to RED and says they are basically the same, plus saturation. It gives one way to measure saturation on Kubernetes: a service's CPU use as a fraction of its quota (0 to 1), which can drive an alert.
- (Two Sides of the Same Coin) Recommendation to use both: RED for the user's view of a service, USE for the health of the machines. Described as two complementary views of one system.
- (Footer) "Copyright 2026 (c) Grafana Labs", with links to terms and legal pages; no separate license text for blog posts. The registry records it as all-rights-reserved, rewrite-only.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| RED = Rate (requests per second), Errors (number of failing requests), Duration (time those requests take) | The RED Method | These are the exact three words; the page capitalizes them as Rate, Errors, Duration. Quote at most a short phrase |
| RED created in 2015 by Tom Wilkie | Introduction | Per the speaker's own recap, not independently checked |
| Golden signals are "basically" RED plus saturation | The Four Golden Signals | The mapping is the page's: Rate to Traffic, Duration to Latency, Errors to Errors |
| Use USE for resources (machines) and RED for services | The RED Method; Two Sides of the Same Coin | |
| Saturation proxy: CPU used / CPU quota as a value from 0 to 1 | The Four Golden Signals | A Kubernetes example, not needed for Unit 0 |

## Relevant to concepts

- `basic-monitoring` (unit 0), objective 2 "Bisa memilih metrik minimum untuk memantau sebuah service (rate, error, duration)": SUPPORTED, and it is the only source in the registry that uses exactly the words rate, errors and duration. It states the three metrics, what each measures, and why they are enough as a minimum (they track what the user experiences). It does not explain how to compute them or which duration statistic to keep (it says "some distribution of latency", not percentiles); pair with `google-sre-book-monitoring-ch6` (separate success and failure latency, tail) and `prometheus-instrumentation-practices` for the how. If the lesson uses the acronym RED it must cite this source.
- `single-machine-limits`, objective 2 (USE on one resource): it restates USE in one paragraph and says USE is for resources and RED for services, a useful bridge sentence, but `gregg-use-method` is the primary source.
- Unit 6 observability concept (current mapping in `concepts.yaml`): RED vs USE vs golden signals comparison.

## Warnings

- It is a third-hand summary: a blog post by a different author about a conference talk. Quotations are of the speaker, not of a written method specification. Good enough for a definition of the acronym; do not cite it for how to implement.
- Written for microservices and Kubernetes; for Unit 0, say "a service" and use a single app as the example.
- "Errors" is defined as a count of failing requests in the list, but the narrative says "error rate"; a lesson should say error rate (failing requests per second or as a fraction of requests) and pick one.
- The wording "for every resource" under RED is an inconsistency on the page.
