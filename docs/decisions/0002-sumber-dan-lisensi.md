# ADR 0002 — Aturan pemakaian sumber pihak ketiga

- **Status:** diterima
- **Tanggal:** 2026-11-12

## Konteks

Materi disuling dari buku, paper, artikel engineering, dan postmortem yang mayoritas berhak cipta. Sebagian berlisensi terbuka dengan syarat berbeda. Contohnya System Design Primer berlisensi CC BY 4.0 (boleh diadaptasi dengan atribusi), sedangkan Google SRE Book berlisensi CC BY-NC-ND 4.0 (tidak boleh dibuat turunannya).

## Keputusan

1. **Hanya sumber di `references/registry.yaml`** dengan status `approved` yang boleh dikutip di konten terbit. Status `candidate` boleh dipakai di draft.
2. **Default untuk semua sumber: tulis ulang.** Ambil konsep dan fakta, tulis dengan kata dan struktur sendiri, lalu tautkan sumbernya.
3. **Kutipan langsung** maksimal satu kalimat pendek (< 15 kata) per sumber per lesson, hanya kalau kata-kata persisnya penting.
4. **Diagram selalu dibuat sendiri.** Tidak ada diagram yang disalin atau dijiplak dari sumber.
5. **Adaptasi** (mengambil struktur atau teks lalu mengubahnya) hanya untuk sumber `license: CC-BY-*` atau domain publik, dengan atribusi sesuai `docs/conventions/citation-guide.md`.
6. **Sumber Tier 6** (kursus/buku persiapan interview) hanya untuk memetakan topik dan soal yang umum, tidak menjadi sumber isi.

## Konsekuensi

Produksi konten lebih lambat dibanding merangkum langsung, tapi konten bebas dirilis dengan CC BY 4.0, dan audit di M5 menjadi sederhana.

*Catatan: ini kebijakan proyek, bukan nasihat hukum.*
