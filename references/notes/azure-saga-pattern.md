---
source: azure-saga-pattern
read_by: agent
date: 2026-11-16
sections_read: ["Context and problem", "Solution", "Problems and considerations", "When to use this pattern"]
---

# Notes: Saga Design Pattern (Azure Architecture Center)

> Notes are in English and in your own words.

## Key points

- (Context and problem) With a database per service, one ACID transaction cannot span services; the page names two-phase commit as the traditional option and says sagas often suit these cases better.
- (Solution) A saga is a chain of local transactions; each commits in its own service and triggers the next via an event or message. On failure, compensating transactions undo earlier steps.
- (Key concepts) Steps are compensable (can be undone), pivot (the point of no return), or retryable (after the pivot, must be idempotent and eventually succeed).
- (Choreography) Services react to each other's events with no central controller: simple for few services, hard to follow as steps grow, risk of cyclic dependencies.
- (Orchestration) A central orchestrator tells participants what to do and tracks state: clearer for complex flows, but it is one more component that can fail.
- (Problems and considerations) Compensation can itself fail; sagas need idempotent handlers, monitoring, and are hard to debug.
- (Data anomalies) Because sagas have no isolation, lost updates, dirty reads and fuzzy reads can happen; countermeasures include semantic locks, commutative updates, rereading values before updating.
- (When to use) Use when you need consistency without tight coupling and can compensate; avoid with tightly coupled steps or cyclic dependencies.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Two implementation styles: choreography and orchestration | Solution | |

## Relevant to concepts

- `distributed-transactions`: saga vs two-phase commit, compensation, idempotency, anomalies.
- `transactions-acid`: what is lost when ACID stops at the service boundary.

## Warnings

- Azure-oriented in places; mentions 2PC only briefly, so pair with `pg-docs-prepare-transaction`.
- Original saga paper (1987) not opened.
