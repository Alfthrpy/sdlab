---
source: hikaricp-readme
read_by: agent
date: 2026-11-17
sections_read: ["Configuration (knobs): connectionTimeout, maximumPoolSize, leakDetectionThreshold, metricRegistry, registerMbeans, poolName", "LICENSE file"]
---

# Notes: HikariCP README (configuration reference)

> Notes are in English and in your own words. README read from the raw file (`curl` of README.md on the dev branch, 2026-11-17). The repository LICENSE file is the Apache License 2.0 (confirmed by `curl` of LICENSE and by the GitHub license API). The README itself shows no date or author.

## Key points

- (connectionTimeout) How long a caller waits for a connection from the pool before an exception is thrown. Default 30,000 ms; minimum accepted 250 ms.
- (maximumPoolSize) Upper bound on connections in the pool, idle plus in use, which is also the maximum number of real connections to the database from this pool. When the pool is at that size with none idle, `getConnection()` blocks up to connectionTimeout. Default 10. The page points to the "About Pool Sizing" wiki page for choosing a value.
- (leakDetectionThreshold) If a connection stays out of the pool longer than this, a leak warning is logged. Default 0 (off); minimum 2,000 ms when enabled.
- (metricRegistry / registerMbeans) Pool metrics are exposed through a Dropwizard registry or JMX, both opt-in.
- (poolName) Naming a pool gives stable metric names.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| connectionTimeout default 30000 ms (30 s), min 250 ms | connectionTimeout | Defines how long a request can sit waiting before failing |
| maximumPoolSize default 10 | maximumPoolSize | |
| leakDetectionThreshold default 0 (disabled), min 2000 ms | leakDetectionThreshold | A cause of "exhaustion" that is really connections never returned |

## Relevant to concepts

- `connection-pooling` objective 3 (diagnose exhaustion): PARTLY. It defines the mechanism (pool full, caller blocks up to connectionTimeout, then exception) and a leak-detection tool. It does not list exhaustion symptoms or a diagnosis routine; the exact exception text is not in the README (the "Bad Behavior: Handling Database Down" wiki page shows "Timeout after 5027ms of waiting for a connection" in a DB-down test).
- `connection-pooling` objective 2: gives the default and the pointer to the sizing page only.

## Warnings

- Java/JDBC specific. The README is long and has many options irrelevant to Unit 0.
- The repository is Apache-2.0, so README text is reusable with attribution, but we still rewrite.
- Defaults come from the dev branch on the day of reading; no version string on the page.
