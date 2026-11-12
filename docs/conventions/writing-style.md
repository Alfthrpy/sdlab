# Panduan gaya tulisan (v0, difinalkan di P1-031)

Pembacanya engineer yang sibuk. Tulisan harus langsung, spesifik, dan tidak terdengar seperti dibuat mesin.

## Bahasa

- Bahasa Indonesia baku tapi santai. Sapaan "kamu".
- Istilah teknis tetap dalam bahasa Inggris dan dicetak miring saat pertama muncul, lalu dijelaskan singkat. Contoh: *throughput* (jumlah request yang selesai per detik).
- Jangan menerjemahkan paksa: "cache", bukan "tembolok"; "load balancer", bukan "penyeimbang beban".

## Lesson

- Kalimat pertama adalah intinya. Jangan dibuka dengan "Pada lesson ini kita akan...".
- Satu lesson = satu ide. Panjang 300–600 kata, bisa dibaca dalam 3–5 menit.
- Wajib ada **satu contoh konkret** dengan angka atau skenario nyata (bersumber).
- Wajib ada **satu "kapan tidak dipakai"** atau trade-off.
- Diagram ditulis sebagai Mermaid atau deskripsi untuk dibuat ulang. Tidak ada gambar yang disalin.
- Hindari: "sangat penting", "di era modern", "mari kita selami", "kesimpulannya", emoji, dan daftar berpoin yang sebenarnya satu kalimat.

## Soal

- Uji pemahaman atau penerapan, bukan hafalan definisi.
- **Anti-bocor:** judul, kata kunci di pertanyaan, dan panjang opsi tidak boleh mengarah ke jawaban. Opsi benar tidak boleh selalu yang paling panjang atau paling detail.
- Pengecoh harus masuk akal: diambil dari miskonsepsi nyata di `misconceptions.md`.
- Setiap soal punya pembahasan 1–3 kalimat: kenapa jawaban benar, dan kenapa pengecoh utama salah.
- Soal estimasi memberi rentang jawaban yang diterima, bukan satu angka.

## Contoh singkat

Buruk:
> Caching adalah teknik yang sangat penting dalam system design modern untuk meningkatkan performa.

Baik:
> Cache menyimpan hasil yang sering dibaca di tempat yang lebih cepat dari sumber aslinya. Kalau 90% request membaca 10% data yang sama, cache di depan database bisa memangkas sebagian besar beban baca. Tapi data di cache bisa basi, jadi kamu harus memutuskan seberapa basi yang masih bisa diterima.
