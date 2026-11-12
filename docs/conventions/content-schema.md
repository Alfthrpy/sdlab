# Data & content schema (v0)

The registry and curriculum parts are final for M1–M2. The content part is a draft finalized in P1-030. Everything is checked by `scripts/validate.py`.

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
    license: all-rights-reserved      # all-rights-reserved | CC-BY-4.0 | CC-BY-SA-4.0 | CC-BY-NC-ND-4.0 | MIT | public-domain | unknown
    usage: rewrite-only               # rewrite-only | adapt-with-attribution | map-only
    access: paywalled                 # free | partial | paywalled
    units: [3, 4, 5]                  # curriculum units 1–6
    topics: [replication, partitioning, transactions]
    status: candidate                 # candidate | approved | rejected | deprecated
    notes: ""                         # reasons, warnings, free companion sources (English)
```

Validator rules:
- `usage: adapt-with-attribution` only for licenses `CC-BY-*`, `MIT`, or `public-domain`.
- `tier: 6` requires `usage: map-only`.
- `type: paper` should have a `doi` (warning, not an error).

## 2. `curriculum/concepts.yaml`

```yaml
concepts:
  - id: caching-basics                # kebab-case
    unit: 2
    title: Dasar caching              # Indonesian (learner-facing)
    objectives:                       # 1–4 testable objectives, Indonesian, starting with "Bisa ..."
      - Bisa menjelaskan kapan cache-aside lebih cocok daripada write-through
    prerequisites: [latency-throughput]   # other concept ids; must form a DAG
    sources: [system-design-primer, aws-builders-caching]   # ≥2 registry ids
    formats: [lesson, quiz, lab]      # lesson | quiz | lab | incident
    status: planned                   # planned | drafting | review | published
```

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
