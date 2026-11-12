---
id: P1-015
title: "Riset kandidat sumber — Unit 6 + postmortem"
milestone: M1
type: research
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-010]
estimate: 2
outputs:
  - references/registry.yaml
  - references/notes/
---

## Konteks

Mengisi Registry Referensi untuk Unit 6: Reliabilitas produksi (timeout, retry/backoff/jitter, circuit breaker, load shedding, cascading & metastable failure, observability, deploy aman). Pakai subagent `researcher`; review oleh `source-verifier`.

## Tugas

1. Turunkan daftar sub-topik dari tabel unit di `curriculum/README.md`.
2. Untuk setiap sub-topik cari minimal: satu sumber Tier 1–2, satu Tier 3 atau dokumentasi resmi, dan satu sumber gratis.
3. Kumpulkan ≥ 12 postmortem resmi (beragam perusahaan dan mekanisme kegagalan; prioritaskan 2023–2026) sebagai bahan paket insiden.
4. Buka setiap sumber; catat entri `candidate` sesuai `templates/source-entry.yaml`.
5. Tulis catatan baca untuk 3–5 sumber terpenting.
6. Daftar sub-topik yang belum punya sumber memadai di bagian Catatan.

## Kriteria selesai

- [ ] ≥ 15 kandidat + ≥ 12 postmortem untuk unit ini, semuanya dibuka di sesi
- [ ] Setiap sub-topik punya ≥ 1 sumber Tier 1–3 atau tercatat sebagai celah
- [ ] Catatan baca untuk 3–5 sumber utama
- [ ] `source-verifier` menyatakan lolos
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
