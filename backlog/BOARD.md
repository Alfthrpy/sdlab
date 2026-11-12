# Board

> File ini di-generate oleh `python scripts/board.py`. Jangan diedit manual.

**Ringkasan:** todo 37 · in-progress 0 · review 0 · blocked 0 · done 2

## Siap dikerjakan agent

| Ticket | Judul | Prioritas | Estimasi (sesi) |
| --- | --- | --- | --- |
| [P1-010](tickets/P1-010-finalisasi-kriteria-sumber-dan-skema-registry.md) | Finalisasi kriteria sumber dan skema registry | high | 1 |
| [P1-065](tickets/P1-065-selaraskan-dokumen-dengan-target-junior-dan.md) | Selaraskan dokumen dengan target junior dan tiga tujuan | high | 1 |
| [P1-004](tickets/P1-004-mirror-backlog-ke-github-projects-opsional.md) | Mirror backlog ke GitHub Projects (opsional) | low | 1 |

## Menunggu owner (manusia)

| Ticket | Tugas | Keadaan |
| --- | --- | --- |
| [P1-019](tickets/P1-019-g0-approve-registry-referensi-v1.md) | G0 — Approve Registry Referensi v1 | menunggu dependensi |
| [P1-024](tickets/P1-024-g1-approve-kurikulum.md) | G1 — Approve kurikulum | menunggu dependensi |
| [P1-034](tickets/P1-034-g2-uji-pilot-ke-5-orang.md) | G2 — Uji pilot ke 5 orang target | menunggu dependensi |
| [P1-064](tickets/P1-064-g3-freeze-konten-v1.md) | G3 — Freeze konten v1 | menunggu dependensi |
| [P1-003](tickets/P1-003-keputusan-nama-kerja-lisensi-konten-dan.md) | Keputusan: nama kerja, lisensi konten, dan reviewer teknis | siap |
| [P1-063](tickets/P1-063-spot-check-sampel-konten-oleh-manusia.md) | Spot-check sampel konten oleh manusia | menunggu dependensi |

## Semua ticket per milestone

### M0 — Fondasi (2/5 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| ✓ | [P1-001](tickets/P1-001-setup-repo-workflow-ticket-dan-file.md) | Setup repo, workflow ticket, dan file pendukung agent | agent | none | — |
| ✓ | [P1-002](tickets/P1-002-keputusan-bahasa-konten-dan-target-pengguna.md) | Keputusan: bahasa konten dan target pengguna | human | none | — |
| · | [P1-003](tickets/P1-003-keputusan-nama-kerja-lisensi-konten-dan.md) | Keputusan: nama kerja, lisensi konten, dan reviewer teknis | human | none | — |
| · | [P1-004](tickets/P1-004-mirror-backlog-ke-github-projects-opsional.md) | Mirror backlog ke GitHub Projects (opsional) | agent | human | P1-001 |
| · | [P1-065](tickets/P1-065-selaraskan-dokumen-dengan-target-junior-dan.md) | Selaraskan dokumen dengan target junior dan tiga tujuan | agent | agent | P1-002 |

### M1 — Registry Referensi (0/10 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| · | [P1-010](tickets/P1-010-finalisasi-kriteria-sumber-dan-skema-registry.md) | Finalisasi kriteria sumber dan skema registry | agent | agent | P1-001 |
| · | [P1-011](tickets/P1-011-riset-kandidat-sumber-unit-1-2.md) | Riset kandidat sumber — Unit 1 & 2 | agent | agent | P1-010 |
| · | [P1-012](tickets/P1-012-riset-kandidat-sumber-unit-3.md) | Riset kandidat sumber — Unit 3 | agent | agent | P1-010 |
| · | [P1-013](tickets/P1-013-riset-kandidat-sumber-unit-4.md) | Riset kandidat sumber — Unit 4 | agent | agent | P1-010 |
| · | [P1-014](tickets/P1-014-riset-kandidat-sumber-unit-5.md) | Riset kandidat sumber — Unit 5 | agent | agent | P1-010 |
| · | [P1-015](tickets/P1-015-riset-kandidat-sumber-unit-6-postmortem.md) | Riset kandidat sumber — Unit 6 + postmortem | agent | agent | P1-010 |
| · | [P1-016](tickets/P1-016-verifikasi-lisensi-versi-dan-metadata-semua.md) | Verifikasi lisensi, versi, dan metadata semua kandidat | agent | agent | P1-011, P1-012, P1-013, P1-014, P1-015 |
| · | [P1-017](tickets/P1-017-peta-sumber-topik-dan-daftar-celah.md) | Peta sumber → topik dan daftar celah | agent | agent | P1-016 |
| · | [P1-018](tickets/P1-018-panduan-sitasi-dan-atribusi-final.md) | Panduan sitasi dan atribusi final | agent | agent | P1-010 |
| · | [P1-019](tickets/P1-019-g0-approve-registry-referensi-v1.md) | G0 — Approve Registry Referensi v1 | human | human | P1-016, P1-017, P1-018 |

