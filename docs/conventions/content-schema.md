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

`status` is `draft | review | published` and sets how strict the validator is. In `draft`, gaps are warnings. From `review` on, they are errors: core lesson length outside 300–600 words, a `## Lebih dalam` section over 250 words, fewer than 6 questions, a learning objective that no question covers, a missing `misconceptions.md`, a question without `objective`, fewer than 3 misconceptions. `published` also requires `reviewed_by` and approved sources only.

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

Body: core 300–600 words, plus an optional last section `## Lebih dalam` of at most 250 words that is not counted in the core length (see [writing-style](writing-style.md), "Two reading layers"). Indonesian, `[^id]` markers for specific claims (every marker must be in `sources`), at most one short quote per source. The validator counts words with `\w+` after removing fenced code blocks, `[^id]` markers, and URLs, so `x-y` counts as two words.

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
    explanation: "..."              # required; 1-3 sentences (a longer one only warns)
    sources: [system-design-primer]
    own_computation: true           # optional; use instead of `sources` when the answer is arithmetic from the prompt's own numbers
    targets_misconception: stale-read-ok   # optional; must be an id in misconceptions.md
```

| `type` | Extra fields and `answer` format |
| --- | --- |
| `mcq` | `options` (3-5); `answer`: one option index |
| `multi` | `options` (4-6); `answer`: list of 2 or more distinct indexes, never all options |
| `order` | `options` (3-6); `answer`: every index exactly once, in the correct sequence. The list is positions in the *correct order*: for options `[C-step, A-step, B-step]` whose right order is A, B, C, the answer is `[1, 2, 0]` (the index of the first step, then of the second, then of the third). Reading it the other way (the position of each option) gives `[2, 0, 1]`, which is wrong; check by reading the options back through the answer. |
| `match` | `pairs`: 3 or more `[left, right]` pairs with distinct left and distinct right items; the pairs are the answer, so there is no `answer` field |
| `estimate` | `unit` (string); `answer`: `{min, max}` numbers with `min < max` (the accepted range) |

A `match` question has no per-option link to a misconception: `targets_misconception` applies to the question as a whole, and the explanation says which pairing is the common mistake. (Per-pair links were considered in P1-035 and rejected: no question in the pilot needed them, and they would add a second answer structure to the format.) A question with no `sources` warns unless it sets `own_computation: true`.

Every learning objective of the concept must be covered by at least one question (via `objective`), checked from `review` on. An `objective` index outside the concept's objectives is an error at any stage. Anti-leak and style heuristics (option length, answer position, prompt echo, escape-hatch options, explanation length, difficulty mix, filler) only warn; see the "Automatic checks" table in [writing-style](writing-style.md).

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

## 5. Labs — `lab.yaml` and `*.lab.yaml` (final, P1-033)

A lab is a simulator spec. `content/concepts/<concept-id>/lab.yaml` is the concept's first lab; further labs of the same concept are `<name>.lab.yaml` in the same folder; an incident's diagnose-mode spec is `content/incidents/<id>.lab.yaml`. The simulator side (catalog, engine, grading) is defined in the STUD Simulator Master Plan; this section fixes what `sdlab` writes and checks. Learner-facing values (title, goal, hints, feedback, debrief) are Indonesian; keys and ids are English. Template: `templates/concept/lab.yaml`.

| Field | Meaning |
| --- | --- |
| `id`, `concept`, `secondary_concepts`, `contract_version` | Kebab-case unique lab id; the one owning concept (must be the folder name for concept labs; others go in `secondary_concepts`); semver string of the simulator contract the spec was written against |
| `mode` | `tune` (fixed topology, change parameters), `diagnose` (a hidden scenario: find it, then fix it), or `build` (constrained palette) |
| `difficulty`, `duration_min` | 1-3; a lab targets 10-20 minutes (outside it only warns) |
| `illustrative`, `illustrative_note` | `true` plus a non-empty Indonesian note when any used component, scenario or metric is labelled illustrative in the catalog |
| `title`, `goal` | `goal` states the symptom and the objective, never the fix |
| `topology` | `nodes`: `{id, type, params}` (kebab-case ids, catalog `type`); `edges`: `[from, to]` or `{from, to, policies}` |
| `traffic`, `scenarios` | `traffic.schedule`: `[{at_s, rate}]` sorted by time, optional `read_share` 0-1; `scenarios`: `[{id, at_s, ...}]` (catalog scenario ids, required in `diagnose`) |
| `allowed_edits` (tune, diagnose) / `palette` (build) | `[{node, param, min, max}]` where each node and parameter exists in the topology; or `[{type, max}]` |
| `targets` | `{id, metric, node?, window: {from_s, to_s}, aggregate: mean\|max\|p99, op: <=\|>=\|<\|>, value, feedback_pass, feedback_fail}` |
| `structural_rules` | `{id, predicate, args, feedback_pass, feedback_fail}` with predicate one of `has-node`, `has-edge`, `node-between`, `param-unchanged`, `param-range`, `count-le`, `policy-present`, `no-spof` |
| `hints` | Tiers 1, 2 and 3: symptom, then where to look, then mechanism. Never a value |
| `reference_solution`, `wrong_answers` | Edits `{node, param, value}` that must pass; wrong answers `{edits, reason, brute_force?}` that must fail, each with an Indonesian reason |
| `brute_force_ok` | Alternative to a `brute_force: true` wrong answer: a reason why setting every numeric edit to its extreme is acceptable |
| `debrief`, `sources` | Indonesian explanation shown after passing (or after 3 failed attempts); registry ids |

Checked now by `scripts/validate.py` (rule ids follow the master plan): the spec is a mapping with every required field, and `concept` exists (C06; a concept in `review` or `published` that lists `lab` but has no lab file is an error); known enums, window and traffic shapes; every edit and node reference resolves inside the topology (C13); each target and structural rule has a unique id and Indonesian `feedback_pass` and `feedback_fail` (C07); a latency target is paired with an `error_rate` or `goodput_rps` target (C12); `illustrative` needs a note (C05); a reference solution and at least one wrong answer exist, every edit is inside `allowed_edits` and its range, the reference meets `param-unchanged` and `param-range` rules, and a brute-force wrong answer or `brute_force_ok` exists (C09, C13, A3); anti-leak (C08): the goal and tier 1 and 2 hints must not contain a reference value (error) or the name of a component the reference edits (warning); sources are registry ids and not `map-only`. Invalid YAML is an error, not a crash.

Unknown fields are errors at every level (`display_scale`, for example, was removed from the plan). `scenarios` belong to `diagnose` mode, `allowed_edits` to `tune` and `diagnose`, `palette` to `build`. A wrong answer identical to the reference, a duplicated allowed edit, and a non-numeric edit value are errors. The anti-leak check reads Indonesian numbers (`0,5`, `1.000`) and trailing units (`20ms`), skips a reference value of 0, and also checks string reference values.

Deliberate differences from the master plan, to feed back into it: structural rules need `feedback_pass` and `feedback_fail` (C07 says every grading rule; the plan's example omits them); a brute-force wrong answer is marked `brute_force: true` (the plan only puts the words in the reason); the C08 component-name check is a warning because short ids like `app` or `db` would false-positive; C06 warns when a concept lacks `lab` in `formats`.

Not yet specified (waits for the simulator catalog): the argument shapes of the predicates other than `param-unchanged` and `param-range`, the shape of `policies` on edges, scenario fields beyond `id` and `at_s`, valid metric ids and their units (utilization is a fraction from 0 to 1), the solution shape of a `build` lab, and the meaning of each node parameter. The C12 check only recognizes a latency metric by the word `latency` in its id. A reference solution is checked against only two of the eight predicates, and a brute-force wrong answer is not checked to be extreme or to fail a rule.

Not checked yet: rules that need the simulator catalog (`contracts/sim/catalog.json`, vendored from `stud-sim`): that component, policy, scenario, metric and predicate ids exist and parameters are inside catalog ranges (C03-C04), the JSON Schema (C01) and the contract version against `contracts/sim/VERSION` (C02), that an incident's `sim_scenarios` ids exist (C10), and the catalog checksum (C11). They are added when the catalog is vendored. Quiz questions about a lab's concept must not reuse the lab's exact numbers (A5); the `content-reviewer` checks that.

## 6. Incidents (final, P1-033)

`content/incidents/<id>.md` is the learner-facing narrative. Metadata for choosing incidents stays in `curriculum/case-studies.yaml` (`kind: incident`, section 3); the file name equals the item id. Template: `templates/incident.md`.

```yaml
---
id: incident-gcp-service-control-2025       # equals the file name and the case-studies.yaml item
title: GCP Service Control, Juni 2025       # Indonesian
date: 2025-06-12                            # YYYY-MM-DD, the day of the incident
sources: [gcp-service-control-outage-2025-06-12]   # registry ids; at least one of type postmortem
concepts: [safe-deploys, retry-backoff-jitter]
modelability: modeled                       # modeled | illustrative | text-only
sim_spec: content/incidents/incident-gcp-service-control-2025.lab.yaml   # diagnose-mode lab spec; not for text-only
sim_scenarios: [restart-herd]               # catalog scenario ids; not for text-only
---
```

Then five sections, in this order, with these Indonesian headings: `## Ringkasan` (in the author's own words), `## Kronologi`, `## Mekanisme kegagalan`, `## Skenario untuk pemain` (initial state, visible symptoms and metrics, decisions to make), `## Pembahasan`. Specific claims carry `[^id]` markers from `sources`.

`modelability` says how much the simulator can honestly reproduce: `modeled` (the mechanism is in the catalog), `illustrative` (the shape is right, details are not), `text-only` (no simulation; only the narrative). Only `modeled` and `illustrative` incidents have a `sim_spec` and `sim_scenarios`. The validator checks the frontmatter and unknown fields, that the id matches the file and the case-studies entry, that sources are registry ids with a postmortem among them, that `sim_spec` is a `.lab.yaml` under `content/incidents/` in `diagnose` mode that exists, that every `sim_scenarios` id is a scenario of that spec, and the five sections in order. Footnote definitions such as `[^id]: ...` are not used; only markers.

## 7. Case-study content (draft, finalized in P1-047)

Case-study content includes a design-quality rubric and a time frame for a time-boxed explanation, so case studies serve both design practice and interview-style delivery (ADR 0004). The format is finalized when the first case study is written (P1-047).
