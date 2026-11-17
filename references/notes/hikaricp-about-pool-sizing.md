---
source: hikaricp-about-pool-sizing
read_by: agent
date: 2026-11-17
sections_read: ["Intro", "10,000 Simultaneous Front-End Users", "But why?", "Limited Resources", "The Formula", "Axiom: You want a small pool, saturated with threads waiting for connections", "Pool-locking", "Caveat Lector"]
---

# Notes: About Pool Sizing (HikariCP wiki)

> Notes are in English and in your own words. Do not copy source sentences. Every point gives its location.
> Read in full (whole page) via WebFetch and confirmed on the raw page with `curl` on 2026-11-17. The page header says last edited by Leo Bayer on Dec 7, 2021 (31 revisions).

## Key points

- (Intro, "10,000 Simultaneous Front-End Users") The central claim: the question is how small a pool can be, not how big. The author points to an Oracle Real-World Performance demo video (about 10 min, not watched) in which only the pool size was reduced and response time fell from about 100 ms to about 2 ms.
- (But why?) A CPU core runs one thread at a time; the OS only gives the illusion of parallelism by time-slicing. Beyond the number of cores, extra threads add context-switch cost and do not add throughput.
- (Limited Resources) The real limits of a database are CPU, disk and network (memory is ignored because its bandwidth is orders of magnitude higher). If there were no disk or network, pool size = core count would be optimal (the page uses an 8-core server as the example).
- (Limited Resources) Because queries block on disk I/O (and sometimes on network buffers), a pool somewhat larger than the core count can still pay off: while one connection waits, the CPU runs another. More connections help only to the extent that blocking creates idle CPU time.
- (Limited Resources) Counter-intuitive point: faster storage (SSD, no seek time) means less blocking, so the best pool size moves closer to the core count, not further away.
- (The Formula) Starting point: connections = (core_count * 2) + effective_spindle_count. The page attributes the formula to the PostgreSQL project and says it is probably applicable to other databases; it is a starting point, and you must load-test around it with simulated expected load.
- (The Formula) Core count excludes hyperthreads; effective spindle count is about zero if the active data set is fully cached and grows toward the real number of disks as cache hit rate falls. The page says no analysis exists yet on how the formula behaves with SSDs.
- (The Formula) Worked example on the page: a 4-core machine with one disk gives 9, rounded to 10. The author claims this could serve about 3,000 front-end users at about 6,000 TPS with simple queries (an assertion, not shown with data).
- (Axiom) The desired state is a small pool with many application threads waiting for a connection. Pools of 10,000, 1,000 or even 100 are called wrong for a large user base; a few dozen at most.
- (Axiom) A well-tuned pool sits at the number of queries the database can process at the same time, which the author says is rarely much above cores x 2. Over-provisioning is also criticized for small in-house apps with a handful of users and a pool of 100.
- (Pool-locking) If one thread needs several connections at once, a pool can deadlock when all threads each hold some connections and wait for more. Minimum pool size to rule this out: Tn x (Cm - 1) + 1 (Tn = max threads, Cm = max connections held by one thread at once). The page says to look at the application first (reduce multi-connection use) before enlarging the pool.
- (Caveat Lector) Sizing is deployment-specific. A mix of long and very short transactions is hardest; two separate pools (long jobs vs realtime queries) can help. For mostly long transactions, size the job queue to fit the pool, not the other way around.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Oracle demo: response time about 100 ms down to about 2 ms (over 50x) by shrinking the pool only | "10,000 Simultaneous Front-End Users" | Claim about a video the notes author did not watch; cite as "the page reports", not as verified |
| Scenario: 10,000 simultaneous users, about 20,000 transactions per second | same section | Illustrative scenario of the page |
| Formula connections = (core_count * 2) + effective_spindle_count | "The Formula" | Taken by the page from PostgreSQL docs/wiki; starting point only |
| Example: 4 cores, 1 disk gives 9, call it 10 | "The Formula" | Good worked example for a lesson or lab |
| Oracle video: 2048 down to 96 connections; the page says even 96 is probably too high unless a 16 or 32-core box | "Limited Resources" | Exact numbers confirmed on the raw page |
| PostgreSQL benchmark chart: TPS flattens around 50 connections | "Limited Resources" | The chart is an image; only the sentence about it was read |
| Deadlock-free minimum: Tn x (Cm - 1) + 1; examples 3 x (4-1)+1 = 10 and 8 x (3-1)+1 = 17 | "Pool-locking" | This is the minimum to avoid deadlock, explicitly not the optimal size |

## Relevant to concepts

- `connection-pooling` objective 1 (explain why opening a new connection per request wastes resources): weakly supported. The page is about how many connections to keep, and never discusses connection setup cost. Use pg-docs-connections / pg-wiki-number-of-connections or another source for the "why pool at all" part. The page does support the neighbouring idea that too many simultaneous connections hurt the database.
- `connection-pooling` objective 2 (compute a sensible pool size from cores, query load and DB connection limit, then validate by measurement): the best source in the mapping for this objective. It gives the formula, a worked example, the reasoning (CPU, disk I/O, network), an explicit "load-test around this starting point" instruction, and caveats for mixed long/short transactions. Gaps: it does not mention the database server's own connection limit (e.g. max_connections) or how to divide it among several app instances, and it gives no measurement procedure beyond "simulate load and try nearby values". A lesson must take those two pieces from pg-docs-connections / pg-wiki-number-of-connections.
- `connection-pooling` objective 3 (diagnose a pool that is exhausted, i.e. requests waiting for a connection): NOT well supported. The page treats waiting threads as the normal and desired state; it has no symptoms, metrics, timeout settings or procedure for telling healthy waiting from exhaustion. The only related material is the deadlock case in "Pool-locking" (all threads holding connections while waiting for more), which is one cause of a stuck pool. Another source is needed for diagnosis (the wiki sidebar lists other pages such as "Bad Behavior: Handling Database Down", which were not opened).
- `single-machine-limits` (depends on connection-pooling): the "10,000 users do not need a 10,000 pool" argument is useful background, but the concept is not mapped to this source.

## Warnings

- NO-AUTHOR and all-rights-reserved (see registry): short facts and numbers are fine; do not copy paragraphs. The formula is a general idea, and its PostgreSQL origin should be cited to the PostgreSQL source rather than to this page.
- Java/HikariCP-centric voice and some strong rhetoric ("sheer insanity"); numbers such as "3,000 users at 6,000 TPS" are the authors' claims without shown measurements.
- The disk discussion assumes spinning disks; the page itself says the formula was not analyzed for SSDs and then argues that SSDs push the optimum toward the core count. Do not present the formula as exact for modern hardware.
- The formula is about connections actively working in the database. In a lesson it must not be read as "the number of connections an app may open", and the page does not talk about several app servers sharing one database.
- Last edit is December 2021; there is no date for when the text was written.
