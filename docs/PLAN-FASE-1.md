# Plan Fase 1 — Materi

**Tujuan:** menghasilkan materi v1 yang siap dipakai aplikasi, yaitu sekitar 40 konsep, 300 soal, 15 spesifikasi lab, 8 insiden, dan 6 studi kasus. Setiap klaimnya bersumber dari Registry Referensi yang terverifikasi.

**Cara kerja:** agent-heavy. Agent mengerjakan riset, pemetaan, dan drafting. Agent lain mereview tanpa ikut mengerjakan. Owner repo (manusia) hanya memutuskan di gerbang milestone, mengerjakan uji ke pengguna, dan spot-check kualitas. Detail alur ada di [workflow.md](workflow.md).

**Perkiraan durasi:** 22 minggu untuk volume penuh. M1–M3 (sekitar 6 minggu) adalah jalur kritis. M4 bisa dipercepat dengan menambah sesi agent paralel per unit.

## Milestone dan gerbang

| Milestone | Isi | Minggu | Gerbang keluar (diputuskan manusia) |
| --- | --- | --- | --- |
| **M0** Fondasi | Repo, workflow, keputusan dasar | 1 | Keputusan bahasa, target, reviewer tercatat di ADR |
| **M1** Registry Referensi | Kriteria, riset kandidat per unit, verifikasi lisensi & versi, peta celah | 1–2 | **G0:** setiap unit punya ≥1 sumber Tier 1–2 dan ≥1 Tier 3–4 |
| **M2** Kurikulum | ~40 konsep + tujuan belajar, graf prasyarat, studi kasus & insiden, mapping sumber | 3–5 | **G1:** DAG valid, tiap konsep punya tujuan belajar + ≥2 sumber |
| **M3** Pedagogi & pilot | Skema konten + validator, panduan gaya, pilot konsep "caching" di semua format, uji 5 orang | 5–6 | **G2:** pilot diuji, template direvisi |
| **M4** Produksi | 6 unit konten, paket insiden, paket studi kasus | 7–22 | Per unit: lolos review agent + sampel human |
| **M5** QA & freeze | Audit sitasi, audit plagiarisme, kalibrasi soal, rilis konten v1 | 21–22 | **G3:** konten v1 dibekukan (tag `content-v1.0`) |

## Urutan produksi M4

Unit dikerjakan berdasarkan nilai pembeda dan ketergantungan:

1. **Unit 1 Fondasi.** Semua unit lain membutuhkannya.
2. **Unit 2 Building blocks.** Dasar untuk lab pertama.
3. **Unit 6 Reliabilitas produksi.** Pembeda utama (retry storm, metastable, insiden nyata), dan paling dekat dengan simulator.
4. **Unit 3 Data.**
5. **Unit 4 Asinkron & aliran.**
6. **Unit 5 Konsistensi & koordinasi.**

Paket insiden dan studi kasus berjalan paralel setelah unit yang dibutuhkannya selesai.

Ticket epic per unit (`P1-040` dst.) dipecah oleh agent menjadi satu sub-ticket per konsep ketika unit dimulai, memakai `scripts/new_ticket.py`.

## Pembagian kerja

| | Agent | Manusia |
| --- | --- | --- |
| Jumlah ticket awal | 31 | 7 |
| Jenis | Riset, pemetaan, kurikulum, skema, drafting, review silang, QA otomatis | Keputusan dasar, 3 gerbang, uji pilot, spot-check QA |
| Perkiraan waktu manusia | — | 2–4 jam per gerbang, ±1 jam/minggu spot-check |

## Output akhir Fase 1

```
references/registry.yaml          ~150 sumber, status approved, lisensi & versi tercatat
references/notes/*.md             catatan baca per sumber utama
curriculum/concepts.yaml          ~40 konsep, tujuan belajar, prasyarat, sumber
curriculum/case-studies.yaml      20–25 studi kasus & insiden terpilih
content/concepts/<id>/            lesson.md, questions.yaml, lab.yaml (opsional), misconceptions.md
content/incidents/<id>.md         8 skenario insiden dari postmortem publik
content/case-studies/<id>.md      6 studi kasus dengan rubrik
```

Format setiap file didefinisikan di [conventions/content-schema.md](conventions/content-schema.md) dan dicek oleh `scripts/validate.py`.

## Risiko Fase 1

| Risiko | Mitigasi |
| --- | --- |
| Agent mengarang sumber atau URL | Aturan "buka dulu baru catat" di AGENTS.md, field `accessed` wajib, reviewer `source-verifier` membuka ulang setiap URL baru |
| Konten terlalu mirip sumber | Panduan tulis ulang, pengecekan kemiripan di QA M5, larangan menyalin diagram |
| Konten terasa "buatan AI" | Panduan gaya (contoh konkret, angka bersumber, tanpa basa-basi), uji pilot ke manusia di G2 |
| Produksi lambat | Sesi agent paralel per unit setelah G2 |
| Gerbang tertahan menunggu manusia | Agent menyiapkan ringkasan keputusan siap-approve di setiap ticket gerbang |

## Daftar ticket

Status terkini selalu di [../backlog/BOARD.md](../backlog/BOARD.md). Daftar awal:

**M0 Fondasi**
- P1-001 Setup repo & workflow — agent (selesai)
- P1-002 Keputusan: bahasa konten & target pengguna — **human**
- P1-003 Keputusan: nama kerja & reviewer teknis — **human**
- P1-004 Mirror backlog ke GitHub Projects (opsional) — agent

**M1 Registry Referensi**
- P1-010 Finalisasi kriteria & skema registry — agent
- P1-011 s.d. P1-015 Riset kandidat per unit (6 unit, 5 ticket) — agent
- P1-016 Verifikasi lisensi & versi semua kandidat — agent
- P1-017 Peta sumber → topik & daftar celah — agent
- P1-018 Panduan sitasi & atribusi final — agent
- P1-019 **G0** Approve Registry v1 — **human**

**M2 Kurikulum**
- P1-020 Daftar konsep v0 dengan tujuan belajar — agent
- P1-021 Graf prasyarat & validasi DAG — agent
- P1-022 Pilih studi kasus & insiden — agent
- P1-023 Mapping konsep → sumber — agent
- P1-024 **G1** Approve kurikulum — **human**

**M3 Pedagogi & pilot**
- P1-030 Skema konten & validator — agent
- P1-031 Panduan gaya & anti-bocor soal — agent
- P1-032 Pilot konsep "caching" semua format — agent
- P1-033 Format spesifikasi lab & insiden — agent
- P1-034 **G2** Uji pilot ke 5 orang target — **human**
- P1-035 Revisi template dari hasil pilot — agent

**M4 Produksi** (epic, dipecah per konsep saat mulai)
- P1-040 Unit 1 Fondasi
- P1-041 Unit 2 Building blocks
- P1-042 Unit 6 Reliabilitas produksi
- P1-043 Unit 3 Data
- P1-044 Unit 4 Asinkron & aliran
- P1-045 Unit 5 Konsistensi & koordinasi
- P1-046 Paket insiden (8)
- P1-047 Paket studi kasus (6)

**M5 QA & freeze**
- P1-060 Audit sitasi & tautan mati — agent
- P1-061 Audit kemiripan teks dengan sumber — agent
- P1-062 Kalibrasi tingkat kesulitan soal — agent
- P1-063 Spot-check sampel konten — **human**
- P1-064 **G3** Freeze konten v1 — **human**
