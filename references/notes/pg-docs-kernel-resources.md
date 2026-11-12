---
source: pg-docs-kernel-resources
read_by: agent
date: 2026-11-12
sections_read: ["18.4 Managing Kernel Resources (section list and Resource Limits / Linux Memory Overcommit checked on the page, 2026-11-12)"]
---

# Notes: PostgreSQL 18 Documentation, 18.4. Managing Kernel Resources

> Notes are in English and in your own words.

## Key points

- (18.4.1 Shared Memory and Semaphores) PostgreSQL needs shared memory and semaphores; semaphores scale with the number of connections and background workers. Hitting an OS limit can stop the server from starting at all. Lowering `max_connections` is the quick workaround.
- (18.4.3) PostgreSQL runs one OS process per connection, so the per-user process limit and the open-file limits have to cover `max_connections` plus everything else on the machine.
- (18.4.3) The listen backlog for new TCP connections is small by default and can overflow during a burst of connection attempts; it is raised via a kernel setting (net.core.somaxconn on Linux).
- (18.4.4) On Linux, memory overcommit means the OOM killer may kill the database when RAM and swap run out. The docs list mitigations: add swap, reduce per-connection and shared memory settings, use a connection pooler, set strict overcommit, and protect the main process.
- (18.4.5) Huge pages reduce memory-management overhead for large shared buffers, but are optional.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| One server process per client connection | 18.4.3 | Why connection count is a memory/process limit, not just a counter |
| The OOM killer acts only after RAM and swap are both exhausted | 18.4.4 | Basis for "how you hit the memory limit" |

## Relevant to concepts

- `limits-of-one-machine`: memory, processes, file descriptors, and connections as concrete ceilings.
- `connection-pooling`: the docs themselves list a pooler as a way to reduce memory pressure.

## Warnings

- Real structure of 18.4 (checked on the page): 18.4.1 Shared Memory and Semaphores, 18.4.2 systemd RemoveIPC, 18.4.3 Resource Limits, 18.4.4 Linux Memory Overcommit, 18.4.5 Linux Huge Pages. Process-per-connection, open-file limits and the listen backlog are all in 18.4.3. The fetch tool summarizes pages, so re-read exact wording before quoting.
- Linux/BSD/macOS details vary; the OOM text is Linux only.
- Advanced tuning (huge pages, System V IPC) is beyond Unit 0.
