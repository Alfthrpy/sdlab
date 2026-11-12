# Curriculum

Files in this folder are created in milestone M2. Structural fields are English; learner-facing text (concept `title`, `objectives`) is Indonesian.

| File | Created in ticket | Schema |
| --- | --- | --- |
| `concepts.yaml` | P1-020, P1-021, P1-023 | `docs/conventions/content-schema.md` §2 |
| `case-studies.yaml` | P1-022 | `docs/conventions/content-schema.md` §3 |

## Reader prerequisite knowledge

Readers (students and junior engineers, ADR 0004) are assumed to know only:

- Basic programming: variables, functions, loops, common data structures.
- Basic arithmetic and ratios (percentages, orders of magnitude); Unit 1 explains any other math it needs.
- HTTP basics: request/response, methods, status codes.
- Basic SQL: `SELECT`, `INSERT`, `UPDATE`, and simple joins.

They have not operated a distributed system. **Unit 1 assumes nothing beyond this list.** Every other term (server, latency, replica, queue, ...) is explained on first use, and no concept may depend on knowledge outside this list unless a prerequisite concept covers it.

## Units (starting point from the master plan)

| Unit | Core concepts |
| --- | --- |
| 1. Foundations | Latency vs. throughput, back-of-envelope estimation, Little's law, percentiles, SLI/SLO |
| 2. Building blocks | Load balancer, reverse proxy, cache, CDN, API (REST/gRPC), idempotency |
| 3. Data | Data models, indexes, replication, partitioning, transactions & isolation |
| 4. Async & streams | Message queue, log, delivery semantics, outbox, backpressure |
| 5. Consistency & coordination | CAP/PACELC, consistency models, consensus, locks & leases, time & clocks |
| 6. Production reliability | Timeout, retry + backoff + jitter, circuit breaker, load shedding, cascading & metastable failure, observability, safe deploys |
