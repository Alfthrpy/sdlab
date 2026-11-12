---
id: P1-002
title: "Keputusan: bahasa konten dan target pengguna"
milestone: M0
type: decision
owner: human
review: none
status: done
priority: high
depends_on: []
estimate: 1
outputs:
  - docs/decisions/0004-bahasa-dan-target.md
---

## Konteks

ADR 0003 memakai default sementara (Indonesia, junior–mid + mahasiswa, tujuan ganda interview & produksi). Agent sudah bisa jalan dengan default ini, tapi kurikulum (M2) sebaiknya dikunci setelah keputusan final.

## Tugas

1. Baca ADR 0003.
2. Putuskan: bahasa konten (Indonesia saja / Indonesia + Inggris), target pengguna utama, tujuan utama (interview / produksi / keduanya).
3. Tulis keputusan singkat (boleh di komentar PR atau chat ke agent; agent yang menuliskan ADR 0004).

## Kriteria selesai

- [x] Keputusan bahasa tercatat
- [x] Keputusan target & tujuan tercatat
- [x] ADR 0003 diperbarui statusnya

## Catatan

Keputusan owner 2026-11-12: target mahasiswa dan junior engineer; tiga tujuan setara: memahami sistem skala produksi, belajar hal baru, dan persiapan interview (interview ditambahkan owner setelah keputusan pertama). Bahasa tidak disebut eksplisit, jadi default Indonesia dipertahankan dan ditandai belum dikonfirmasi di ADR 0004.
Penyelarasan dokumen dengan tiga tujuan dan target junior dipisah ke P1-065.
