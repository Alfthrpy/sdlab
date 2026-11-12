---
source: aws-sqs-visibility-timeout
read_by: agent
date: 2026-11-12
sections_read: ["Visibility timeout use cases", "Setting and adjusting the visibility timeout", "In flight messages and quotas", "Understanding visibility timeout in standard and FIFO queues", "Handling failures", "Changing and terminating visibility timeout", "Best practices"]
---

# Notes: Amazon SQS visibility timeout (AWS docs)

> Notes are in English and in your own words.

## Key points

- (Intro) Receiving a message does not remove it; it becomes hidden from other consumers for a period. The consumer must delete it explicitly after success.
- (Setting and adjusting) Timer starts at delivery; default is 30 seconds per queue, overridable per message with ChangeMessageVisibility.
- (Handling failures) If the consumer crashes or is too slow, the message reappears and another attempt happens. A very long timeout delays that retry.
- (Standard and FIFO) Because of at-least-once delivery, duplicates are still possible even within the timeout in standard queues. In FIFO, later messages in the same group wait until the in-flight one is deleted or expires, which keeps in-group order.
- (In flight messages) Messages received but not deleted count as in flight; standard queues cap this at roughly 120,000, and hitting the cap blocks further receives.
- (Best practices) Size the timeout to the normal processing time, extend with a heartbeat for long work, hard maximum of 12 hours from first receive, and attach a dead-letter queue for repeated failures.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Default visibility timeout 30 s | Setting and adjusting | Quota can change; re-check |
| Max 12 hours from first receive | Best practices | Extending does not reset it |
| About 120,000 in-flight (standard) | In flight messages and quotas | |

## Relevant to concepts

- `ack-redelivery`: delete = ack; timeout expiry = redelivery.
- `dlq`: the recommended partner mechanism.
- `idempotent-consumer`: duplicates remain possible.

## Warnings

- SQS specific vocabulary (no explicit ack message). No license in the fetched text; registry records all-rights-reserved.
