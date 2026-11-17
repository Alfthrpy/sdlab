---
source: craver-stack-overflow-architecture-2016
read_by: agent
date: 2026-11-17
sections_read: ["Opening statistics (day of Feb 9, 2016)", "Hardware list", "Ground Rules", "The Internets", "Load Balancers (HAProxy)", "Web Tier", "Service Tier", "Cache & Pub/Sub (Redis)", "Websockets", "Search (Elasticsearch)", "Databases (SQL Server)", "Libraries"]
---

# Notes: Stack Overflow: The Architecture - 2016 Edition (Nick Craver)

> Notes are in English and in your own words. Whole post read via WebFetch and re-checked against the raw HTML with curl; all numbers below were verified in the raw text. Post date: Feb 17, 2016. Statistics are for one day, Feb 9, 2016. Percent/ratio figures marked "my arithmetic" are mine, not on the page.

## Key points

- (Opening statistics) The post starts with one day of traffic and server-side work, compared with Nov 2013 figures, so it shows how much traffic a modest fleet carried and where time went (SQL, Redis, tag engine, ASP.NET).
- (Opening statistics) Per-page timings: question page render averages 22.71 ms (19.12 ms inside ASP.NET), home page 11.80 ms. The author credits a 2015 hardware upgrade and application performance tuning for the large drop in ASP.NET time even though request volume rose.
- (Hardware list) The whole public fleet at the time: 4 SQL Servers, 11 IIS web servers, 2 Redis servers, 3 tag engine servers, 3 Elasticsearch servers, 4 HAProxy load balancers, plus network gear. The author says the site needs only 1 web server to run and that this has been (unintentionally) tested a few times, and adds that it works but is not a good idea.
- (Ground Rules) Everything is redundant: paired racks, two power feeds, a second data center (Colorado). So this is a case of "big, well-tuned hardware, but redundant", not a single-box setup.
- (Load Balancers) HAProxy on CentOS terminates TLS, routes mainly by host header, applies rate limiting, and logs performance headers sent back from the web tier. The balancers have 64 GB or more of RAM so TLS sessions can be cached and resumed cheaply.
- (Web Tier) 9 primary web servers plus 2 dev/meta (staging). The main Q&A app is multi-tenant: one application serves all Q&A sites, and the author says the whole Q&A network can run off a single application pool on a single server. The author says the web tier is deliberately over-provisioned for rolling builds, headroom, and redundancy.
- (Cache & Pub/Sub) Redis handles about 160 billion operations per month with every instance below 2% CPU; two-level cache (local HTTP cache, then Redis, then the source). Main Redis servers have 256 GB RAM with about 90 GB used.
- (Websockets) Around 500,000 concurrent websocket connections at peak, served from the web tier. Efficient versus polling at that scale, but load balancer port and file handle exhaustion are mentioned as problems.
- (Databases) SQL Server is the single source of truth; Redis and Elasticsearch are derived from it. Two clusters, each one primary taking nearly all load and asynchronous replicas (one in each data center). Cluster 1: 384 GB RAM, 4 TB PCIe SSD, 2x12 cores per server; cluster 2: 768 GB RAM, 6 TB PCIe SSD, 2x8 cores. The author keeps database CPU low on purpose, though it was a bit high at the time due to plan cache issues.
- (Databases) Query style is deliberately simple (Dapper micro-ORM; only one stored procedure left), which the author ties to speed.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 209,420,973 HTTP requests to the load balancer in one day (Feb 9, 2016); about 2,400 per second on average (my arithmetic) | Opening statistics | Daily average only; peak rate is not given on the page |
| 66,294,789 of those were page loads (about 770 per second average; my arithmetic) | Opening statistics | |
| 504,816,843 SQL queries from HTTP requests in that day (about 5,800 per second average; my arithmetic) | Opening statistics | About 2.4 SQL queries per HTTP request (my arithmetic) |
| 607,073,066 ms (168 hours) spent running SQL queries; 1,609,944,301 ms (447 hours) in ASP.NET; 10,396,073 ms (2.8 hours) on Redis hits | Opening statistics | Cumulative time summed over all requests, not wall-clock latency of one request. Good for "where does time go" |
| 22.71 ms average question page render (19.12 ms in ASP.NET), over 49,180,275 renders; home page 11.80 ms (8.81 ms in ASP.NET) over 6,370,076 renders | Opening statistics | |
| 11 web, 4 SQL, 2 Redis, 4 load balancer servers, etc. | Hardware list | Fleet size in 2016 |
| Needs only 1 web server to run (author: works, not a good idea) | Text after the hardware list | Anecdotal, not a load test |
| Redis ~160 billion ops/month, each instance < 2% CPU | Cache & Pub/Sub | |
| Redis main servers 256 GB RAM (~90 GB used); Providence servers 384 GB (~125 GB used) | Cache & Pub/Sub | |
| ~500,000 concurrent websocket connections at peak | Websockets | |
| SQL cluster 1: 384 GB RAM, 4 TB PCIe SSD, 2x12 cores; cluster 2: 768 GB RAM, 6 TB PCIe SSD, 2x8 cores | Databases | Hardware sizing of the biggest machines they used |
| Elasticsearch: 3 nodes per cluster, 192 GB RAM, SSD | Search | |

## Relevant to concepts

- `single-machine-limits` (unit 0), objective 3 (decide whether vertical scaling is enough from utilization data and the biggest machine available): partly supported. It gives a real example of scaling up (hundreds of GB of RAM, TB-scale PCIe SSD, very low CPU use on Redis) and the claim that heavy traffic ran on a small number of strong servers. It does not show a decision process or utilization-vs-capacity reasoning, and the fleet is not single-machine.
- `single-machine-limits`, objectives 1 and 2 (recognize the bottleneck resource from symptoms and metrics; apply the USE method): not really supported. The post mentions a few symptoms (port and file handle exhaustion on the load balancer, SQL CPU raised by plan cache issues, L2/L3 cache pressure from one service), each in one line without diagnosis. Use gregg-use-method and pg-docs-kernel-resources.
- `app-plus-database` (unit 0), objective 1 (calculate that one app plus one database is enough): partly supported as a scale reference: one SQL primary per cluster takes nearly all load while average load is about 2,400 requests/s. The numbers show that a database primary on big hardware can handle that, but also that the site's application is not a single app plus a single database (there are 11 web servers, Redis, Elasticsearch, two data centers), so it is an upper reference, not an example of "one server is enough".
- `request-lifecycle` (not mapped to this source): the per-stage time table (SQL, Redis, ASP.NET) and the render-time averages are a useful real example for "which stage dominates", worth considering if the objective 2 gap is to be filled.

## Warnings

- Data is from 2016 and describes one company's Windows/.NET/SQL Server stack on its own hardware. It is not a cloud reference and it is not a blueprint for a beginner's app.
- The author is describing his employer's infrastructure; the page does not state his job title (the registry note also says this).
- The 1-web-server remark is explicitly anecdotal and caveated by the author; do not present it as "Stack Overflow runs on one server". The system is redundant everywhere (Ground Rules).
- The daily totals are sums, so per-second values are averages; peak load is higher and unspecified. Time figures such as "168 hours of SQL" are totals across all requests.
- Several claims (why so over-provisioned; "performance is a feature") are only teased and deferred to later posts in the series (not read).
- Post says the hardware appendix post follows; not read.
