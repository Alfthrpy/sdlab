---
id: P1-084
title: "Check licenses of docs.aws.amazon.com entries (Site Terms say CC-BY-SA-4.0)"
milestone: M4
type: research
owner: agent
review: agent
status: todo
priority: low
depends_on: []
estimate: 1
outputs: []
---

## Context

Found by the source-verifier in P1-083: the AWS Site Terms (https://aws.amazon.com/terms/) say documentation hosted on docs.aws.amazon.com is licensed CC-BY-SA-4.0 (code MIT-0), unless otherwise licensed. The two new EC2 specification entries were corrected. About 13 older entries with a docs.aws.amazon.com URL (for example `dynamodb-docs-*`, `aws-sqs-*`) still say `all-rights-reserved`. This changes what may be adapted, not what is cited today, so it is low priority and does not block Unit 0.

## Tasks

1. List registry entries whose URL is on docs.aws.amazon.com (not aws.amazon.com blog or product pages, not builder.aws.com).
2. Reopen the Site Terms and confirm the license sentence and its scope. Decide per entry (some pages may carry their own terms), then update `license`, `usage`, and `notes`. If an entry becomes `adapt-with-attribution`, write the `attribution` line (see citation-guide.md).

## Done criteria

- [ ] Every docs.aws.amazon.com entry has a license that matches the Site Terms, or a note saying why not
- [ ] `python scripts/validate.py` passes

## Notes

(Filled in during the work.)
