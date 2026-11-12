---
id: P1-065
title: "Selaraskan dokumen dengan target junior dan tiga tujuan"
milestone: M0
type: curriculum
owner: agent
review: agent
status: todo
priority: high
depends_on: [P1-002]
estimate: 1
outputs:
  - docs/PLAN-FASE-1.md
  - docs/ROADMAP.md
  - docs/conventions/writing-style.md
  - curriculum/README.md
---

## Konteks

ADR 0004 menetapkan target mahasiswa dan junior engineer dengan tiga tujuan setara: memahami sistem skala produksi, belajar hal baru, dan persiapan interview. Dokumen yang ditulis sebelum keputusan ini memakai asumsi junior–mid, dan sebagian menggambarkan tujuan hanya sebagai persiapan interview atau hanya sebagai pemahaman produksi. Perlu diselaraskan sebelum riset (M1) dan kurikulum (M2) berjalan penuh.

## Tugas

1. Periksa dan sesuaikan penyebutan target dan tujuan di: `docs/PLAN-FASE-1.md`, `docs/ROADMAP.md`, `docs/conventions/*.md`, `curriculum/README.md`, `.claude/agents/*.md`, `AGENTS.md`. Gantikan asumsi "junior–mid" dengan "mahasiswa dan junior engineer".
2. Tambahkan bagian "Prasyarat pengetahuan pembaca" di `curriculum/README.md` (pemrograman dasar, HTTP, SQL dasar) dan aturan bahwa Unit 1 tidak mengasumsikan hal lain.
3. Di ticket P1-022 dan P1-047, pastikan studi kasus melayani dua tujuan: latihan merancang sistem, dan latihan menjelaskan desain dalam waktu terbatas. Rubrik dan kerangka waktu mencakup keduanya.
4. Di `writing-style.md`, tulis aturan kesulitan soal: tingkat 3 berarti menantang untuk junior.
5. Jangan mengubah ADR 0002 (Tier 6 tetap `map-only`). Catat di bagian Catatan hal yang sengaja tidak diubah.

## Kriteria selesai

- [ ] Target dan tujuan di semua dokumen konsisten dengan ADR 0004
- [ ] Prasyarat pengetahuan pembaca tertulis di `curriculum/README.md`
- [ ] P1-022 dan P1-047 menyebut kedua tujuan studi kasus
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
