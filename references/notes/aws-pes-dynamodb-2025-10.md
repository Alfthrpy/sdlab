---
source: aws-pes-dynamodb-2025-10
read_by: agent
date: 2026-11-12
sections_read: ["Whole summary page: DynamoDB DNS, EC2 DWFM, Network Manager, NLB, other services, follow-up actions"]
---

# Notes: Summary of the Amazon DynamoDB Service Disruption in US-EAST-1 (October 2025)

> Notes are in English and in your own words. Times are PDT as on the page; UTC is PDT + 7 hours.

## Key points

- (DynamoDB DNS) DynamoDB manages its regional endpoint DNS with a planner (makes plans) and several enactors (apply plans to Route 53). A slow enactor applied an old plan after a newer one had been applied, and a clean-up step then deleted the old plan, leaving the endpoint with no IP addresses. The state could not self-repair; operators had to fix it.
- (Timeline) DNS failures began 2025-10-19 23:48 PDT; DNS was fully restored 2025-10-20 02:25 PDT; customer caches recovered about 02:40.
- (EC2) The DropletWorkflow Manager lost its leases while DynamoDB was down. After DNS recovered, lease re-establishment timed out repeatedly and the manager fell into congestive collapse. Engineers throttled work and restarted manager hosts to clear queues.
- (Network propagation) A backlog of network-state updates meant new instances launched without full connectivity.
- (NLB) Health checks failed on instances whose network state had not propagated; nodes flapped in and out of DNS; the health-check system was overloaded and automatic AZ failover removed capacity. AWS turned off automatic failover for a few hours and then turned it back on.
- (Other services) Lambda, Redshift, STS, and Connect saw backlogs or secondary effects; Redshift was the last service to recover: replacement instances began launching 2025-10-20 14:46 PDT and impaired clusters were restored by 2025-10-21 04:05 PDT.
- (Follow-up) The DNS automation was disabled worldwide pending a fix; NLB will get a velocity limit on capacity removal; EC2 gets a recovery test suite and queue-size-based throttling.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Start 2025-10-19 23:48 PDT; page states end 2025-10-20 14:20 PDT (ECS, EKS, Fargate recovered by then), but Redshift cluster restoration finished 2025-10-21 04:05 PDT | timeline | The stated end time conflicts with the page's own Redshift entry; convert to UTC for lessons |
| NLB automatic failover disabled 09:36 PDT, re-enabled 14:09 PDT | NLB section | |

## Relevant to concepts

- `metastable-failure` / recovery backlog: the DNS fault was fixed in hours, but the backlog and collapsed workflow kept other services down longer.
- `load-shedding` and throttling during recovery.
- `health-checks` that remove capacity when many nodes fail at once.
- ladder trigger: shows why recovery limits matter after a dependency comes back.

## Warnings

- The page shows no publication date; the registry stores `published: null` with a NO-DATE note.
- Some third-party blogs call this a "retry storm"; the AWS page itself describes lease timeouts and backlogs. Use only what the AWS page says.
- The page's stated event end (14:20 PDT, 20 Oct) is earlier than the Redshift restoration (04:05 PDT, 21 Oct); do not present 14:20 as the end of all impact.
