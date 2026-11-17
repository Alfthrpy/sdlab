---
source: robustperception-peak-to-mean-ratio
read_by: agent
date: 2026-11-17
sections_read: ["whole post (about 400 words)"]
---

# Notes: Do you know your peak-to-mean ratio? (Brian Brazil, Robust Perception blog, 2015-09-14)

> Notes are in English and in your own words. Whole post read on 2026-11-17 from the raw HTML (curl, text extracted). Byline: Brian Brazil; date September 14, 2015; tags best practices, capacity, estimation, provisioning, reliability. The page footer shows only blog, training, book and privacy links: no license statement.

## Key points

- (opening) User traffic is not constant: it rises and falls over the day and the week because people work, sleep, and live in different time zones. The author says this easily produces a 3-4x gap between the minimum and the maximum load over a day.
- (example 1) Converting 10 million requests per day to a rate: about 115 requests per second on average. Provisioning for the average means failing at the peak.
- (example 2) The opposite error: if you size storage as if the peak rate lasted all day (115 req/s each needing 1 MB), you get about 10 TB, which is too much, because the trough hours store less.
- (definition) Peak-to-mean ratio = peak traffic per second divided by average traffic per second, measured over a day or a week. It lets you convert safely in both directions between per-day volume and peak per-second load.
- (typical value) For a globally distributed user base, he says a ratio of roughly 1.6 to 1.7 is typical. Using it, the 10M/day example becomes about 200 req/s at peak (10M / 86,400 x 1.7).
- (advice) Always apply the ratio when moving between per-second or per-minute peaks and per-day, per-week or per-month totals.
- (aside) Rough design-stage math uses about 100,000 seconds in a day (a rounding), but for provisioning and capacity planning the author says to be more precise.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| 10,000,000 requests/day = about 115 requests/s on average (10M / 86,400) | example 1 | Plain arithmetic, matches the 86,400 s/day divisor |
| About 200 requests/s at peak for the same volume with ratio 1.7 | example 1 | |
| Typical peak-to-mean ratio about 1.6-1.7 for a globally distributed user base | definition paragraph | The author's experience, no data shown. A product used in one country or one time zone peaks harder |
| Min-to-max load difference over a day of 3-4x is easy to reach | opening | Same caveat |

## Relevant to concepts

- `app-plus-database` (unit 0), objective 1 (calculate from users and requests per second whether one app plus one database suffices): SUPPORTS the "per-day volume to average req/s to peak req/s" step and gives one numeric peak factor. It does not cover the users-to-requests step (requests per user per day) and does not say how many req/s one machine can serve. The users-to-req/s factor can come from the System Design Primer's conversion guide (1 req/s is about 2.5 million requests per month); the capacity side from SQLite (100K hits/day) and Craver (about 2,400 req/s average on a large tuned fleet).
- `latency-throughput`, `littles-law` (unit 1): minor, the idea that average load hides peaks.

## Warnings

- A practitioner blog post, 2015, on the blog of a Prometheus consultancy (the page's header says "Prometheus Monitoring Experts"); no data or method for how the 1.6-1.7 was obtained. Treat as a reasonable starting assumption, to be replaced by the reader's own traffic graphs.
- The 1.6-1.7 is for a global audience. A product for Indonesian users in one time zone (mostly WIB) has a bigger day/night swing, so the lesson should show the ratio as an input to measure, and a larger value as the cautious assumption. The post's 3-4x figure is a minimum-to-maximum gap, not a peak-to-mean ratio, so any specific larger ratio (for example 3) would be the lesson author's own assumption, not the post's.
- The post says "there are 100,000 seconds in a day" for rough design math (about 16% above 86,400); use 86,400 for the calculation.
- No license stated; rewrite only.
