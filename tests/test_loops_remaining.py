"""Rule-by-rule checks for the four loops built after decision follow-up.

Each test breaks one rule in a copy of the loop's demo and requires the
checker to name the problem. A checker that passes everything fails these.
"""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_") + "_check", REPO / "skills" / name / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rewrite(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture setup: {old!r} not in {path}"
    path.write_text(text.replace(old, new), encoding="utf-8")


class LoopCase:
    loop = None

    def problems(self, mutate=None):
        c = load(self.loop)
        with tempfile.TemporaryDirectory() as t:
            ws = Path(t) / "ws"
            shutil.copytree(REPO / "skills" / self.loop / "demo", ws)
            if mutate:
                mutate(ws)
            return "\n".join(c.check(ws))

    def out(self, ws):
        return ws / "loops" / self.loop / "2026-11-21.md"

    def state(self, ws):
        return ws / "loops" / self.loop / "state.json"

    def fails(self, mutate, expect):
        self.assertIn(expect, self.problems(mutate))

    def test_demo_is_clean(self):
        self.assertEqual(self.problems(), "")


class WeeklyMetricReview(LoopCase, unittest.TestCase):
    loop = "weekly-metric-review"

    def test_big_move_called_steady_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| 50.0 | unexplained |", "| 50.0 | steady |"), "cannot be steady")

    def test_quiet_metric_called_explained_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| 3.3 | steady |", "| 3.3 | explained |"), "status must be steady")

    def test_wrong_change_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| -22.5 |", "| -12.5 |"), "should be -22.5")

    def test_value_differs_from_data_fails(self):
        self.fails(lambda ws: rewrite(ws / "metrics" / "values.csv", "Rows loaded,2026-11-16,1500000", "Rows loaded,2026-11-16,1100000"),
                   "differs from values.csv")

    def test_explained_without_tag_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "`(stakeholder-verbal, Ana Reyes, 2026-11-19)`", "Unknown"),
                   "needs a provenance-tagged cause")

    def test_unexplained_without_owner_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Ana Reyes checks the load log", "Someone checks the load log"),
                   "must name its owner Ana Reyes")

    def test_unexplained_without_date_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "by 2026-11-24", "soon"), "needs a check date")

    def test_missing_metric_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| Median query seconds | 2.0 | 2.1 | 5.0 | steady | Inside the 25% threshold. | - | None. |\n", ""),
                   "defined but missing")

    def test_invented_metric_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| Rows loaded |", "| Rows invented |"), "invented metric")

    def test_state_drift_fails(self):
        self.fails(lambda ws: rewrite(self.state(ws), '"unexplained": [\n    "Rows loaded"\n  ]', '"unexplained": []'),
                   "unexplained does not match")

    def test_zero_baseline_needs_na(self):
        def zero(ws):
            rewrite(ws / "metrics" / "values.csv", "Rows loaded,2026-11-09,1000000", "Rows loaded,2026-11-09,0")
            rewrite(self.out(ws), "| 1000000 | 1500000 | 50.0 |", "| 0 | 1500000 | 50.0 |")
        self.fails(zero, "change must be 'n/a'")


