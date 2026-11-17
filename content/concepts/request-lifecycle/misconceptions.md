---
concept: request-lifecycle
---

## database-always-slowest

**Keyakinan keliru:** Kalau halaman terasa lambat, penyebabnya hampir pasti query database, jadi langsung saja tambah index atau upgrade database.

**Kenapa keliru:** Waktu sampai byte pertama adalah jumlah beberapa fase: redirect, DNS, koneksi dan negosiasi TLS, lalu pekerjaan backend.[^web-dev-ttfb] Database hanya bagian dari fase terakhir. Tanpa data waktu per tahap, tebakan "pasti database" bisa mengoptimalkan tahap yang kecil.

## browser-talks-directly-to-app

**Keyakinan keliru:** Browser mengirim request langsung ke kode aplikasi, dan aplikasi langsung mengembalikan jawabannya.

**Kenapa keliru:** Di antara client dan server bisa ada perantara (proxy) yang meneruskan, menyaring, men-cache, atau mencatat pesan.[^mdn-http-overview] Reverse proxy seperti NGINX meneruskan request ke aplikasi, mengambil responsnya, lalu mengirimkannya ke client, dan secara default mengubah beberapa header di perjalanan.[^nginx-reverse-proxy-admin-guide]

## dns-every-request

**Keyakinan keliru:** Setiap request HTTP diawali pencarian DNS dan koneksi baru, jadi dua tahap itu selalu memakan waktu yang sama.

**Kenapa keliru:** Resolver menyimpan jawaban DNS selama TTL record-nya, sehingga pencarian berulang dalam rentang itu melewati seluruh penelusuran.[^aws-route53-how-dns-routes-traffic] Koneksi TCP juga bisa dipakai ulang (*persistent connection*), karena membuka koneksi baru untuk tiap request memboroskan beberapa round trip.[^mdn-http-overview] Karena itu DNS dan koneksi biasanya mahal di request pertama saja.

## one-page-one-request

**Keyakinan keliru:** Membuka satu halaman web berarti satu request ke server.

**Kenapa keliru:** Browser mengambil HTML dulu, lalu mengirim request tambahan untuk tiap resource yang disebut halaman itu: CSS, script, gambar.[^mdn-http-overview] Satu kunjungan bisa berarti banyak request, dan tiap request punya tahap-tahap server sendiri.

## server-time-is-user-time

**Keyakinan keliru:** Waktu yang dicatat log server sama dengan waktu yang dirasakan pengguna, jadi kalau log server bagus berarti tidak ada yang perlu diperiksa lagi.

**Kenapa keliru:** Waktu yang dirasakan pengguna dihitung dari awal navigasi di browser dan sudah memuat DNS serta koneksi dan TLS sebelum server mulai bekerja.[^web-dev-ttfb] Log server hanya melihat bagian setelah request sampai.
