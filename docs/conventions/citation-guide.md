# Citation & attribution guide (v0, finalized in P1-018)

## Inside content

Every content file lists its sources by **registry id**, not raw URLs. URLs are pulled from the registry at build time, so fixing a link happens in one place.

In lesson frontmatter:

```yaml
sources:
  - id: ddia-2e
    loc: "bab 6, Replication"         # chapter/section/page — required for books and papers
  - id: aws-builders-timeouts-retries
```

In the body, reference specific claims with a `[^id]` marker:

```markdown
Retry tanpa jitter membuat semua klien mencoba ulang di waktu yang sama.[^aws-builders-timeouts-retries]
```

The validator checks that every `[^id]` exists in `sources` and in the registry.

## When a citation is required

- Numbers (latency, throughput, cost, years, incident durations)
- Specific behavior of a product or system
- "Best practice" claims or recommendations
- Incident timelines and root causes

General knowledge found in many sources still needs at least one source in `sources`, though it does not need a marker per sentence.

## Direct quotes

At most one short sentence (< 15 words) per source per lesson, in quotation marks with a source marker. Use only when the exact wording matters, such as a definition or an official statement.

## Attribution for CC BY material

When adapting CC BY material (for example System Design Primer), add this at the end of the file (the attribution text is learner-facing, so it is in Indonesian; the validator looks for "diadaptasi"):

```markdown
---
Sebagian materi diadaptasi dari *System Design Primer* oleh Donne Martin,
CC BY 4.0, https://github.com/donnemartin/system-design-primer. Telah diubah.
```

## Forbidden

- Copying paragraphs, chapter structure, or point order from copyrighted sources
- Copying or tracing diagrams
- Citing `status: candidate` sources in `published` content
- Citing Tier 6 sources as content references
