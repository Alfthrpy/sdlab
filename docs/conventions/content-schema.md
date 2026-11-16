# Data & content schema (v0)

The registry schema is final as of P1-010. The curriculum part is final for M2. The per-concept content schema (section 4) is final as of P1-030. Lab and incident formats (section 5) are finalized in P1-033. Everything is checked by `scripts/validate.py`.

Language: field names, keys, ids, and enum values are English. Learner-facing values (concept `title`, `objectives`, lesson text, questions, explanations) are Indonesian (see [ADR 0005](../decisions/0005-agent-facing-language.md)).

## 1. `references/registry.yaml`

```yaml
sources:
  - id: ddia-2e                       # kebab-case, unique, stable (do not rename once used)
    title: "Designing Data-Intensive Applications, 2nd Edition"
    authors: [Martin Kleppmann, Chris Riccomini]
    publisher: O'Reilly Media         # or site/organization name
    type: book                        # book | paper | article | postmortem | docs | repo | course | talk
    tier: 1                           # 1–6, see research-protocol.md
    url: https://www.oreilly.com/library/view/-/9781098119058
    doi: null                         # required for papers when one exists
    published: "2026-02"              # YYYY, YYYY-MM, or YYYY-MM-DD
    edition: "2"                      # optional
    accessed: "2026-11-12"            # date the page was opened
    license: all-rights-reserved      # all-rights-reserved | CC-BY-4.0 | CC-BY-SA-4.0 | CC-BY-NC-4.0 | CC-BY-NC-SA-4.0 | CC-BY-NC-ND-4.0 | CC-BY-3.0 | CC-BY-SA-2.5 | MIT | Apache-2.0 | ISC | PostgreSQL | public-domain | unknown
    usage: rewrite-only               # rewrite-only | adapt-with-attribution | map-only
    access: paywalled                 # free | partial | paywalled
    units: [3, 4, 5]                  # curriculum units 0–6 (0 = single-server starting unit)
    topics: [replication, partitioning, transactions]
    status: candidate                 # candidate | approved | rejected | deprecated
    free_companion: []                # registry ids of FREE sources covering the same topics (required if approved + paywalled)
    superseded_by: null               # registry id of the newer edition (only with status: deprecated)
    version: ""                       # doc/repo version or commit hash when there is no edition (e.g. "commit 1a2b3c4")
    archive_url: ""                   # web.archive.org snapshot, protects against link rot
    attribution: ""                   # credit line to paste into content; required if approved + adapt-with-attribution
    lang: en                          # en | id (absent means en; set id for Indonesian-language sources)
    verified_on: ""                   # YYYY-MM-DD the page was reopened and metadata checked (required if approved)
    notes: ""                         # reasons, warnings, caveats (English)
```

Required for every entry: `id`, `title`, `url`, `accessed`, `type`, `tier`, `license`, `usage`, `access`, `status`. All other fields are optional while the status is `candidate`. `accessed` must be a full date (`YYYY-MM-DD`); `doi` is the bare DOI (`10.xxxx/...`), not a URL; `topics` are kebab-case.

Validator rules (errors unless marked warning):
- Unknown field names are rejected, with a "did you mean" hint.
- `usage: adapt-with-attribution` only for licenses `CC-BY-4.0`, `CC-BY-3.0`, `CC-BY-SA-4.0`, `CC-BY-SA-2.5`, `MIT`, `Apache-2.0`, `ISC`, `PostgreSQL`, or `public-domain`.
- `tier: 6` requires `usage: map-only`. (warning) `map-only` on other tiers.
- (warning) `type: postmortem` should be tier 4 and `type: paper` tier 3. (warning) tier 5 with a non-open license.
- (warning) `type: paper` without a `doi`.
- `free_companion` entries must exist in the registry, must not be the source itself, and must have `access: free`.
- `superseded_by` is only valid with `status: deprecated` and must name an existing id.
- Additional rules for `status: approved`:
  - `license` is not `unknown`, and the `SEED` marker is gone from `notes`.
  - `verified_on` is set (a valid date, not in the future).
  - `usage: adapt-with-attribution` has an `attribution` credit line.
  - `authors` and `published` are filled in, or `notes` contains `NO-AUTHOR: <reason>` / `NO-DATE: <reason>` (e.g. a corporate postmortem).
  - `units` and `topics` are not empty.
  - `access: paywalled` requires a non-empty `free_companion`.
  - (warning) a book without an `edition`.
- (warning) `rejected` or `deprecated` without an explanation in `notes`; (warning) `deprecated` without `superseded_by`.
- Malformed input (non-mapping entries, wrong types, duplicate list items, invalid calendar dates, DOIs not matching `10.xxxx/...`) gives a clear error instead of a crash.

## 2. `curriculum/concepts.yaml`

```yaml
concepts:
  - id: caching-basics                # kebab-case
    unit: 2                           # 0–6; Unit 0 is the single-server starting unit
    title: Dasar caching              # Indonesian (learner-facing)
    objectives:                       # 1–4 testable objectives, Indonesian, starting with "Bisa ..."
      - Bisa menjelaskan kapan cache-aside lebih cocok daripada write-through
    trigger: Bacaan database mendominasi beban dan query yang sama diulang terus   # Indonesian; the symptom/number that says it is time to use this (units 1–6; optional in Unit 0)
    prerequisites: [latency-throughput]   # other concept ids; must form a DAG
    sources: [system-design-primer, aws-builders-caching]   # ≥2 registry ids
    formats: [lesson, quiz, lab]      # lesson | quiz | lab | incident
    status: planned                   # planned | drafting | review | published
```

