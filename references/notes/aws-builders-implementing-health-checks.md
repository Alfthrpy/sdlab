---
source: aws-builders-implementing-health-checks
read_by: agent
date: 2026-11-12
sections_read: ["Small failures with outsized impact", "Health check tradeoffs", "Ways to measure health", "Reacting safely to health check failures", "Balancing dependency health checks with the scope of impact", "Real things that have gone wrong with health checks", "Conclusion"]
---

# Notes: Implementing health checks (Amazon Builders' Library)

> Notes are in English and in your own words. Re-opened 2026-11-12; section names are the headings shown on the page. The fetch tool summarizes pages, so re-read exact wording before quoting.

## Key points

- (Ways to measure health) Liveness checks: basic connectivity and process presence (TCP port, HTTP 200), usually done by a load balancer or external monitor.
- (Ways to measure health) Local health checks: exercise resources not shared with peers (for example disk read/write, an end-to-end request through the proxy into the app), so failures are unlikely to hit the whole fleet at once.
- (Ways to measure health) Dependency health checks: test whether the server can use what it needs. They can catch local problems, but give false positives when the dependency itself is down.
- (Ways to measure health) Anomaly detection compares each server to its peers to spot outliers. This is fleet-level and beyond Unit 0.
- (Small failures with outsized impact) A broken server that answers errors quickly can look better than healthy peers and attract more traffic.
- (Health check tradeoffs) One bad server in a ten-server fleet can cost about 10% availability; the tension is between thorough checks and false positives that affect the whole fleet.
- (Reacting safely to health check failures) "Fail open": if every server looks unhealthy, keep sending traffic to all of them. The article says Amazon teams tend to keep fast-acting load balancer checks local, with deeper checks handled by centralized systems.
- (Health checks without a circuit breaker, a subsection of the above) Automation that acts on health checks should use thresholds, rate limits and feedback that brings in humans when limits are crossed.
- (Prioritize your health, a subsection of the above) An overloaded server may answer health checks too slowly and be removed, pushing load onto the rest.
- (Balancing dependency health checks with the scope of impact) A dependency check can turn a soft dependency into a hard one.
- (Real things that have gone wrong) Examples listed: deployments, asynchronous processors, disks filling up, zombies.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Published 2019-12-05 | page header | Author shown only as "David" |
| One bad server in a ten-server fleet can drop availability to about 90% | Health check tradeoffs | Illustrates why fleet size matters |

## Relevant to concepts

- `health-checks`: liveness vs. local vs. dependency; for Unit 0 a simple endpoint plus a database ping.
- Later (Unit 2): load balancing and automatic removal.

## Warnings

- Aimed at large fleets; most of the reaction and anomaly-detection material needs multiple servers and belongs in Unit 2+.
- Whether a Unit 0 single server should fail its check when the database is down is a judgment the article does not settle for single-server setups.
