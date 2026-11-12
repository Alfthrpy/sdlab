# Curriculum

Files in this folder are created in milestone M2. Structural fields are English; learner-facing text (concept `title`, `objectives`) is Indonesian.

| File | Created in ticket | Schema |
| --- | --- | --- |
| `concepts.yaml` | P1-020, P1-021, P1-023 | `docs/conventions/content-schema.md` §2 |
| `case-studies.yaml` | P1-022 | `docs/conventions/content-schema.md` §3 |

## Reader prerequisite knowledge

Readers (students and junior engineers, ADR 0004) are assumed to know only:

- Basic programming: variables, functions, loops, common data structures.
- Basic arithmetic and ratios (percentages, orders of magnitude); Units 0 and 1 explain any other math they need.
- HTTP basics: request/response, methods, status codes.
- Basic SQL: `SELECT`, `INSERT`, `UPDATE`, and simple joins.

They have not operated a distributed system. **Unit 0 assumes nothing beyond this list**, and later units build only on earlier ones. Every other term (server, latency, replica, queue, ...) is explained on first use, and no concept may depend on knowledge outside this list unless a prerequisite concept covers it.

## The growth ladder

Per ADR 0004 Amendment 1, the course is taught as a ladder: start with a single-server backend (Unit 0), measure it (Unit 1), and add each distributed-systems idea (Units 2–6) as what you reach for when the previous stage stops being enough. Two consequences for every concept in Units 1–6:

- **Trigger.** The concept records a `trigger` (see `content-schema.md` §2): the symptom or number that says it is time to use it, for example a metric crossing a limit. Triggers feed lessons, questions, and labs.
- **Honest simplicity.** The lesson says plainly when the simpler stage is still enough (the existing "when not to use it" section).

## Units (starting point from the master plan)

| Unit | Core concepts |
| --- | --- |
| 0. Single-server backend | The request lifecycle on one machine, one app plus one database, indexes and query basics, connection pooling, backups and recovery basics, simple deploys, basic monitoring (logs, metrics, health checks), and the limits of one machine (CPU, memory, disk, connections) and how to tell you are hitting them |
| 1. Foundations | Latency vs. throughput, back-of-envelope estimation, Little's law, percentiles, SLI/SLO; how to measure whether a stage is still enough |
| 2. Building blocks | Load balancer, reverse proxy, cache, CDN, API (REST/gRPC), idempotency |
| 3. Data | Data models, indexes, replication, partitioning, transactions & isolation |
| 4. Async & streams | Message queue, log, delivery semantics, outbox, backpressure |
| 5. Consistency & coordination | CAP/PACELC, consistency models, consensus, locks & leases, time & clocks |
| 6. Production reliability | Timeout, retry + backoff + jitter, circuit breaker, load shedding, cascading & metastable failure, observability, safe deploys |
