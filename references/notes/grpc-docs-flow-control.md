---
source: grpc-docs-flow-control
read_by: agent
date: 2026-11-15
sections_read: ["Overview", "Note and Warning callouts", "Language Support"]
---

# Notes: Flow Control (gRPC docs)

> Notes are in English and in your own words. Short page; the fetch tool summarized it.

## Key points

- (Overview) Flow control stops a fast sender from overwhelming a slow receiver. It matters for streaming RPCs; unary RPCs do not need it. gRPC handles it by default.
- (Overview) The transport tells gRPC when it may send more. When the receiving side reads data it sends back an acknowledgement carrying the size, which opens capacity for the sender.
- (Overview) A write call on the sender hands the message to the gRPC library, which buffers it and passes it on; it does not mean the peer has the data. If the sender is too fast the library pauses the write call until there is room. This works the same for client-to-server and server-to-client streams.
- (Warning) Deadlock risk: if both sides do blocking reads, or both use manual flow control, and both write a lot without reading, they can block each other.
- (Language Support) Manual flow control is offered in some languages; the page only points to a Java example.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Page last modified October 5, 2023 | page footer | Content license CC BY 4.0 per the grpc.io repository LICENSE |

## Relevant to concepts

- `backpressure-consumer-lag`: backpressure crossing a network boundary between two services, where the slow receiver slows the sender through the protocol, versus a broker queue in between.

## Warnings

- Does not explain HTTP/2 windows or limits; do not claim details beyond acknowledgement-based sending.
- Only streaming RPCs; ordinary request-response calls need timeouts, concurrency limits and load shedding instead (see grpc-docs-deadlines, sre-book-handling-overload-ch21).
