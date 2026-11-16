"""Fixture tests for lab specs and incident files in scripts/validate.py (check_labs).

Run: python -m unittest discover tests
"""
import copy
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate  # noqa: E402

REG = {
    "pm": {"type": "postmortem", "status": "approved", "usage": "rewrite-only"},
    "blog": {"type": "article", "status": "approved", "usage": "rewrite-only"},
    "map": {"type": "docs", "status": "approved", "usage": "map-only"},
}
CONCEPTS = {"c1": {"formats": ["lesson", "lab"], "status": "planned"}, "c2": {"formats": ["lesson"]}}

LAB = yaml.safe_load("""
id: c1-lab
concept: c1
contract_version: "0.1.0"
mode: tune
difficulty: 1
duration_min: 15
illustrative: false
title: Judul
goal: Turunkan beban database ke bawah 60% tanpa menambah koneksi.
topology:
  nodes:
    - {id: users, type: client, params: {timeout_ms: 2000}}
    - {id: cache, type: cache, params: {capacity_pct: 0, ttl_s: 30}}
    - {id: db, type: db, params: {pool: 4}}
  edges: [[users, cache], [cache, db]]
traffic: {read_share: 0.9, schedule: [{at_s: 0, rate: 80}, {at_s: 120, rate: 160}]}
allowed_edits:
  - {node: cache, param: capacity_pct, min: 0, max: 50}
  - {node: cache, param: ttl_s, min: 0, max: 600}
targets:
  - {id: db-load, metric: utilization, node: db, window: {from_s: 180, to_s: 600}, aggregate: mean, op: "<=",
     value: 0.6, feedback_fail: gagal, feedback_pass: lulus}
structural_rules:
  - {id: pool-tetap, predicate: param-unchanged, args: {node: db, param: pool}, feedback_fail: gagal, feedback_pass: lulus}
  - {id: memori, predicate: param-range, args: {node: cache, param: capacity_pct, max: 25}, feedback_fail: gagal,
     feedback_pass: lulus}
hints:
  - {tier: 1, text: "Lihat grafik utilisasi."}
  - {tier: 2, text: "Perhatikan bacaan yang berulang."}
  - {tier: 3, text: "Kunci populer terbuang terlalu cepat."}
reference_solution:
  - {node: cache, param: capacity_pct, value: 20}
  - {node: cache, param: ttl_s, value: 300}
wrong_answers:
  - {edits: [{node: cache, param: ttl_s, value: 600}], reason: "kosong"}
  - {edits: [{node: cache, param: capacity_pct, value: 50}], brute_force: true, reason: "melanggar batas"}
debrief: Penjelasan setelah lulus.
sources: [blog]
""")


def run(spec, name="lab.yaml", folder="c1", concepts=CONCEPTS, raw=None):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        cdir = root / "concepts" / folder
        cdir.mkdir(parents=True)
        (cdir / name).write_text(raw if raw is not None else yaml.safe_dump(spec, allow_unicode=True, sort_keys=False),
                                encoding="utf-8")
        old = (validate.CONTENT, validate.rel, validate.CASES)
        validate.CONTENT, validate.rel = root, lambda p: p.name
        validate.CASES = root / "none.yaml"
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_labs(REG, concepts)
            return list(validate.errors), list(validate.warnings)
        finally:
            validate.CONTENT, validate.rel, validate.CASES = old


def has(msgs, text):
    return any(text in m for m in msgs)


def mod(**kw):
    s = copy.deepcopy(LAB)
    for k, v in kw.items():
        if v is None:
            s.pop(k, None)
        else:
            s[k] = v
    return s


