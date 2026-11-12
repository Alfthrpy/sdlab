---
source: pg-docs-kernel-resources
read_by: agent
date: 2026-11-12
sections_read: ["18.4 Managing Kernel Resources (all subsections as summarized by the fetch tool)"]
---

# Notes: PostgreSQL 18 Documentation, 18.4. Managing Kernel Resources

> Notes are in English and in your own words.

## Key points

- (18.4.1) PostgreSQL needs shared memory and semaphores; semaphores scale with the number of connections and background workers. Hitting an OS limit can stop the server from starting at all. Lowering `max_connections` is the quick workaround.
- (18.4.2) PostgreSQL runs one OS process per connection, so the per-user process limit and the open-file limits have to cover `max_connections` plus everything else on the machine.
- (18.4.2) The listen backlog for new TCP connections is small by default and can overflow during a burst of connection attempts; it is raised via a kernel setting.
- (18.4.4) On Linux, memory overcommit means the OOM killer may kill the database when RAM and swap run out. The docs list mitigations: add swap, reduce per-connection and shared memory settings, use a connection pooler, set strict overcommit, and protect the main process.
- (18.4.5) Huge pages reduce memory-management overhead for large shared buffers, but are optional.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| One server process per client connection | 18.4.2 | Why connection count is a memory/process limit, not just a counter |
| The OOM killer acts only after RAM and swap are both exhausted | 18.4.4 | Basis for "how you hit the memory limit" |

## Relevant to concepts

- `limits-of-one-machine`: memory, processes, file descriptors, and connections as concrete ceilings.
- `connection-pooling`: the docs themselves list a pooler as a way to reduce memory pressure.

## Warnings

- The fetch tool returned a summary of this page rather than the verbatim text, and the subsection numbers (18.4.1 etc.) in these notes are not confirmed from the page; check them against the page before citing.
- Linux/BSD/macOS details vary; the OOM text is Linux only.
- Advanced tuning (huge pages, System V IPC) is beyond Unit 0.