class DataQualityWatch(LoopCase, unittest.TestCase):
    loop = "data-quality-watch"

    def obs(self, ws):
        return ws / "quality" / "observed.json"

    def test_stale_table_reported_passing_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| 40.0 h | fail |", "| 40.0 h | pass |"), "numbers say fail")

    def test_passing_check_reported_failing_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| 5.0 h | pass |", "| 5.0 h | fail |"), "numbers say pass")

    def test_report_number_differs_from_data_fails(self):
        self.fails(lambda ws: rewrite(self.obs(ws), '"rows": 1002345', '"rows": 410000'), "should be '410000 rows'")

    def test_volume_out_of_band_fails(self):
        self.fails(lambda ws: rewrite(self.obs(ws), '"rows": 1002345', '"rows": 410000'), "numbers say fail")

    def test_schema_drift_missed_fails(self):
        self.fails(lambda ws: rewrite(self.obs(ws), '"payer": "text"}\n    },\n    "consumer_queries"', '"payer": "int"}\n    },\n    "consumer_queries"'),
                   "payer text to int")

    def test_failure_without_owner_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Ana Reyes checks the payer mapping change by 2026-11-24.", "Look into it."),
                   "must name its owner Ana Reyes")

    def test_failure_without_date_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Marcus Webb restarts the query-log load by 2026-11-22.", "Marcus Webb restarts the query-log load."),
                   "needs a date after")

    def test_missing_check_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| consumer_queries | volume | 500 to 5000 rows | 2310 rows | pass | - |\n", ""),
                   "declared check is missing")

    def test_invented_check_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| claims_feed | volume |", "| claims_feed | latency |"), "not a declared check")

    def test_observed_on_wrong_day_fails(self):
        self.fails(lambda ws: rewrite(self.obs(ws), "2026-11-21T07:00:00Z", "2026-11-20T07:00:00Z"), "observed_at must be on the last_run date")

    def test_table_missing_from_observed_fails(self):
        def drop(ws):
            rewrite(ws / "quality" / "expectations.json", '"tables": {', '"tables": {"ghost_table": {"owner": "X", "max_age_hours": 1, "min_rows": 1, "max_rows": 2, "columns": {}},')
        self.fails(drop, "missing from observed.json")

    def test_state_drift_fails(self):
        self.fails(lambda ws: rewrite(self.state(ws), '"consumer_queries:schema"', '"consumer_queries:volume"'), "failing does not match")


class AgentEvalRegression(LoopCase, unittest.TestCase):
    loop = "agent-eval-regression"

    def out(self, ws):
        return ws / "loops" / self.loop / "2026-11-21.md"

    def cand(self, ws):
        return ws / "eval" / "runs" / "2026-11-21.json"

    def test_regression_called_pass_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Verdict: HOLD", "Verdict: PASS"), "verdict must be HOLD")

    def test_flat_total_does_not_hide_regression(self):
        # The demo totals are equal (8 and 8) and still hold.
        self.assertIn("| total | 10 | 8 | 8 |", (REPO / "skills" / self.loop / "demo" / "loops" / self.loop / "2026-11-21.md").read_text())
        self.fails(lambda ws: rewrite(self.out(ws), "Regressed: q03, q08", "Regressed: none"), "'Regressed:' must list ['q03', 'q08']")

    def test_no_regression_must_pass(self):
        def fixall(ws):
            rewrite(self.cand(ws), '"q03": 498', '"q03": 512')
            rewrite(self.cand(ws), '"q08": 1200000', '"q08": null')
        self.fails(fixall, "verdict must be PASS")

    def test_slice_score_wrong_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| counts | 4 | 4 | 3 |", "| counts | 4 | 4 | 4 |"), "rescoring gives")

    def test_tolerance_band_is_applied(self):
        # 18.45 vs key 18.4 is inside 0.1. 19.5 is outside, so the rates slice drops.
        self.fails(lambda ws: rewrite(self.cand(ws), '"q05": 18.4,', '"q05": 19.5,'), "slice 'rates' scores")

    def test_number_on_abstain_question_is_wrong(self):
        self.fails(lambda ws: rewrite(self.cand(ws), '"q10": null', '"q10": 7'), "slice 'abstain' scores")

    def test_missing_answer_is_wrong(self):
        self.fails(lambda ws: rewrite(self.cand(ws), '"q01": 2694,', ""), "slice 'counts' scores")

    def test_different_data_pin_fails(self):
        self.fails(lambda ws: rewrite(self.cand(ws), "2026-11-14", "2026-12-01"), "different data than the key")

    def test_hold_without_owner_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Next step: Priya Nair reads", "Next step: Someone reads"), "names the owner")

    def test_hold_without_date_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "decides by 2026-11-24", "decides soon"), "decision date after")

    def test_unknown_question_in_run_fails(self):
        self.fails(lambda ws: rewrite(self.cand(ws), '"q01": 2694,', '"q01": 2694, "q99": 1,'), "unknown question q99")

    def test_state_drift_fails(self):
        self.fails(lambda ws: rewrite(self.state(ws), '"verdict": "HOLD"', '"verdict": "PASS"'), "state.json: verdict")


