# Curriculum

Files in this folder are created in milestone M2. Structural fields are English; learner-facing text (concept `title`, `objectives`) is Indonesian.

| File | Created in ticket | Schema |
| --- | --- | --- |
| `concepts.yaml` | P1-020, P1-021, P1-023 | `docs/conventions/content-schema.md` §2 |
| `case-studies.yaml` | P1-022 | `docs/conventions/content-schema.md` §3 |

## Units (starting point from the master plan)

| Unit | Core concepts |
| --- | --- |
| 1. Foundations | Latency vs. throughput, back-of-envelope estimation, Little's law, percentiles, SLI/SLO |
| 2. Building blocks | Load balancer, reverse proxy, cache, CDN, API (REST/gRPC), idempotency |
| 3. Data | Data models, indexes, replication, partitioning, transactions & isolation |
| 4. Async & streams | Message queue, log, delivery semantics, outbox, backpressure |
| 5. Consistency & coordination | CAP/PACELC, consistency models, consensus, locks & leases, time & clocks |
| 6. Production reliability | Timeout, retry + backoff + jitter, circuit breaker, load shedding, cascading & metastable failure, observability, safe deploys |
