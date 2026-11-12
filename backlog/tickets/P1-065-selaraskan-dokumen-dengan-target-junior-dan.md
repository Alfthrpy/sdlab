---
id: P1-065
title: "Selaraskan dokumen dengan target junior dan tujuan produksi"
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
  - docs/conventions/writing-style.md
  - curriculum/README.md
---

## Konteks

ADR 0004 menetapkan target mahasiswa dan junior engineer dengan tujuan memahami sistem skala produksi dan belajar hal baru. Persiapan interview bukan tujuan utama. Beberapa dokumen dan ticket masih memakai kerangka interview atau asumsi pembaca junior–mid. Harus dirapikan sebelum riset (M1) dan kurikulum (M2) berjalan, supaya agent tidak membawa asumsi lama.

## Tugas

1. Cari kerangka interview dan asumsi level di dokumen berikut, lalu sesuaikan: `docs/PLAN-FASE-1.md`, `docs/ROADMAP.md`, `docs/conventions/*.md`, `curriculum/README.md`, `.claude/agents/*.md`, `AGENTS.md`.
2. Ticket yang menyebut interview: P1-022 (pilih studi kasus) dan P1-047 (paket studi kasus). Bingkai ulang sebagai latihan merancang dan meninjau desain, termasuk rubrik dan kerangka waktu.
3. Tambahkan bagian "Prasyarat pengetahuan pembaca" ke `curriculum/README.md` (pemrograman dasar, HTTP, SQL dasar) dan aturan bahwa Unit 1 tidak mengasumsikan hal lain.
4. Tulis ulang aturan kesulitan soal di `writing-style.md`: tingkat 3 berarti menantang untuk junior.
5. Jangan mengubah isi ADR 0002 (aturan Tier 6 `map-only` tetap berlaku). Catat di Catatan hal yang sengaja tidak diubah.

## Kriteria selesai

- [ ] Tidak ada dokumen yang menyebut persiapan interview sebagai tujuan utama
- [ ] P1-022 dan P1-047 tidak lagi dibingkai sebagai soal interview
- [ ] Prasyarat pengetahuan pembaca tertulis di `curriculum/README.md`
- [ ] `python scripts/validate.py` lolos

## Catatan

(Diisi saat dikerjakan.)
