---
source: system-design-primer
read_by: agent
date: 2026-11-17
sections_read: ["README: Step 1 outline of the interview approach", "README: Back-of-the-envelope calculations (pointer)", "README Appendix: Powers of two table, Latency numbers every programmer should know, Handy metrics", "solutions/system_design/pastebin/README.md: Step 1 (assumptions, Calculate usage, Handy conversion guide) and Step 4 comments", "solutions/system_design/scaling_aws/README.md: Step 1 and 'Start with a single box'"]
---

# Notes: The System Design Primer (Donne Martin), parts relevant to Unit 0 estimation

> Notes are in English and in your own words. This repo is large; these notes cover only the parts used for estimation and the single-box start. Raw files fetched with curl from raw.githubusercontent.com on 2026-11-17; license is CC BY 4.0 per `LICENSE.txt` (Copyright 2017 Donne Martin), already recorded in the registry. Not read: most of the main README and most solution folders. The mint, social_graph, sales_rank and web_crawler solutions were searched for "peak" and "spike" only, to see whether any gives a peak factor (none gives a number; the ones that mention peaks only say "higher at peak" or "traffic spikes").

## Key points

- (README, Step 1) The interview approach begins with questions that fix the scale: who uses it, how many users, how much data, how many requests per second, the read-to-write ratio.
- (Appendix, Latency numbers) A table lists typical latencies from CPU cache up to a trans-continental packet, with the same caveat of age as other copies of the table; the lines useful for a request path are: main memory reference about 100 ns, round trip within one datacenter about 500 microseconds, SSD random 4 KB read about 150 microseconds, HDD seek about 10 ms, a packet California to the Netherlands and back about 150 ms. The table notes at the end say 1 ns = 10^-9 s, 1 us = 10^-6 s, 1 ms = 10^-3 s.
- (Appendix, Handy metrics) Derived throughputs: about 30 MB/s sequential HDD read, 100 MB/s over 1 Gbps Ethernet, 1 GB/s SSD, 4 GB/s main memory; 6-7 worldwide round trips per second and about 2,000 round trips per second inside one datacenter.
- (Pastebin solution, Step 1) A worked estimate from user numbers: 10 million users, 10 million paste writes and 100 million paste reads per month (10:1 read-to-write), traffic stated as not evenly distributed. It derives 4 writes per second and 40 reads per second on average, and about 12.7 GB of new content per month.
- (Pastebin solution, "Handy conversion guide") The conversion between per-month and per-second rates: about 2.5 million seconds in a month; so 1 request per second is about 2.5 million requests per month, 40 requests per second is about 100 million per month, 400 requests per second is about 1 billion per month. The same guide is repeated in the scaling_aws solution.
- (Pastebin solution, Step 4) It calls the 40 reads per second and 4 writes per second "average", says the peak is higher without giving a number, and says a single SQL write master should manage 4 writes per second. In other solutions the same sentence says 2,000 or 400 average writes per second "might be tough" for one SQL write master, i.e. the primer's own threshold for "one database is no longer obviously enough" sits somewhere between a few and a few hundred writes per second, with no measurements behind it.
- (scaling_aws solution, "Start with a single box") For a few users: web server and MySQL on one EC2 box, bigger box when needed ("vertical scaling"), watch basic metrics (CPU, memory, I/O, network) to find the bottleneck; the page lists the drawbacks as vertical scaling getting very expensive and having no redundancy or failover. Then it adds a static IP, DNS (Route 53), and closing all ports except 80, 443 and a whitelisted SSH.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| About 2.5 million seconds per month; 1 req/s is about 2.5 million requests/month; 40 req/s is about 100 million/month; 400 req/s is about 1 billion/month | pastebin and scaling_aws solutions, Step 1 "Handy conversion guide" | 30 days x 86,400 s = 2.592 million, so the rounding is fine (my arithmetic) |
| Example sizing: 10M users, 100M reads/month, 10M writes/month gives 40 reads/s and 4 writes/s average | pastebin Step 1 | An interview-style hypothetical, not measured traffic. It implies about 10 reads per user per month, which is a very light user |
| Round trip within one datacenter about 500 us; main memory reference about 100 ns; HDD seek about 10 ms | Appendix, latency table | Old numbers (about 2012); order of magnitude only |
| Peak is "higher" than average, no factor given | pastebin Step 4 | Use `robustperception-peak-to-mean-ratio` for a number |
| Single box, vertical scaling "can get very expensive", no redundancy | scaling_aws, "Start with a single box" | Qualitative only, no prices |

## Relevant to concepts

- `app-plus-database` (unit 0), objective 1 (compute from user numbers and requests per second whether one app plus one database suffices): PARTLY supported. It supplies the per-month to per-second conversion and a worked users-to-req/s example, but no requests-per-user rule, no peak factor, and no capacity of a single database in req/s (only the unmeasured "might be tough" remarks). Pair with `robustperception-peak-to-mean-ratio` (peak factor), `sqlite-appropriate-uses` and `craver-stack-overflow-architecture-2016` (reference loads).
- `single-machine-limits` (unit 0), objective 3: weakly supported (the "bigger box, watch the metrics, gets expensive" paragraph). The size ceiling and prices must come from `aws-docs-ec2-memory-optimized-instance-types` and `aws-ec2-price-list-us-east-1`.
- `latency-throughput`, back-of-envelope estimation (unit 1): the latency table and the method.
- `request-lifecycle` (unit 0), objective 2: the latency table gives orders of magnitude for a datacenter round trip and a disk seek, which helps a learner sanity-check scenario numbers.

## Warnings

- The latency table is from about 2012 and is labeled as community-contributed numbers; disks and networks are faster now. Use for orders of magnitude only.
- The solutions are interview-style exercises with invented user counts; they are not measured capacity data.
- The registry entry's units are [1, 2, 3, 4]; these parts are used in Unit 0 (needs a units update by whoever edits the registry).
- The repo says several linked originals are on web.archive.org; only the content in the repo itself was used here.