class LabBasics(unittest.TestCase):
    def test_valid_lab(self):
        errs, warns = run(LAB)
        self.assertEqual(errs, [])
        self.assertFalse(has(warns, "lab.yaml"))

    def test_yaml_syntax_error_is_reported(self):
        errs, _ = run(None, raw="goal: a: b: c\n  bad: [\n")
        self.assertTrue(has(errs, "invalid YAML"))

    def test_not_a_mapping(self):
        errs, _ = run(None, raw="- a\n- b\n")
        self.assertTrue(has(errs, "must be a mapping"))

    def test_required_fields(self):
        for f in ("goal", "targets", "hints", "reference_solution", "wrong_answers", "debrief", "sources", "topology"):
            errs, _ = run(mod(**{f: None}))
            self.assertTrue(has(errs, f"`{f}` is missing"), f)

    def test_concept_rules(self):
        errs, _ = run(mod(concept="nope"))
        self.assertTrue(has(errs, "is not in curriculum/concepts.yaml"))
        errs, _ = run(mod(concept="c2"), folder="c2")
        self.assertEqual(errs, [])
        errs, warns = run(mod(concept="c2"), folder="c2")
        self.assertTrue(has(warns, "does not list `lab`"))
        errs, _ = run(LAB, folder="c2")
        self.assertTrue(has(errs, "lab in folder `c2` names concept `c1`"))

    def test_secondary_concepts_must_exist(self):
        errs, _ = run(mod(secondary_concepts=["zzz"]))
        self.assertTrue(has(errs, "secondary concept `zzz`"))

    def test_enums_and_versions(self):
        self.assertTrue(has(run(mod(mode="free"))[0], "mode must be one of"))
        self.assertTrue(has(run(mod(difficulty=4))[0], "difficulty must be"))
        self.assertTrue(has(run(mod(difficulty=True))[0], "difficulty must be"))
        self.assertTrue(has(run(mod(contract_version="1.0"))[0], "semver"))
        self.assertTrue(has(run(mod(id="Bad_ID"))[0], "id must be kebab-case"))

    def test_duration_warns_outside_target(self):
        errs, warns = run(mod(duration_min=45))
        self.assertEqual(errs, [])
        self.assertTrue(has(warns, "outside the 10-20 minute target"))
        self.assertTrue(has(run(mod(duration_min=-1))[0], "positive number"))

    def test_illustrative_needs_a_note(self):
        self.assertTrue(has(run(mod(illustrative=True))[0], "illustrative_note"))
        errs, _ = run(mod(illustrative=True, illustrative_note="Angka ini ilustrasi."))
        self.assertEqual(errs, [])

    def test_duplicate_lab_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "concepts" / "c1").mkdir(parents=True)
            for n in ("lab.yaml", "second.lab.yaml"):
                (root / "concepts" / "c1" / n).write_text(yaml.safe_dump(LAB), encoding="utf-8")
            old = (validate.CONTENT, validate.rel, validate.CASES)
            validate.CONTENT, validate.rel, validate.CASES = root, lambda p: p.name, root / "none.yaml"
            validate.errors.clear()
            try:
                validate.check_labs(REG, CONCEPTS)
                self.assertTrue(has(validate.errors, "duplicate lab id"))
            finally:
                validate.CONTENT, validate.rel, validate.CASES = old


class LabTopology(unittest.TestCase):
    def test_edge_to_unknown_node(self):
        s = mod()
        s["topology"]["edges"].append(["cache", "ghost"])
        self.assertTrue(has(run(s)[0], "unknown node: ghost"))

    def test_duplicate_and_bad_node_ids(self):
        s = mod()
        s["topology"]["nodes"].append({"id": "db", "type": "db"})
        self.assertTrue(has(run(s)[0], "duplicate node id"))
        s = mod()
        s["topology"]["nodes"][0]["id"] = "Users_1"
        self.assertTrue(has(run(s)[0], "kebab-case"))

    def test_edges_may_be_mappings(self):
        s = mod()
        s["topology"]["edges"] = [{"from": "users", "to": "cache", "policies": ["timeout"]}, ["cache", "db"]]
        self.assertEqual(run(s)[0], [])

    def test_traffic_rules(self):
        s = mod()
        s["traffic"]["schedule"] = [{"at_s": 120, "rate": 1}, {"at_s": 0, "rate": 1}]
        self.assertTrue(has(run(s)[0], "sorted by at_s"))
        s["traffic"]["schedule"] = []
        self.assertTrue(has(run(s)[0], "schedule"))
        s = mod()
        s["traffic"]["read_share"] = 1.5
        self.assertTrue(has(run(s)[0], "read_share"))


