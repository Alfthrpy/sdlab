# Panduan sitasi & atribusi (v0, difinalkan di P1-018)

## Di dalam konten

Setiap file konten mencantumkan sumbernya lewat **id registry**, bukan URL mentah. URL diambil dari registry saat build, sehingga perbaikan tautan cukup dilakukan di satu tempat.

Di frontmatter lesson:

```yaml
sources:
  - id: ddia-2e
    loc: "bab 6, Replication"         # bab/bagian/halaman — wajib untuk buku dan paper
  - id: aws-builders-timeouts-retries
```

Di badan teks, rujuk klaim spesifik dengan penanda `[^id]`:

```markdown
Retry tanpa jitter membuat semua klien mencoba ulang di waktu yang sama.[^aws-builders-timeouts-retries]
```

Validator memastikan setiap `[^id]` ada di `sources` dan di registry.

## Kapan wajib bersitasi

- Angka (latensi, throughput, biaya, tahun, durasi insiden)
- Perilaku spesifik sebuah produk atau sistem
- Klaim "praktik terbaik" atau rekomendasi
- Kronologi dan akar masalah insiden

Pengetahuan umum yang ada di banyak sumber tetap butuh minimal satu sumber di `sources`, walaupun tidak perlu penanda per kalimat.

## Kutipan langsung

Maksimal satu kalimat pendek (< 15 kata) per sumber per lesson, ditandai dengan tanda kutip dan penanda sumber. Pakai hanya kalau kata-kata persisnya penting, misalnya definisi atau pernyataan resmi.

## Atribusi untuk materi CC BY

Kalau mengadaptasi materi berlisensi CC BY (misalnya System Design Primer), tambahkan di akhir file:

```markdown
---
Sebagian materi diadaptasi dari *System Design Primer* oleh Donne Martin,
CC BY 4.0, https://github.com/donnemartin/system-design-primer. Telah diubah.
```

## Yang dilarang

- Menyalin paragraf, struktur bab, atau urutan poin dari sumber berhak cipta
- Menyalin atau menjiplak diagram
- Mengutip sumber `status: candidate` di konten yang sudah `published`
- Mengutip sumber Tier 6 sebagai rujukan isi
