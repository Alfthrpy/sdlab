# Source coverage and gap list

Input for gate G0 (P1-019). Produced by P1-017 on 2026-11-13 from `references/registry.yaml` (163 entries, all `candidate`, all with `verified_on` after P1-016 and P1-071).

## How to read this

- **Sub-topics** are the core concepts of each unit in `curriculum/README.md` (the master-plan table). The curriculum itself does not exist yet (M2), so these rows are the starting point and may be split or merged by P1-020.
- **Matching rule:** an entry covers a sub-topic when it lists that unit in `units` and shares at least one `topics` tag with the sub-topic's tag set. Tags are matched mechanically, so a hit means "relevant", not "good". Counts can include entries that only touch the sub-topic.
- **Columns:** `T1` book, `T2d` official docs (Tier 2, `type: docs`), `T2a` other Tier 2 (articles, talks, repo), `T3` papers, `T4` postmortems, `T5` open material, `T6` interview maps (`map-only`, never counted as coverage). `Free` = number of Tier 1-5 matches with `access: free` (`partial` and `paywalled` are not counted). `Concept` = free Tier 1-3 matches that are not official docs (article, paper, talk, repo; paywalled books such as DDIA do not count), because official docs describe one product and are a weak base for teaching the general idea.
- **Caveat on counts:** `Concept` and `Free` count entries that are abstract-only, unread, or flagged in their notes (for example `nishtala-memcache-nsdi13`, `little-2011-littles-law-50th` as a mirror with unverified posting rights, `reactive-manifesto` as vocabulary only, `sre-book-handling-overload-ch21` matching Back-of-envelope only by tag). Rows can look healthier than they are; sections A and B correct for the known cases.
- A gap is declared when a sub-topic has **no free Tier 1-2 source** (ticket rule), or **fewer than two free concept sources** (stricter rule added here), or a note from a research ticket says the existing sources are thin. The ticket rule alone finds nothing: every sub-topic has at least one free Tier 1-2 entry, mostly official docs.

## Matrix

### Unit 0 - Single-server backend

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Request lifecycle on one machine | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | `nginx-reverse-proxy-admin-guide`, `mdn-http-overview` |
| One app + one database | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | `twelve-factor-app`, `sqlite-appropriate-uses` |
| Indexes and query basics | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 4 | 1 | `use-the-index-luke`, `pg-docs-indexes-intro`, `pg-docs-using-explain`, `mysql-84-optimization-indexes` |
| Connection pooling | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 5 | 2 | `pg-wiki-number-of-connections`, `hikaricp-about-pool-sizing`, `pg-docs-connections`, `pg-docs-kernel-resources` |
| Backups and recovery basics | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | `pg-docs-backup-restore`, `mysql-84-backup-recovery` |
| Simple deploys | 0 | 1 | 2 | 0 | 1 | 0 | 0 | 4 | 2 | `twelve-factor-app`, `fowler-bluegreen-deployment`, `heroku-june-10-outage-2025`, `systemd-service-man` |
| Basic monitoring (logs, metrics, health checks) | 1 | 3 | 3 | 0 | 0 | 0 | 0 | 7 | 4 | `google-sre-book-monitoring-ch6`, `twelve-factor-app`, `gregg-use-method`, `aws-builders-implementing-health-checks` |
| Limits of one machine and how to detect them | 1 | 3 | 2 | 0 | 0 | 0 | 0 | 6 | 3 | `google-sre-book-monitoring-ch6`, `gregg-use-method`, `craver-stack-overflow-architecture-2016`, `pg-docs-kernel-resources` |

### Unit 1 - Foundations

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Latency vs. throughput | 0 | 1 | 3 | 2 | 0 | 0 | 0 | 6 | 5 | `brooker-tail-latency-matters`, `tene-how-not-to-measure-latency`, `aws-builders-load-shedding`, `tail-at-scale-cacm13` |
| Back-of-envelope estimation | 1 | 0 | 1 | 1 | 0 | 0 | 2 | 3 | 3 | `sre-book-handling-overload-ch21`, `brooker-telling-stories-littles-law`, `dean-software-engineering-advice-slides` |
| Little's law | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 2 | 2 | `brooker-telling-stories-littles-law`, `little-2011-littles-law-50th` |
| Percentiles and tail latency | 1 | 1 | 2 | 1 | 0 | 0 | 0 | 5 | 4 | `sre-book-slo-ch4`, `brooker-tail-latency-matters`, `tene-how-not-to-measure-latency`, `tail-at-scale-cacm13` |
| SLI / SLO | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | `google-sre-book`, `sre-book-slo-ch4`, `sre-book-embracing-risk-ch3`, `sre-workbook-implementing-slos` |
| Measuring whether a stage is still enough | 4 | 0 | 3 | 0 | 0 | 0 | 0 | 7 | 7 | `google-sre-book`, `google-sre-book-monitoring-ch6`, `sre-workbook-implementing-slos`, `sre-book-handling-overload-ch21` |

