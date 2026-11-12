# ADR 0003 — Default sementara (menunggu keputusan owner)

- **Status:** sebagian diganti. Baris bahasa dan target pengguna diganti oleh [ADR 0004](0004-bahasa-dan-target.md) (P1-002). Baris nama, reviewer, dan lisensi masih sementara sampai P1-003 selesai.
- **Tanggal:** 2026-11-12

Supaya agent bisa mulai bekerja sebelum owner memutuskan, nilai-nilai berikut dipakai:

| Hal | Default | Ditentukan di |
| --- | --- | --- |
| Bahasa konten | Indonesia. Istilah teknis tetap dalam bahasa Inggris (cache, replica, throughput), dijelaskan saat pertama muncul. | ADR 0004 (tetap, belum dikonfirmasi eksplisit) |
| Bahasa sumber | Inggris (sebagian besar sumber primer berbahasa Inggris) | — |
| Target pengguna | ~~Engineer backend junior–mid dan mahasiswa tingkat akhir. Tujuan ganda: persiapan interview dan pemahaman sistem produksi.~~ **Diganti ADR 0004:** mahasiswa dan junior engineer; tujuan memahami sistem skala produksi dan belajar hal baru. | ADR 0004 |
| Nama kerja | SD Lab | P1-003 |
| Reviewer teknis manusia | Owner repo | P1-003 |
| Lisensi konten | CC BY 4.0 | P1-003 |