class StrategyReview(LoopCase, unittest.TestCase):
    loop = "strategy-review"

    def test_input_must_name_the_decision_log(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Input: decisions/LOG.md", "Input: notes"), "must name decisions/LOG.md")

    def test_outcome_must_match_follow_up(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| Priya Nair | reverse |", "| Priya Nair | keep |"), "outcome 'keep' should be 'reverse'")

    def test_unreviewed_decision_is_not_given_an_outcome(self):
        def drop_followup(ws):
            rewrite(ws / "loops" / "decision-follow-up" / "2026-11-21.md", "| keep | Close.", "| keep | Close.")
            for f in (ws / "loops" / "decision-follow-up").iterdir():
                f.unlink()
        self.fails(drop_followup, "should be 'not-reviewed'")

    def test_missing_decision_fails(self):
        self.fails(lambda ws: rewrite(ws / "decisions" / "LOG.md", "| 2026-11-02 | Pause", "| 2026-09-30 | Pause"),
                   "decided in 2026-Q3 but missing")

    def test_pending_decision_in_review_fails(self):
        self.fails(lambda ws: rewrite(ws / "decisions" / "LOG.md", "decided | 2026-10-30", "pending | 2026-10-30"), "not a decided or superseded")

    def test_change_without_note_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| change | Priya Nair writes the superseding record with a new window. |", "| change | - |"),
                   "needs a note")

    def test_keep_against_reverse_needs_note(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| change | Priya Nair writes the superseding record with a new window. |", "| keep | - |"),
                   "'keep' against a reverse outcome")

    def test_superseded_note_must_name_replacement(self):
        self.fails(lambda ws: rewrite(self.out(ws), "Owned by 2026-08-04-friday-refresh.", "Replaced."), "must name the record that supersedes it")

    def test_bad_call_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| keep | - |", "| maybe | - |"), "operator call 'maybe'")

    def test_changed_question_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "| Keep, change or stop? | keep |", "| Anything to add? | keep |"), "question must be")

    def test_groups_line_wrong_fails(self):
        self.fails(lambda ws: rewrite(self.out(ws), "reverse 1, extend 0", "reverse 2, extend 0"), "'Groups:' must read")

    def test_row_order_fails(self):
        def swap(ws):
            p = self.out(ws)
            lines = p.read_text().splitlines(keepends=True)
            i = next(n for n, l in enumerate(lines) if "friday-refresh" in l)
            j = next(n for n, l in enumerate(lines) if "thirty-day-window" in l)
            lines[i], lines[j] = lines[j], lines[i]
            p.write_text("".join(lines))
        self.fails(swap, "grouped in this order")

    def test_operator_must_be_a_decider(self):
        def stranger(ws):
            rewrite(self.out(ws), "Operator: Priya Nair", "Operator: Sam Doe")
            rewrite(self.state(ws), '"operator": "Priya Nair"', '"operator": "Sam Doe"')
        self.fails(stranger, "is not a decider")

    def test_open_quarter_fails(self):
        self.fails(lambda ws: rewrite(self.state(ws), '"quarter": "2026-Q3"', '"quarter": "2026-Q4"'), "has not ended")

    def test_next_run_must_be_quarterly(self):
        self.fails(lambda ws: rewrite(self.state(ws), "2027-02-20", "2026-11-28"), "at least 60 days")

    def test_state_open_drift_fails(self):
        self.fails(lambda ws: rewrite(self.state(ws), '"open": [\n    "2026-09-01-retire-lag-export.md"\n  ]', '"open": []'),
                   "open does not match")


if __name__ == "__main__":
    unittest.main()
