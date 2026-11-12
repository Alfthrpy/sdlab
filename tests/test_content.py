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


def run(text, questions=None, status_published=False):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        cdir = root / "concepts" / "c1"
        cdir.mkdir(parents=True)
        (cdir / "lesson.md").write_text(text, encoding="utf-8")
        if questions is not None:
            (cdir / "questions.yaml").write_text(yaml.safe_dump({"questions": questions}))
        old = (validate.CONTENT, validate.rel)
        validate.CONTENT, validate.rel = root, lambda p: p.name
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_content(REG, {})
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
        errs, warns = run_with(reg, sample + "\n")
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