class LabModes(unittest.TestCase):
    def test_tune_needs_allowed_edits(self):
        self.assertTrue(has(run(mod(allowed_edits=None))[0], "needs `allowed_edits`"))

    def test_allowed_edit_checks(self):
        s = mod()
        s["allowed_edits"].append({"node": "cache", "param": "ghost", "min": 0, "max": 1})
        self.assertTrue(has(run(s)[0], "has no initial param `ghost`"))
        s = mod()
        s["allowed_edits"][0]["min"] = 99
        self.assertTrue(has(run(s)[0], "min <= max"))
        s = mod()
        s["allowed_edits"].append({"node": "ghost", "param": "x", "min": 0, "max": 1})
        self.assertTrue(has(run(s)[0], "unknown node: ghost"))

    def test_diagnose_needs_a_scenario(self):
        self.assertTrue(has(run(mod(mode="diagnose"))[0], "hidden scenario"))
        errs, _ = run(mod(mode="diagnose", scenarios=[{"id": "bad-deploy", "at_s": 60}]))
        self.assertEqual(errs, [])

    def test_build_needs_a_palette(self):
        self.assertTrue(has(run(mod(mode="build", allowed_edits=None))[0], "needs a `palette`"))
        errs, _ = run(mod(mode="build", allowed_edits=None, palette=[{"type": "cache", "max": 2}],
                          reference_solution=[{"node": "cache", "param": "x", "value": 1}]))
        self.assertFalse(has(errs, "palette"))


class LabGrading(unittest.TestCase):
    def test_feedback_required_and_ids_unique(self):
        s = mod()
        del s["targets"][0]["feedback_fail"]
        self.assertTrue(has(run(s)[0], "`feedback_fail` (Indonesian feedback) is required"))
        s = mod()
        s["structural_rules"][0]["id"] = "db-load"
        self.assertTrue(has(run(s)[0], "duplicate grading rule id"))

    def test_target_fields(self):
        s = mod()
        s["targets"][0].update(aggregate="median", op="!=", value="x", window={"from_s": 9, "to_s": 1})
        errs, _ = run(s)
        for text in ("aggregate must be", "op must be", "value must be a number", "from_s < to_s"):
            self.assertTrue(has(errs, text), text)

    def test_latency_target_needs_an_error_or_goodput_target(self):
        s = mod()
        s["targets"][0]["metric"] = "latency_p99_ms"
        self.assertTrue(has(run(s)[0], "must be paired with an error_rate or goodput_rps"))
        s["targets"].append(dict(s["targets"][0], id="ok", metric="error_rate"))
        self.assertEqual(run(s)[0], [])

    def test_predicate_must_be_known(self):
        s = mod()
        s["structural_rules"][0]["predicate"] = "magic"
        self.assertTrue(has(run(s)[0], "predicate must be one of"))

    def test_hints_cover_three_tiers(self):
        s = mod()
        s["hints"] = s["hints"][:2]
        self.assertTrue(has(run(s)[0], "tiers 1, 2 and 3"))


class LabSolutions(unittest.TestCase):
    def test_reference_edit_must_be_allowed(self):
        s = mod()
        s["reference_solution"].append({"node": "db", "param": "pool", "value": 8})
        self.assertTrue(has(run(s)[0], "db.pool is not in allowed_edits"))

    def test_reference_value_must_be_in_range(self):
        s = mod()
        s["reference_solution"][1]["value"] = 9999
        self.assertTrue(has(run(s)[0], "outside its allowed range"))

    def test_reference_must_not_break_structural_rules(self):
        s = mod()
        s["reference_solution"][0]["value"] = 40      # memori rule: capacity_pct max 25
        self.assertTrue(has(run(s)[0], "breaks rule memori"))
        s = mod()
        s["allowed_edits"].append({"node": "db", "param": "pool", "min": 1, "max": 9})
        s["reference_solution"].append({"node": "db", "param": "pool", "value": 8})
        self.assertTrue(has(run(s)[0], "keeps unchanged"))

    def test_wrong_answers_required_with_reason(self):
        s = mod(wrong_answers=[{"edits": [{"node": "cache", "param": "ttl_s", "value": 1}]}])
        self.assertTrue(has(run(s)[0], "needs `edits` and a `reason`"))

    def test_brute_force_entry_or_waiver(self):
        s = mod()
        s["wrong_answers"][1].pop("brute_force")
        self.assertTrue(has(run(s)[0], "brute_force: true"))
        s["brute_force_ok"] = "Tidak ada jalan pintas; tiap nilai berbahaya."
        self.assertEqual(run(s)[0], [])

    def test_wrong_answer_edits_checked_against_allowed_edits(self):
        s = mod()
        s["wrong_answers"][0]["edits"][0]["value"] = 99999
        self.assertTrue(has(run(s)[0], "wrong_answers[0]"))


