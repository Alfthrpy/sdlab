---
source: rabbitmq-docs-flow-control
read_by: agent
date: 2026-11-15
sections_read: ["Overview", "How Does Flow Control Work"]
---

# Notes: Flow Control (RabbitMQ docs, 4.4)

> Notes are in English and in your own words. Very short page; the fetch tool summarized it.

## Key points

- (Overview) RabbitMQ protects itself with a backpressure mechanism applied to publishing connections, so that broker memory does not grow without bound when publishers are faster than the broker's slower parts (replicating to peer nodes, writing to disk).
- (How Does Flow Control Work) The broker slows down only connections that publish faster than queues can take messages. Nothing to configure.
- (How Does Flow Control Work) A throttled connection is shown in the state `flow`: it is blocked and unblocked many times per second to match the rate the server can sustain. For the client this looks like slower network bandwidth, not an error.
- (How Does Flow Control Work) Channels and queues can also be in flow state, and the pressure propagates back to the publishing connection. If connections are in flow, check whether consumers or prefetch settings are the real bottleneck.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Throttled connection state is called `flow` | How Does Flow Control Work | Visible in rabbitmqctl, management UI, HTTP API |

## Relevant to concepts

- `backpressure-consumer-lag`: an automatic, implicit form of backpressure (slow the sender down instead of rejecting); contrast with explicit rejection in rabbitmq-docs-maxlength.

## Warnings

- The page does not describe credit mechanics, memory or disk alarms, or the connection.blocked notification; those are on other RabbitMQ pages that were not opened.
- Producer throttling hides slowness as latency: a service that publishes inside a request will see requests get slower.
- Copyright Broadcom, no open license; rewrite only.
