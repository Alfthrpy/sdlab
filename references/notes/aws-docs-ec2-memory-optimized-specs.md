---
source: aws-docs-ec2-memory-optimized-specs
read_by: agent
date: 2026-11-17
sections_read: ["Performance specifications table (memory optimized families)", "Networking and EBS tables for U7i rows (skimmed)", "instance-types.html index page (current generation list, end-of-sale notice)"]
---

# Notes: Specifications for Amazon EC2 memory optimized instances (AWS EC2 documentation, Instance Types guide)

> Notes are in English and in your own words. Page opened on 2026-11-17 with a text fetch and checked in the raw HTML (curl): instance type names, memory and vCPU numbers were taken from the raw table cells. The page shows no date; the aws.amazon.com U7i product page (cross-checked) shows "(c) 2026 Amazon Web Services". Numbers change as AWS adds instance types, so the date of reading matters: 2026-11-17.

## Key points

- (Performance specifications table) Each row gives an instance type, memory in GiB, processor, vCPUs, physical cores, threads per core, and accelerator fields. The memory optimized group contains the R, X, z1d and U families.
- (U7i rows) The U7i family is the biggest single machine in this table. The names and numbers, exactly as the table shows them:
  - u7i-6tb.112xlarge: 6144 GiB memory, 448 vCPUs.
  - u7i-8tb.112xlarge: 8192 GiB, 448 vCPUs.
  - u7i-12tb.224xlarge: 12288 GiB, 896 vCPUs.
  - u7in-16tb.224xlarge: 16384 GiB, 896 vCPUs.
  - u7in-24tb.224xlarge: 24576 GiB, 896 vCPUs.
  - u7in-32tb.224xlarge: 32768 GiB, 896 vCPUs.
  - u7inh-32tb.480xlarge: 32768 GiB, 1920 vCPUs (960 physical cores, 2 threads per core).
  All are Intel Xeon Sapphire Rapids.
- (Other memory optimized rows) For scale: r7i.48xlarge has 1536 GiB and 192 vCPUs. The old high-memory U-3tb1 to U-24tb1 types appear in the family list, and the index page says U-9tb1, U-12tb1, U-18tb1 and U-24tb1 can no longer be newly launched; AWS recommends U7i instead.
- (index page, instance-types.html) The EC2 documentation separates the families into general purpose, compute optimized, memory optimized, storage optimized, accelerated computing, and high-performance computing, and lists current-generation names (M, C, R, U, X and others).

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Largest EC2 type in the memory optimized table on 2026-11-17: u7inh-32tb.480xlarge, 32768 GiB memory, 1920 vCPUs | Performance specifications table | Read 2026-11-17. This is a specialised SAP HANA class machine (the U7i product page describes SAP-certified in-memory databases); a general web app will not be sized this way |
| u7in-32tb.224xlarge: 32768 GiB, 896 vCPUs; u7i-12tb.224xlarge: 12288 GiB, 896 vCPUs | same table | The "-224xlarge" size is the 896-vCPU class |
| r7i.48xlarge: 1536 GiB, 192 vCPUs | same table | A more ordinary big memory-optimized size |
| U-9tb1, U-12tb1, U-18tb1, U-24tb1 are end of sale for new launches | instance-types.html, top notice | Shows that the ceiling moves over time |
| Compared with the 2015 figure in `aws-startups-scaling-part1-primer` (about 40 vCPUs, 244 GB) the 2026 ceiling is 1920 vCPUs and 32768 GiB (about 48x the vCPUs and about 134x the memory; my arithmetic) | table vs the primer | Good illustration that ceilings keep rising |

## Relevant to concepts

- `single-machine-limits` (unit 0), objective 3 (decide whether vertical scaling is enough from utilization data and the largest or priciest machine available): SUPPORTS the "largest machine available" input with a dated, current number. Together with `aws-docs-ec2-general-purpose-specs` (the ordinary-size ceiling) and `aws-ec2-price-list-us-east-1` (what it costs) a worked decision is possible. It says nothing about when to scale, which comes from `gregg-use-method` utilization reading.
- `app-plus-database` (unit 0): minor, the point that a single database server can have very large memory.

## Warnings

- Vendor documentation for one cloud. Other clouds and bare-metal vendors have different maximums; the argument "a ceiling exists and it is far above a beginner's workload" is general, the numbers are AWS's.
- The biggest sizes are EBS-only high-memory machines aimed at SAP-style in-memory databases (per the U7i product page), and are rarely the right choice for a typical web database. Regional availability was not checked. For the general ceiling, use the general-purpose family (see the other notes).
- A single machine this large is still a single point of failure (the author's reasoning, not the page's); do not present it as "no need to scale out".
- The page gives no prices, and has no date. Re-read before publishing; numbers can change.
