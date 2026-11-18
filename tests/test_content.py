"""Fixture tests for citation rules in scripts/validate.py (check_content).

Run: python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate  # noqa: E402

REG = {
    "blog": {"type": "article", "status": "approved", "usage": "rewrite-only", "title": "A Blog"},
    "book": {"type": "book", "status": "approved", "usage": "rewrite-only", "title": "A Book"},
    "cand": {"type": "article", "status": "candidate", "usage": "rewrite-only", "title": "Cand"},
    "map": {"type": "docs", "status": "approved", "usage": "map-only", "title": "Map"},
    "ccby": {"type": "article", "status": "approved", "usage": "adapt-with-attribution", "title": "CC Source"},
}


def lesson(sources, body, status="draft"):
    fm = yaml.safe_dump({"concept": "c1", "title": "T", "sources": sources, "status": status})
    return f"---\n{fm}---\n{body}\n"


def run(text, questions=None, status_published=False, misc=None, concepts=None):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        cdir = root / "concepts" / "c1"
        cdir.mkdir(parents=True)
        (cdir / "lesson.md").write_text(text, encoding="utf-8")
        if questions is not None:
            (cdir / "questions.yaml").write_text(yaml.safe_dump({"questions": questions}))
        if misc is not None:
            (cdir / "misconceptions.md").write_text(misc, encoding="utf-8")
        old = (validate.CONTENT, validate.rel)
        validate.CONTENT, validate.rel = root, lambda p: p.name
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_content(REG, concepts or {})
            return list(validate.errors), list(validate.warnings)
        finally:
            validate.CONTENT, validate.rel = old


def has(msgs, text):
    return any(text in m for m in msgs)


class Citations(unittest.TestCase):
    def test_clean_lesson(self):
        errs, _ = run(lesson(["blog"], "Retry tanpa jitter itu berbahaya.[^blog]"))
        self.assertEqual(errs, [])

    def test_marker_not_in_sources(self):
        errs, _ = run(lesson(["blog"], "Klaim.[^book]"))
        self.assertTrue(has(errs, "[^book] is not in frontmatter sources"))

    def test_marker_not_in_registry(self):
        errs, _ = run(lesson(["blog"], "Klaim.[^ghost]"))
        self.assertTrue(has(errs, "[^ghost] is not in the registry"))

    def test_published_cannot_cite_candidate(self):
        errs, _ = run(lesson(["cand"], "Klaim.[^cand]", status="published"), questions=[])
        self.assertTrue(has(errs, "not approved: cand"))
        errs, _ = run(lesson(["cand"], "Klaim.[^cand]", status="draft"))
        self.assertFalse(has(errs, "not approved"))

    def test_published_question_cannot_cite_candidate(self):
        q = [{"id": "q1", "type": "estimate", "prompt": "p", "explanation": "e", "sources": ["cand"],
              "answer": {"min": 1, "max": 2}}]
        errs, _ = run(lesson(["blog"], "Klaim.[^blog]", status="published"), questions=q)
        self.assertTrue(has(errs, "q1: published content cites a source that is not approved: cand"))

    def test_map_only_source_forbidden(self):
        errs, _ = run(lesson(["map"], "Klaim.[^map]"))
        self.assertTrue(has(errs, "map-only"))

    def test_loc_required_for_books(self):
        errs, _ = run(lesson(["book"], "Klaim.[^book]"))
        self.assertTrue(has(errs, "`loc`"))
        errs, _ = run(lesson([{"id": "book", "loc": "bab 6"}], "Klaim.[^book]"))
        self.assertFalse(has(errs, "`loc`"))

    def test_attribution_required_for_adapt_source(self):
        errs, _ = run(lesson(["ccby"], "Klaim.[^ccby]"))
        self.assertTrue(has(errs, "attribution line"))
        ok = "Klaim.[^ccby]\n\n---\nSebagian materi diadaptasi dari *CC Source* oleh X, CC BY 4.0. Telah diubah."
        errs, warns = run(lesson(["ccby"], ok))
        self.assertEqual(errs, [])
        self.assertEqual(warns and [w for w in warns if "attribution" in w], [])


class Coverage(unittest.TestCase):
    def test_sources_must_be_in_registry(self):
        errs, _ = run(lesson(["ghost"], "Klaim."))
        self.assertTrue(has(errs, "source not in registry: ghost"))
        q = [{"id": "q1", "type": "estimate", "prompt": "p", "explanation": "e", "sources": ["ghost"],
              "answer": {"min": 1, "max": 2}}]
        errs, _ = run(lesson(["blog"], "Klaim.[^blog]"), questions=q)
        self.assertTrue(has(errs, "q1: source not in registry: ghost"))

    def test_map_only_question_source_forbidden(self):
        q = [{"id": "q1", "type": "estimate", "prompt": "p", "explanation": "e", "sources": ["map"],
              "answer": {"min": 1, "max": 2}}]
        errs, _ = run(lesson(["blog"], "Klaim.[^blog]"), questions=q)
        self.assertTrue(has(errs, "q1: a map-only"))

    def test_attribution_should_name_title(self):
        body = "Klaim.[^ccby]\n\n---\nSebagian materi diadaptasi dari sebuah sumber. Telah diubah."
        errs, warns = run(lesson(["ccby"], body))
        self.assertEqual(errs, [])
        self.assertTrue(has(warns, "should name the source title"))

    def test_guide_sample_lesson(self):
        guide = (Path(__file__).resolve().parent.parent / "docs/conventions/citation-guide.md").read_text()
        sample = guide.split("## Sample lesson", 1)[1].split("```markdown\n", 1)[1].split("\n```", 1)[0]
        reg = dict(REG, **{"aws-builders-timeouts-retries": REG["blog"], "ddia-2e": REG["book"]})
        errs, warns = run_with(reg, sample.replace("concept: example-retries", "concept: c1") + "\n")
        self.assertEqual(errs, [])


def run_with(reg, text):
    saved = dict(REG)
    REG.clear(); REG.update(reg)
    try:
        return run(text)
    finally:
        REG.clear(); REG.update(saved)


class Quotes(unittest.TestCase):
    def test_one_short_quote_ok(self):
        errs, _ = run(lesson(["blog"], 'Definisinya: "sistem yang tetap berjalan saat gagal".[^blog]'))
        self.assertEqual(errs, [])

    def test_long_quote_rejected(self):
        long = " ".join(["kata"] * 15)
        errs, _ = run(lesson(["blog"], f'Kutipan: "{long}"[^blog]'))
        self.assertTrue(has(errs, "15 words"))

    def test_quoted_terms_and_code_are_not_quotes(self):
        body = 'Istilah "split brain"[^blog] dan "eventual consistency"[^blog].\n\n```\nx = "a b c d e"[^blog]\n```'
        errs, _ = run(lesson(["blog"], body))
        self.assertEqual(errs, [])

    def test_second_quote_from_same_source_rejected(self):
        body = 'Satu: "pendek satu dua tiga".[^blog] Dua: “pendek dua tiga empat”[^blog]'
        errs, _ = run(lesson(["blog"], body))
        self.assertTrue(has(errs, "2 direct quotes from blog"))


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------- final content schema (P1-030)
WORDS = " ".join(["kata"] * 320)
CONCEPTS = {"c1": {"objectives": ["Bisa A", "Bisa B"]}}


def q(i, type="mcq", **kw):
    base = {"id": f"c1-q{i:02d}", "type": type, "difficulty": 2, "prompt": "P?", "explanation": "E.",
            "objective": 1}
    if type == "mcq":
        base.update(options=["aa", "bbbb", "cc"], answer=0)
    base.update(kw)
    return base


MISC = ("---\nconcept: c1\n---\n\n## stale-ok\n\n**Keyakinan keliru:** x\n\n**Kenapa keliru:** y\n\n"
        "## ttl-safe\n\n**Keyakinan keliru:** x\n\n**Kenapa keliru:** y\n\n"
        "## cache-free\n\n**Keyakinan keliru:** x\n\n**Kenapa keliru:** y\n")


class FinalSchema(unittest.TestCase):
    def test_frontmatter_requires_fields_and_folder_match(self):
        errs, _ = run("---\nconcept: other\ntitle: T\nstatus: draft\n---\nteks\n")
        self.assertTrue(has(errs, "`sources` is required"))
        self.assertTrue(has(errs, "does not match the folder"))

    def test_status_enum_and_reviewed_by(self):
        errs, _ = run(lesson(["blog"], "x", status="done"))
        self.assertTrue(has(errs, "status must be one of"))
        errs, _ = run(lesson(["blog"], "x", status="published"))
        self.assertTrue(has(errs, "needs `reviewed_by`"))

    def test_length_warns_in_draft_errors_in_review(self):
        short = "Retry itu penting.[^blog]"
        errs, warns = run(lesson(["blog"], short))
        self.assertFalse(has(errs, "lesson length"))
        self.assertTrue(has(warns, "lesson length"))
        errs, _ = run(lesson(["blog"], short, status="review"))
        self.assertTrue(has(errs, "lesson length"))
        errs, _ = run(lesson(["blog"], WORDS, status="review"), misc=MISC)
        self.assertFalse(has(errs, "lesson length"))

    def answer_errors(self, **kw):
        errs, _ = run(lesson(["blog"], WORDS), [q(1, **kw)], misc=MISC, concepts=CONCEPTS)
        return errs

    def test_mcq_answer_range(self):
        self.assertTrue(has(self.answer_errors(answer=5), "valid option index"))
        self.assertEqual(self.answer_errors(answer=1), [])

    def test_multi_answer_format(self):
        ok = dict(type="multi", options=["a", "b", "c", "d"], answer=[0, 2])
        self.assertEqual(self.answer_errors(**ok), [])
        self.assertTrue(has(self.answer_errors(**dict(ok, answer=[0])), "multi answer"))
        self.assertTrue(has(self.answer_errors(**dict(ok, answer=[0, 0])), "multi answer"))
        self.assertTrue(has(self.answer_errors(**dict(ok, answer=[0, 1, 2, 3])), "multi answer"))

    def test_order_answer_is_a_permutation(self):
        ok = dict(type="order", options=["a", "b", "c"], answer=[2, 0, 1])
        self.assertEqual(self.answer_errors(**ok), [])
        self.assertTrue(has(self.answer_errors(**dict(ok, answer=[0, 0, 1])), "order answer"))
        self.assertTrue(has(self.answer_errors(**dict(ok, answer=[0, 1])), "order answer"))

    def test_match_pairs(self):
        ok = dict(type="match", pairs=[["a", "1"], ["b", "2"], ["c", "3"]])
        self.assertEqual(self.answer_errors(**ok), [])
        self.assertTrue(has(self.answer_errors(**dict(ok, pairs=[["a", "1"], ["b", "1"], ["c", "3"]])), "distinct"))
        self.assertTrue(has(self.answer_errors(**dict(ok, pairs=[["a", "1"]])), "match needs"))

    def test_estimate_range_and_unit(self):
        ok = dict(type="estimate", answer={"min": 10, "max": 20}, unit="ms")
        self.assertEqual(self.answer_errors(**ok), [])
        self.assertTrue(has(self.answer_errors(**dict(ok, answer={"min": 20, "max": 10})), "min < max"))
        self.assertTrue(has(self.answer_errors(**dict(ok, unit=None)), "needs a `unit`"))

    def test_difficulty_and_id_prefix(self):
        self.assertTrue(has(self.answer_errors(difficulty=4), "difficulty must be"))
        self.assertTrue(has(self.answer_errors(id="other-q01"), "must look like"))

    def test_duplicate_question_id(self):
        errs, _ = run(lesson(["blog"], WORDS), [q(1), q(1)], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(errs, "empty/duplicate"))

    def test_objective_coverage_in_review(self):
        qs = [q(i) for i in range(1, 7)]
        errs, _ = run(lesson(["blog"], WORDS, status="review"), qs, misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(errs, "objective(s) [2] are not covered"))
        qs[0]["objective"] = 2
        errs, _ = run(lesson(["blog"], WORDS, status="review"), qs, misc=MISC, concepts=CONCEPTS)
        self.assertFalse(has(errs, "not covered"))

    def test_objective_coverage_only_warns_in_draft(self):
        errs, warns = run(lesson(["blog"], WORDS), [q(1)], misc=MISC, concepts=CONCEPTS)
        self.assertFalse(has(errs, "not covered"))
        self.assertTrue(has(warns, "not covered"))

    def test_objective_index_out_of_range(self):
        errs, _ = run(lesson(["blog"], WORDS), [q(1, objective=3)], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(errs, "objective must be an index"))

    def test_question_without_sources_warns_unless_own_computation(self):
        _, warns = run(lesson(["blog"], WORDS), [q(1)], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(warns, "no `sources`"))
        _, warns = run(lesson(["blog"], WORDS), [q(1, own_computation=True)], misc=MISC, concepts=CONCEPTS)
        self.assertFalse(has(warns, "no `sources`"))
        _, warns = run(lesson(["blog"], WORDS), [q(1, sources=["blog"])], misc=MISC, concepts=CONCEPTS)
        self.assertFalse(has(warns, "no `sources`"))

    def test_own_computation_with_sources_warns(self):
        _, warns = run(lesson(["blog"], WORDS), [q(1, sources=["blog"], own_computation=True)], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(warns, "both `sources` and `own_computation"))

    def test_stats_table_lists_each_concept(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as d:
            cdir = Path(d) / "concepts" / "c1"
            cdir.mkdir(parents=True)
            (cdir / "lesson.md").write_text(lesson(["blog"], "satu dua tiga"), encoding="utf-8")
            (cdir / "misconceptions.md").write_text(MISC, encoding="utf-8")
            old = validate.CONTENT
            validate.CONTENT = Path(d)
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    validate.print_stats()
            finally:
                validate.CONTENT = old
        row = [line.split() for line in buf.getvalue().splitlines() if line.startswith("c1 ")][0]
        self.assertEqual(row, ["c1", "draft", "3", "0", "3"])

    def test_lebih_dalam_section_is_not_counted_in_core_length(self):
        body = "satu dua tiga\n\n## Lebih dalam\n\nempat lima enam tujuh"
        self.assertEqual(validate.lesson_words(body), 3)  # only "satu dua tiga"; the heading and the deep text are not core
        self.assertEqual(validate.deep_words(body), 4)
        self.assertEqual(validate.deep_words("tanpa bagian dalam"), 0)

    def test_lebih_dalam_is_capped(self):
        deep = " ".join(["kata"] * (validate.DEEP_MAX_WORDS + 5))
        text = lesson(["blog"], WORDS + "\n\n## Lebih dalam\n\n" + deep, status="review")
        errs, _ = run(text, misc=MISC)
        self.assertTrue(has(errs, "Lebih dalam"))
        text = lesson(["blog"], WORDS + "\n\n## Lebih dalam\n\n" + "kata " * 50, status="review")
        errs, _ = run(text, misc=MISC)
        self.assertFalse(has(errs, "Lebih dalam"))
        self.assertFalse(has(errs, "lesson length"))

    def test_readability_warns_on_many_italic_terms_and_long_sentences(self):
        terms = " ".join(f"*istilah{i}*" for i in range(validate.NEW_TERMS_MAX + 1))
        _, warns = run(lesson(["blog"], f"Inti. {terms}."))
        self.assertTrue(has(warns, "italic first-use terms"))
        _, warns = run(lesson(["blog"], "Inti. *a* dan **tebal** dan *b*."))
        self.assertFalse(has(warns, "italic first-use terms"))
        long = " ".join(["kata"] * (validate.SENTENCE_WORDS_MAX + 6)) + "."
        _, warns = run(lesson(["blog"], long))
        self.assertTrue(has(warns, "average sentence"))
        _, warns = run(lesson(["blog"], "Kalimat pendek ini. Satu lagi di sini."))
        self.assertFalse(has(warns, "average sentence"))

    def test_lesson_words_counts_like_the_length_check(self):
        body = "satu dua[^blog] tiga https://x.example/a empat\n```\nkode kode\n```\nx-y"
        self.assertEqual(validate.lesson_words(body), 6)

    def test_question_count_in_review(self):
        errs, _ = run(lesson(["blog"], WORDS, status="review"), [q(1)], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(errs, "questions (target"))

    def test_misconception_target_must_exist(self):
        errs, _ = run(lesson(["blog"], WORDS), [q(1, targets_misconception="nope")], misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(errs, "is not in misconceptions.md"))
        errs, _ = run(lesson(["blog"], WORDS), [q(1, targets_misconception="stale-ok")], misc=MISC,
                      concepts=CONCEPTS)
        self.assertFalse(has(errs, "misconceptions.md"))
        errs, _ = run(lesson(["blog"], WORDS), [q(1, targets_misconception="stale-ok")], concepts=CONCEPTS)
        self.assertTrue(has(errs, "needs a misconceptions.md"))


class Misconceptions(unittest.TestCase):
    def test_valid_file(self):
        errs, _ = run(lesson(["blog"], WORDS), misc=MISC)
        self.assertEqual(errs, [])

    def test_labels_and_ids_checked(self):
        bad = MISC.replace("**Kenapa keliru:** y", "tanpa label", 1).replace("## ttl-safe", "## stale-ok")
        errs, _ = run(lesson(["blog"], WORDS), misc=bad)
        self.assertTrue(has(errs, "missing the label **Kenapa keliru:**"))
        self.assertTrue(has(errs, "duplicate misconception id"))

    def test_kebab_case_id_and_concept(self):
        bad = MISC.replace("concept: c1", "concept: zzz").replace("## cache-free", "## Cache_Free")
        errs, _ = run(lesson(["blog"], WORDS), misc=bad)
        self.assertTrue(has(errs, "must be kebab-case"))
        self.assertTrue(has(errs, "does not match the folder"))

    def test_missing_file_errors_only_in_review(self):
        errs, _ = run(lesson(["blog"], WORDS))
        self.assertFalse(has(errs, "misconceptions.md"))
        errs, _ = run(lesson(["blog"], WORDS, status="review"))
        self.assertTrue(has(errs, "needs misconceptions.md"))

    def test_unknown_source_marker(self):
        bad = MISC.replace("y\n\n## ttl", "y [^nope]\n\n## ttl", 1)
        errs, _ = run(lesson(["blog"], WORDS), misc=bad)
        self.assertTrue(has(errs, "[^nope] is not in the registry"))


class Hardening(unittest.TestCase):
    """Malformed structures give error lines, never a traceback."""

    def qerrs(self, raw):
        with tempfile.TemporaryDirectory() as d:
            cdir = Path(d) / "concepts" / "c1"
            cdir.mkdir(parents=True)
            (cdir / "lesson.md").write_text(lesson(["blog"], WORDS), encoding="utf-8")
            (cdir / "questions.yaml").write_text(raw, encoding="utf-8")
            old = (validate.CONTENT, validate.rel)
            validate.CONTENT, validate.rel = Path(d), lambda p: p.name
            validate.errors.clear()
            validate.warnings.clear()
            try:
                validate.check_content(REG, {})
                return list(validate.errors)
            finally:
                validate.CONTENT, validate.rel = old

    def test_questions_file_shapes(self):
        for raw in ("questions: {a: 1}\n", "- a\n", "hello\n"):
            self.assertTrue(has(self.qerrs(raw), "questions.yaml must be a mapping"), raw)
        self.assertTrue(has(self.qerrs("questions: [abc]\n"), "must be a mapping, got"))
        self.assertTrue(has(self.qerrs("questions:\n  - \n"), "must be a mapping, got"))

    def test_unhashable_or_wrong_typed_fields(self):
        for item in ("{id: [a]}", "{id: c1-q01, type: [a]}", "{id: c1-q01, type: mcq, sources: [[a]]}",
                     "{id: c1-q01, type: mcq, sources: blog}", "{id: c1-q01, type: mcq, targets_misconception: [a]}",
                     "{id: c1-q01, type: mcq, options: [[1], [2], [3]], answer: 0}"):
            self.qerrs("questions:\n  - " + item + "\n")  # must not raise

    def test_difficulty_must_be_a_plain_int(self):
        for bad in ("true", "2.0"):
            errs = self.qerrs("questions:\n  - {id: c1-q01, type: mcq, difficulty: %s}\n" % bad)
            self.assertTrue(has(errs, "difficulty must be"), bad)

    def test_frontmatter_shapes(self):
        errs, _ = run("---\n- a\n---\nteks\n")
        self.assertTrue(has(errs, "frontmatter must be a mapping"))
        errs, _ = run(lesson("blog", WORDS))
        self.assertTrue(has(errs, "`sources` must be a list"))
        errs, _ = run(lesson([["a"]], WORDS))
        self.assertTrue(has(errs, "`sources` must be a list"))
        errs, _ = run(lesson(["blog"], WORDS), misc="---\n- a\n---\n")
        self.assertTrue(has(errs, "frontmatter must be a mapping"))

    def test_non_kebab_heading_is_reported_not_ignored(self):
        bad = MISC.replace("## cache-free", "## Stale Read")
        errs, _ = run(lesson(["blog"], WORDS), misc=bad)
        self.assertTrue(has(errs, "must be kebab-case"))

    def test_labels_inside_code_fence_do_not_count(self):
        bad = MISC.replace("**Kenapa keliru:** y\n\n## ttl", "```\n**Kenapa keliru:** y\n```\n\n## ttl", 1)
        errs, _ = run(lesson(["blog"], WORDS), misc=bad)
        self.assertTrue(has(errs, "missing the label **Kenapa keliru:**"))

    def test_without_concept_objective_bounds_are_skipped(self):
        errs, _ = run(lesson(["blog"], WORDS), [q(1, objective=9)], misc=MISC)
        self.assertFalse(has(errs, "objective must be"))


class WordCount(unittest.TestCase):
    def words(self, n, status="review"):
        text = " ".join(["kata"] * n) + "[^blog]"
        errs, _ = run(lesson(["blog"], text, status=status), misc=MISC)
        return has(errs, "lesson length")

    def test_boundaries(self):
        self.assertTrue(self.words(299))
        self.assertFalse(self.words(300))
        self.assertFalse(self.words(600))
        self.assertTrue(self.words(601))

    def test_markers_and_urls_are_not_counted(self):
        text = " ".join(["kata"] * 300) + " https://example.com/a/b/c [^blog][^blog]"
        errs, _ = run(lesson(["blog"], text, status="review"), misc=MISC)
        self.assertFalse(has(errs, "lesson length"))


class OrderAnswers(unittest.TestCase):
    def test_duplicate_and_bool_indexes_rejected(self):
        for ans in ([0, 0, 1], [True, 1, 2], [0, 1, "2"]):
            errs, _ = run(lesson(["blog"], WORDS), [q(1, type="order", options=["a", "b", "c"], answer=ans)],
                          misc=MISC, concepts=CONCEPTS)
            self.assertTrue(has(errs, "order answer"), ans)


# ---------------------------------------------------------------- anti-leak and style heuristics (P1-031)
def mq(i, opts, answer, prompt="Mana yang benar tentang topik ini?", **kw):
    return q(i, options=opts, answer=answer, prompt=prompt, **kw)


def leak_warnings(qs, body=WORDS):
    _, warns = run(lesson(["blog"], body), qs, misc=MISC, concepts=CONCEPTS)
    return warns


BALANCED = [["alpha satu", "beta dua", "gamma tiga"]]


class AntiLeak(unittest.TestCase):
    def test_clean_set_has_no_leak_warnings(self):
        qs = [mq(i, ["alpha satu", "beta dua", "gamma tiga"], i % 3, difficulty=1 + i % 3) for i in range(1, 7)]
        self.assertFalse(has(leak_warnings(qs), "anti-leak"))

    def test_longest_correct_option(self):
        qs = [mq(i, ["pendek", "juga pendek", "jawaban benar yang jauh lebih panjang"], 2) for i in range(1, 6)]
        self.assertTrue(has(leak_warnings(qs), "is the longest in"))

    def test_answer_position_bias(self):
        qs = [mq(i, ["alpha satu", "beta dua", "gamma tiga"], 1, difficulty=1 + i % 3) for i in range(1, 6)]
        w = leak_warnings(qs)
        self.assertTrue(has(w, "is option 2 in 5/5"))

    def test_prompt_echo(self):
        qs = [mq(i, ["menggabungkan permintaan serupa", "mempercepat jaringan", "menambah disk"], 0,
                 prompt="Apa fungsi menggabungkan permintaan serupa pada cache?", difficulty=1 + i % 3)
              for i in range(1, 6)]
        self.assertTrue(has(leak_warnings(qs), "repeats the most words from the prompt"))

    def test_absolute_words_only_in_wrong_options(self):
        qs = [mq(i, ["bergantung pada beban", "selalu lebih cepat", "tidak pernah berguna"], 0,
                 difficulty=1 + i % 3) for i in range(1, 6)]
        self.assertTrue(has(leak_warnings(qs), "absolute words"))

    def test_escape_hatch_option(self):
        qs = [mq(1, ["alpha satu", "beta dua", "semua jawaban benar"], 2)]
        self.assertTrue(has(leak_warnings(qs), "avoid 'semua jawaban benar'"))
        qs = [mq(1, ["alpha satu", "beta dua", "A dan B benar"], 2)]
        self.assertTrue(has(leak_warnings(qs), "avoid 'semua jawaban benar'"))

    def test_long_explanation(self):
        qs = [mq(1, ["alpha satu", "beta dua", "gamma tiga"], 0, explanation="Satu. Dua. Tiga. Empat.")]
        self.assertTrue(has(leak_warnings(qs), "explanations longer than 3"))
        qs = [mq(1, ["alpha satu", "beta dua", "gamma tiga"], 0, explanation="Hanya satu. Dua kalimat.")]
        self.assertFalse(has(leak_warnings(qs), "explanations longer"))

    def test_difficulty_mix(self):
        qs = [mq(i, ["alpha satu", "beta dua", "gamma tiga"], i % 3, difficulty=2) for i in range(1, 6)]
        self.assertTrue(has(leak_warnings(qs), "use a mix of levels"))

    def test_heuristics_need_enough_mcq(self):
        qs = [mq(i, ["pendek", "juga pendek", "jawaban benar yang jauh lebih panjang"], 2, difficulty=1 + i % 3)
              for i in range(1, 4)]
        self.assertFalse(has(leak_warnings(qs), "is the longest in"))

    def test_heuristics_are_warnings_only(self):
        qs = [mq(i, ["pendek", "juga pendek", "jawaban benar yang jauh lebih panjang"], 2) for i in range(1, 6)]
        errs, _ = run(lesson(["blog"], WORDS), qs, misc=MISC, concepts=CONCEPTS)
        self.assertFalse(has(errs, "anti-leak"))


class LessonStyle(unittest.TestCase):
    def style(self, text):
        _, warns = run(lesson(["blog"], text))
        return warns

    def test_announcing_opener(self):
        self.assertTrue(has(self.style("Pada lesson ini kita akan membahas retry. " + WORDS), "core point"))
        self.assertFalse(has(self.style("Retry yang serentak membanjiri server. " + WORDS), "core point"))

    def test_filler_phrases(self):
        self.assertTrue(has(self.style("Caching sangat penting di era modern. " + WORDS), "filler phrases"))
        self.assertFalse(has(self.style("Cache menyimpan hasil bacaan. " + WORDS), "filler phrases"))

    def test_emoji(self):
        self.assertTrue(has(self.style("Cache itu cepat \U0001F680 sekali. " + WORDS), "no emoji"))

    def test_style_ignores_code_fences(self):
        self.assertFalse(has(self.style("Cache cepat.\n```\nsangat penting\n```\n" + WORDS), "filler phrases"))


class ReviewFixes(unittest.TestCase):
    """Regressions found in the P1-031 review."""

    def test_non_iterable_options_do_not_crash(self):
        for bad in ("5", "true", "abc"):
            run(lesson(["blog"], WORDS), [q(1, type="multi", options=yaml.safe_load(bad), answer=[0])],
                misc=MISC, concepts=CONCEPTS)

    def test_abbreviations_do_not_end_a_sentence(self):
        qs = [mq(1, ["alpha satu", "beta dua", "gamma tiga"], 0, explanation="Mis. cache, dst. lalu x. Ok.")]
        self.assertFalse(has(leak_warnings(qs), "explanations longer"))

    def test_unterminated_last_sentence_counts(self):
        qs = [mq(1, ["alpha satu", "beta dua", "gamma tiga"], 0, explanation="Satu. Dua. Tiga. Empat")]
        self.assertTrue(has(leak_warnings(qs), "explanations longer"))

    def test_check_marks_are_not_emoji(self):
        _, warns = run(lesson(["blog"], "Cache cepat ✓ tapi basi ✗. " + WORDS))
        self.assertFalse(has(warns, "no emoji"))

    def test_semua_alone_is_not_an_absolute_leak(self):
        qs = [mq(i, ["Semua request lewat satu node", "bergantung pada beban", "dibagi per shard"], 1,
                 difficulty=1 + i % 3) for i in range(1, 6)]
        self.assertFalse(has(leak_warnings(qs), "absolute words"))

    def test_lowercase_letters_are_not_a_combo_option(self):
        qs = [mq(1, ["alpha satu", "beta dua", "memakai a dan c keduanya"], 0)]
        self.assertFalse(has(leak_warnings(qs), "avoid 'semua jawaban benar'"))

    def test_quoted_or_coded_filler_is_a_mention(self):
        for text in ('Hindari kata "sangat penting" di lesson. ', "Hindari `sangat penting` di lesson. "):
            _, warns = run(lesson(["blog"], text + WORDS))
            self.assertFalse(has(warns, "filler phrases"), text)

    def test_word_boundary_and_heading_before_opener(self):
        _, warns = run(lesson(["blog"], "Cache sangat pentingnya bagi hasil. " + WORDS))
        self.assertFalse(has(warns, "filler phrases"))
        _, warns = run(lesson(["blog"], "# Judul\n\nPada lesson ini kita bahas cache. " + WORDS))
        self.assertTrue(has(warns, "core point"))
        _, warns = run(lesson(["blog"], "Kali ini kita bahas cache. " + WORDS))
        self.assertTrue(has(warns, "core point"))

    def test_position_check_needs_five_mcq(self):
        qs = [mq(i, ["alpha satu", "beta dua", "gamma tiga"], 1, difficulty=1 + i % 3) for i in range(1, 5)]
        self.assertFalse(has(leak_warnings(qs), "vary the position"))

    def test_difficulty_mix_ignores_unrated_questions(self):
        qs = [mq(i, ["alpha satu", "beta dua", "gamma tiga"], i % 3, difficulty=1) for i in range(1, 4)]
        qs.append(mq(4, ["alpha satu", "beta dua", "gamma tiga"], 0, difficulty=7))
        self.assertFalse(has(leak_warnings(qs), "use a mix of levels"))

    def test_stopwords_do_not_count_as_echo(self):
        qs = [mq(i, ["dengan caranya", "beta dua", "gamma tiga"], 0, prompt="Manakah yang dengan karena adalah?",
                 difficulty=1 + i % 3) for i in range(1, 6)]
        self.assertFalse(has(leak_warnings(qs), "repeats the most words"))


class Provenance(unittest.TestCase):
    PHRASES = ["menurut Azure, urutan ini penting", "Azure menyebut urutan ini penting", "Ini penalaran penulis.",
               "Ini hitungan sendiri.", "Asumsi buatan sendiri: 10 ms.", "Itu bukan fakta dari sumber.",
               "Catatan: ini bukan klaim.", "Sumbernya tidak membahas ini."]

    def test_lesson_phrases_warn(self):
        for ph in self.PHRASES:
            _, warns = run(lesson(["blog"], ph + " " + WORDS))
            self.assertTrue(has(warns, "do not narrate provenance"), ph)

    def test_plain_statements_do_not_warn(self):
        for ph in ["Misalkan 2.000 bacaan per detik.", "Data sensitif ambil dari sumber utamanya.",
                   "Cache lebih cepat daripada sumber aslinya.", "Urutan ini penting.[^blog]"]:
            _, warns = run(lesson(["blog"], ph + " " + WORDS))
            self.assertFalse(has(warns, "do not narrate provenance"), ph)

    def test_question_and_misconception_text_warn(self):
        _, warns = run(lesson(["blog"], WORDS), [q(1, explanation="Hitungan sendiri: 5 kali.")],
                       misc=MISC, concepts=CONCEPTS)
        self.assertTrue(has(warns, "c1-q01 explanation: do not narrate"))
        _, warns = run(lesson(["blog"], WORDS), misc=MISC.replace("x\n\n**Kenapa", "Menurut sumber, x\n\n**Kenapa", 1))
        self.assertTrue(has(warns, "misconceptions: do not narrate"))

    def test_quoted_phrase_in_lesson_is_a_mention(self):
        _, warns = run(lesson(["blog"], 'Jangan menulis "penalaran penulis" di teks. ' + WORDS))
        self.assertFalse(has(warns, "do not narrate provenance"))
