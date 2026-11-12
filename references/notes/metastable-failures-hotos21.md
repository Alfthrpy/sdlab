---
source: metastable-failures-hotos21
read_by: agent
date: 2026-11-12
sections_read: ["Abstract", "1 Introduction", "2 Case studies (2.1-2.4)", "3 Approaches to handling metastability", "4 Discussion and research directions"]
---

# Notes: Metastable Failures in Distributed Systems (HotOS '21)

> Notes are in English and in your own words. Read from the free PDF text (sigops.org copy); the figures were not examined.

## Key points

- (Abstract, 1) A metastable failure is a bad state that persists after the trigger that caused it is gone. Goodput is very low, and a sustaining effect (usually extra work or lower efficiency) keeps the system there. Failures that heal when the trigger ends (for example a plain DoS attack) do not count.
- (1) Three states: stable, vulnerable (healthy but exposed to a trigger), metastable. Many systems run in the vulnerable state on purpose because it is more efficient.
- (1) Blaming the trigger is a common mistake; the paper treats the sustaining feedback loop as the true root cause. Loops tend to be stronger at larger scale, so tests at small scale can miss them.
- (2.1) Retries example: a web tier with one retry after 1 s in front of a database that is fast below about 300 QPS. A 10 s network outage causes a burst, retries double the load, every query times out, and the system stays down until load or retries drop.
- (2.1) Failover can also spread a failure to healthy replicas when shards are laid out differently.
- (2.2) Look-aside cache: losing a cache with a 90% hit rate means 10x more database queries; the app's timeouts stop it from refilling the cache, so the cache stays cold. A read-through cache can keep filling in the background.
- (2.3) Slow error handling: error paths (stack traces, DNS lookups, logging) are expensive and add load exactly when resources are short.
- (2.4) Link imbalance: a connection pool policy (most recently used first) pushed all traffic onto one congested link; the fix was a one-line policy change after years of outages.
- (3) Mitigations they list: change policies under overload (retry budgets, disabling retries and failover, LIFO queues, smaller queues, priorities, load shedding, circuit breaker), lower priority for retried requests, fast error paths, outlier hygiene, spare capacity via autoscaling, and stress tests in production-like conditions.
- (3) Priorities help but do not bound work amplification: one system with extra retries and failover had worst-case amplification above 100x.
- (4) Ideas for prediction: a "characteristic metric" that stays abnormal while the loop runs (queueing delay is more robust than QPS), "hidden capacity" (where the system can still self-heal) versus advertised capacity, and trigger intensity.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Example DB fast below about 300 QPS; app at 280 QPS; 10 s outage; retries double load to 560 QPS | 2.1 | Simplified illustration, not measured data |
| Hit rate 90% turns 300 QPS database limit into 3,000 QPS app capacity | 2.2 | Illustration; loses 10x when cache lost |
| Worst-case work amplification above 100x in one geo-distributed system | 3 (Prioritization) | Anecdote, system not named |
| Link imbalance failure resisted diagnosis for more than two years | 2.4 | Paper's own account |

## Relevant to concepts

- `metastable-failure`: definition, three states, trigger versus sustaining effect.
- `retry-storm` and `retry-budget`: section 2.1 plus section 3.
- `load-shedding`: why it is the standard recovery action.
- `cache-stampede` / cold cache: section 2.2.
- ladder trigger: when retries, caches and failover were added for reliability and a short blip now leaves the system stuck.

## Warnings

- Vision paper: examples are simplified versions of Facebook-era failures, and the paper itself says a systematic prevention method is an open problem.
- Do not state the numbers as measurements; they are teaching examples.
- The ACM landing page was not openable (HTTP 403); the PDF copy was used.
