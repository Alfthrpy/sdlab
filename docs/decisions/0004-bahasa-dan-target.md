# ADR 0004 — Target pengguna dan tujuan belajar

- **Status:** diterima
- **Tanggal:** 2026-11-12
- **Ticket:** P1-002 (keputusan oleh owner)

## Keputusan

| Hal | Keputusan |
| --- | --- |
| Target pengguna | **Mahasiswa dan junior engineer.** Menggantikan "junior–mid + mahasiswa tingkat akhir" di ADR 0003. |
| Tujuan utama | **Tiga tujuan setara:** (1) memahami sistem berskala produksi, (2) mempelajari hal baru, (3) persiapan interview system design. |
| Bahasa konten | **Indonesia**, istilah teknis tetap dalam bahasa Inggris (lihat `writing-style.md`). Owner belum menyatakan pilihan bahasa secara eksplisit, jadi ini masih default dari ADR 0003 dan bisa diubah kapan saja. |

## Konsekuensi untuk konten

1. **Asumsi pengetahuan awal rendah.** Pembaca bisa pemrograman dasar, HTTP, dan SQL dasar, tapi belum pernah mengoperasikan sistem terdistribusi. Istilah dijelaskan saat pertama muncul dan Unit 1 tidak mengasumsikan latar belakang apa pun di luar itu. Daftar prasyarat pengetahuan ini ditulis di kurikulum.
2. **"Kenapa" lebih penting daripada "apa".** Setiap konsep menjelaskan masalah yang diselesaikan, apa yang pecah tanpanya, dan harga yang dibayar. Ini melayani ketiga tujuan: pemahaman produksi, belajar hal baru, dan kemampuan menjelaskan trade-off di interview.
3. **Contoh dari sistem nyata** (insiden, postmortem, paper, artikel engineering) menjadi tulang punggung materi. Ini melayani tujuan 1 dan 2, dan memberi bahan cerita konkret untuk tujuan 3.
4. **Tujuan interview dilayani lewat format, bukan lewat isi.** Isi tetap berbasis sumber primer. Studi kasus dan kerangka penyampaian (requirements, estimasi, desain, deep dive, trade-off) tetap dipertahankan sebagai salah satu format latihan. Sumber Tier 6 tetap `map-only` (ADR 0002) dan dipakai untuk memastikan cakupan topik dan soal umum.
5. **Studi kasus punya dua tujuan:** latihan merancang sistem secara umum, dan latihan menjelaskan desain dalam waktu terbatas. Rubrik dan kerangka waktu perlu mencakup keduanya (ticket tindak lanjut di bawah).
6. **Tingkat kesulitan** soal dan lab dikalibrasi untuk junior. Soal tingkat 3 berarti "menantang untuk junior", bukan setara soal senior.

## Tindak lanjut

- **P1-065** menyelaraskan dokumen dan ticket dengan tiga tujuan dan target junior: `docs/PLAN-FASE-1.md`, `docs/ROADMAP.md`, `docs/conventions/writing-style.md`, `curriculum/README.md`, ticket P1-022 dan P1-047, serta deskripsi subagent.
- ADR 0003 diperbarui statusnya untuk baris bahasa dan target. Baris nama, reviewer, dan lisensi masih menunggu P1-003.
