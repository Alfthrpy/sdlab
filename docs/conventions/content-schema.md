# Data & content schema (v0)

The registry schema is final as of P1-010. The curriculum part is final for M2. The content part is a draft finalized in P1-030. Everything is checked by `scripts/validate.py`.

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
    license: all-rights-reserved      # all-rights-reserved | CC-BY-4.0 | CC-BY-SA-4.0 | CC-BY-NC-4.0 | CC-BY-NC-SA-4.0 | CC-BY-NC-ND-4.0 | MIT | Apache-2.0 | public-domain | unknown
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
- `usage: adapt-with-attribution` only for licenses `CC-BY-4.0`, `CC-BY-SA-4.0`, `MIT`, `Apache-2.0`, or `public-domain`.
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

## 4. Content per concept — `content/concepts/<concept-id>/` (draft)

| File | Contents |
| --- | --- |
| `lesson.md` | Frontmatter (`concept`, `title`, `sources` with `loc`, `status`, `reviewed_by`) + lesson text |
| `questions.yaml` | List of questions (schema below) |
| `misconceptions.md` | Common misconceptions + source/reason, used for distractors |
| `lab.yaml` | Lab spec (optional, finalized in P1-033) |

`questions.yaml`:

```yaml
questions:
  - id: caching-basics-q01
    type: mcq                         # mcq | multi | order | match | estimate
    difficulty: 2                     # 1–3
    prompt: "..."
    options: ["...", "...", "...", "..."]   # mcq/multi/order
    answer: 1                         # index (mcq), list of indexes (multi/order), {min, max} (estimate)
    explanation: "..."
    sources: [system-design-primer]
    targets_misconception: stale-read-ok   # optional
```

## 5. Incidents & case studies (draft, finalized in P1-033)

`content/incidents/<id>.md`: frontmatter (`id`, `title`, `date`, `sources`, `concepts`), then sections (Indonesian headings, since this is learner-facing content): **Ringkasan** (own words), **Kronologi**, **Mekanisme kegagalan**, **Skenario untuk pemain** (initial state, visible symptoms/metrics, decisions to make), **Pembahasan**.

Case-study content (format finalized in P1-033/P1-047) includes a design-quality rubric and a time frame for a time-boxed explanation, so they serve both design practice and interview-style delivery (ADR 0004).
