# Citation & attribution guide (final, P1-018)

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

`loc` is required for `book` and `paper` sources (chapter, section, or page).

What `python scripts/validate.py` enforces in content:

| Rule | Level |
| --- | --- |
| Every `[^id]` marker is in the registry and in the lesson's `sources` | error |
| Every id in `sources` (and in a question's `sources`) is in the registry | error |
| `status: published` content cites only `approved` sources (lesson and questions) | error |
| Tier 6 (`map-only`) sources are never cited | error |
| `book`/`paper` sources have `loc` | error |
| A lesson using an `adapt-with-attribution` source has the attribution line (contains "diadaptasi") | error |
| The attribution line names the source title | warning |
| More than one direct quote per source per lesson, or a quote over 14 words (heuristic, see below) | error |

Tests for these rules: `tests/test_content.py`.

## When a citation is required

- Numbers (latency, throughput, cost, years, incident durations)
- Specific behavior of a product or system
- "Best practice" claims or recommendations
- Incident timelines and root causes

General knowledge found in many sources still needs at least one source in `sources`, though it does not need a marker per sentence.

## Direct quotes

At most **one** short quote per source per lesson: fewer than 15 words, in quotation marks, with a source marker right after it. Use a quote only when the exact wording matters, such as a definition or an official statement. Everything else is rewritten in your own words.

The validator is a heuristic. It counts a quoted span of 4 or more words, in straight or curly double quotes, that is followed by a `[^id]` marker (punctuation may sit between them). Shorter quoted terms such as "split brain" are not counted, and code blocks are skipped. It does not catch quotes with no marker, quotes in `questions.yaml`, or single-quote styles, so the reviewer still checks those. A fragment counts as a quote just like a full sentence.

| Example | Verdict |
| --- | --- |
| `Definisi resminya: "sistem yang tetap berjalan saat sebagian komponen gagal".[^src]` | OK: one short quote, marker attached |
| Two separate quoted phrases, both followed by `[^src]` | Not OK: second quote from the same source |
| A quoted sentence of 15 or more words | Not OK: too long; paraphrase it or cut it down |
| Reordering a source's three-point list in the same order with the same wording | Not OK: this is copying structure, not quoting; restructure it (reviewer-judged) |
| "Retry tanpa jitter bikin semua klien mencoba lagi bersamaan.[^src]" with no quotation marks | OK: this is a paraphrase, not a quote (reviewer-judged) |

Diagrams are always your own.

## Attribution for CC BY material

When adapting CC BY material (for example System Design Primer), add this at the end of the file (the attribution text is learner-facing, so it is in Indonesian; the validator looks for "diadaptasi"):

```markdown
---
Sebagian materi diadaptasi dari *System Design Primer* oleh Donne Martin,
CC BY 4.0, https://github.com/donnemartin/system-design-primer. Telah diubah.
```

## Sample lesson (dummy, for checking the rules)

```markdown
---
concept: example-retries
title: "Retry dan jitter"
status: draft
sources:
  - id: aws-builders-timeouts-retries
  - id: ddia-2e
    loc: "bab 8, Unreliable Networks"      # loc is required for books and papers
---

Retry tanpa jitter membuat semua klien mencoba ulang di waktu yang sama.[^aws-builders-timeouts-retries]
Jaringan bisa menunda atau menghilangkan paket tanpa memberi tahu pengirim.[^ddia-2e]
```

`tests/test_content.py` runs this exact sample through the validator. `status: draft` lessons may cite `candidate` sources; `published` ones may not.

## Forbidden

- Copying paragraphs, chapter structure, or point order from copyrighted sources
- Copying or tracing diagrams
- Citing `status: candidate` sources in `published` content
- Citing Tier 6 sources as content references
