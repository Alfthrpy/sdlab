---
source: aws-ec2-price-list-us-east-1
read_by: agent
date: 2026-11-17
sections_read: ["JSON price list: publicationDate, products (attributes), terms.OnDemand for selected instance types", "region_index.json (disclaimer, publicationDate)", "AWS docs page 'Getting price list files using the AWS Price List Bulk API'"]
---

# Notes: Amazon EC2 price list file, region us-east-1 (AWS Price List Bulk API)

> Notes are in English and in your own words. The file (about 460 MB of JSON) was downloaded with curl on 2026-11-17 into a scratch folder and queried with jq; it is not stored in the repo. The index file `region_index.json` gives `publicationDate` 2026-11-14T01:29:26Z, and the us-east-1 file's own `publicationDate` is the same. The index file also carries a disclaimer: the list is for information only and prices are subject to the terms on the AWS pricing pages. AWS's "Getting price list files ..." documentation page describes how these files are published; it was opened to confirm that the URL pattern is official. The AWS on-demand pricing web page (aws.amazon.com/ec2/pricing/on-demand/) was fetched too, and its text has no per-instance price table, which is why the JSON is used.

## Key points

- (query used) Filter: operating system Linux, shared tenancy, no pre-installed software, capacity status Used, region us-east-1 (N. Virginia). The price shown is the On-Demand price per hour in USD.
- (M7i) Price per hour goes up in exact proportion to size: m7i.large (2 vCPU, 8 GiB) 0.1008 USD; m7i.xlarge (4, 16) 0.2016; m7i.2xlarge (8, 32) 0.4032; m7i.4xlarge (16, 64) 0.8064; m7i.8xlarge (32, 128) 1.6128; m7i.16xlarge (64, 256) 3.2256; m7i.48xlarge (192, 768) 9.6768. That is 0.0504 USD per vCPU-hour at every size (my arithmetic): doubling the machine doubles the price.
- (other big sizes) r7i.48xlarge (192 vCPU, 1536 GiB) 12.7008 USD per hour; m8i.96xlarge (384, 1536) 20.32128 USD per hour; u7i-12tb.224xlarge (896, 12288 GiB) 125.58182 USD per hour; u7in-32tb.224xlarge (896, 32768 GiB) 360.98695 USD per hour.
- (absence) u7inh-32tb.480xlarge, the biggest type in the AWS documentation (1920 vCPUs), has no product entry at all in the us-east-1 file, so no price was found for it. The u7in and u7i rows exist.

## Citable numbers & facts

All prices are On-Demand, Linux, shared tenancy, us-east-1, from the file published 2026-11-14 and read 2026-11-17. Monthly figures use 730 hours per month (my arithmetic, rounded).

| Instance type (as the file shows it) | vCPU | Memory | USD per hour | About USD per month |
| --- | --- | --- | --- | --- |
| m7i.large | 2 | 8 GiB | 0.1008 | 74 |
| m7i.xlarge | 4 | 16 GiB | 0.2016 | 147 |
| m7i.4xlarge | 16 | 64 GiB | 0.8064 | 589 |
| m7i.16xlarge | 64 | 256 GiB | 3.2256 | 2,355 |
| m7i.48xlarge | 192 | 768 GiB | 9.6768 | 7,064 |
| r7i.48xlarge | 192 | 1536 GiB | 12.7008 | 9,272 |
| m8i.96xlarge | 384 | 1536 GiB | 20.32128 | 14,835 |
| u7i-12tb.224xlarge | 896 | 12288 GiB | 125.58182 | 91,675 |
| u7in-32tb.224xlarge | 896 | 32768 GiB | 360.98695 | 263,520 |

Ratios (my arithmetic): m7i price per vCPU-hour is constant at 0.0504; m8i.96xlarge is 0.0529 and r7i.48xlarge 0.0662; u7i-12tb.224xlarge is 0.140 and u7in-32tb.224xlarge is 0.403 per vCPU-hour, but they are priced for memory (about 0.010 to 0.011 USD per GiB-hour against 0.0126 for m7i).

## Relevant to concepts

- `single-machine-limits` (unit 0), objective 3 (decide whether vertical scaling is enough from utilization and the biggest or priciest machine available): SUPPORTS the cost input. Inside the M7i family each doubling of size doubles the hourly price, so the price of the next step up is predictable from the current bill; at the top of the range, memory-heavy machines cost far more per vCPU. It does not say when a bigger machine is better than scaling out; that reasoning is the lesson author's.
- `app-plus-database` (unit 0): minor, a way to attach a monthly cost to "one big server".

## Warnings

- Prices change, differ between regions (a Jakarta region, ap-southeast-3, has its own file; not read) and between operating systems, and exclude storage, data transfer, reserved or savings-plan discounts. Always repeat the date: prices as of 2026-11-14 publication, read 2026-11-17.
- It is a machine-readable data file, not an explanatory page; it is cited for numbers only. For anyone checking: use the AWS Price List Bulk API as described on the AWS docs page, then filter as above.
- The file's `current` URL changes content with each publication; the version used is identified by `publicationDate`. The file has no license text; AWS pricing pages carry "(c) 2026 Amazon Web Services, Inc. or its affiliates. All rights reserved." so the registry entry is all-rights-reserved, rewrite-only (facts only).
- Dollar numbers are illustrations: the lesson should round them and say "sekitar" with the date.