Rules: `unit` is an integer 0–6. `trigger` (growth ladder, ADR 0004 Amendment 1) is a short learner-facing string; concepts in units 1–6 get a warning without it until they reach `review`, where it becomes an error. Unit 0 concepts are the baseline and may omit it.

## 3. `curriculum/case-studies.yaml`

```yaml
items:
  - id: incident-aws-dynamodb-dns-2025
    kind: incident                    # incident | case-study
    title: DNS DynamoDB us-east-1, Okt 2025   # Indonesian (learner-facing)
    concepts: [dns, dependency-blast-radius, retry-backoff-jitter]
    sources: [aws-pes-dynamodb-2025-10]
    status: planned
```

## 4. Content per concept — `content/concepts/<concept-id>/` (final, P1-030)

| File | Contents |
| --- | --- |
| `lesson.md` | Frontmatter + lesson text (below). Citation rules: [citation-guide](citation-guide.md) |
| `questions.yaml` | 6–10 questions (schema below) |
| `misconceptions.md` | 3–6 common misconceptions, used for distractors (format below) |
| `lab.yaml` | Lab spec (optional, finalized in P1-033) |

The folder name is the concept id and must exist in `curriculum/concepts.yaml`.

### Stage: `status` in the lesson frontmatter

`status` is `draft | review | published` and sets how strict the validator is. In `draft`, gaps are warnings. From `review` on, they are errors: lesson length outside 300–600 words, fewer than 6 questions, a learning objective that no question covers, a missing `misconceptions.md`, a question without `objective`, fewer than 3 misconceptions. `published` also requires `reviewed_by` and approved sources only.

### `lesson.md`

```yaml
---
concept: caching-basics            # must equal the folder name
title: Dasar caching               # Indonesian
sources:                           # registry ids; {id, loc} where `loc` is required for book/paper sources
  - azure-cache-aside-pattern
  - {id: ddia-2e, loc: "ch. 3"}
status: draft                      # draft | review | published
reviewed_by: content-reviewer      # required when published (agent or person)
---
```

Body: 300–600 words, Indonesian, `[^id]` markers for specific claims (every marker must be in `sources`), at most one short quote per source. The validator counts words with `\w+` after removing fenced code blocks, `[^id]` markers, and URLs, so `x-y` counts as two words.

### `questions.yaml`

```yaml
questions:
  - id: caching-basics-q01          # <concept-id>-qNN, unique
    type: mcq                       # mcq | multi | order | match | estimate
    difficulty: 2                   # 1-3 (see writing-style.md)
    objective: 1                    # 1-based index into the concept's `objectives` in concepts.yaml
    prompt: "..."
    options: ["...", "...", "..."]  # mcq 3-5, multi 4-6, order 3-6; distinct
    answer: 1                       # see the table
    explanation: "..."              # required; 1-3 sentences (style rule in writing-style.md, not enforced)
    sources: [system-design-primer]
    targets_misconception: stale-read-ok   # optional; must be an id in misconceptions.md
```

| `type` | Extra fields and `answer` format |
| --- | --- |
| `mcq` | `options` (3-5); `answer`: one option index |
| `multi` | `options` (4-6); `answer`: list of 2 or more distinct indexes, never all options |
| `order` | `options` (3-6); `answer`: every index exactly once, in the correct sequence |
| `match` | `pairs`: 3 or more `[left, right]` pairs with distinct left and distinct right items; the pairs are the answer, so there is no `answer` field |
| `estimate` | `unit` (string); `answer`: `{min, max}` numbers with `min < max` (the accepted range) |

Every learning objective of the concept must be covered by at least one question (via `objective`), checked from `review` on. An `objective` index outside the concept's objectives is an error at any stage. Anti-leak: the validator warns when the correct mcq option is the longest in more than 40% of mcq questions.

Always errors, at any stage: a duplicate or non-kebab-case id, a question id that is not `<concept-id>-qNN`, a `targets_misconception` that is not in `misconceptions.md` (or that file is missing), a source that is not in the registry or is `map-only`, and a malformed structure (the file or a question is not a mapping, `sources` is not a list of ids). More than 10 questions or more than 6 misconceptions only warn.

### `misconceptions.md`

```markdown
---
concept: caching-basics            # must equal the folder name
---

## stale-read-ok                   # kebab-case id, unique; referenced by `targets_misconception`

**Keyakinan keliru:** (the belief, as a learner would say it)

**Kenapa keliru:** (why it is wrong, with a `[^source-id]` marker when it rests on a source)
```

Both labels are required in every section; a missing label, a duplicate id, or a non-kebab-case heading is an error. A `[^id]` marker must be a registry id. Headings and labels inside code fences are ignored.

## 5. Incidents & case studies (draft, finalized in P1-033)

`content/incidents/<id>.md`: frontmatter (`id`, `title`, `date`, `sources`, `concepts`), then sections (Indonesian headings, since this is learner-facing content): **Ringkasan** (own words), **Kronologi**, **Mekanisme kegagalan**, **Skenario untuk pemain** (initial state, visible symptoms/metrics, decisions to make), **Pembahasan**.

Case-study content (format finalized in P1-033/P1-047) includes a design-quality rubric and a time frame for a time-boxed explanation, so they serve both design practice and interview-style delivery (ADR 0004).
