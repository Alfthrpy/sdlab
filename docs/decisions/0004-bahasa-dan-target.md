# ADR 0004 — Target pengguna dan tujuan belajar

- **Status:** diterima
- **Tanggal:** 2026-11-12
- **Ticket:** P1-002 (keputusan oleh owner)

## Keputusan

| Hal | Keputusan |
| --- | --- |
| Target pengguna | **Mahasiswa dan junior engineer.** Menggantikan "junior–mid + mahasiswa tingkat akhir" di ADR 0003. |
| Tujuan utama | **Memahami sistem berskala produksi dan mempelajari hal baru.** Persiapan interview bukan tujuan utama. |
| Bahasa konten | **Indonesia**, istilah teknis tetap dalam bahasa Inggris (lihat `writing-style.md`). Owner belum menyatakan pilihan bahasa secara eksplisit, jadi ini masih default dari ADR 0003 dan bisa diubah kapan saja. |

## Konsekuensi untuk konten

1. **Asumsi pengetahuan awal rendah.** Pembaca bisa pemrograman dasar, HTTP, dan SQL dasar, tapi belum pernah mengoperasikan sistem terdistribusi. Istilah dijelaskan saat pertama muncul dan Unit 1 tidak mengasumsikan latar belakang apa pun di luar itu. Daftar prasyarat pengetahuan ini ditulis di kurikulum.
2. **"Kenapa" lebih penting daripada "apa".** Setiap konsep menjelaskan masalah yang diselesaikan, apa yang pecah tanpanya, dan harga yang dibayar. Daftar teknologi dan jawaban hafalan tidak jadi fokus.
3. **Contoh dari sistem nyata** (insiden, postmortem, paper, artikel engineering) menjadi tulang punggung materi. Ini selaras dengan tujuan memahami skala produksi dan memperkuat peran Unit 6 serta paket insiden.
4. **Sumber Tier 6 (persiapan interview) hanya pemeriksa cakupan.** Aturannya tetap `map-only` (ADR 0002), tapi bobotnya turun. Cukup untuk memastikan tidak ada topik umum yang terlewat.
5. **Studi kasus tidak dibingkai sebagai soal interview.** Format tetap berupa merancang sebuah sistem, tapi tujuannya latihan merancang dan meninjau desain. Kerangka waktu interview dan rubrik gaya interview perlu ditinjau ulang (ticket tindak lanjut di bawah).
6. **Tingkat kesulitan** soal dan lab dikalibrasi untuk junior. Soal tingkat 3 berarti "menantang untuk junior", bukan setara soal senior.

## Tindak lanjut

- **P1-065** menyelaraskan dokumen yang masih memakai kerangka interview: `docs/PLAN-FASE-1.md`, `docs/conventions/writing-style.md`, `curriculum/README.md`, tiket P1-022, P1-047, serta deskripsi subagent.
- ADR 0003 diperbarui statusnya untuk baris bahasa dan target. Baris nama, reviewer, dan lisensi masih menunggu P1-003.
