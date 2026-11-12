# Writing style guide (v0, finalized in P1-031)

This guide governs **learner-facing content**, which is written in Indonesian. The guide itself is in English; examples of Indonesian text are kept in Indonesian on purpose.

Readers are students, junior engineers, and solo developers or beginners (ADR 0004). They know basic programming, HTTP, and basic SQL, but have not operated a distributed system, and they are busy. Writing must be direct, specific, and must not sound machine-made. Explain the problem a concept solves and what breaks without it before describing the mechanism; explain every term on first use.

## Language

- Standard Indonesian but relaxed. Address the reader as "kamu".
- Technical terms stay in English and are italicized on first appearance, then briefly explained. Example: *throughput* (jumlah request yang selesai per detik).
- Do not force translations: "cache", not "tembolok"; "load balancer", not "penyeimbang beban".

## Lessons

- The first sentence is the core point. Do not open with "Pada lesson ini kita akan...".
- One lesson = one idea. Length 300–600 words, readable in 3–5 minutes.
- Must include **one concrete example** with real (sourced) numbers or a real scenario.
- Must include **one "when not to use it"** or trade-off.
- Units 1–6: state the concept's **trigger** (the symptom or number that says it is time to use it).
- Diagrams are written as Mermaid or as a description to be redrawn. No copied images.
- Avoid these filler phrases (Indonesian originals; in English: "very important", "in the modern era", "let's dive in", "in conclusion"), emoji, and bullet lists that are really one sentence: "sangat penting", "di era modern", "mari kita selami", "kesimpulannya".

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

## Short example

Bad (generic filler):
> Caching adalah teknik yang sangat penting dalam system design modern untuk meningkatkan performa.

Good (core point first, concrete, with trade-off):
> Cache menyimpan hasil yang sering dibaca di tempat yang lebih cepat dari sumber aslinya. Kalau 90% request membaca 10% data yang sama, cache di depan database bisa memangkas sebagian besar beban baca. Tapi data di cache bisa basi, jadi kamu harus memutuskan seberapa basi yang masih bisa diterima.
