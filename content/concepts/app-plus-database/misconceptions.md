---
concept: app-plus-database
---

## average-is-enough

**Keyakinan keliru:** Cukup hitung request per detik rata-rata dari total request harian, lalu pastikan server sanggup menanganinya.

**Kenapa keliru:** Trafik naik dan turun sepanjang hari karena pengguna bekerja, tidur, dan berada di zona waktu berbeda. Kalau kapasitas hanya dibangun untuk rata-rata, kamu akan bermasalah saat puncak.[^robustperception-peak-to-mean-ratio] Karena itu rata-rata harus dikalikan *peak-to-mean ratio* dulu sebelum dibandingkan dengan kapasitas.

## one-db-is-toy

**Keyakinan keliru:** Satu database hanya cocok untuk proyek mainan; produk yang serius harus langsung memakai banyak server dan database terpisah.

**Kenapa keliru:** Rilis pertama sebuah toko online memang bisa berupa satu aplikasi dan satu database di satu mesin.[^aws-startups-scaling-part1-primer] Cukup atau tidaknya ditentukan hitungan: puncak RPS dibandingkan dengan kapasitas database yang kamu ukur sendiri. Situs besar memakai banyak server karena bebannya jauh lebih besar. Stack Overflow, misalnya, menerima 209.420.973 request HTTP dalam satu hari di 2016, dan satu primary di tiap cluster databasenya menanggung hampir seluruh beban.[^craver-stack-overflow-architecture-2016] Tapi mereka juga punya banyak web server, replika, Redis, dan Elasticsearch,[^craver-stack-overflow-architecture-2016] jadi itu acuan beban, bukan contoh satu mesin.

## memory-survives-restart

**Keyakinan keliru:** Kalau aplikasi hanya berjalan sebagai satu proses, data di variabel memori atau file lokal aman, karena tidak ada server lain yang bisa membuatnya hilang.

**Kenapa keliru:** Memori proses selalu hilang saat proses di-restart, termasuk saat hanya ada satu proses. File lokal bisa bertahan di VPS biasa. Tetapi state lokal biasanya ikut terhapus saat lingkungan memindahkan proses ke mesin atau container lain.[^twelve-factor-app] Data yang harus bertahan perlu disimpan di layanan pendukung seperti database, bukan di proses aplikasi.[^twelve-factor-app]

## small-rps-means-no-risk

**Keyakinan keliru:** Kalau hitungan RPS puncak jauh di bawah kapasitas, satu aplikasi dan satu database pasti aman dalam segala hal.

**Kenapa keliru:** Hitungan RPS hanya memeriksa volume. Dengan satu mesin, satu kegagalan mematikan semuanya,[^aws-startups-scaling-part1-primer] jadi hitungan yang kecil tidak menjawab apakah toko boleh mati total saat mesinnya rusak. Kapasitas juga harus diukur, bukan hanya dihitung. Kalau databasenya SQLite (database berupa satu file di dalam aplikasi), beban tulis yang berat atau banyak server aplikasi juga menjadi alasan pindah ke database client/server, yaitu proses database terpisah yang diakses lewat jaringan.[^sqlite-appropriate-uses]

## all-state-in-database

**Keyakinan keliru:** Karena proses aplikasi harus stateless, semua data, termasuk hasil olahan sementara di tengah satu request atau job, harus ditulis ke database dulu.

**Kenapa keliru:** Memori proses boleh dipakai untuk nilai sementara selama satu tugas, misalnya gambar yang sedang diubah ukurannya dalam satu request upload, asalkan hasil akhirnya ditulis ke database. Yang tidak boleh adalah mengandalkan isinya masih ada di request atau job berikutnya.[^twelve-factor-app]
