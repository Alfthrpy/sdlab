---
source: fowler-bluegreen-deployment
read_by: agent
date: 2026-11-17
sections_read: ["whole article (single page, untitled body sections, Further Reading, Updates)"]
---

# Notes: Blue Green Deployment (Martin Fowler, martinfowler.com)

> Notes are in English and in your own words. The page is short and has no numbered sections, so locations are given as "para N" (paragraph count in the main body, starting at the first paragraph under the title) or by section name. Read with WebFetch and re-checked with the raw HTML via curl; the page text was fully available.

## Key points

- (para 1-2) The author's starting point is that deployment should be fully automated, because manual steps create delay between "code done" and "users get value". The technique comes from the Continuous Delivery book (Humble and Farley), which was not yet published when this was written.
- (para 3) The hard step of an automated deploy is the cut-over: moving software from its final testing stage to live production. It should be quick to keep downtime small.
- (para 3) Blue-green answer: keep two production environments that are as identical as possible. One is live. The new release gets its final testing in the idle one. When it works, a router switch sends all incoming requests to the idle one, which becomes live; the old one is now idle.
- (para 4) Rollback is the same switch in reverse: if the new environment misbehaves, point the router back at the old one.
- (para 4) Rollback is not free of data problems: transactions that arrived while the new environment was live may be missing from the old one. Two mitigations are named: feed transactions to both environments so the old one stays a usable backup, or put the application in read-only mode before cut-over, run briefly that way, then switch to read-write.
- (para 5) The two environments can be separate hardware, separate virtual machines (same or different hardware), or one operating environment split into zones with separate IP addresses.
- (para 6) After the new version is stable, the old environment becomes the staging area for the next release; the two environments rotate between live, previous version (for rollback), and staging.
- (para 7) The same mechanism is what a hot standby needs, so each release also exercises the disaster-recovery procedure.
- (para 8) Variations: one project switched by restarting ("bouncing") the web server instead of changing the router; another kept one shared database and switched only the web and domain layers.
- (para 9, added in the 2015 update) Database schema changes are the main difficulty. Recommended order: first apply a schema change that works for both old and new application versions, deploy it and check that all is well (this gives a rollback point), then deploy the new application version, and only after it has settled remove the schema support for the old version.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Page dated 1 March 2010; update on 5 June 2015 added the database paragraph and Further Reading | page header, "Updates" section | The schema-change advice is the 2015 addition, so it is less tied to the original 2010 framing |
| Name credited to a "foggy combination" of Daniel Terhorst-North and Jez Humble | last paragraph of the body, before Further Reading | Attribution only |
| No downtime figures or guarantees are given anywhere | whole page | The only claim is that the router switch is fast; do not cite a number from this page |

## Relevant to concepts

- `simple-deploys` objective 1 (arrange the steps of one deploy including database migration and rollback): supports well for the shape of a safe deploy, namely test in the idle environment, switch, keep the old one for rollback, and the 4-step expand/deploy/contract order for schema changes (para 9). It does not give concrete commands or a checklist, so the lesson must add its own step list.
- `simple-deploys` objective 2 (why a direct deploy to one server causes brief downtime, and how to reduce it): only partly supported. The page never explains the mechanism of downtime in an in-place deploy; it only says the cut-over should be quick to minimize downtime (para 3). What it does give for reducing downtime is the two-environment idea and, relevant to a single machine, the variants "zones with separate IPs" (para 5) and "bounce the web server" (para 8). The "why" (old process stopped before new one is ready, in-flight requests dropped) must come from another source or the writer's own reasoning, and the writer should label it as such.
- `simple-deploys` objective 3 (config separate from code): not supported by this source (twelve-factor-app covers it).
- Unit 6 (registry `units: [0, 6]`): safe-deploy strategies, no mapping checked here.

## Warnings

- Written at the time of Continuous Delivery's publication; the page does not discuss containers, load balancers by name, Kubernetes, or cloud autoscaling. It does not use the terms "in-place deploy" or "downtime duration".
- Blue-green needs two environments, which on a single-server setup means either a second port/process set on the same machine or a zone/VM split. The article offers these ideas but not a recipe, and capacity cost (double the resources while both exist) is not discussed.
- The "feed transactions to both environments" and "read-only mode" ideas are suggestions ("you may be able to"), not guaranteed techniques.
- Copyright Martin Fowler, no reuse license (registry: all-rights-reserved, rewrite-only).
