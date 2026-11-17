---
id: P1-083
title: "Close Unit 0 objective-to-source gaps found while writing reading notes"
milestone: M4
type: research
owner: agent
review: agent
status: done
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

- [x] Every gap 1-7 is closed (source added and noted, source mapped, objective narrowed) or accepted with a reason in the Notes
- [x] Gap 8 decided in the Notes
- [x] `python scripts/validate.py` passes

## Notes

Work: two researcher runs (connection-pooling cluster; capacity and request cluster) opened the pages and wrote 22 new reading notes (15 for new sources, 7 for approved sources that had none: `grafana-red-method`, `system-design-primer`, `mdn-transport-layer-security`, `mdn-tcp-handshake-glossary`, `aws-route53-how-dns-routes-traffic`, `brooker-telling-stories-littles-law`, and `recall-ai` was dropped, see below). 15 new `candidate` entries are in `references/registry.yaml` (owner approves candidates later, as in P1-072); `units` gained 0 on five existing sources. No objective was narrowed.

**Decision per gap** (sources mapped in `curriculum/concepts.yaml`):

1. `connection-pooling` obj 1: mapped `pg-docs-connect-estab`, `brandur-postgres-connections-2018`, `freund-connection-scalability-2020`. Support is **qualitative only** (a backend process per connection, per-connection memory, TLS and authentication named but not timed). The lesson must not invent millisecond figures; a lab may use the author's own measurement.
2. `connection-pooling` obj 2: mapped `heroku-concurrency-database-connections` and `brandur-postgres-connections-2018` (dividing a DB limit across instances, deploy overlap) and `brooker-telling-stories-littles-law` (L = arrival rate x W). **The application to a pool (hold time as W, plus headroom) is the author's own arithmetic.** No cloud-vendor source for splitting a limit was found (Cloud SQL page rejected: it says it does not cover it).
3. `connection-pooling` obj 3: mapped `pgbouncer-usage`, `pgbouncer-config`, `hikaricp-readme`, `hikaricp-wiki-dropwizard-metrics` (cl_waiting, maxwait, query_wait_timeout, pending threads, Wait vs Usage). The rule "high wait with high usage means slow queries or leaks, high wait with low usage means a small pool" is the author's reading of the metrics. Do not name a HikariCP exception message unless quoted from a source.
4. `request-lifecycle` obj 1 and 2: mapped `aws-route53-how-dns-routes-traffic` (DNS), `mdn-transport-layer-security` (TLS), `web-dev-ttfb` (phases that make up TTFB), `pg-docs-query-path` (database stage), `craver-stack-overflow-architecture-2016` (server-side where-time-goes totals). **Per-stage timing numbers in exercises are the author's own scenario**, kept at order of magnitude; no source gives typical DNS or TLS times. `mdn-navigation-resource-timings` (new candidate) and `mdn-tcp-handshake-glossary` have notes but are not mapped.
5. `app-plus-database` obj 1: mapped `system-design-primer` (2.5 million seconds per month conversion, users to requests per second example) and `robustperception-peak-to-mean-ratio` (peak-to-mean 1.6-1.7 for a global audience). **Requests per user per day and the threshold at which one box suffices are the author's explicit assumptions**; a single-time-zone product peaks harder.
6. `basic-monitoring` obj 2: mapped `grafana-red-method`, which uses the exact words Rate, Errors, Duration. A lesson that says "RED" must cite it; the SRE golden signals and Prometheus pages stay for the how.
7. `single-machine-limits` obj 3: mapped `aws-docs-ec2-memory-optimized-specs`, `aws-docs-ec2-general-purpose-specs`, `aws-ec2-price-list-us-east-1` (largest type u7inh-32tb.480xlarge, 1920 vCPUs, 32768 GiB; m7i.48xlarge 192 vCPUs, 768 GiB, USD 9.6768 per hour; us-east-1, On-Demand Linux, price file of 2026-11-14). **Dated figures: state the date and region in the lesson and re-read them before publishing.** The "when to scale" reasoning stays with `gregg-use-method`. Owner note: the price source is a 460 MB data file, not stored in the repo; if unwanted, cite instance sizes only and treat prices as illustration.
8. Gap 8 accepted as the author's own reasoning, no new source: `simple-deploys` obj 2 (a restart is stop then start per systemd `ExecStop=`; ways to shorten it from Fowler and systemd), `backup-recovery` obj 2 (RPO and RTO defined by Atlassian and SRE ch. 26; deriving a schedule from them is the author's arithmetic), `app-plus-database` obj 2 (twelve-factor IV and VI).

**Not mapped, deliberately:** `recall-ai-postgres-postmaster-2026` (extreme workload, optional; entry and note removed, can be re-added if a measured postmaster figure is wanted). `connection-pooling` now lists 13 sources, more than a 500-word lesson can use: the writer picks per objective (obj 1: `pg-docs-connect-estab`, `brandur`; obj 2: existing two plus `heroku`, `brooker`; obj 3: `pgbouncer-usage`, `hikaricp-wiki-dropwizard-metrics`, `hikaricp-readme`).

**Verification.** `source-verifier` reopened 8 of the 15 new sources (all three AWS entries, brandur, heroku, pgbouncer-usage, web-dev-ttfb, robustperception) and the mapping: pass with minor fixes. All numbers and prices matched (the price file was downloaded in the scratchpad, 481 MB, and deleted). Fixes applied: the two `docs.aws.amazon.com` entries are CC-BY-SA-4.0 per the AWS Site Terms (not all-rights-reserved), three wording fixes in notes. `verified_on: 2026-11-17` is set for those 8 only; **7 new entries were not sampled and have empty `verified_on`**: `pgbouncer-config`, `hikaricp-readme`, `hikaricp-wiki-dropwizard-metrics`, `pg-docs-connect-estab`, `freund-connection-scalability-2020`, `mdn-navigation-resource-timings`, `pg-docs-query-path`. Licenses of `pg-docs-*` follow `pg-docs-indexes-intro` and `mdn-navigation-resource-timings` follows the other MDN entries; neither legal page was reopened. These seven should be reopened before the owner approves candidates.

Spin-off: P1-084 (low), older docs.aws.amazon.com entries likely carry the wrong license. The same note applies to the pre-existing `hikaricp-about-pool-sizing` note, which still calls obj 3 "not supported"; the new sources close it.

