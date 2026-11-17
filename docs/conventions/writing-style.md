# Writing style guide (final, P1-031)

This guide governs **learner-facing content**, which is written in Indonesian. The guide itself is in English; examples of Indonesian text are kept in Indonesian on purpose.

Readers are students, junior engineers, and solo developers or beginners (ADR 0004). They know basic programming, HTTP, and basic SQL, but have not operated a distributed system, and they are busy. Writing must be direct, specific, and must not sound machine-made. Explain the problem a concept solves and what breaks without it before describing the mechanism; explain every term on first use.

## Language

- Standard Indonesian but relaxed. Address the reader as "kamu".
- Technical terms stay in English and are italicized on first appearance, then briefly explained. Example: *throughput* (jumlah request yang selesai per detik).
- Do not force translations: "cache", not "tembolok"; "load balancer", not "penyeimbang beban".

## Lessons

- The first sentence is the core point. Do not open with "Pada lesson ini kita akan...".
- One lesson = one idea. Length 300–600 words, readable in 3–5 minutes. Check the count while writing with `python scripts/validate.py --stats` (same method as the validator; a lesson near 600 has no room for review fixes, so aim for about 500).
- Must include **one concrete example** with real (sourced) numbers or a real scenario.
- Must include **one "when not to use it"** or trade-off.
- Units 1–6: state the concept's **trigger** (the symptom or number that says it is time to use it).
- Diagrams are written as Mermaid or as a description to be redrawn. No copied images.
- Do not narrate provenance in learner text ("menurut sumber", "penalaran penulis", "hitungan sendiri", "bukan dari sumber"). The `[^id]` markers carry it; see [citation-guide](citation-guide.md). Worked examples open with "Misalkan ...".
- No filler and no emoji. Filler phrases the validator looks for: "sangat penting", "di era modern", "mari kita selami", "kesimpulannya", "dalam dunia yang semakin", "tidak dapat dipungkiri", "perlu diingat bahwa". Do not replace one filler phrase with a synonym; say the fact instead.
- Bullet lists are for parallel items, not for one sentence broken into lines.

## Questions

- Test understanding or application, not memorized definitions.
- **Anti-leak:** the title, keywords in the question, and option length must not point to the answer. The correct option must not always be the longest or most detailed.
- Distractors must be plausible: drawn from real misconceptions in `misconceptions.md`.
- Every question has a 1–3 sentence explanation: why the answer is right, and why the main distractor is wrong.
- Estimation questions give an accepted range, not a single number.

### Difficulty levels

Calibrated for juniors, not seniors:

| Level | Meaning |
| --- | --- |
| 1 | Recognize or recall one concept and why it exists. |
| 2 | Apply one concept to a simple scenario, or compare two options. |
| 3 | **Challenging for a junior:** combine two or more concepts, diagnose a symptom, or weigh trade-offs. It is not a senior-level question; a student who studied the lesson and thought carefully can solve it. |

Every concept should have a mix of levels.

## Good and bad examples

Indonesian text is kept in Indonesian on purpose. Each pair shows the pattern to avoid and a fix.

### Lessons

**1. The opening sentence.**

Bad (announces instead of saying something):
> Pada lesson ini kita akan membahas retry dan kenapa itu penting.

Good (the core point first):
> Kalau ribuan client mengulang request di detik yang sama, server yang sedang lambat justru dibanjiri dan makin sulit pulih.

**2. Specific instead of generic.**

Bad:
> Banyak perusahaan besar memakai sharding untuk menangani data yang besar.

Good (a real scenario with sourced numbers, cited with a `[^id]` marker):
> Slack mencatat sekitar 2,3 juta query per detik di puncak, dan hampir semuanya lewat Vitess yang membagi data ke banyak shard MySQL.[^slack-vitess-datastores-2020]

**3. A trade-off, not a promise.**

Bad:
> Replication membuat sistem selalu lebih andal.

Good:
> Replication asinkron membuat pembacaan lebih cepat dan sistem tahan satu mesin mati. Harganya: tulisan yang belum sempat disalin ke follower bisa hilang kalau leader mati.

**4. Terms explained on first use.**

Bad:
> Pakai idempotency key supaya request aman di-retry.

Good:
> Pakai *idempotency key*, yaitu kode unik yang dikirim client supaya server tahu bahwa request yang diulang sama dengan request pertama, sehingga pembayaran tidak terpotong dua kali.

**5. Filler.** "Sangat penting", "di era modern", "mari kita selami", "kesimpulannya", and emoji add no information. Delete the sentence, or replace it with the fact it was hiding.

### Questions

**6. The prompt gives the answer away.**

