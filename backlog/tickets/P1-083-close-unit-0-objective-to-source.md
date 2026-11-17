---
id: P1-083
title: "Close Unit 0 objective-to-source gaps found while writing reading notes"
milestone: M4
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-035a]
estimate: 1
outputs: []
---

## Context

P1-035a wrote reading notes for the 28 sources mapped to Unit 0 and checked each Unit 0 objective against them. Some objectives are not supported by any mapped source. Under ADR 0007 Unit 0 ships first, so these must be closed (a source added, an objective narrowed, or the gap accepted as the writer's own arithmetic) before the Unit 0 concept tickets (P1-048a onward) write lessons. This ticket is a sibling of P1-072 and P1-081. Do not fill gaps from memory: a new source goes through `references/registry.yaml` and verification (AGENTS.md rule 2).

**Gaps (concept: objective, what is missing, options):**

1. `connection-pooling` obj 1 (why a new connection per request wastes resources): no mapped source explains connection setup cost; the PostgreSQL wiki covers the harm of too many concurrent connections, and `pg-docs-connections` does not mention pooling or per-connection processes. Needs a new source or a narrowed objective.
2. `connection-pooling` obj 2 (size a pool from cores, query load and DB connection limit, then validate by measurement): the wiki and HikariCP give the core-based rule of thumb and "load-test around the formula"; nothing gives the query-load part (arrival rate x query time) or sharing `max_connections` across several app instances. Options: a source, or narrow the objective to the sourced inputs and treat the load part as the author's own arithmetic.
3. `connection-pooling` obj 3 (diagnose an exhausted pool): not supported by the notes written so far. HikariCP treats waiting threads as the desired state and gives only the pool-locking minimum; PgBouncer's usage and configuration pages were not opened. Check those pages first, then decide.
4. `request-lifecycle` obj 1 and 2: MDN and the nginx guide cover the HTTP flow and the proxy-to-app hop; DNS, TLS and the database stage are not covered, and no mapped source gives per-stage timing data. The Stack Overflow architecture post (`craver-stack-overflow-architecture-2016`, already read) has a per-stage time table that would fit; map it, or accept timing questions as the author's own scenario.
5. `app-plus-database` obj 1 (calculate from users and requests per second that one app and one database suffice): SQLite gives a rule of thumb (about 100K hits per day) and Craver gives a large-site average; no mapped source teaches users to requests per second or a peak factor, and the AWS primer has no numbers. Needs a sourced rule of thumb, or an explicit own-computation policy.
6. `basic-monitoring` obj 2 (minimum metrics: "rate, error, duration"): neither `google-sre-book-monitoring-ch6` (four golden signals: latency, traffic, errors, saturation) nor `prometheus-instrumentation-practices` (queries, errors, latency) uses the words RED, rate or duration. `grafana-red-method` is in the registry but mapped only to the Unit 6 observability concept. Options: map it to `basic-monitoring` (after checking it is approved), or reword the objective with the sourced terms. A lesson that says "RED" must cite the source that uses it.
7. `single-machine-limits` obj 3 (decide whether vertical scaling is enough from utilisation and machine size or price limits): USE-method utilisation reading is sourced (`gregg-use-method`); the machine size ceiling is only a 2015 maximum in the AWS primer (40 vCPU, 244 GB) and Craver's hardware numbers. Needs a current, sourced size ceiling, or the objective is narrowed to "from utilisation data".
8. Partly supported, probably acceptable with the author's own reasoning (decide while closing the above, no new source required unless the owner wants one): `simple-deploys` obj 2 (why a direct deploy causes brief downtime: the systemd ExecStop paragraph says a restart is stop then start; Fowler does not explain the mechanism), `backup-recovery` obj 2 (RPO and RTO to a backup schedule: Atlassian defines both and shows results; MySQL never uses the terms; no method to derive a schedule), `app-plus-database` obj 2 (twelve-factor VI and IV support it; SQLite does not).

**Registry follow-ups:** done in P1-035a after the source-verifier confirmed them (version string of the two PostgreSQL pages, AWS primer footer, notes of twelve-factor-app and mysql-84-backup-recovery). Nothing left for this ticket.

## Tasks

1. Work through gaps 1-7 in order of the Unit 0 concepts (`request-lifecycle` first). For each, decide with the `curriculum-designer` role: add a source (researcher: open the page, then record it), map an existing source, narrow the objective in `concepts.yaml`, or accept it as the author's own arithmetic (and say so in the Notes).
2. Open the PgBouncer usage/configuration pages and the HikariCP wiki pages on pool locking before you look for new sources for gap 3.
3. Reopen a sample of any new source (source-verifier). Update the reading notes for every newly mapped source.

## Done criteria

- [ ] Every gap 1-7 is closed (source added and noted, source mapped, objective narrowed) or accepted with a reason in the Notes
- [ ] Gap 8 decided in the Notes
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