### Unit 2 - Building blocks

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Load balancer | 3 | 2 | 1 | 1 | 0 | 1 | 0 | 8 | 5 | `google-sre-book`, `sre-book-handling-overload-ch21`, `sre-book-load-balancing-frontend-ch19`, `aws-builders-load-shedding` |
| Reverse proxy | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 3 | 0 | `system-design-primer`, `nginx-reverse-proxy-admin-guide`, `envoy-docs-lb-overview` |
| Cache | 0 | 4 | 1 | 2 | 0 | 1 | 0 | 8 | 3 | `aws-builders-caching-challenges`, `nishtala-memcache-nsdi13`, `fielding-rest-dissertation-ch5`, `system-design-primer` |
| CDN | 0 | 3 | 0 | 0 | 1 | 1 | 0 | 5 | 0 | `system-design-primer`, `fastly-outage-2021-06-08`, `mdn-http-caching`, `mdn-cdn-glossary` |
| API design (REST / gRPC) | 0 | 6 | 3 | 1 | 0 | 1 | 0 | 11 | 4 | `aws-builders-idempotent-apis`, `stripe-blog-idempotency`, `microsoft-rest-api-guidelines`, `fielding-rest-dissertation-ch5` |
| Idempotency | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 5 | 2 | `aws-builders-idempotent-apis`, `stripe-blog-idempotency`, `stripe-docs-idempotent-requests`, `ietf-idempotency-key-header-draft` |

### Unit 3 - Data

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Data models | 1 | 5 | 0 | 3 | 0 | 0 | 0 | 8 | 3 | `ddia-2e`, `dynamo-sosp07`, `bigtable-osdi06`, `codd-relational-model-1970` |
| Indexes (data-structure level) | 0 | 2 | 1 | 2 | 0 | 0 | 0 | 5 | 3 | `use-the-index-luke`, `bigtable-osdi06`, `oneil-lsm-tree`, `pg-docs-index-types` |
| Replication | 1 | 5 | 0 | 1 | 0 | 1 | 0 | 7 | 1 | `ddia-2e`, `dynamo-sosp07`, `system-design-primer`, `pg-docs-high-availability` |
| Partitioning / sharding | 1 | 4 | 1 | 3 | 0 | 1 | 0 | 9 | 4 | `ddia-2e`, `notion-sharding-postgres-2021`, `dynamo-sosp07`, `bigtable-osdi06` |
| Transactions and isolation | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 4 | 1 | `ddia-2e`, `berenson-critique-ansi-isolation-1995`, `jepsen-consistency-models`, `pg-docs-transaction-iso` |

### Unit 4 - Async & streams

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Message queue | 0 | 6 | 2 | 0 | 0 | 0 | 0 | 8 | 2 | `aws-builders-load-shedding`, `aws-builders-insurmountable-queue-backlogs`, `rabbitmq-tutorial-work-queues`, `aws-sqs-visibility-timeout` |
| Log / event streaming | 0 | 4 | 0 | 1 | 0 | 0 | 0 | 5 | 1 | `kafka-netdb-2011`, `kafka-docs-design`, `kafka-docs-introduction`, `kafka-docs-basic-operations` |
| Delivery semantics | 0 | 7 | 4 | 1 | 0 | 0 | 0 | 12 | 5 | `confluent-exactly-once-2017`, `microservices-io-transactional-outbox`, `microservices-io-idempotent-consumer`, `debezium-outbox-pattern-2019` |
| Outbox and change data capture | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 3 | 2 | `microservices-io-transactional-outbox`, `debezium-outbox-pattern-2019`, `debezium-docs-outbox-event-router` |
| Backpressure | 0 | 4 | 2 | 0 | 0 | 0 | 0 | 6 | 2 | `aws-builders-insurmountable-queue-backlogs`, `reactive-manifesto`, `kafka-docs-basic-operations`, `azure-queue-based-load-leveling` |

