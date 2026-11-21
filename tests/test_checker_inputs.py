"""Checkers must report bad input as a problem line, never crash."""
import shutil
import tempfile
import unittest
from pathlib import Path

import test_validate as tv
from test_loops_remaining import LoopCase, rewrite


class AgentEvalBadKey(LoopCase, unittest.TestCase):
    loop = "agent-eval-regression"

    def test_text_in_exact_key_is_a_problem(self):
        self.fails(lambda ws: rewrite(ws / "eval" / "answer_key.json", '"q01": 2694', '"q01": "2694"'),
                   "q01: answer key value must be a number")

    def test_text_in_tolerance_key_is_a_problem(self):
        self.fails(lambda ws: rewrite(ws / "eval" / "answer_key.json", '"q05": 18.4', '"q05": "18.4"'),
                   "q05: answer key value must be a number")


class DataQualityBadExpectations(LoopCase, unittest.TestCase):
    loop = "data-quality-watch"

    def exp(self, ws):
        return ws / "quality" / "expectations.json"

    def test_text_max_age_is_a_problem(self):
        self.fails(lambda ws: rewrite(self.exp(ws), '"max_age_hours": 26,\n      "min_rows": 900000', '"max_age_hours": "26",\n      "min_rows": 900000'),
                   "claims_feed: max_age_hours must be a number")

    def test_text_min_rows_is_a_problem(self):
        self.fails(lambda ws: rewrite(self.exp(ws), '"min_rows": 900000', '"min_rows": "900000"'),
                   "claims_feed: min_rows must be a number")

    def test_text_max_rows_is_a_problem(self):
        self.fails(lambda ws: rewrite(self.exp(ws), '"max_rows": 1100000', '"max_rows": null'),
                   "claims_feed: max_rows must be a number")

    def test_text_null_limit_is_a_problem(self):
        self.fails(lambda ws: rewrite(self.exp(ws), '"payer": 5.0', '"payer": "5%"'),
                   "claims_feed: max_null_pct for payer must be a number")


class DataQualityBadObserved(LoopCase, unittest.TestCase):
    loop = "data-quality-watch"

    def test_text_null_pct_is_a_problem(self):
        self.fails(lambda ws: rewrite(ws / "quality" / "observed.json", '"payer": ', '"payer": "x", "_old": '),
                   "no numeric null_pct for column payer")


class LogDates(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        tv.copy_scaffold(self.tmp)

    def row(self, date, review):
        log = self.tmp / "decisions" / "LOG.md"
        log.write_text(log.read_text() + f"| {date} | Ship | A. Person | Unknown | decided | {review} |  |\n")
        return tv.run_cli(self.tmp)

    def test_good_dates_pass(self):
        self.assertEqual(self.row("2026-01-05", "2026-03-01").returncode, 0)

    def test_unknown_review_date_passes(self):
        self.assertEqual(self.row("2026-01-05", "Unknown").returncode, 0)

    def test_bad_date_named(self):
        self.assertIn("row 3 date 'Jan 5' is not YYYY-MM-DD", self.row("Jan 5", "2026-03-01").stdout)

    def test_bad_review_date_named(self):
        self.assertIn("row 3 review date 'soon' is not YYYY-MM-DD or Unknown", self.row("2026-01-05", "soon").stdout)

    def test_empty_review_date_named(self):
        self.assertIn("row 3 review date '' is not YYYY-MM-DD or Unknown", self.row("2026-01-05", "").stdout)


if __name__ == "__main__":
    unittest.main()
