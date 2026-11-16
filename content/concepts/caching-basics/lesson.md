---
concept: caching-basics
title: Dasar caching
sources:
  - azure-cache-aside-pattern
  - aws-builders-caching-challenges
  - mdn-http-caching
  - rfc-9111-http-caching
status: review
---

*Cache* menyimpan hasil bacaan yang sering diulang di tempat yang lebih cepat daripada sumber aslinya, sehingga database tidak menjawab pertanyaan yang sama terus-menerus.

## Kapan cache diperlukan, dan kapan belum

Patokan kurikulum ini (bukan fakta dari sumber): pertimbangkan cache kalau bacaan mendominasi lebih dari 80% query database dan query yang sama terus diulang. Kalau database masih santai, cache belum perlu. Kalau sebagian besar request tidak ketemu di cache, biaya mengecek dan mengisinya bisa melebihi manfaat.[^azure-cache-aside-pattern] Kalau cache hilang, layanan hilir seperti database bisa kewalahan.[^aws-builders-caching-challenges]

## Cache-aside dan write-through

Bagaimana aplikasi membaca dan menulis lewat cache biasa? Dengan *cache-aside*, aplikasi mengurusnya sendiri: ia mengecek cache, dan kalau miss (item tidak ada), membaca database lalu menyimpan hasilnya ke cache. Saat menulis, ia mengubah database dulu, baru meng-invalidate item (menghapusnya dari cache).[^azure-cache-aside-pattern]

Kenapa database dulu? Azure menyebut urutan ini penting: kalau item dihapus lebih dulu, request lain bisa miss sebelum database berubah, lalu mengisi cache dengan nilai lama.[^azure-cache-aside-pattern] Kalau dipikir lebih jauh (penalaran penulis): database-dulu mempersempit celah itu tanpa menutupnya, karena pembaca yang sudah mengambil nilai lama sebelum update masih bisa mengisi cache sesudah penghapusan.

Banyak cache komersial punya *read-through* dan *write-through* bawaan, jadi aplikasi cukup bicara dengan cache; cache-aside dipakai kalau fitur itu tidak ada.[^azure-cache-aside-pattern] *Write-through* memperbarui database dan cache dalam satu operasi tulis, jadi pembaca langsung melihat nilai baru. Cache-aside hanya menghapus, jadi pembaca bisa kena miss atau data lama sebentar; jalur yang butuh nilai terbaru lebih cocok dengan write-through.[^azure-cache-aside-pattern] Ada juga *write-behind*: sistem cache menulis balik perubahan ke database.[^azure-cache-aside-pattern] Istilah umumnya *write-back*, tetapi nama itu bukan dari sumber. Di sini ia baru diperkenalkan; trade-off-nya dibahas nanti.

## TTL dan invalidation

*TTL* (*time to live*) adalah umur item sebelum dianggap kedaluwarsa. TTL terlalu pendek membuat aplikasi terus ke database; terlalu panjang membuat data basi.[^azure-cache-aside-pattern] Tentukan TTL dari traffic nyata, bukan tebakan.[^aws-builders-caching-challenges] Mulai dari toleransi basi data.

Cache HTTP memakai *header* (metadata respons) `Cache-Control`. *Validasi* berarti cache bertanya ke *origin* (server asli) apakah salinannya masih sah.[^mdn-http-caching]

- `max-age=604800`: segar seminggu tanpa bertanya ke origin.
- `no-cache`: boleh disimpan, tetapi harus divalidasi sebelum dipakai ulang.
- `no-store`: tidak boleh disimpan cache mana pun.
- `private`: hanya cache satu pengguna, seperti browser.
- `public`: cache bersama (proxy, CDN) boleh menyimpan, tetapi baru perlu ditulis kalau request memakai header `Authorization`.
- `immutable`: isi tidak berubah selama masa segar.

File `bundle.v123.js` boleh disimpan setahun karena isi baru berarti URL baru. HTML dengan URL tetap cocok dengan `no-cache`, karena selalu divalidasi dulu.[^mdn-http-caching] Mirip cache-aside, cache HTTP wajib meng-invalidate URL target setelah PUT, POST, atau DELETE dijawab status non-error.[^rfc-9111-http-caching]

## Contoh skenario tipikal: hit ratio

Asumsi buatan sendiri, bukan data sumber: 2.000 bacaan per detik, cek cache 1 ms, query database 20 ms (miss membayar 21 ms). *Hit ratio* adalah porsi request yang dijawab cache.

- Hit ratio 90%: database menerima 10% x 2.000 = 200 query per detik; latency rata-rata 0,9 x 1 + 0,1 x 21 = 3 ms.
- Hit ratio 99%: database hanya menerima 20 query per detik.

Beban database mengikuti miss ratio, jadi kenaikan 9 poin memangkas beban sepuluh kali.

## Trade-off

Cache-aside tidak menjamin cache sama dengan database: proses lain bisa mengubah database kapan saja, baru terlihat setelah item dimuat ulang. Cache cocok untuk data yang jarang berubah; data sensitif ambil dari sumber utamanya.[^azure-cache-aside-pattern] Kalau cache mati lama, layanan yang langsung beralih ke database bisa melonjakkan traffic ke sana.[^aws-builders-caching-challenges]