### M2 — Kurikulum (0/5 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| · | [P1-020](tickets/P1-020-daftar-konsep-v0-dengan-tujuan-belajar.md) | Daftar konsep v0 dengan tujuan belajar | agent | agent | P1-019 |
| · | [P1-021](tickets/P1-021-graf-prasyarat-dan-validasi-dag.md) | Graf prasyarat dan validasi DAG | agent | agent | P1-020 |
| · | [P1-022](tickets/P1-022-pilih-studi-kasus-dan-insiden.md) | Pilih studi kasus dan insiden | agent | agent | P1-020 |
| · | [P1-023](tickets/P1-023-mapping-konsep-sumber.md) | Mapping konsep → sumber | agent | agent | P1-021 |
| · | [P1-024](tickets/P1-024-g1-approve-kurikulum.md) | G1 — Approve kurikulum | human | human | P1-021, P1-022, P1-023, P1-002 |

### M3 — Pedagogi & pilot (0/6 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| · | [P1-030](tickets/P1-030-skema-konten-final-dan-validator-konten.md) | Skema konten final dan validator konten | agent | agent | P1-024 |
| · | [P1-031](tickets/P1-031-panduan-gaya-dan-aturan-anti-bocor.md) | Panduan gaya dan aturan anti-bocor soal | agent | agent | P1-024 |
| · | [P1-032](tickets/P1-032-pilot-konsep-caching-di-semua-format.md) | Pilot konsep 'caching' di semua format | agent | agent | P1-030, P1-031 |
| · | [P1-033](tickets/P1-033-format-spesifikasi-lab-dan-insiden.md) | Format spesifikasi lab dan insiden | agent | agent | P1-024 |
| · | [P1-034](tickets/P1-034-g2-uji-pilot-ke-5-orang.md) | G2 — Uji pilot ke 5 orang target | human | none | P1-032 |
| · | [P1-035](tickets/P1-035-revisi-template-dan-panduan-dari-hasil.md) | Revisi template dan panduan dari hasil pilot | agent | agent | P1-034 |

### M4 — Produksi konten (0/8 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| · | [P1-040](tickets/P1-040-epic-produksi-unit-1.md) | EPIC Produksi Unit 1 | agent | agent | P1-035 |
| · | [P1-041](tickets/P1-041-epic-produksi-unit-2.md) | EPIC Produksi Unit 2 | agent | agent | P1-035 |
| · | [P1-042](tickets/P1-042-epic-produksi-unit-6.md) | EPIC Produksi Unit 6 | agent | agent | P1-035 |
| · | [P1-043](tickets/P1-043-epic-produksi-unit-3.md) | EPIC Produksi Unit 3 | agent | agent | P1-035 |
| · | [P1-044](tickets/P1-044-epic-produksi-unit-4.md) | EPIC Produksi Unit 4 | agent | agent | P1-035 |
| · | [P1-045](tickets/P1-045-epic-produksi-unit-5.md) | EPIC Produksi Unit 5 | agent | agent | P1-035 |
| · | [P1-046](tickets/P1-046-paket-insiden-8-skenario.md) | Paket insiden (8 skenario) | agent | agent | P1-033, P1-042 |
| · | [P1-047](tickets/P1-047-paket-studi-kasus-6.md) | Paket studi kasus (6) | agent | agent | P1-040, P1-041, P1-043 |

### M5 — QA & freeze (0/5 selesai)

| | Ticket | Judul | Owner | Review | Bergantung pada |
| --- | --- | --- | --- | --- | --- |
| · | [P1-060](tickets/P1-060-audit-sitasi-dan-tautan-mati.md) | Audit sitasi dan tautan mati | agent | agent | P1-040, P1-041, P1-042, P1-043, P1-044, P1-045 |
| · | [P1-061](tickets/P1-061-audit-kemiripan-teks-dengan-sumber.md) | Audit kemiripan teks dengan sumber | agent | agent | P1-040, P1-041, P1-042, P1-043, P1-044, P1-045 |
| · | [P1-062](tickets/P1-062-kalibrasi-tingkat-kesulitan-soal.md) | Kalibrasi tingkat kesulitan soal | agent | agent | P1-040, P1-041, P1-042 |
| · | [P1-063](tickets/P1-063-spot-check-sampel-konten-oleh-manusia.md) | Spot-check sampel konten oleh manusia | human | none | P1-060, P1-061 |
| · | [P1-064](tickets/P1-064-g3-freeze-konten-v1.md) | G3 — Freeze konten v1 | human | human | P1-046, P1-047, P1-060, P1-061, P1-062, P1-063 |

Legenda: · todo · ▶ in-progress · ◆ review · ✖ blocked · ✓ done
