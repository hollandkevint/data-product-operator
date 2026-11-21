import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRADER = REPO / "grader"
VALIDATE = REPO / ".claude" / "skills" / "dpm-os" / "scaffold" / "scripts" / "validate.py"

sys.path.insert(0, str(GRADER))
import data  # noqa: E402
import grade  # noqa: E402

HAS_DUCKDB = importlib.util.find_spec("duckdb") is not None
HAS_DATA = HAS_DUCKDB and data.DB.is_file()
NEEDS_DATA = "needs duckdb and grader/.data/ (run: python3 grader/data.py)"


class GraderShapeTests(unittest.TestCase):
    def test_question_count_and_ids(self):
        ids = [q["id"] for q in grade.questions()]
        self.assertTrue(25 <= len(ids) <= 30)
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_question_has_key_sql_and_committed_answer(self):
        key = grade.answer_key()
        for q in grade.questions():
            self.assertTrue((grade.KEY_DIR / f"{q['id']}.sql").is_file(), q["id"])
            self.assertIn(q["id"], key)
            self.assertIsNotNone(key[q["id"]], q["id"])

    def test_every_question_has_a_scoring_rule(self):
        for q in grade.questions():
            self.assertIn(q["scoring"]["type"], {"exact", "tolerance"}, q["id"])

    def test_base_answers_every_question(self):
        files = grade.resolve("base")
        for q in grade.questions():
            self.assertIn(f"sql/{q['id']}.sql", files)

    def test_specialized_harness_inherits_and_overrides(self):
        files = grade.resolve("cohorts")
        self.assertEqual(grade.owner("cohorts", "definitions/20_condition_records.sql"), "cohorts")
        self.assertEqual(grade.owner("cohorts", "sql/q09.sql"), "base")
        self.assertEqual(grade.owner("cohorts", "context/strategy.md"), "scaffold")
        self.assertEqual(files["sql/q09.sql"], grade.HARNESSES / "base" / "sql" / "q09.sql")

    def test_specialized_harnesses_declare_a_real_slice(self):
        for name in grade.all_harnesses()[1:]:
            meta = grade.harness_meta(name)
            self.assertEqual(meta["parent"], "base")
            self.assertTrue(grade.slice_ids(meta["slice"]))

    def test_materialized_harness_is_a_valid_dpm_os_instance(self):
        for name in grade.all_harnesses():
            with tempfile.TemporaryDirectory() as d:
                dest = grade.materialize(name, Path(d) / name)
                r = subprocess.run([sys.executable, str(VALIDATE), str(dest)], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, f"{name}: {r.stdout}")
                self.assertTrue((dest / "GRADER_TASK.md").is_file())


class ScoringTests(unittest.TestCase):
    def test_exact(self):
        self.assertTrue(grade.correct(10, 10, {"type": "exact"}))
        self.assertFalse(grade.correct(10.5, 10, {"type": "exact"}))
        self.assertFalse(grade.correct(None, 10, {"type": "exact"}))

    def test_tolerance(self):
        rule = {"type": "tolerance", "abs": 0.1}
        self.assertTrue(grade.correct(50.05, 50.0, rule))
        self.assertFalse(grade.correct(50.2, 50.0, rule))


class ShipRuleTests(unittest.TestCase):
    BASE = {"a": True, "b": False, "c": True, "d": False}

    def test_ships_when_slice_improves_and_nothing_breaks(self):
        v = grade.ship_verdict(self.BASE, {"a": True, "b": True, "c": True, "d": False}, ["a", "b"])
        self.assertTrue(v["ship"])
        self.assertEqual(v["fixed"], ["b"])

    def test_rejects_a_regression_outside_the_slice(self):
        v = grade.ship_verdict(self.BASE, {"a": True, "b": True, "c": False, "d": False}, ["a", "b"])
        self.assertFalse(v["ship"])
        self.assertEqual(v["regressions"], ["c"])

    def test_rejects_a_regression_inside_the_slice_even_with_a_net_gain(self):
        base = {"a": True, "b": False, "e": False}
        v = grade.ship_verdict(base, {"a": False, "b": True, "e": True}, ["a", "b", "e"])
        self.assertFalse(v["ship"])

    def test_rejects_no_improvement(self):
        v = grade.ship_verdict(self.BASE, dict(self.BASE), ["a", "b"])
        self.assertFalse(v["ship"])
        self.assertEqual(v["regressions"], [])


@unittest.skipUnless(HAS_DATA, NEEDS_DATA)
class EndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs = {n: grade.replay(n) for n in grade.all_harnesses()}

    def test_committed_answer_key_matches_the_key_sql(self):
        self.assertEqual(grade.compute_key(), json.loads(grade.KEY_FILE.read_text()))

    def test_committed_run_log_matches_a_fresh_replay(self):
        self.assertEqual(grade.render_runs(self.runs), grade.RUNS_FILE.read_text())

    def test_no_harness_sql_errors(self):
        for name, results in self.runs.items():
            errors = {i: r["error"] for i, r in results.items() if r["error"]}
            self.assertEqual(errors, {}, name)

    def test_demo_verdicts(self):
        self.assertTrue(grade.verdict_for("cohorts", self.runs)["ship"])
        v = grade.verdict_for("utilization", self.runs)
        self.assertFalse(v["ship"])
        self.assertGreater(v["slice_candidate"], v["slice_base"])
        self.assertTrue(v["regressions"])

    def test_base_is_not_perfect(self):
        # A base that already passes everything leaves no room for the ship rule to say anything.
        passes = grade.score(self.runs["base"])
        self.assertLess(sum(passes.values()), len(passes))


if __name__ == "__main__":
    unittest.main()
