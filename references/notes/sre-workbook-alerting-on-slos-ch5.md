---
source: sre-workbook-alerting-on-slos-ch5
read_by: agent
date: 2026-11-16
sections_read: ["Whole chapter, through a WebFetch summary of the page (headings and main tables), not the raw HTML"]
---

# Notes: The Site Reliability Workbook, Chapter 5: Alerting on SLOs

> Notes are in English and in your own words. This note comes from a model-written summary of the page, not from my own reading of the full text. Numbers below should be rechecked against the page by the verifier before a lesson cites them.

## Key points

- (Ways to alert) The chapter walks through six approaches, each fixing a weakness of the previous: threshold on error rate, longer window, requiring a duration, burn-rate alerts, several burn rates, and finally multiwindow multi-burn-rate.
- (Burn rate) Burn rate is how fast the error budget is consumed compared with the rate that would exactly use it up over the SLO window. For a 99.9% SLO over 30 days, a rate of 1 empties the budget in 30 days.
- (Multi burn rate) Choose alerts by how much budget would be consumed: fast burns page a human, slow burns open a ticket. The summary gives for a 99.9% SLO: 14.4x over 1 hour (2% of budget), 6x over 6 hours (5%), 1x over 3 days (10%) as the ticket level.
- (Multiwindow) Add a short window (about one twelfth of the long one) that must also exceed the threshold, so the alert resets soon after the problem ends. The chapter recommends this as the most suitable approach for most applications.
- (Low traffic) Services with few requests make a single failure look like a huge burn; options include synthetic traffic, combining services, or loosening the SLO or window.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 14.4x / 1 h / 2% budget; 6x / 6 h / 5%; 1x / 3 days / 10% | multi burn rate section | For a 99.9% SLO; check page |

## Relevant to concepts

- `observability`: alert on user-visible symptoms tied to an SLO.
- `sli-slo`: practical use of the error budget for alerting.

## Warnings

- Needs prior SLO knowledge (see `sre-book-slo-ch4`, `sre-workbook-implementing-slos`).
- The "Alerting at Scale" and "Extreme Availability Goals" sections were not examined.
