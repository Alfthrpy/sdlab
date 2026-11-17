---
source: aws-docs-ec2-general-purpose-specs
read_by: agent
date: 2026-11-17
sections_read: ["Performance specifications table (M7i, M8i rows)"]
---

# Notes: Specifications for Amazon EC2 general purpose instances (AWS EC2 documentation, Instance Types guide)

> Notes are in English and in your own words. Opened 2026-11-17 with a text fetch (which read the first part of a very long page) and re-checked in the raw HTML (curl); numbers below come from the raw table cells. No date on the page. Only the M7i and M8i rows (current general purpose families that go up to the largest sizes) and the table columns were read in detail; other families were not.

## Key points

- (Performance specifications table) Columns are: instance type, memory in GiB, processor, vCPUs, physical cores, threads per core, accelerators. The M7i family (Intel Xeon Sapphire Rapids) lists sizes from large to 48xlarge; M8i (Intel Xeon Granite Rapids) goes up to 96xlarge.
- (M7i rows) The sizes the page shows, in order, with memory and vCPUs: m7i.large 8 GiB / 2 vCPUs; m7i.xlarge 16 / 4; m7i.2xlarge 32 / 8; m7i.4xlarge 64 / 16; m7i.8xlarge 128 / 32; m7i.12xlarge 192 / 48; m7i.16xlarge 256 / 64; m7i.24xlarge 384 / 96; m7i.48xlarge 768 GiB / 192 vCPUs. So within a family each step doubles the memory and vCPUs (4 GiB per vCPU).
- (M8i rows) m8i.96xlarge has 1536 GiB and 384 vCPUs (192 physical cores, 2 threads per core). The raw table also lists m8i.metal-48xl and m8i.metal-96xl (bare-metal sizes).
- (m7i.large row) 1 physical core with 2 threads gives 2 vCPUs: a "vCPU" on these types is a hardware thread, not a full core. Useful when a lesson compares "cores" in a pool-size formula with vCPUs of a cloud instance.

## Citable numbers & facts

| Fact | Location | Context note |
| --- | --- | --- |
| Largest general purpose size found in this read: m8i.96xlarge, 1536 GiB, 384 vCPUs; largest M7i: m7i.48xlarge, 768 GiB, 192 vCPUs | table rows | Read 2026-11-17; other general purpose families (M6, M8a, M8g) not checked, so this is "the largest I checked", not a verified overall maximum |
| M7i doubles memory and vCPUs with each size step, 4 GiB per vCPU | table rows | The ratio is the page's data; the "doubles" description is my reading |
| vCPUs = 2 x physical cores on the Intel types shown (2 threads per core) | table rows | |

## Relevant to concepts

- `single-machine-limits` (unit 0), objective 3: SUPPORTS the "ordinary" ceiling: an everyday machine can go from 2 vCPUs / 8 GiB up to 192 vCPUs / 768 GiB (M7i) or 384 vCPUs / 1536 GiB (M8i) in standard steps, so for most web apps the question "is vertical scaling enough" is about cost and the single point of failure more than about running out of machine sizes. Use with `aws-docs-ec2-memory-optimized-specs` (absolute ceiling) and `aws-ec2-price-list-us-east-1` (cost).
- `connection-pooling` (unit 0): minor, vCPU vs core distinction for the pool-size formula.

## Warnings

- AWS-only, and the family names are specific to this generation (M7i, M8i); expect new generations to replace them. Re-read before publishing.
- The page is very long (many families); the numbers above are for the rows listed only.
- No prices on this page.
