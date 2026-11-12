# Kurikulum

File di folder ini dibuat di milestone M2:

| File | Dibuat di ticket | Skema |
| --- | --- | --- |
| `concepts.yaml` | P1-020, P1-021, P1-023 | `docs/conventions/content-schema.md` §2 |
| `case-studies.yaml` | P1-022 | `docs/conventions/content-schema.md` §3 |

## Unit (titik awal dari rencana induk)

| Unit | Konsep inti |
| --- | --- |
| 1. Fondasi | Latency vs throughput, estimasi back-of-envelope, hukum Little, persentil, SLI/SLO |
| 2. Building blocks | Load balancer, reverse proxy, cache, CDN, API (REST/gRPC), idempotency |
| 3. Data | Model data, indeks, replikasi, partisi, transaksi & isolasi |
| 4. Asinkron & aliran | Message queue, log, semantik pengiriman, outbox, backpressure |
| 5. Konsistensi & koordinasi | CAP/PACELC, model konsistensi, consensus, lock & lease, waktu & jam |
| 6. Reliabilitas produksi | Timeout, retry + backoff + jitter, circuit breaker, load shedding, cascading & metastable failure, observability, deploy aman |
