---
id: P1-015
title: "Research candidate sources — Unit 6 + postmortems"
milestone: M1
type: research
owner: agent
review: agent
status: done
priority: high
depends_on: [P1-010, P1-068]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Context

Fill the Reference Registry for Unit 6: Production reliability (timeout, retry/backoff/jitter, circuit breaker, load shedding, cascading & metastable failure, observability, safe deploys). Use the `researcher` subagent; review by `source-verifier`.

## Tasks

1. Derive the list of sub-topics from the unit table in `curriculum/README.md`.
2. For each sub-topic find at least: one Tier 1–2 source, one Tier 3 source or official documentation, and one free source.
3. Collect ≥ 12 official postmortems (varied companies and failure mechanisms; prioritize 2023–2026) as material for the incident pack.
4. Open every source; record `candidate` entries per `templates/source-entry.yaml`.
5. Write reading notes for the 3–5 most important sources.
6. List sub-topics without adequate sources in the Notes section.

## Done criteria

- [x] ≥ 15 candidates + ≥ 12 postmortems for this unit, all opened in the session
- [x] Every sub-topic has ≥ 1 Tier 1–3 source or is recorded as a gap
- [x] Reading notes for the 3–5 main sources
- [x] `source-verifier` says pass
- [x] `python scripts/validate.py` passes

## Notes

Result: 29 new entries (14 Tier 1-3 candidates + 13 new Tier 4 postmortems and 2 existing postmortem seeds verified and fixed = 15 postmortems), unit 6 added to several existing entries, 5 reading notes. `source-verifier`: pass with small fixes; fixes applied by a second `researcher` run. Not re-reviewed: the GitHub 6 Aug wording (the fixer found the page does mention sidecar CPU throttling/OOM restarts and revoked jobs retried; the verifier could not confirm) and the OTel/backoff-jitter footer licenses (fetch showed no footer).

Postmortems (all own-company pages, rewrite-only): AWS DynamoDB 2025-10 (no publish date on page), Cloudflare 2025-11-18, GCP Service Control 2025-06, CrowdStrike 2024-08, Cloudflare 1.1.1.1 2025-07, Cloudflare Workers KV 2025-06, Cloudflare control plane 2023-11, Datadog 2023-03, Azure Front Door 2025-10, Heroku 2025-06, GitHub availability report 2026-08 (monthly summary, do not count as full postmortem), Slack 2021-01, Atlassian 2022-04, Fastly 2021-06, Meta 2021-10. Eleven are 2023-2026.

Gaps and weak spots:
- **Postmortems not opened:** Roblox 2021 (ECONNRESET), Stripe, Discord; no 2023-2026 postmortems from Stripe, Slack, Discord or Meta. Only GitHub 2026 and GCP 2025 are strong retry-storm cases.
- **`analyzing-metastable-hotos25`:** seed still unopened (ACM 403).
- **Missing sub-topic depth:** hedged requests / tail latency with retries (`tail-at-scale-cacm13` abstract only), adaptive concurrency limits, beginner SLO-based alerting, SRE book release-engineering and tracing chapters, `dapper-2010` full text.
- **Weak tiers:** Fowler and Hodgson pages are practitioner-consultant pieces at Tier 2 (judgment call); `grafana-red-method` is a vendor blog summary, not the main RED source; Envoy "circuit breaking" means static limits.
- **Metadata caveats:** the `aws-builders-timeouts-retries` byline is only "Marc", recorded as `authors: []`, but `aws-builders-load-shedding` and `aws-builders-implementing-health-checks` still use `authors: [David]`; settle one convention for bare-first-name bylines (a follow-up ticket or P1-070). OTel and Kubernetes docs are CC BY 4.0 and need an `attribution` line at approval. Azure Front Door `published` is really the review date (follow-ups into 2026). Workers KV and GCP pages contain internal duration/window conflicts. DynamoDB page says the event ended 14:20 PDT 20 Oct while its own timeline shows Redshift recovering by 04:05 PDT 21 Oct. Metastable OSDI'22 abstract says 22 failures but Table 1 says 21.

Trigger hints (registry notes of aws-builders-timeouts-retries, metastable-failures-hotos21, sre-book ch22, aws-builders-automating-safe-deployments, fowler-bluegreen-deployment, grpc-docs-retry, sre-workbook-canarying-releases-ch16): a second remote call means one slow dependency can hold all threads (timeouts); transient failures plus synchronized clients mean backoff and jitter; retries at several layers or a long outage mean retry budget and circuit breaker; traffic above capacity means load shedding; a system that stays down after the trigger is gone is metastable; can't tell which service is slow means request-level signals; deploys and config pushes as main outage source mean canary, blue/green, flags, rollback. Hints for the other entries still need placing by the curriculum designer.
