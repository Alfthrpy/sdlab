---
source: aws-startups-scaling-part1-primer
read_by: agent
date: 2026-11-17
sections_read: ["Introduction", "AWS Background Knowledge (Regions, Availability Zones, platform overview)", "Day One, User One", "Day Two, User > 1 (vertical scaling, decoupling tiers, stateless servers, ELB, horizontal scaling)", "Summary", "page footer"]
---

# Notes: Scaling on AWS Part I: A Primer (David Kuo, AWS Startups Blog, 2015-11-25)

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location. Whole page read on 2026-11-17 via fetch plus the raw HTML (`curl`); the article is short and has no code or benchmarks.

## Key points

- (Introduction) Frames the problem as on-premise scaling being hard because you must guess peak capacity, wait for hardware, and get the setup right the first time. The cloud pitch is that you can grow in steps instead.
- (Day One, User One) The starting design is deliberately minimal: web server, application server, and database all on a single virtual machine (an EC2 instance), for example a LAMP or .NET stack, placed in a public subnet of a virtual private network (VPC) with DNS (Route 53) in front. The example instance is a small general-purpose type (t2.medium).
- (Day Two, User > 1) The first reaction to growth is vertical scaling: stop the VM, change its type to a bigger one, start it again. On an EBS-backed instance this is described as taking minutes.
- (Day Two) Vertical scaling hits a ceiling. The article quotes the largest instance then available as roughly 40 vCPUs and 244 GB of RAM.
- (Day Two) Two further weaknesses of the one-machine design are named besides the size ceiling: no redundant server (a single failure takes everything down) and a single Availability Zone (health tied to one location).
- (Day Two) Recommended first step is to separate (decouple) tiers, because web, app, and database layers have different resource needs and grow at different rates; each tier then gets an instance type that fits it.
- (Day Two) Next step is to make the app tier stateless: any server can answer any request with the same result, and application state lives outside the individual server so a follow-up request need not return to the same machine.
- (Day Two) Once servers are stateless you add more instances to a tier and spread requests with a load balancer (Elastic Load Balancing). The load balancer is described as scaling horizontally itself, terminating SSL, and running health checks so only healthy instances get traffic.
- (Day Two, end) Horizontal scaling means a pool of cheap commodity machines instead of a few expensive high-end ones; the article presents it as the cost-effective way to take high traffic.
- (Summary) Vertical scaling is acceptable but limited; horizontal scaling needs decoupled tiers and a distributed (stateless) application design.
- (AWS Background Knowledge) Regions and Availability Zones are introduced as AWS vocabulary: a region is a geographic cluster of data centers; each region has two or more AZs that are isolated from each other's failures, with single-digit-millisecond links between them.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Largest EC2 instance quoted: up to 244 GB RAM and 40 vCPUs | Day Two, User > 1 (vertical scaling paragraph) | Figure is from 2015 and is long out of date; use only as an example of "a ceiling exists", never as a current limit |
| Resizing an EBS-backed instance = stop, change type, start; "should take minutes" | Day Two, User > 1 | Implies vertical scaling causes a short downtime window on a single server |
| Starting architecture: web + app + database on one EC2 instance (t2.medium) | Day One, User One | Matches the Unit 0 single-server starting point |
| Two named weaknesses of single-machine design: no redundancy, single AZ | Day Two, User > 1 | Good "trigger" wording for the growth ladder |
| AWS had 11 regions with 5 more planned (Korea, India, Ohio, UK, second China region); AWS operating since 2006; 50+ services | AWS Background Knowledge | Dated 2015 trivia; do not cite as current |
| Footer: (c) 2026 Amazon Web Services, Inc. or its affiliates, all rights reserved | page footer (raw HTML) | Confirms the all-rights-reserved assumption in the registry entry; the byline reads "AWS Editorial Team ... By David Kuo, Solutions Architect, AWS" |

## Relevant to concepts

- `app-plus-database` (obj. 1, calculate from user count and requests per second that one app plus one database is enough): NOT supported. The article gives no user counts, requests per second, or capacity numbers for the single-box stage. It only supports the qualitative picture of the starting architecture (Day One, User One). (obj. 2, tell state kept in the database from state lost when the app process restarts): only weakly supported. The "stateless" paragraph states that state must be stored outside the server so any server can serve any request, but it does not discuss what is lost on a process restart.
- `single-machine-limits` (obj. 3, decide whether vertical scaling is enough from utilization data and the largest available machine): partly supported. It shows the mechanics (resize in minutes), that a hard ceiling exists, and the 2015 maximum size. It gives no utilization data, no decision rule, and no price information, so the "decide from data" behavior must come from other sources (e.g. gregg-use-method). Objectives 1 and 2 (identify the bottleneck resource; apply the USE method): NOT supported.
- Growth ladder (Unit 0 to Unit 2): the Day One to Day Two progression (single box, bigger box, split tiers, stateless app servers behind a load balancer) is a ready-made narrative for the "trigger" of the next stage.

## Warnings

- Dated 2015 and AWS-specific. Instance limits, region counts, and service names are out of date; use the page for ladder logic, not product facts.
- It is a vendor blog promoting AWS services, so the "scale horizontally" advice is not neutral about cost; no measurements back the claims.
- Only a primer: the database tier is deliberately left to Part 2 (the article only promises "database options and additional AWS services" there), so it gives nothing on database scaling.
- The article is part of a 4-part series; only Part 1 was read for these notes.
