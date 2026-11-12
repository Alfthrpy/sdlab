"""Fixture tests for the registry rules in scripts/validate.py.

Run: python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate  # noqa: E402

BASE = dict(
    title="T", url="https://example.com", accessed="2026-11-12", type="article", tier=2,
    license="all-rights-reserved", usage="rewrite-only", access="free", status="candidate",
)
OPEN = dict(BASE, id="open-src", type="repo", tier=5, license="CC-BY-4.0", usage="adapt-with-attribution",
            status="approved", authors=["A"], published="2020", units=[1], topics=["caching"])


def run(entries):
    """Validate a registry made of `entries`; return (errors, warnings) as plain strings."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "registry.yaml"
        path.write_text(yaml.safe_dump({"sources": entries}))
        old = (validate.REGISTRY, validate.rel)
        validate.REGISTRY, validate.rel = path, lambda p: "registry.yaml"
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_registry()
            return list(validate.errors), list(validate.warnings)
        finally:
            validate.REGISTRY, validate.rel = old


def entry(**kw):
    return dict(BASE, id=kw.pop("id", "src"), **kw)


class Registry(unittest.TestCase):
    def assertErr(self, entries, text):
        errs, _ = run(entries)
        self.assertTrue(any(text in e for e in errs), f"{text!r} not in {errs}")

    def assertClean(self, entries):
        self.assertEqual(run(entries), ([], []))

    def test_diverse_approved_entries_pass(self):
        approved = dict(authors=["A"], published="2020", units=[1], topics=["x"], status="approved")
        self.assertClean([
            OPEN,
            entry(id="book", type="book", tier=1, edition="2", access="paywalled",
                  free_companion=["open-src"], **approved),
            entry(id="paper", type="paper", tier=3, doi="10.1145/3713082.3730380", access="partial", **approved),
            entry(id="pm", type="postmortem", tier=4, authors=[], status="approved", units=[6], topics=["dns"],
                  notes="NO-AUTHOR: corporate postmortem", published="2025-10"),
            entry(id="t6", type="course", tier=6, usage="map-only", access="paywalled",
                  free_companion=["open-src"], **approved),
        ])

    def test_bad_id_and_unknown_field(self):
        self.assertErr([entry(id="Bad_ID")], "kebab-case")
        self.assertErr([entry(licence="x")], "did you mean 'license'")

    def test_enums_and_tier(self):
        self.assertErr([entry(tier=7)], "tier")
        self.assertErr([entry(tier=True)], "tier")
        self.assertErr([entry(license="GPL")], "license")

    def test_usage_rules(self):
        self.assertErr([entry(usage="adapt-with-attribution")], "open license")
        self.assertErr([entry(tier=6, usage="rewrite-only")], "tier 6")

    def test_dates_and_doi(self):
        self.assertErr([entry(accessed="2026-11")], "valid full date")
        self.assertErr([entry(accessed="2026-13-45")], "valid full date")
        self.assertErr([entry(accessed="2999-01-01")], "future")
        self.assertErr([entry(published="2026-99")], "published")
        self.assertErr([entry(doi="https://doi.org/10.1/x")], "bare DOI")

    def test_approved_rules(self):
        base = dict(status="approved", authors=["A"], published="2020", units=[1], topics=["x"])
        self.assertErr([entry(**dict(base, license="unknown"))], "unknown")
        self.assertErr([entry(**dict(base, notes="SEED. check"))], "SEED")
        self.assertErr([entry(**dict(base, authors=[]))], "NO-AUTHOR")
        self.assertErr([entry(**dict(base, published=""))], "NO-DATE")
        self.assertErr([entry(**dict(base, units=[]))], "units")
        self.assertErr([entry(**dict(base, topics=[]))], "topics")
        self.assertErr([entry(**dict(base, access="paywalled"))], "free_companion")
        self.assertErr([entry(**dict(base, authors=[], notes="x"))], "NO-AUTHOR")  # vague notes are not enough
        self.assertClean([entry(**dict(base, notes="Seeds of the idea"))])  # only the standalone word SEED trips

    def test_free_companion(self):
        self.assertErr([entry(free_companion=["ghost"])], "unknown source id")
        self.assertErr([entry(free_companion=["src"])], "itself")
        self.assertErr([entry(id="a", access="paywalled"), entry(id="b", free_companion=["a"])], "must have access 'free'")
        self.assertErr([entry(free_companion="abc")], "list of non-empty strings")
        self.assertErr([entry(free_companion=[{"a": 1}])], "list of non-empty strings")

    def test_superseded_by(self):
        self.assertErr([entry(superseded_by="src")], "only valid")
        self.assertErr([entry(status="deprecated", superseded_by="src")], "itself")
        self.assertErr([entry(status="deprecated", superseded_by="ghost")], "unknown source id")
        self.assertErr([entry(status="deprecated", superseded_by=["x"])], "single registry id")

    def test_malformed_input_does_not_crash(self):
        self.assertErr(["abc"], "mapping")
        self.assertErr([entry(title=["x"])], "title")
        self.assertErr([entry(units=[True])], "units")
        self.assertErr([entry(units=[1, 1])], "duplicate")
        self.assertErr([entry(topics=["Bad Topic"])], "kebab-case")

    def test_warnings(self):
        _, w = run([entry(type="postmortem", tier=2)])
        self.assertTrue(any("tier" in x for x in w))
        _, w = run([entry(type="paper", tier=3)])
        self.assertTrue(any("doi" in x for x in w))


if __name__ == "__main__":
    unittest.main()
