"""Fixture tests for concept rules (unit range, trigger) in scripts/validate.py.

Run: python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate  # noqa: E402


def run(concepts):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "concepts.yaml"
        path.write_text(yaml.safe_dump({"concepts": concepts}))
        old = (validate.CONCEPTS, validate.CASES, validate.rel)
        validate.CONCEPTS, validate.CASES = path, Path(d) / "none.yaml"
        validate.rel = lambda p: "concepts.yaml"
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_curriculum({})
            return list(validate.errors), list(validate.warnings)
        finally:
            validate.CONCEPTS, validate.CASES, validate.rel = old


def concept(**kw):
    return dict(dict(id="c1", unit=2, title="T", objectives=["Bisa x"], status="planned"), **kw)


class Concepts(unittest.TestCase):
    def test_unit_range_includes_zero(self):
        self.assertEqual(run([concept(unit=0)])[0], [])
        self.assertTrue(any("unit" in e for e in run([concept(unit=7)])[0]))
        self.assertTrue(any("unit" in e for e in run([concept(unit=True)])[0]))

    def test_trigger_warning_before_review(self):
        errs, warns = run([concept()])
        self.assertEqual(errs, [])
        self.assertTrue(any("trigger" in w for w in warns))

    def test_trigger_error_at_review(self):
        # review also needs >= 2 sources, so look for the trigger message specifically
        errs, _ = run([concept(status="review")])
        self.assertTrue(any("needs a trigger" in e for e in errs), errs)

    def test_unit_zero_trigger_optional(self):
        _, warns = run([concept(unit=0)])
        self.assertFalse(any("trigger" in w for w in warns))
        errs, _ = run([concept(unit=0, status="review")])
        self.assertFalse(any("trigger" in e for e in errs))

    def test_trigger_blank_and_unit_string(self):
        self.assertTrue(any("trigger must be" in e for e in run([concept(trigger="  ")])[0]))
        self.assertTrue(any("unit" in e for e in run([concept(unit="0")])[0]))

    def test_trigger_must_be_string(self):
        errs, _ = run([concept(trigger=["x"])])
        self.assertTrue(any("trigger must be" in e for e in errs), errs)
        _, warns = run([concept(trigger="Bacaan database mendominasi beban")])
        self.assertFalse(any("trigger" in w for w in warns))


if __name__ == "__main__":
    unittest.main()


class PrerequisiteGraph(unittest.TestCase):
    def test_cycle_and_unknown_id(self):
        errs, _ = run([concept(id="a", prerequisites=["b"]), concept(id="b", prerequisites=["a"])])
        self.assertTrue(any("cycle" in e for e in errs), errs)
        errs, _ = run([concept(id="a", prerequisites=["ghost"])])
        self.assertTrue(any("unknown prerequisite" in e for e in errs), errs)

    def test_prerequisite_in_later_unit(self):
        errs, _ = run([concept(id="a", unit=0), concept(id="b", unit=3, prerequisites=["a"]),
                       concept(id="c", unit=1, prerequisites=["b"])])
        self.assertTrue(any("later unit" in e for e in errs), errs)

    def test_unreachable_concept_warns_then_errors(self):
        _, warns = run([concept(id="a", unit=2)])
        self.assertTrue(any("no prerequisites" in w for w in warns), warns)
        errs, _ = run([concept(id="a", unit=2, status="review")])
        self.assertTrue(any("no prerequisites" in e for e in errs), errs)
        # Unit 0 may have roots
        _, warns = run([concept(id="a", unit=0)])
        self.assertFalse(any("no prerequisites" in w for w in warns), warns)

    def test_redundant_prerequisite_warns(self):
        _, warns = run([concept(id="a", unit=0), concept(id="b", unit=1, prerequisites=["a"]),
                        concept(id="c", unit=2, prerequisites=["a", "b"])])
        self.assertTrue(any("redundant prerequisite a" in w for w in warns), warns)