class LabAntiLeak(unittest.TestCase):
    def test_goal_must_not_contain_a_reference_value(self):
        s = mod(goal="Pasang cache dengan TTL 300 detik untuk menurunkan beban.")
        self.assertTrue(has(run(s)[0], "goal contains the reference value 300"))

    def test_tier_1_and_2_hints_must_not_contain_values_but_tier_3_may_name_mechanism(self):
        s = mod()
        s["hints"][1]["text"] = "Coba kapasitas 20 persen."
        self.assertTrue(has(run(s)[0], "hint tier 2 contains the reference value 20"))
        s = mod()
        s["hints"][2]["text"] = "TTL 300 cukup lama."
        self.assertFalse(has(run(s)[0], "anti-leak"))

    def test_numbers_inside_other_numbers_are_not_matches(self):
        s = mod(goal="Turunkan beban di bawah 60% pada 3000 request per detik tanpa 1200 error.")
        self.assertFalse(has(run(s)[0], "anti-leak"))

    def test_component_name_in_a_hint_warns(self):
        s = mod()
        s["hints"][0]["text"] = "Lihat metrik cache saat jam ramai."
        errs, warns = run(s)
        self.assertEqual(errs, [])
        self.assertTrue(has(warns, "names the component `cache`"))


class LabSources(unittest.TestCase):
    def test_sources_must_be_in_the_registry_and_not_map_only(self):
        self.assertTrue(has(run(mod(sources=["ghost"]))[0], "source not in registry"))
        self.assertTrue(has(run(mod(sources=["map"]))[0], "map-only"))
        self.assertTrue(has(run(mod(sources="blog"))[0], "sources must be a list"))


class ConceptsWithLabs(unittest.TestCase):
    def test_review_concept_without_lab_is_an_error(self):
        concepts = {"c1": {"formats": ["lab"], "status": "review"}, "c3": {"formats": ["lab"], "status": "planned"}}
        errs, warns = run(mod(concept="c1"), concepts=concepts)
        self.assertEqual(errs, [])
        self.assertTrue(has(warns, "1 concepts list `lab`"))
        concepts["c3"]["status"] = "review"
        errs, _ = run(mod(concept="c1"), concepts=concepts)
        self.assertTrue(has(errs, "no lab spec: c3"))


INCIDENT = """---
id: inc-one
title: Insiden satu
date: 2025-06-12
sources: [pm]
concepts: [c1]
modelability: modeled
sim_spec: %s
sim_scenarios: [restart-herd]
---

## Ringkasan

Teks.[^pm]

## Kronologi

Teks.

## Mekanisme kegagalan

Teks.

## Skenario untuk pemain

Teks.

## Pembahasan

Teks.
"""


def run_incident(text, items=None, name="inc-one.md", with_spec=True):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "incidents").mkdir()
        spec = root / "incidents" / "inc-one.lab.yaml"
        if with_spec:
            diag = dict(copy.deepcopy(LAB), mode="diagnose", scenarios=[{"id": "restart-herd", "at_s": 60}])
            spec.write_text(yaml.safe_dump(diag), encoding="utf-8")
        (root / "incidents" / name).write_text(text % str(spec) if "%s" in text else text, encoding="utf-8")
        cases = root / "cases.yaml"
        cases.write_text(yaml.safe_dump({"items": items or [{"id": "inc-one", "kind": "incident"}]}), encoding="utf-8")
        old = (validate.CONTENT, validate.rel, validate.CASES, validate.ROOT)
        validate.CONTENT, validate.rel, validate.CASES, validate.ROOT = root, lambda p: p.name, cases, Path("/")
        validate.errors.clear()
        validate.warnings.clear()
        try:
            validate.check_labs(REG, CONCEPTS)
            return list(validate.errors), list(validate.warnings)
        finally:
            validate.CONTENT, validate.rel, validate.CASES, validate.ROOT = old


