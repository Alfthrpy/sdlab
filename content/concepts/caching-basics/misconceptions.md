---
concept: caching-basics
---

## cache-everywhere

**Keyakinan keliru:** Cache hampir selalu mempercepat sistem, jadi pasang saja di depan semua query sejak awal.

**Kenapa keliru:** Cache hanya membantu kalau data yang sama dibaca berulang kali. Kalau sebagian besar request tidak ketemu di cache (*cache miss*), biaya mengecek cache dan mengisinya bisa lebih besar daripada manfaatnya.[^azure-cache-aside-pattern] Cache juga membuat layanan makin bergantung padanya, sehingga kehilangan cache bisa menjadi gangguan.[^aws-builders-caching-challenges]

## cache-always-in-sync

**Keyakinan keliru:** Kalau aplikasi sudah menghapus item cache saat data berubah, isi cache pasti selalu sama dengan database.

**Kenapa keliru:** Cache-aside tidak menjamin konsistensi. Proses lain bisa mengubah database kapan saja, dan perubahan itu baru terlihat setelah item dimuat ulang. Di antara penulisan dan pembacaan berikutnya, pembaca juga bisa melihat data lama sebentar.[^azure-cache-aside-pattern]

## ttl-as-long-as-possible

**Keyakinan keliru:** TTL sebaiknya diset sepanjang mungkin supaya database paling jarang disentuh.

**Kenapa keliru:** TTL yang terlalu panjang membuat data basi. Sebaliknya, TTL yang terlalu pendek membuat aplikasi terus mengambil dari database dan mengisi ulang cache. Nilainya harus cocok dengan pola akses dan toleransi basi data, dan sebaiknya ditentukan dari pengukuran traffic nyata.[^azure-cache-aside-pattern][^aws-builders-caching-challenges]

## invalidate-order-irrelevant

**Keyakinan keliru:** Saat data diubah, urutan "hapus cache" dan "update database" tidak penting selama keduanya dilakukan.

**Kenapa keliru:** Kalau cache dihapus lebih dulu, request lain bisa menyela sebelum database berubah. Request itu miss, membaca nilai lama dari database, lalu menaruhnya kembali di cache, sehingga data basi tertahan.[^azure-cache-aside-pattern] Azure karena itu menyuruh update database lebih dulu, baru menghapus item cache.[^azure-cache-aside-pattern] Catatan: ini penalaran penulis, bukan klaim sumber. Urutan database-dulu mempersempit celah, tetapi pembaca yang sudah mengambil nilai lama sebelum update masih bisa mengisi cache sesudah penghapusan.

## no-cache-means-no-storage

**Keyakinan keliru:** Header `Cache-Control: no-cache` berarti respons tidak disimpan sama sekali, jadi aman untuk data sensitif.

**Kenapa keliru:** `no-cache` tetap membolehkan penyimpanan. Yang dilarang hanyalah memakai ulang tanpa memeriksa ke origin dulu. Yang melarang penyimpanan adalah `no-store`.[^mdn-http-caching][^rfc-9111-http-caching]

## hit-ratio-linear

**Keyakinan keliru:** Hit ratio naik dari 90% ke 99% hanya menambah sedikit manfaat, karena angkanya cuma naik 9 poin.

**Kenapa keliru:** Beban database sebanding dengan miss ratio, bukan hit ratio. Dari 10% miss menjadi 1% miss, beban database turun sepuluh kali lipat (hitungan sederhana, bukan klaim dari sumber).