### Unit 5 - Consistency & coordination

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP / PACELC | 1 | 0 | 1 | 2 | 0 | 0 | 0 | 4 | 4 | `sre-book-managing-critical-state-ch23`, `kleppmann-stop-calling-cp-ap-2015`, `brewer-cap-twelve-years-2012`, `abadi-pacelc-2012` |
| Consistency models | 0 | 3 | 2 | 1 | 0 | 0 | 0 | 6 | 3 | `kleppmann-stop-calling-cp-ap-2015`, `vogels-eventually-consistent-2008`, `dynamo-sosp07`, `jepsen-consistency-models` |
| Consensus | 1 | 3 | 1 | 6 | 0 | 0 | 0 | 11 | 8 | `sre-book-managing-critical-state-ch23`, `kleppmann-distributed-locking-2016`, `raft-extended-paper`, `lamport-paxos-made-simple` |
| Locks, leases, fencing | 1 | 7 | 1 | 3 | 0 | 0 | 0 | 12 | 5 | `sre-book-managing-critical-state-ch23`, `kleppmann-distributed-locking-2016`, `raft-extended-paper`, `chubby-lock-service` |
| Time and clocks | 0 | 1 | 1 | 4 | 0 | 0 | 0 | 6 | 5 | `cockroach-living-without-atomic-clocks`, `dynamo-sosp07`, `lamport-time-clocks-1978`, `spanner-osdi12` |

### Unit 6 - Production reliability

| Sub-topic | T1 | T2d | T2a | T3 | T4 | T5 | T6 | Free | Concept | Main sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Timeout | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 3 | 2 | `sre-book-addressing-cascading-failures-ch22`, `aws-builders-timeouts-retries`, `grpc-docs-deadlines` |
| Retry + backoff + jitter | 2 | 4 | 3 | 2 | 2 | 0 | 0 | 13 | 7 | `sre-book-handling-overload-ch21`, `sre-book-addressing-cascading-failures-ch22`, `aws-builders-timeouts-retries`, `aws-builders-idempotent-apis` |
| Circuit breaker | 0 | 2 | 2 | 0 | 1 | 0 | 0 | 5 | 2 | `aws-builders-timeouts-retries`, `fowler-circuit-breaker`, `github-availability-report-2026-08`, `azure-circuit-breaker-pattern` |
| Load shedding | 2 | 1 | 1 | 2 | 3 | 0 | 0 | 9 | 5 | `sre-book-handling-overload-ch21`, `sre-book-addressing-cascading-failures-ch22`, `aws-builders-load-shedding`, `metastable-failures-hotos21` |
| Cascading and metastable failure | 3 | 1 | 2 | 3 | 5 | 0 | 0 | 13 | 7 | `google-sre-book`, `sre-book-handling-overload-ch21`, `sre-book-addressing-cascading-failures-ch22`, `aws-builders-load-shedding` |
| Observability | 1 | 1 | 2 | 1 | 0 | 0 | 0 | 5 | 4 | `google-sre-book-monitoring-ch6`, `gregg-use-method`, `grafana-red-method`, `dapper-2010` |
| Safe deploys | 1 | 1 | 3 | 0 | 3 | 0 | 0 | 8 | 4 | `sre-workbook-canarying-releases-ch16`, `aws-builders-automating-safe-deployments`, `fowler-bluegreen-deployment`, `hodgson-feature-toggles` |

## G0 check per unit

`PLAN-PHASE-1.md` sets G0 as: every unit has at least one Tier 1-2 source and at least one Tier 3-4 source. Counts exclude `map-only` entries; Tier 1-2 counts only `access: free`.