class Incidents(unittest.TestCase):
    def test_valid_incident(self):
        errs, _ = run_incident(INCIDENT)
        self.assertFalse(any("inc-one.md" in e for e in errs), errs)

    def test_id_must_match_file_and_fields_required(self):
        errs, _ = run_incident(INCIDENT.replace("id: inc-one", "id: other"))
        self.assertTrue(has(errs, "must equal the file name"))
        errs, _ = run_incident(INCIDENT.replace("date: 2025-06-12\n", ""))
        self.assertTrue(has(errs, "`date` is required"))
        errs, _ = run_incident(INCIDENT.replace("2025-06-12", "12 Juni 2025"))
        self.assertTrue(has(errs, "YYYY-MM-DD"))

    def test_needs_a_postmortem_source_and_known_concepts(self):
        errs, _ = run_incident(INCIDENT.replace("sources: [pm]", "sources: [blog]").replace("[^pm]", ""))
        self.assertTrue(has(errs, "needs a source of type postmortem"))
        errs, _ = run_incident(INCIDENT.replace("concepts: [c1]", "concepts: [zzz]"))
        self.assertTrue(has(errs, "unknown concept: zzz"))

    def test_modelability_rules(self):
        errs, _ = run_incident(INCIDENT.replace("modelability: modeled", "modelability: maybe"))
        self.assertTrue(has(errs, "modelability must be one of"))
        errs, _ = run_incident(INCIDENT.replace("sim_scenarios: [restart-herd]\n", ""))
        self.assertTrue(has(errs, "sim_scenarios"))
        errs, _ = run_incident(INCIDENT.replace("sim_spec: %s\n", ""))
        self.assertTrue(has(errs, "sim_spec"))
        errs, _ = run_incident(INCIDENT.replace("sim_spec: %s", "sim_spec: nowhere/x.lab.yaml"))
        self.assertTrue(has(errs, "sim_spec does not exist"))

    def test_text_only_needs_no_spec(self):
        text = INCIDENT.replace("modelability: modeled", "modelability: text-only")
        text = text.replace("sim_spec: %s\n", "").replace("sim_scenarios: [restart-herd]\n", "")
        errs, warns = run_incident(text)
        self.assertFalse(any("inc-one.md" in e for e in errs), errs)

    def test_sections_required_and_ordered(self):
        errs, _ = run_incident(INCIDENT.replace("## Kronologi", "## Lain"))
        self.assertTrue(has(errs, "missing section `## Kronologi`"))
        swapped = INCIDENT.replace("## Kronologi", "## TMP").replace("## Pembahasan", "## Kronologi").replace("## TMP", "## Pembahasan")
        errs, _ = run_incident(swapped)
        self.assertTrue(has(errs, "out of order"))

    def test_listed_in_case_studies(self):
        errs, _ = run_incident(INCIDENT, items=[{"id": "inc-one", "kind": "case-study"}])
        self.assertTrue(has(errs, "another kind"))
        _, warns = run_incident(INCIDENT, items=[{"id": "something-else", "kind": "incident"}])
        self.assertTrue(has(warns, "not listed in curriculum/case-studies.yaml"))

    def test_marker_must_be_in_sources(self):
        errs, _ = run_incident(INCIDENT.replace("Teks.[^pm]", "Teks.[^blog]"))
        self.assertTrue(has(errs, "[^blog] is not in frontmatter sources"))

    def test_missing_frontmatter(self):
        errs, _ = run_incident("tanpa frontmatter\n")
        self.assertTrue(has(errs, "frontmatter missing"))


class Templates(unittest.TestCase):
    def test_lab_template_passes_the_validator(self):
        template = Path(__file__).resolve().parent.parent / "templates" / "concept" / "lab.yaml"
        reg = dict(REG, **{"registry-id": REG["blog"]})
        concepts = {"concept-id": {"formats": ["lab"], "status": "planned"}}
        old_reg = REG.copy()
        REG.update(reg)
        try:
            errs, _ = run(None, folder="concept-id", concepts=concepts, raw=template.read_text(encoding="utf-8"))
        finally:
            REG.clear()
            REG.update(old_reg)
        self.assertEqual(errs, [])


if __name__ == "__main__":
    unittest.main()
