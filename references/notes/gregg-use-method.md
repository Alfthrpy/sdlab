---
source: gregg-use-method
read_by: agent
date: 2026-11-17
sections_read: ["Intro", "Summary (incl. Does Low Utilization Mean No Saturation?, Resource List)", "Metrics (tables of basic and harder metrics)", "Software Resources", "Suggested Interpretations", "Cloud Computing", "Strategy", "Other Methodologies", "Conclusion", "Updates"]
---

# Notes: The USE Method (Brendan Gregg, brendangregg.com)

> Notes are in English and in your own words. Located by section heading because the page has no section numbers. Read with WebFetch, and the numbers below (70%, 80%, five-minute averages) were re-checked in the raw HTML via curl. The Linux checklist subpages were not opened. Not read in detail: the Apollo section and the later "Updates" list of third-party mentions.

## Key points

- (Intro, Summary) The method is a question-first checklist: list every resource of the system, then for each one check utilization, saturation, and errors. It is meant for the early phase of a performance investigation to find systemic bottlenecks and errors quickly. The author is open that it is one tool in a larger toolbox and does not solve every problem type.
- (Intro) The author's own claim is that it solves about 80% of server issues with about 5% of the effort. This is a personal estimate, not a measured result.
- (Summary, terminology) Resource: any physical server component (CPUs, memory, disks, network interfaces, buses); some software-imposed limits can also be treated as resources.
- (Summary, terminology) Utilization: the average time a resource was busy doing work. An alternative definition is the fraction of capacity used, where 100% means no more work can be accepted. Saturation: how much extra work a resource has that it cannot serve right now, usually waiting in a queue. Errors: the count of error events.
- (Summary, terminology) Typical forms: utilization as a percentage over an interval, saturation as a queue length, errors as a plain count.
- (Resource List) Generic server list: CPUs (sockets, cores, hardware threads), memory capacity, network interfaces, storage devices (both as I/O and as capacity), controllers, interconnects.
- (Metrics, basic table) Example metrics: CPU utilization = busy percent, CPU saturation = run-queue length or scheduler latency; memory utilization = free memory, memory saturation = paging/swapping; network utilization = throughput relative to maximum bandwidth; storage I/O utilization = device busy percent, storage saturation = wait queue length, storage errors = device error counters.
- (Metrics, harder table) Items that are harder to get: memory errors (failed allocations), network saturation (drops or overruns), controller and interconnect utilization.
- (Does Low Utilization Mean No Saturation?) Low average utilization does not rule out saturation: a long averaging window can hide short bursts at 100%. The page tells of a customer who had CPU latency problems while 5-minute monitoring showed at most 80%, because the CPU hit 100% for seconds at a time.
- (Suggested Interpretations) 100% utilization is usually a bottleneck, so confirm with saturation. Utilization beyond about 70% can start to hurt for two reasons: long averages hide bursts, and resources that cannot be interrupted mid-operation (disks are the example) queue more often once above roughly 70%. Any non-zero saturation can be a problem. Non-zero error counts are worth investigating, especially if still growing while performance is poor. Low utilization with no saturation and no errors is also useful: it removes that resource from suspicion.
- (Software Resources) Some software limits can be treated the same way, with examples: mutex locks, thread pools (utilization = time threads are busy, saturation = requests waiting for a thread), process/thread capacity, file descriptor capacity. The author says not to worry too much about these and to use latency-based methods if the metrics are awkward.
- (Cloud Computing) In cloud environments, hypervisor or container (cgroup) limits on memory, CPU, network and storage I/O, and external limits such as network throughput, should be examined with the same three checks.
- (Strategy) Steps: build the resource list; per resource check errors first if easy (quick to read), then utilization and saturation; treat each finding as a candidate bottleneck to investigate further with other methods; continue through the remaining resources because several problems can coexist; decide whether to reduce the applied load or tune/upgrade the resource.
- (Intro/Other Methodologies) The method deliberately starts from questions, then looks for metrics, so metrics that are missing are recorded as "known unknowns" instead of silently skipped.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Rule of thumb: utilization above about 70% can begin to cause problems | Suggested Interpretations | Phrased as "can begin to be a problem" with reasons, not as a hard limit; the same number is used as the trigger in `capacity-headroom` in Unit 1 |
| 100% utilization is usually a bottleneck; check saturation to confirm | Suggested Interpretations | |
| Example: monitoring showed CPU at most 80% over 5-minute averages while the CPU hit 100% for seconds at a time and caused latency | Does Low Utilization Mean No Saturation? | Good illustration for why averages hide saturation |
| "Solves about 80% of server issues with 5% of the effort" | Intro | Author's subjective claim; present as opinion, if used at all |
| Page last updated 24 Aug 2017 | footer | Concepts are general and have not changed, but the specific Linux tool checklists live on other pages not read here |

## Relevant to concepts

- `single-machine-limits` objective 1 (recognize which of CPU, memory, disk, or connections is the bottleneck from symptoms and metrics): supports well for CPU, memory, disk, and network via the basic metrics table and the interpretation rules. It does not mention database connection counts as a resource, except through the generic "software resources" idea (thread pools, file descriptors); for connections the lesson needs `pg-docs-kernel-resources` or the database docs.
- `single-machine-limits` objective 2 (apply the USE method to one resource): this is the primary source and supports it fully. Definitions, the three checks per resource, an example metric for each resource type, interpretation hints, and the "low utilization does not imply no saturation" pitfall are all there, so a worked exercise ("for the disk, which three metrics, and what does each value mean?") can be built from it.
- `single-machine-limits` objective 3 (decide if vertical scaling is enough from per-resource utilization and the size or price limits of the largest machine): only half supported. The source tells how to read utilization and saturation per resource and that the final step is to either reduce the load or tune/upgrade the resource (Strategy), but it contains nothing about machine size limits, prices, or when scaling up stops being sensible. That half has to come from the other mapped sources (craver-stack-overflow-architecture-2016, aws-startups-scaling-part1-primer) or be flagged as a gap.
- `capacity-headroom` (Unit 1, not the target of this ticket): the 70% rule of thumb and the saturation caveat are relevant.
- `basic-monitoring` (not mapped to this source): the "saturation" signal in the SRE golden signals has the same meaning as the USE saturation; see google-sre-book-monitoring-ch6.

## Warnings

- Author name: the page itself shows only "Brendan" in the nav header ("Brendan's site"); the full name is inferred from the domain (as already noted in the registry).
- The method is about resource bottlenecks, not a method for every problem type: the page says it does not solve all of them and points to latency-based methods (Method R) for DBAs and developers, so slow queries and lock contention are the note writer's examples of what it misses. In `single-machine-limits`, use it as a first screening step, not a complete diagnosis.
- The 70% figure is conditional (depends on averaging window and whether the resource can be preempted); do not turn it into a blanket "scale at 70%" rule without that caveat.
- The tables are Unix/Linux-flavored examples at the level of concept names; actual commands per OS are in separate checklist pages that were not opened.
- The page uses "utilization" in two senses (time busy, and fraction of capacity); say which one you mean in a lesson.