| Unit | Free Tier 1-2 | Tier 3 | Tier 4 | Meets G0 |
| --- | --- | --- | --- | --- |
| 0 Single-server backend | 24 | 0 | 1 | yes, but only through one postmortem (`heroku-june-10-outage-2025`) |
| 1 Foundations | 13 | 3 | 1 | yes |
| 2 Building blocks | 23 | 3 | 4 | yes |
| 3 Data | 17 | 6 | 1 | yes |
| 4 Async & streams | 22 | 1 | 0 | yes, but only through one course-hosted paper copy (`kafka-netdb-2011`) |
| 5 Consistency & coordination | 17 | 11 | 1 | yes |
| 6 Production reliability | 22 | 4 | 15 | yes (one Tier 4 entry is a monthly summary, not a full postmortem) |

Units 0 and 4 pass on a single entry each; the owner may want one more Tier 3-4 source for them (see A1-A2 and A9-A10 below). The PLAN scope note says Unit 0 may pass G0 through official documentation where Tier 1-3 sources are scarce.

## Gap list

Actions use four labels: **research** (new research ticket, agent), **accept** (docs-only coverage is acceptable, decide at G0), **merge** (fold the sub-topic into a neighbour in M2), **drop** (leave out of v1). Pointers named below as "to look for" have **not been opened** and are not in the registry.

### A. Rule-based gaps (fewer than two free concept sources)

