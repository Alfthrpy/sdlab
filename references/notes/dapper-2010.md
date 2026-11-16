---
source: dapper-2010
read_by: agent
date: 2026-11-16
sections_read: ["Abstract", "1 Introduction", "2 Distributed Tracing in Dapper (2.1-2.6)", "3 Deployment Status (3.1-3.3)", "4 Managing Tracing Overhead (4.1-4.6)", "5 General-Purpose Dapper Tools (5.1-5.2)", "6 Experiences (6.1-6.6)", "7 Other lessons learned", "8 Related work (partly)", "9 Conclusions (skimmed)"]
---

# Notes: Dapper, a Large-Scale Distributed Systems Tracing Infrastructure

> Notes are in English and in your own words. Read in full via pdftotext of research.google.com/archive/papers/dapper-2010-1.pdf (6 PDF pages of dense text). The first page prints "Google Technical Report dapper-2010-1, April 2010", so it is a technical report, April 2010. Figure contents were not visible in the extracted text.

## Key points

- (1) Motivation: one user request fans out across many services owned by different teams, so looking at total latency does not say which service is at fault. Two requirements follow: tracing must be everywhere, and it must be always on. Design goals: low overhead, no need for application developers to do anything, scalability; data available within about a minute.
- (2, 2.1) The model is a trace tree of spans. A span is a unit of work with a name, span id, parent id, start and end times and optional annotations; all spans of one request share a trace id (64-bit, probabilistically unique). A span with no parent is the root. Client and server both write into an RPC span, and clock skew is handled by noting that a request is sent before it is received.
- (2.2) Transparency is reached by instrumenting a few shared libraries (thread-local trace context, callbacks that carry the context, the common RPC framework) instead of every application. This only worked because Google's stack is homogeneous.
- (2.3) Developers can add text or key-value annotations, with a cap per span so they cannot crowd out the structural data.
- (2.5) Collection is out-of-band: spans go to local log files, daemons pull them, and they land in a Bigtable repository, one trace per row. Median collection delay is under 15 seconds; the 98th percentile can reach hours. Reasons for out-of-band: in-band data would swamp small RPC responses, and not all calls nest.
- (2.6) Payloads are not logged for privacy reasons; only method names are, and developers opt in with annotations.
- (4.1-4.3) Overhead is small per span (hundreds of nanoseconds) and the collection daemon uses well under 1% of a core. Without sampling, tracing every request on a web-search workload raised average latency noticeably; sampling below 1/16 (such as 1/1024) stayed within experimental error, while 1/16 itself still added about 2% latency (Table 2).
- (4.4, 4.5) Sampling: first a uniform 1 in 1024, then an adaptive scheme that targets a rate of traces per unit time, and records the sampling probability with each trace. For high-traffic services even very low sampling rates still catch recurring patterns; low-traffic services can trace everything.
- (4.6) A second sampling stage at collection hashes the trace id, so whole traces are kept or dropped; this controls storage and Bigtable write rate with one config knob.
- (5, 5.1, 5.2) Access via a trace id lookup, MapReduce over all traces, and a composite index (service, host, time). The UI groups traces by execution pattern, shows a latency histogram, and lets users open one trace.
- (6) Use cases: development of an ads service (latency improved by about two orders of magnitude, found needless calls to master DB), exception reports linked to traces, long-tail latency of universal search (critical-path analysis, network lag), service dependency inference, network usage attribution, shared storage attribution.
- (7) Limits: batching hides who caused work; batch/offline workloads need another id; tracing finds where the slowness is but not always why (queuing); kernel info is hard to tie in; firefighting needs fresh data, and aggregated analysis was too slow (not within 10 minutes) for some shared-storage incidents.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Sampling 1 in 1024 as first production default | Sec. 4.4 | Later made adaptive |
| Sampling frequencies below 1/16 (e.g. 1/1024) are within experimental error for web search latency; 1/16 itself still showed +2.12% latency | Sec. 4.3, Table 2 | Full tracing (1/1) added 16.3% average latency in that test |
| Median trace collection delay under 15 s | Sec. 2.5 | 98th percentile can be hours |
| Average span about 426 bytes; under 0.01% of network traffic | Sec. 4.2 | Google 2010 |
| Instrumentation core under 1000 lines C++ and under 800 lines Java | Sec. 3.1 | Shows how small the shared-library hook can be |
| Over 1 TB of sampled trace data per day | Sec. 4.6 | 2010 |

## Relevant to concepts

- `observability`: where traces fit next to metrics and logs; why context propagation matters.
- `observability` (tracing part): trace, span, parent id, sampling trade-offs.
- `timeouts`/tail latency: the critical path method used for long-tail debugging (pair with `tail-at-scale-cacm13`, not read by this agent).

## Warnings

- Google 2010, homogeneous RPC stack; modern systems use W3C trace-context headers and OpenTelemetry, not these exact designs. The paper does not use the words "OpenTelemetry" or "W3C".
- Figures (trace tree, UI screenshots, Table values in layout) were not seen in extracted text; numbers above come from running text and are checked against it, but table layouts could be misaligned.
- The Google Research page says "Google, Inc. (2010)" with no venue; the PDF says technical report, April 2010. The registry entry was updated to published 2010-04 during verification.