Bad (the correct option repeats the prompt's words, and nothing else in the other options relates to them):
> Apa itu *cache stampede*?
> A. Banyak request menyerbu database saat key populer di *cache* kedaluwarsa  ← benar
> B. Cache yang penuh dan menghapus data lama
> C. Cache yang menyimpan data dua kali

Good (the prompt describes a situation; every option is a believable reaction, similar in length and shape):
> Seribu request meminta key yang sama tepat saat cache-nya kedaluwarsa. Apa yang paling mengurangi beban database?
> A. Satu request membangun ulang nilainya, request lain menunggu hasilnya  ← benar
> B. Menaikkan TTL semua key dua kali lipat agar kedaluwarsa lebih jarang
> C. Menambah jumlah koneksi ke database agar lebih banyak request terlayani
> D. Menghapus key kedaluwarsa tiap menit supaya cache tidak terlalu penuh

Note that the right answer here is reachable only by understanding why the requests pile up, not by matching words.

**7. The correct option is the longest or the most detailed.** Write the distractors with the same length and the same level of detail as the correct option. If the correct option needs a clause, give each distractor a clause as well.

**8. Implausible distractors.**

Bad:
> Di mana cache biasanya disimpan? ... C. Di pita magnetik

Good: a distractor is a real misconception from `misconceptions.md`, for example "Cache konsisten dengan database karena ditulis bersamaan". If nobody would believe it, it is not a distractor.

**9. Escape-hatch options.** Do not use "semua jawaban benar", "tidak ada yang benar", or "A dan B benar". They let a learner pass without knowing the content.

**10. Absolute words in wrong options only.** Options with *selalu*, *tidak pernah*, *semua*, *pasti* are almost always wrong, so a learner learns to skip them. Use absolutes in correct options sometimes, or avoid them.

**11. The explanation.**

Bad:
> Jawaban A benar.

Good (1–3 sentences: why it is right, and why the main distractor is wrong):
> Hanya satu request yang perlu membangun ulang nilai; yang lain bisa menunggu hasilnya. Menaikkan TTL (B) hanya menunda masalah yang sama sampai kedaluwarsa berikutnya.

**12. Odd-one-out shape.** Check each mcq for a correct option that differs from the others in form, not content: the only one with a stated reason, the only one that does not start with the opening word the others share (for example "Karena ..."), the only one with a number. A learner picks it without reading the prompt. Give every option the same grammatical shape and the same amount of explanation.

**13. Estimate ranges that accept the common wrong result.** For every `estimate` question, compute the answer the common wrong method gives (the miss that is billed 40 ms instead of 2 + 40, a percentage-point change read as a ratio, ...) and make sure it falls outside `answer.min`..`answer.max`. A range of 7.5-8.5 accepts the wrong 7.6; narrow it, or change the numbers so the two results are far apart. Name the wrong result in the explanation when it is a likely one.

**14. Test only what the lesson teaches.** Every question must be answerable from the lesson plus the concept's prerequisites, and must match the objective it is tagged with. A question about HTTP directives the lesson never mentions, or about a detail that no objective names, tests the learner's luck, not the concept. If it deserves a question, put the idea into the lesson first.

### Mix of difficulty

Each concept should mix levels. A level 1 question: a service opens a new database connection for every request and gets slower under load; why? A level 2 question gives a pool size and a request rate and asks whether the pool is enough. A level 3 question shows a latency graph with a pool at its limit and asks what to change first and what the trade-off is.

## Automatic checks (warnings)

`python scripts/validate.py` warns, never fails, on these patterns (thresholds are constants in `scripts/validate.py`). They flag likely problems for the author or the `content-reviewer`; they are not proof. The first four checks look only at mcq questions with 3 or more options, and need 4 or more of them (5 or more for the position check), because they are statistics over a concept's question set.

| Check | Warns when |
| --- | --- |
| Longest correct option | the correct option is strictly the longest in more than 40% of mcq questions |
| Answer position | one option position holds the correct answer in more than 50% of mcq questions (5 or more mcq) |
| Prompt echo | the correct option shares the most words (5+ letters, minus common function words) with the prompt in more than 50% of mcq questions |
| Absolute words | `selalu`, `tidak pernah`, `pasti`, `mustahil`, `selamanya`, `satu-satunya` appear only in wrong options in 3 or more mcq questions (and in more than 30% of them) |
| Escape-hatch options | any question type: an option says "semua jawaban benar", "tidak ada yang benar", or "A dan B benar" |
| Explanation length | an explanation has more than 3 sentences (abbreviations such as "mis." and "dst." do not count as sentence ends) |
| Difficulty mix | 4 or more questions with a valid difficulty all have the same one |
| Lesson opener | the first sentence (after headings) opens with "Pada/Dalam/Di lesson ini ...", "Kali ini kita ...", or "Mari kita ..." |
| Filler and emoji | a lesson contains a filler phrase from the list in "Lessons" or an emoji. Fenced code, inline code, and quoted phrases are ignored. |
| Question without a source | a question has no `sources` and no `own_computation: true` (use the flag for arithmetic that follows only from the numbers in the prompt, like hit-ratio and latency estimates) |
| Provenance narration | a lesson, misconception or question explanation says where a statement comes from ("menurut Azure", "dari sumber", "penalaran penulis", "hitungan sendiri", ...) |

What the validator cannot see (the reviewer must): a distractor that is implausible, a prompt that hints through meaning rather than words, a wrong difficulty level, a claim that the source does not support. The `content-reviewer` uses these warnings as input, not as a verdict.

## Short example (lesson paragraph)

Bad (generic filler):
> Caching adalah teknik yang sangat penting dalam system design modern untuk meningkatkan performa.

Good (core point first, concrete, with trade-off):
> Cache menyimpan hasil yang sering dibaca di tempat yang lebih cepat dari sumber aslinya. Kalau 90% request membaca 10% data yang sama, cache di depan database bisa memangkas sebagian besar beban baca. Tapi data di cache bisa basi, jadi kamu harus memutuskan seberapa basi yang masih bisa diterima.