| # | Sub-topic | What exists | Proposed action |
| --- | --- | --- | --- |
| A1 | U0 Request lifecycle on one machine | Only `mdn-http-overview` and the nginx guide; no source follows one request from DNS to the database (P1-069 gap). | **research**: find one free article that follows a request end to end. Fallback **accept**: write it from MDN plus own diagram (Unit 0 may pass G0 on official docs per `PLAN-PHASE-1.md`). |
| A2 | U0 Backups and recovery basics | PostgreSQL and MySQL manuals only; mechanics are covered, but not schedules, off-machine copies, or restore drills. | **research**: one operator-practice source on backup policy and restore testing (the SRE book data-integrity chapter is my suggestion, not from a ticket note, and is not registered). Fallback **accept**. |
| A3 | U0 One app + one database | `twelve-factor-app` (license unresolved, treated as all-rights-reserved) plus SQLite docs. | **accept**: this is a framing concept; the lesson is mostly the course's own argument. |
| A4 | U0 Indexes and query basics | `use-the-index-luke` is the only concept source (free, Tier 2) next to the vendor manuals. | **accept**: one strong source plus two manuals is enough. |
| A5 | U2 Reverse proxy | nginx docs and a Tier 5 entry; no conceptual explainer (P1-011 gap; HAProxy docs fetch failed). | **merge** with Load balancer in M2 (one concept "proxy and load balancer"), else **research** for a vendor-neutral explainer. |
| A6 | U2 CDN | MDN glossary, Cloudflare docs, a Tier 4 incident, a Tier 5 entry; no Tier 1 or concept article. | **research**: one vendor-neutral CDN explainer or paper; else **accept** with MDN and Cloudflare docs and teach critically. |
| A7 | U3 Replication | `ddia-2e` is paywalled and unverified for its chapters; only `dynamo-sosp07` is a free concept source. Multi-leader has only a thin CouchDB intro; failover has only PostgreSQL HA docs. | **research**: an operator source on failover and replication lag (Builders' Library or an operator postmortem to look for), and a free multi-leader source. Add per-topic `free_companion` entries to `ddia-2e`. |
| A8 | U3 Transactions and isolation | `ddia-2e` (paywalled) and Berenson (abstract page only); no paper read in full. | **research**: one free explainer on isolation levels and anomalies (PostgreSQL transaction-isolation docs already cover the behaviour); re-read Berenson in full. |
| A9 | U4 Log / event streaming | `kafka-netdb-2011` is a course-hosted copy with no DOI; Kreps "The Log" returned 404/400 and is not registered. | **research**: find a working URL for "The Log" (manual check) and check whether the Kafka design docs cover retention and compaction (my suggestion, not from a ticket note). |
| A10 | U4 Backpressure | Concept count is 2 only because `reactive-manifesto` is counted; it is vocabulary only (P1-013) and the Node.js streams page is in-process only. The one real concept source is `aws-builders-insurmountable-queue-backlogs`. | **research**: one source on bounded queues and flow control between services (see B8). |

### A+. Unit 0 gaps carried over from P1-069 (not visible in the matrix)

| # | Gap | Proposed action |
| --- | --- | --- |
| A11 | A deploy procedure for one box (rolling a version, migrations, rollback). The "Simple deploys" row looks healthy only because of tag matches (12-factor, Fowler blue-green, systemd man page, a Heroku postmortem). | **research** (small), or **accept** and write the procedure from `systemd-service-man`, Fowler blue-green, and the database-migration entries. |
| A12 | A dedicated logging source (only the 12-factor list of factors). | **research** (small): vendor-neutral logging guidance; else **accept** with SRE book monitoring ch. 6. |
| A13 | A primary engineering article on scaling from one server. | **research** (small): one practitioner article; `craver-stack-overflow-architecture-2016` is not single-server (P1-069 doubt). |
| A14 | A beginner-friendly Tier 1 book chapter for Unit 0 (Tier 1 is only an SRE book chapter). | **accept**: Unit 0 may pass G0 on official docs per the PLAN scope note. |

### B. Thin spots recorded by the research tickets

| # | Unit | Spot | Proposed action |
| --- | --- | --- | --- |
| B1 | 1 | Back-of-envelope estimation (the matrix Concept count of 3 is a tag artifact: the SRE overload chapter and the Brooker Little's-law post do not teach estimation): only the undated Jeff Dean slides (license unknown, course-site copy) and two Tier 6 maps. | **accept**, teach the method and not the numbers; **research** for a free estimation primer only if the lesson needs worked examples. |
| B2 | 1 | Latency vs. throughput has no standalone source; `ddia-2e` (paywalled) is the likely one. | **accept**: the Brooker posts and Tene's talk cover the ideas; confirm the DDIA chapter at G0 prep. |
| B3 | 1 | "Is this stage still enough?" is covered only indirectly (SRE overload chapter, SLO sources, AWS load shedding). | **accept**: the course provides the framing; no source needed beyond the existing ones. |
| B4 | 2 | CDN, REST, gRPC: no Tier 1; only vendor docs, MDN, RFCs, and API guides (Microsoft, Google AIP) that were only partly read. | **accept**; re-read the API guides when the API concept is written. |
| B5 | 3 | Failover in production, sharding in production (Notion is the only case), LSM vs B-tree beyond the original paper, MySQL InnoDB MVCC, no Tier 4 data incidents. | **research** one ticket for Unit 3 depth (sharding case such as Instagram/GitHub/Vitess to look for, a modern write-amplification source). |
| B6 | 3 | Vendor docs (MongoDB, DynamoDB, Cassandra) favour their own designs. | **accept**: flag in lessons; prefer Dynamo paper and DDIA for concepts. |
| B7 | 4 | Ordering guarantees (per partition vs total) have no dedicated free primary source. | **research** (small): Kafka KIP-98, SQS FIFO message groups to look for. |
| B8 | 4 | Consumer lag as an operational practice: only Kafka CLI output. Backpressure: `reactive-manifesto` is vocabulary only, the Node.js streams page is in-process only. | **research**: queue-age alerting or consumer-lag monitoring source; do not count the manifesto as coverage. |
| B9 | 5 | Vector clocks (no dedicated source), Zab (paper sections not read), TrueTime detail (abstract only), Jepsen model pages not opened, no split-brain or coordination Tier 4 incident. | **research** one ticket for Unit 5 depth; incident search is optional. |
| B10 | 5 | `kulkarni-hybrid-logical-clocks` has no verified year or venue (non-peer-reviewed, borderline Tier 3); Gilbert-Lynch CAP proof is a bitmap scan. | **accept** HLC with a weaker-tier note; use Brewer's article plus PACELC for CAP. |
| B11 | 6 | Hedged requests and tail latency with retries rest on `tail-at-scale-cacm13`, which was read from the abstract page only. | **research** (small): read the full text via the CACM page by hand (blocked for agents). |
| B12 | 6 | Beginner SLO-based alerting, adaptive concurrency limits, SRE book release-engineering and tracing chapters, `dapper-2010` full text, Envoy "circuit breaking" means static limits. | **research** one small ticket; otherwise **accept** for v1 and **drop** adaptive concurrency. |
| B13 | 6 | Postmortems: `github-availability-report-2026-08` is a monthly summary, not a full postmortem (the Circuit breaker row lists it as Tier 4); not opened: Roblox 2021, Stripe, Discord; no 2023-2026 reports from Stripe, Slack, Discord, Meta. Only GitHub 2026 and GCP 2025 are strong retry-storm cases. | **accept**: 14 full postmortems plus the GitHub summary are enough for the incident pack (P1-046); add more only if P1-022 asks. |
| B14 | 6 | Tier-2 judgment calls: Fowler and Hodgson pieces (consultants), `grafana-red-method` (vendor summary). | **accept**; cite the SRE book for the main claim. |

### C. Cross-cutting issues for G0

| # | Issue | Proposed action |
| --- | --- | --- |
| C1 | `ddia-2e` (Tier 1) is paywalled and unverified for chapter content; its `free_companion` list covers Unit 1 only, so Units 2-6 lean on other sources. | **research** (human-assisted): owner checks the chapter list, then an agent adds per-unit `free_companion` ids. |
| C2 | Tier 1 is `ddia-2e` (paywalled) plus the free Google SRE book and workbook entries, so Tier 1 covers only SRE-flavoured topics (Units 0, 1, 6, parts of 2 and 5) and nothing in Units 3-4; 4 entries are `partial` or `paywalled` (`ddia-2e`, `alex-xu-sdi-vol1-vol2`, `hello-interview-sd-in-a-hurry`, `analyzing-metastable-hotos25`). | **accept**: Tier 6 is map-only; for `analyzing-metastable-hotos25` the OSDI'22 paper `metastable-failures-osdi22` is the free substitute. |
| C3 | Abstract-only reads (`nishtala-memcache-nsdi13`, `maglev-nsdi16`, `tene-how-not-to-measure-latency`, `spanner-osdi12`, `flp-impossibility-1985`, plus `tail-at-scale-cacm13` in B11, `berenson-critique-ansi-isolation-1995` in A8, `dapper-2010` in B12). | **research**: read in full before the concepts that cite them are written (M4), not before G0. |
| C4 | Moving URLs: Cassandra `/latest/`, ZooKeeper `/current/`, Redis `/latest/`, IETF idempotency-key draft is an active Internet-Draft. | **research** (small): pin versions or archive URLs before approval. |
| C5 | License values missing from the schema (CC BY 3.0 pages: Raft site, Kleppmann, Debezium; official-docs tier) and the bare-first-name byline convention. | Already covered by P1-070 (in progress). |
| C6 | Unit 0 has no Tier 3 source and one Tier 4 source (`heroku-june-10-outage-2025`); Tier 1 is only SRE book chapters. | **accept**: Unit 0 may pass G0 on official docs and Tier 2 practice (PLAN scope note); see the G0 check above. |

### Summary for G0

- Every sub-topic has at least one free Tier 1-2 source, so no sub-topic is blocked by the ticket's own rule, and every unit meets the PLAN's G0 criterion (Units 0 and 4 only narrowly).
- Ten sub-topics have at most one free concept source (A1-A9, A10); several rest mostly on official docs. Four more Unit 0 gaps are listed in A11-A14. Of these, A1, A2, A6, A7, A8, A9 deserve research tickets; A3, A4 are acceptable; A5 is best merged with Load balancer.
- Suggested follow-up tickets (not created yet): Unit 0 gaps (A1, A2, A11-A13), Unit 3 depth (A7, A8, B5), Unit 4 depth (A9, A10, B7, B8), Unit 5/6 depth (B9, B11, B12), pinning moving URLs (C4). The owner decides at G0 which are worth doing before M2.

## Dispositions (recorded 2026-11-13, delegated by the owner)

The owner read the summary and delegated the gap list to the agent.

- **research:** A1, A2, A11, A12, A13 -> P1-072; A6 -> P1-073; A7, A8, B5 -> P1-074; A9, A10, B7, B8 -> P1-075; B9, B12 -> P1-076; C4 -> P1-077.
- **accept (docs-only or existing sources are enough for v1):** A3, A4, A14, B1, B2, B3, B4, B6, B10, B13, B14, C2, C6.
- **merge in M2 (P1-020):** A5 Reverse proxy folds into Load balancer as one concept.
- **drop from v1:** adaptive concurrency limits (part of B12).
- **left to the owner / later:** B11 (full read of Tail at Scale, blocked for agents) and C1 (`ddia-2e` chapter list, then per-unit `free_companion`) need the owner. C3 (abstract-only reads) is done before M4 when the citing concepts are written. C5 is covered by P1-070 (done).
