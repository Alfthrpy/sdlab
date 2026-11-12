# Skema data & konten (v0)

Bagian registry dan kurikulum sudah final untuk M1–M2. Bagian konten adalah draft yang difinalkan di P1-030. Semua dicek oleh `scripts/validate.py`.

## 1. `references/registry.yaml`

```yaml
sources:
  - id: ddia-2e                       # kebab-case, unik, stabil (jangan diganti setelah dipakai)
    title: "Designing Data-Intensive Applications, 2nd Edition"
    authors: [Martin Kleppmann, Chris Riccomini]
    publisher: O'Reilly Media         # atau nama situs/organisasi
    type: book                        # book | paper | article | postmortem | docs | repo | course | talk
    tier: 1                           # 1–6, lihat research-protocol.md
    url: https://www.oreilly.com/library/view/-/9781098119058
    doi: null                         # wajib untuk paper kalau ada
    published: "2026-02"              # YYYY, YYYY-MM, atau YYYY-MM-DD
    edition: "2"                      # opsional
    accessed: "2026-11-12"            # tanggal halaman dibuka
    license: all-rights-reserved      # all-rights-reserved | CC-BY-4.0 | CC-BY-SA-4.0 | CC-BY-NC-ND-4.0 | MIT | public-domain | unknown
    usage: rewrite-only               # rewrite-only | adapt-with-attribution | map-only
    access: paywalled                 # free | partial | paywalled
    units: [3, 4, 5]                  # unit kurikulum 1–6
    topics: [replication, partitioning, transactions]
    status: candidate                 # candidate | approved | rejected | deprecated
    notes: ""                         # alasan, peringatan, sumber pendamping gratis
```

Aturan validator:
- `usage: adapt-with-attribution` hanya untuk lisensi `CC-BY-*`, `MIT`, atau `public-domain`.
- `tier: 6` wajib `usage: map-only`.
- `type: paper` sebaiknya punya `doi` (peringatan, bukan error).

## 2. `curriculum/concepts.yaml`

```yaml
concepts:
  - id: caching-basics                # kebab-case
    unit: 2
    title: Dasar caching
    objectives:                       # 1–4 tujuan yang bisa diuji, diawali "Bisa ..."
      - Bisa menjelaskan kapan cache-aside lebih cocok daripada write-through
    prerequisites: [latency-throughput]   # id konsep lain; harus membentuk DAG
    sources: [system-design-primer, aws-builders-caching]   # ≥2 id registry
    formats: [lesson, quiz, lab]      # lesson | quiz | lab | incident
    status: planned                   # planned | drafting | review | published
```

## 3. `curriculum/case-studies.yaml`

```yaml
items:
  - id: incident-aws-dynamodb-dns-2025
    kind: incident                    # incident | case-study
    title: DNS DynamoDB us-east-1, Okt 2025
    concepts: [dns, dependency-blast-radius, retry-backoff-jitter]
    sources: [aws-pes-dynamodb-2025-10]
    status: planned
```

## 4. Konten per konsep — `content/concepts/<concept-id>/` (draft)

| File | Isi |
| --- | --- |
| `lesson.md` | Frontmatter (`concept`, `title`, `sources` dengan `loc`, `status`, `reviewed_by`) + teks lesson |
| `questions.yaml` | Daftar soal (skema di bawah) |
| `misconceptions.md` | Miskonsepsi umum + sumber/alasan, dipakai untuk pengecoh |
| `lab.yaml` | Spesifikasi lab (opsional, difinalkan di P1-033) |

`questions.yaml`:

```yaml
questions:
  - id: caching-basics-q01
    type: mcq                         # mcq | multi | order | match | estimate
    difficulty: 2                     # 1–3
    prompt: "..."
    options: ["...", "...", "...", "..."]   # mcq/multi/order
    answer: 1                         # index (mcq), list index (multi/order), {min, max} (estimate)
    explanation: "..."
    sources: [system-design-primer]
    targets_misconception: stale-read-ok   # opsional
```

## 5. Insiden & studi kasus (draft, difinalkan di P1-033)

`content/incidents/<id>.md`: frontmatter (`id`, `title`, `date`, `sources`, `concepts`), lalu bagian **Ringkasan** (kata sendiri), **Kronologi**, **Mekanisme kegagalan**, **Skenario untuk pemain** (keadaan awal, gejala/metrik yang terlihat, keputusan yang harus diambil), **Pembahasan**.
